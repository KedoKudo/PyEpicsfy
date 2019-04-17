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

Before installing the metapackage `jupyter`, it is recommended to pin the package `tornado` to an older version until BlueSky dev team solve the related [issue#1062](https://github.com/NSLS-II/bluesky/issues/1062).
To do so, create a file named __pinned__ under the directory `CONDA_INSTALL_DIR/env/ENVNAME/conda-meta` with the following content:  
```
tornado<5
```

Then install `jupyter` and `matplotlib` with  
```
conda install jupyter matplotlib
```

For update BlueSky packages, one can always do update with explicit channel name  
```
conda update bluesky -c lightsource2-tag
```

Alternatively, a package configuration file `.condarc` can be placed under `CONDA_INSTALL_DIR/envs/ENV_NAME/` with the following content  
```YAML  
channels:
    - lightsource2-tag  
    - lightsource2-dev  
    - aps-anl-tag  
    - aps-anl-dev  
    - prjemian  
    - defaults  
    - conda-forge
```

> NOTE   
> This is the recommended way to install BlueSky and associated dependencies.

### Install with _pip_

Install bluesky and apstools with pip
```
pip install -U pip
pip install boltons mongoquery pims pyepics pyRestTable tzlocal jupyter suitcase matplotlib
pip install git+https://github.com/Nikea/historydict#egg=historydict \
            git+https://github.com/NSLS-II/amostra#egg=amostra \
            git+https://github.com/NSLS-II/bluesky#egg=bluesky \
            git+https://github.com/NSLS-II/databroker#egg=databroker \
            git+https://github.com/NSLS-II/doct#egg=doct \
            git+https://github.com/NSLS-II/event-model#egg=event_model \
            git+https://github.com/NSLS-II/ophyd#egg=ophyd \
            git+https://github.com/NSLS-II/hklpy#egg=hklpy
pip install apstools
```

Similarly, the package `tornado` need to be downgrade below 5.0 to avoid the runtime error.

## Config Meta-data handler (MongoDB)

Copy the configuration file `configs/mongodb_config.yml ` to `mongodb_config.yml` to enable meta-data handler backed by a MongoDB server.

> The entry __host__ need to be changed to the IP of the machine that hosts the MongoDB service.

## Ipython based control

### Profile

The environment var `IPYTHONDIR` needs to be set where the profile folder is, or simply create symbolic link of the deisred profile to `~/.ipython/`, which is the default location to store all IPython profiles.

