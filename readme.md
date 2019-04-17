# BlueSky Control for 6BM@APS

This repository is a development process for deploying BlueSky based control system for tomography characterization at 6BM@APS.

## Installation

### Install with _conda_

Install bluesky core packages first  
```
conda install bluesky -c lightsource2-tag
```

then the apstools dependencies  
```
conda install pyresttable -c prjemian
```

followed by installing apstools  
```
conda install apstools -c aps-anl-dev
```

Before installing the metapackage `jupyter`, it is recommended to pin the package `tornado` to an older version until BlueSky dev team solve the related runtime errors.
To do so, create a file named __pinned__ under the directory `$CONDA_INSTALL_DIR/env/ENVNAME/conda-meta` with the following content:  
```
tornado<5
```

Then install `jupyter` and `matplotlib` with  
```
conda install jupyter matplotlib
```

> NOTE   
> This is the recommended way to install BlueSky and associated dependencies.


## Ipython based control

### Profile

The environment var `IPYTHONDIR` needs to be set where the profile folder is, or simply create symbolic link of the deisred profile to `~/.ipython/`, which is the default location to store all IPython profiles.

