# MQTT client

this is a small project for providing cmd line interface for using mqtt 
build upon the python pkg **paho_mqtt**

## Getting Started
To use the project, first follow the guide [installation guid](https://python-poetry.org/docs/#installation) to install poetry 
which is the dependency manager and packager 

after than intall the project's dependencies
```hs
poetry install
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
go to `./easy_mqtt`: `cd ./easy_mqtt`

run a `venv` if you want `poetry shell`

install the application through pip: `pip install --editable .`

then you can use it through `easymqtt` in terminal

there two commands:

`easymqtt subscribe`

`easymqtt publish`

use the `--help` flag to see more details
