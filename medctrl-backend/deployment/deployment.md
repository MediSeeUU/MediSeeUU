# Deployment of MedCtrl backend

* [ General info ](#general)
* [ Initial setup ](#initSetup)
* [ Configuration ](#configuration)
* [ Build ](#build)
* [ Deploy ](#deploy)

<a name="general"></a>
# General info

The build and deploy system allows you to easily deploy a new version of the software without tampering with too many files.
There is some initial setup that needs to be done, but once that is done the updating should be as easy as just running the `build.sh` script with an environment variable set.

## Overview

Every build has a buildname. This buildname is used to differentiate between different versions/configurations of the software. This buildname is used in a few places:


* It is used to determine where the build files will be copied to. Every build will have its own directory in `/opt/medctrl/backend`. This is also the place where the socket will be placed through which the application can communicate with Nginx (See [ Deploy ](#deploy) for more details).

* It is used to choose which configuration file to use. So if you have `BUILD_NAME` set to `development`, the build script will set `API/api_settings/settings/deploy_development.py` as the configuration file to choose for this specific build. (See [ Configuration ](#configuration) for more details).

* It is used to start/stop/restart the medctrl service. This is done by passing the name of the build as an `@` argument to the systemctl service that is running. If you have a build named `development` you can edit the service using the following commands:
    * `sudo systemctl stop medctrl@development` to stop
    * `sudo systemctl start medctrl@development` to start
    * `sudo systemctl restart medctrl@development` to restart


<a name="initSetup"></a>
# Inital setup

This section will describe the one time setup that needs to be done to allow for a streamlined build/deploy process.

## Used software

This guide is written for Ubuntu 20.04. The following software should be installed:
| Software     | Version |
|--------------|---------|
| Nginx        | 1.18.0  |
| python3      | 3.10.4  |
| npm          | 8.5.0   |
| node         | 16.14.2 |
| MySQL server | 8.0.28  |

## Prerequisites
We assume some things are already setup before building/deployment of the system:
1. There is already a MySQL database setup to which you have login credentials. [ Link to setup instructions ](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04)

2. There is already a basic Nginx setup available. Adding endpoints for the MedCtrl system is covered in [ Deploy ](#deploy)

## Application setup

At this stage we will create a directory where all the build files will live. We will also create a Unix service that will run the actual application. This Unix service will be modular, so it is possible to have multiple versions/environments running at the same time.


1. Create a folder where the builds will live:
    ```bash
    mkdir -p /opt/medctrl/backend
    mkdir -p /var/www/medctrl/django-static
    ```
    Any builds that you run will end up in a subdirectory of this directory. So if you have a build with name `development` the build files will be placed in `/opt/medctrl/backend/development`.

2. Copy the `medctrl.target` and `medctrl@.service` files to the `/etc/systemd/system` directory:
    ```bash
    cp medctrl.target /etc/systemd/system
    cp medctrl@.service /etc/systemd/system
    ```

3. Reload the systemctl-daemon:
    ```bash
    sudo systemctl daemon-reload
    ```

<a name="configuration"></a>
# Configuration

Every build should have a configuration file. This file is used to store deployment-specific configuration details such as database credentials.

The configuration file for a specific build should be placed in the `API/api_settings/settings/` directory. The name of the settings file should be: \
`deploy_${BUILD_NAME}.py`.

So if you have a buildname `development` the filename should be: \
`deploy_development.py`.

Below is a template with the keys that the configuration file should have, make sure to change the actual values before you deploy.
```py
from api_settings.settings.common import *

SECRET_KEY = "random secret key"

DEBUG = False

# base url where the api will be served from
BASE_URL = "baseurl/"

STATIC_ROOT = "/var/www/medctrl/django-static"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "DATABASE_NAME",
        "USER": "DATABASE_USER",
        "PASSWORD": "DATABASE_PASSWORD",
        "HOST": "DATABASE_HOST",
        "PORT": "DATABASE_PORT",
    }
}
```

<a name="build"></a>
# Build

The actual building of the software is handled in the `build.sh` script. This script will copy the source files to the build directory and install dependencies that are needed to run the project.

The `build.sh` script expects a environment variable `BUILD_NAME` to be set. This `BUILD_NAME` is used to differentiate between different versions/builds.

Below are steps to build and activate the software with a build name `development`:

0. Every build should have a configuration file, so make sure the `API/api_settings/deploy_development.py` file exists with the correct configuration values.

1. Run the `build.sh` script with environment variable set:
    ```bash
    BUILD_NAME=development ./build.sh
    ```

<a name="deploy"></a>
# Deploy

After the `build.sh` script is finished, the application runs on a Unix socket. Every build has a `gunicorn.sock` socket through which it can communicate. This socket can be used by by Nginx to serve requests. In a Nginx configuration file you can put a `location` block which points to the specific build. You can specify which endpoint is connected to which socket as follows:
```nginx
# ... Rest of nginx config file

    # The /api endpoint will be bound to the `development` build
    location /api {
        include proxy_params;
        rewrite ^/api(.*)$ $1 break;
        proxy_pass http://unix:/opt/medctrl/backend/development/gunicorn.sock;
    }

    # The /testapi endpoint will be bound to the `testing` build
    location /testapi {
        include proxy_params;
        rewrite ^/testapi(.*)$ $1 break;
        proxy_pass http://unix:/opt/medctrl/backend/testing/gunicorn.sock;
    }

# ... Rest of nginx config file
```

After reloading Nginx using `nginx -s reload` the webserver should proxy all requests from `/api` to the running MedCtrl backend through the socket for the `development` build. All requests to `/testapi` will be proxied to the socket for the `testing` build.