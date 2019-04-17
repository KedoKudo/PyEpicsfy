#!/bin/bash

# install components for bluesky

PIP_PKGS=
PIP_PKGS+=" boltons"
PIP_PKGS+=" mongoquery"
PIP_PKGS+=" pims"
PIP_PKGS+=" pyepics"
PIP_PKGS+=" pyRestTable"
PIP_PKGS+=" tzlocal"
PIP_PKGS+=" jupyter"
PIP_PKGS+=" suitcase"


# NSLS-II DAMA packages
#  install from GitHub repositories, master branch
PIP_PKGS+=" git+https://github.com/Nikea/historydict#egg=historydict"
PIP_PKGS+=" git+https://github.com/NSLS-II/amostra#egg=amostra"
PIP_PKGS+=" git+https://github.com/NSLS-II/bluesky#egg=bluesky"
PIP_PKGS+=" git+https://github.com/NSLS-II/databroker#egg=databroker"
PIP_PKGS+=" git+https://github.com/NSLS-II/doct#egg=doct"
PIP_PKGS+=" git+https://github.com/NSLS-II/event-model#egg=event_model"
PIP_PKGS+=" git+https://github.com/NSLS-II/ophyd#egg=ophyd"
# PIP_PKGS+=" git+https://github.com/NSLS-II/suitcase#egg=suitcase"
PIP_PKGS+=" git+https://github.com/NSLS-II/hklpy#egg=hklpy"

pip install  $PIP_PKGS