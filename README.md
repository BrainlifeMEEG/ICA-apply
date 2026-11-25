# Apply ICA (reject components) to Raw Data

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Removes selected ICA components from continuous MEG/EEG with MNE-Python ICA.apply(), optionally auto-detecting EOG and ECG components, and outputs the cleaned raw data with an overlay plot and report.**

Reads a fitted ICA object (for example from ICA-fit) and the raw data, excludes the union of components already marked in the ICA, those listed in exclude and, if enabled, those found by find_bads_eog/find_bads_ecg, then reconstructs the signal. Use it to remove ocular or cardiac artifacts after fitting ICA on the same data.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meeg/mne/raw` · `neuro/meeg/mne/ica` |
| 📤 **Outputs** | `neuro/meeg/mne/raw` · `generic/image/png` · `report/html` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 1 CPUs · 20 GB memory |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.679](https://doi.org/10.25663/brainlife.app.679) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meeg/mne/raw` | yes | Continuous MEG/EEG data (MNE raw). |
| `ica` | `neuro/meeg/mne/ica` | yes | Fitted ICA decomposition of the same data (e.g. from ICA-fit). |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | Raw data with the excluded ICA components removed (raw.fif). |
| `out_figs` | `generic/image/png` | Overlay plot of the signal before and after ICA application. |
| `out_report` | `report/html` | HTML QC report with the ICA decomposition and excluded components. |

<details>
<summary><b>⚙️ Parameters</b> (5)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `exclude` | string |  | The indices referring to columns in the ummixing matrix. The components to be zeroed out. If None (default) or an empty list, only components from ica.exclude will be excluded. Else, the union of exclude and ica.exclude will be excluded. |
| `reject_EOG` | boolean | `false` | Detect and reject EOG related components using correlation (using mne.preprocessing.ICA.find_bads_eog) |
| `reject_ECG` | boolean | `false` | Detect and reject ECG related components using correlation (using mne.preprocessing.ICA.find_bads_ecg) |
| `EOG_chan` | string |  | Comma separated EOG channel number(s) or label(s) |
| `ECG_chan` | string |  | Comma separated ECG channel number(s) or label(s) |

</details>

<!-- brainlife-app:end -->

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.679-blue.svg)](https://doi.org/10.25663/brainlife.app.679)

## Description

This Brainlife App applies Independent Component Analysis (ICA) decomposition to raw MEG/EEG data using MNE-Python's `ICA.apply()`. The app reads an ICA object, excludes identified bad components (automatically detected for EOG/ECG artifacts or manually specified), and reconstructs the raw data before saving it.

The app generates:
- Raw data with the ICA components applied (`raw.fif`)
- An overlay visualization comparing the raw data before and after ICA application
- An HTML QC report with the ICA decomposition and excluded-component details
- A `product.json` summarizing the excluded components

## Inputs

- **`mne`** (`neuro/meeg/mne/raw`): continuous MEG/EEG raw data to apply ICA to (required)
- **`ica`** (`neuro/meeg/mne/ica`): fitted ICA decomposition object, e.g. from `ICA-fit` (required)

## Outputs

- **`out_dir/raw.fif`** (`neuro/meeg/mne/raw`): raw data with the ICA components applied
- **`out_figs/plot_overlay.png`** (`generic/image/png`): visualization of the ICA overlay before application
- **`out_report/report.html`** (`report/html`): quality control report with ICA information
- **`product.json`**: metadata about the applied ICA for the Brainlife.io interface

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `exclude` | string | `""` | Comma-separated list of component indices to exclude, in addition to any already in `ica.exclude`. The union of the two is excluded. |
| `reject_EOG` | boolean | `false` | Whether to automatically detect and exclude EOG artifact components using `mne.preprocessing.ICA.find_bads_eog`. |
| `EOG_chan` | string | `""` | EOG channel name or index for automatic EOG detection (optional). |
| `reject_ECG` | boolean | `false` | Whether to automatically detect and exclude ECG artifact components using `mne.preprocessing.ICA.find_bads_ecg`. |
| `ECG_chan` | string | `""` | ECG channel name or index for automatic ECG detection (optional). |

## Usage

### Running on Brainlife.io

1. Select your MEG/EEG raw `.fif` dataset as the `mne` input and the fitted ICA decomposition (e.g. from `ICA-fit`) as the `ica` input.
2. Optionally set `exclude` to a comma-separated list of additional component indices to exclude.
3. Optionally enable `reject_EOG`/`reject_ECG` to automatically detect and exclude EOG/ECG artifact components, specifying `EOG_chan`/`ECG_chan` if needed.
4. Submit the process.

### Local Testing

```bash
# Edit config.json to point "mne" and "ica" at real files, then:
python main.py
```

## Technical Details

The app uses MNE-Python's ICA functionality to apply component exclusion to raw data. It supports:
- Manual component exclusion via index specification
- Automatic EOG artifact detection using correlation analysis
- Automatic ECG artifact detection using cross-trial phase statistics
- Quality control visualization and reporting

## Authors

- Saeed Zahran (https://github.com/saeedzahranutc)
- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

Gramfort A, Luessi M, Larson E, Engemann DA, Strohmeier D, Brodbeck C, Goj R, Jas M, Brooks T, Parkkonen L, and Hämäläinen MS. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience, 7(267):1–13, 2013. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
