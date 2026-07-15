# Apply ICA (reject components) to Raw Data

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.679-blue.svg)](https://doi.org/10.25663/brainlife.app.679)

## Description

This Brainlife App applies Independent Component Analysis (ICA) decomposition to raw MEG/EEG data using MNE-Python. The app reads an ICA object, excludes identified bad components (automatically detected for EOG/ECG artifacts or manually specified), and reconstructs the raw data before saving it.

## Inputs

- **mne** (`meg/fif`): Raw MEG/EEG data file
- **ica** (`ica/fif`): ICA decomposition object file

## Outputs

- **out_dir/raw.fif**: Raw data with ICA components applied
- **out_figs/plot_overlay.png**: Visualization of ICA overlay before application  
- **out_report/report.html**: Quality control report with ICA information
- **product.json**: Metadata about applied ICA for Brainlife.io interface

## Configuration Parameters

- **exclude** (string): Comma-separated list of component indices to exclude (in addition to any specified in ica.exclude)
- **reject_EOG** (boolean): Whether to automatically detect and exclude EOG artifacts  
- **EOG_chan** (string/int): EOG channel name or index for automatic detection
- **reject_ECG** (boolean): Whether to automatically detect and exclude ECG artifacts
- **ECG_chan** (string/int): ECG channel name or index for automatic detection

## Usage

This app runs on the Brainlife.io platform. Configure the input files and parameters through the web interface, then execute the app.

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
We kindly ask that you cite the following articles when publishing papers and code using this code. 

*- brainlife.io Publishing and Apps:*

Avesani, P., McPherson, B., Hayashi, S. et al. **The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services**. Sci Data 6, 69 (2019). https://doi.org/10.1038/s41597-019-0073-y

*- MNE-Python package:* 

Gramfort A, Luessi M, Larson E, Engemann DA, Strohmeier D, Brodbeck C, Goj R, Jas M, Brooks T, Parkkonen L, and Hämäläinen MS.  **MEG and EEG data analysis with MNE-Python**. Frontiers in Neuroscience, 7(267):1–13, 2013. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)


#### MIT Copyright (c) 2026 brainlife.io The University of Texas at Austin and Indiana University

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
