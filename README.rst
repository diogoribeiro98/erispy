Eris python tools
=================

Python tools to reduce and work with [ERIS](https://www.eso.org/sci/facilities/paranal/instruments/eris.html) data.

> [!NOTE]
> This package is still under development

### Installation

To install, download the repository and install it using pip as 

```bash
pip install .
```
The use of python environments is recommended.

### How is the package structured?

The package is separated in two subpackages: one for the NIX instrument and another one for SPIFFI.  

> [!IMPORTANT]
> At the moment, only NIX tools are avaliable.

Each subpackage is organizes into specific modules. The NIX subpackage is subdivided as

* **nix.data:** Fetching data tools for both science and calibration files  
* **nix.calib:** Calibration tools
* **nix.stack:** Frame stacking tools
* **nix.plots:** Visualization tools

An example of how all these modules come together in the reduction process can be found in the example folder