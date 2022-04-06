#!/bin/bash

# Root directory of the builds.
# This is where the different builds will live, each in its own subdirectory
BUILD_ROOT=/opt/medctrl/backend

# Check if BUILD_NAME env variable exists else exit
if [ -z "$BUILD_NAME" ]; then
    echo "BUILD_NAME environment variables not set"
    exit 1
fi

# Subdirectory where the build files for this build will be placed
BUILD_PATH="$BUILD_ROOT/$BUILD_NAME"

# Name of the service which will run the backend
SERVICE_NAME="medctrl@${BUILD_NAME}"


function print_highlight {
    # Helper functin to print status
    echo "###############################################################################"
    echo "### $1"
    echo "###############################################################################"
}


# Setup a python environment
function setup_python_env {
    print_highlight "Setting up python environment"
    python3.10 -m pip install --upgrade pip
    python3.10 -m pip install virtualenv
    python3.10 -m virtualenv virtualenv

    source virtualenv/bin/activate

    print_highlight "Installing dependencies"
    pip install -r requirements.txt
}

function check_config {
    # Check if there exists a file at API/api_settings/settings/deploy_BUILDNAME
    if [ ! -f "API/api_settings/settings/deploy_$BUILD_NAME.py" ]; then
        echo "No deploy config file found at API/api_settings/settings/deploy_$BUILD_NAME.py"
        exit 1
    fi
}

function migrate_db {
    cd API
    print_highlight "Migrating database"
    python manage.py migrate
    cd ..
}

# function to copy mysite and venv to build_path
function copy_to_build_path {
    # Remove old build file if it exists
    if [ -d "$BUILD_PATH" ]; then
        print_highlight "Removing old build path"

        # Sometimes old __pychache__ can't be removed.
        # this is not a problem, but spits out alot of warnings so we suppress them
        rm -rf "$BUILD_PATH" 2&> /dev/null
    fi

    # make sure the build path exists
    print_highlight "Creating build path"
    mkdir -p "$BUILD_PATH"

    print_highlight "Copying to build path"
    cp -r API "$BUILD_PATH"
    cp requirements.txt $BUILD_PATH

    cd $BUILD_PATH
}

function restart_service {
    print_highlight "Restarting service"
    sudo systemctl daemon-reload
    sudo systemctl restart $SERVICE_NAME
}

check_config

copy_to_build_path

setup_python_env

migrate_db

restart_service