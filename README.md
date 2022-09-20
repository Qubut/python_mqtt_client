# MQTT client

this is a small project for providing cmd line interface for using mqtt 
build upon the python pkg **paho_mqtt**

## Getting Started
To use the project, first follow the guide [installation guid](https://python-poetry.org/docs/#installation) to install poetry 
which is the dependency manager and packager 

after that you initialize the project
```hs
poetry init
```
if you wanna add further pkgs use

```hs
poetry add pkg_name
```

runnig a dedicated shell env is done through:
```hs
poetry shell
```
---
there are 3 scripts `subscribe, publish and create_dummy`
use for example `subscribe --help` to get an idea about each one's options