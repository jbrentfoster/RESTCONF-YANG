# REST-CONF YANG
Script for collecting the YANG schema files from a RESTCONF server.

## Setup
1) Make sure you have Python 3 installed on your system
https://www.python.org/downloads/

```
$ python --version
Python 3.9.0
```

2) Switch to the directory where you store your Python virtual environments (or create one if it doesn’t exist)

`$ cd <venv-directory>`

3) Create new Python3 virtual environment for vxr-automation (in this example I named it “vxr-venv”)…

`$ python -m venv restconf-venv`

4) Activate the virtual environment

* On Linux or MAC
```
$ source restconf-venv/bin/activate
(vxr-venv) $
```
* On Windows
```
C:\Users\brfoster\venvs>.\restconf-venv\Scripts\activate
(restconf-venv) C:\Users\brfoster\venvs>
```

4) Use pip package manager to install required packages into the virtual environment
`(restconf-venv) $ pip install requests`


## Usage

````
> python main.py --help
usage: main.py [-h] [-i [N]] [-u [N]] [-p [N]]

A collection tool for RESTCONF APIs

optional arguments:
  -h, --help            show this help message and exit
  -i [N], --server_url [N]
                        Please provide the RESTCONF Server URL
  -u [N], --user [N]    Please provide the user name for the RESTCONF Server
  -p [N], --passwd [N]  Please provide the password for the RESTCONF Server
```

