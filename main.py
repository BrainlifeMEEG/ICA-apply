"""
Apply ICA components to raw MEG/EEG data.

This app reads an ICA object, excludes identified bad components (automatically
detected for EOG/ECG artifacts or manually specified), and reconstructs the raw data
before saving it.

Inputs:
    - mne: Path to MNE raw .fif file
    - ica: Path to ICA decomposition file
    - exclude: Optional comma-separated list of component indices to exclude
    - reject_EOG: Boolean to automatically detect and exclude EOG artifacts
    - reject_ECG: Boolean to automatically detect and exclude ECG artifacts
    - EOG_chan: Optional EOG channel name or index
    - ECG_chan: Optional ECG channel name or index

Outputs:
    - out_dir/raw.fif: Raw data with ICA components applied
    - out_figs/plot_overlay.png: Visualization of ICA overlay before application
    - out_report/report.html: QC report with ICA information
    - product.json: Metadata about applied ICA
"""

# Copyright (c) 2026 brainlife.io
#
# This app applies ICA decomposition to MNE raw data
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import re
import mne
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_raw_info_to_product,
    add_image_to_product,
    save_figure_with_base64,
    require_config_keys
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs', 'out_report')

# Load configuration
config = load_config()
require_config_keys(config, ['mne', 'ica'])

# == LOAD DATA ==
data_file = config['mne']
raw = mne.io.read_raw_fif(data_file, preload=True)

# Load ICA object
fname = config['ica']
ica = mne.preprocessing.read_ica(fname)

# == PARSE EXCLUDE COMPONENTS ==
# Turn config['exclude'] into a list of integers, parsing the separated string to a list
if config.get('exclude') and config['exclude'] != 'None':
    config['exclude'] = [int(x) for x in re.split("\\W+", config['exclude'])]
else:
    config['exclude'] = []

# Set excluded components
ica.exclude.extend(config['exclude'])

# == PARSE EOG/ECG CHANNELS ==
eog_ch = None
if config.get('EOG_chan') and config['EOG_chan'] != 'None':
    eog_ch = config['EOG_chan']
    try:
        # Try to convert to int if it's a number
        eog_ch = int(eog_ch)
    except (ValueError, TypeError):
        # Keep as string (channel name)
        pass

ecg_ch = None
if config.get('ECG_chan') and config['ECG_chan'] != 'None':
    ecg_ch = config['ECG_chan']
    try:
        # Try to convert to int if it's a number
        ecg_ch = int(ecg_ch)
    except (ValueError, TypeError):
        # Keep as string (channel name)
        pass
    
product_items = []

# == DETECT BAD COMPONENTS ==
if config.get('reject_EOG', False):
    eog_epochs = mne.preprocessing.create_eog_epochs(raw, ch_name=eog_ch)
    eog_idx, eog_scores = ica.find_bads_eog(raw, ch_name=eog_ch, threshold=3.0, 
                                            start=None, stop=None, l_freq=1, h_freq=10, 
                                            reject_by_annotation=True, measure='zscore', verbose=None)
    ica.exclude.extend(eog_idx)
    add_info_to_product(product_items,f'Excluded {len(eog_idx)} EOG artifact components')

if config.get('reject_ECG', False):
    ecg_epochs = mne.preprocessing.create_ecg_epochs(raw, ch_name=ecg_ch)
    ecg_idx, ecg_scores = ica.find_bads_ecg(raw, ch_name=ecg_ch, threshold='auto',
                                            start=None, stop=None, l_freq=8, h_freq=16,
                                            method='ctps', reject_by_annotation=True, measure='zscore', verbose=None)
    ica.exclude.extend(ecg_idx)
    add_info_to_product(product_items,f'Excluded {len(ecg_idx)} ECG artifact components')

# == CREATE OVERLAY VISUALIZATION ==
plt.figure(figsize=(12, 6))
ica.plot_overlay(raw, show=False)
overlay_fig_path = os.path.join('out_figs', 'plot_overlay.png')
plt.savefig(overlay_fig_path, dpi=150)
plt.close()

# == CREATE REPORT ==
# verbose=False at construction (not just on save() below), matching
# ICA-fit/epoch's own established convention -- report.save()'s own
# verbose=False only quiets that one call; add_ica() has no verbose
# parameter of its own to pass it to directly, so it inherits whatever
# level the Report object itself was built with. Without this, add_ica()
# runs at MNE's default log level and clogs the cluster log with its own
# chatty per-figure/per-asset progress lines (e.g. "Embedding: ...js").
report = mne.Report(title='ICA Application Report', verbose=False)
report.add_ica(ica, 'ICA Components', inst=raw)

# Add overlay information
report_text = f'<p><b>Total Components:</b> {ica.n_components}</p>'
report_text += f'<p><b>Excluded Components:</b> {len(ica.exclude)}</p>'
if ica.exclude:
    report_text += f'<p><b>Excluded Indices:</b> {sorted(ica.exclude)}</p>'
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == APPLY ICA ==
ica.apply(raw)

# Save processed raw data
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)

# == CREATE PRODUCT.JSON ==
add_raw_info_to_product(product_items, raw)
add_image_to_product(product_items, 'ICA Overlay', filepath=overlay_fig_path)
add_info_to_product(product_items, f'Applied ICA with {len(ica.exclude)} excluded components', 'success')
create_product_json(product_items)

