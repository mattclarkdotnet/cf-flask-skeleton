# A skeleton Flask app for deployment to Cloud Foundry using Travis

While deploying to Cloud Foundry is incredibly easy once you get going it's not always so easy to get everything glued together.  This project contains files and scripts to get up and running with a basic Flask app as quickly as possible.  Out of the box the skeleton provides:

* a Flask app
* Unit tests
* Settings controlled though environment variables alone
* Dev and Prod manifest files with a common base manifest
* Travis CI test and deployment integration
* setup scripts to:
  * set up a python 3 virtual environment correctly
  * create a 'runtime.txt' so that the CF buildpack uses the same python version as the virtualenv
  * install dependencies

## Quick start

_IMPORTANT: OS X users must install a more recent Python._  Cloud Foundry supports only the current and previous two minor python versions, so for python 2.7 only 2.7.8 2.7.9 and 2.7.10 are supported.  Since OS X still, bafflingly, comes with python 2.7.6, you need to install a more recent version, preferably Python 3.4.

Begin by checking out the repository

    $ git clone https://github.com/mattclarkdotnet/cf-flask-skeleton.git
    $ cd cf-flask-skeleton

Then run the setup script to create a python 3 virtual environment and install dependencies:
  
    $ ./setup_venv.sh
    
Switch to the newly created virtual environment and run the unit tests:

    $ workon cf-flask-skeleton
    $ source env_local
    $ nosetests test/unit
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.151s

    OK

Start the app:

    $ ./runlocal.sh
    
And in a separate terminal check that it's responding correctly:

    $ source env_local
    $ curl http://$LOCAL_IP:$LOCAL_PORT/
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="utf-8">
        <title>Skeleton</title>
        <link rel="stylesheet" href="/static/skeleton.css">
    </head>
    <body>
    Just the bones
    </body>
    </html>
    $
           
If you are not already logged in to a Cloud Foundry platform, do it now:

    $ cf login
    
Make sure CF knows what Python runtime you want to use by creating a 'runtime.txt' file:

    $ ./setup_runtime.sh

And finally push the app:

_Don't try this on a Pivotal Web Services (run.pivotal.io) account because I'm already running it there, see the section on manifests and change the name before deployment_:

    $ cf push -f manifest-development.yml
    
## The gory details

Let's go through the app file by file.

### setup_venv.sh

This script assumes you have [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) installed. It creates a new virtual environment using the --no-site-packages flag to keep it completely clean, and using your local Python 3 binary as the runtime.  It then installs the required packages listed in the requirements.txt file.

Note that the Python 2.7.10 binary also runs this app and its dependencies, but earlier versions of python 2.7 may well not.

### requirements.txt

This file both lists the required packages (Flask, Gunicorn and their dependencies), and is used by Cloud Foundry to determine that the python buildpack should be used to create the app image for deployment.  It's updated by running  `pip freeze > requirements.txt` after we install any python packages 

### env_local

All application settings for a cloud native app should be kept in environment variables.  For local development we can't specify these in a CF manifest, so we have a file to source them from.  More or less elaborate schemes for managing environment settings exist, but this works for a simple app such as this.

### runlocal.sh

Most Flask tutorials will have you launch the app by giving a an `if __name__ == '__main__'; app.run()` coda in the app module, but this won't reflect how the app is actually run so it is better to have a separate launch script that matches as closely as possible the 'command' value in the deployment manifest.

### setup_runtime.sh and runtime.txt

Uness you give it a hint, the CF python buildpack will use the version 2.7.10 interpreter.  Even if that's what we wanted we should still specify it explicitly to make our build reproducible.  This script simply converts the output of `python -V` to the format needed by the buildpack to specify the runtime we want in the `runtime.txt` file.

`runtime.txt` is not part of the git repo because its exact value may vary depending on your local setup.

### manifest_base.yml

This is where we specify the aspects of our app that are common across deployments.  A real app would probably have more differences between production and development in terms of scaling, but more common config for services.

### manifest_development.yml

If you try to push the app to Pivotal Web Services using this manifest you will get an error because it's already running under the name 'skeleton-dev' in my space there, so you'll need to edit this file and give it a new name.

We inherit the settings from `manifest_base.yml`, and add in some specific details.  The 'space' is set t 'development', an environment variable is set to trigger the app to set its log level to debug, and we give the app a name which is specific to this space.  If you give an app the same name in two spaces you will get an error on deployment because every app has a 'default route' which is its name, in addition to any specific hostnames you give it (TODO: check specifics and see if this can be overridden).

### manifest_production.yml

If you try to push the app to Pivotal Web Services using this manifest you will get an error because it's already running under the name 'skeleton-prod' in my space there, so you'll need to edit this file and give it a new name.

We inherit the settings from `manifest_base.yml`, and add in some specific details.  The 'space' is set t 'production', and we give the app a name which is specific to this space.  If you give an app the same name in two spaces you will get an error on deployment because every app has a 'default route' which is its name, in addition to any specific hostnames you give it (TODO: check specifics and see if this can be overridden).

### .travis.yml

Probably the most complex file in the project, this specifies to Travis CI how to build, test and deploy the application to production.  Some points worth calling out are:

* `sudo: required` is needed because Travis' cloud foundry deployment mechanism can't run within a container.  This makes builds a lot slower which is a shame (TODO: see if there is a way around this)
* In the `before_deploy` section we set up the runtime.txt and symlink the production manifest to `manifest.yml`.  I'm not aware of any way to specify a manifest explicitly here so a symlink has to do. (TODO: enquire further)
* `edge: true` is required because the CF deployment is not available in mainline Travis.

See [the travis docs](http://docs.travis-ci.com/user/deployment/cloudfoundry/) for more information on integrating Travis with Cloud Foundry

### skeleton/skeleton.py

A fairly standard Flask app which renders a basic template, but note it gets all its config from environment variables

### skeleton/\_\_init.py\_\_

Python 2.7 requires this file to mark a directory as containing a python module.  Not needed if you are running Python 3 exclusively.

### skeleton/static/skeleton.css

A very minimal CSS file for demo purposes only

### skeleton/templates/main.html

A template file which actually doesn't have any variable parts, it's just here to show the principle of the thing.













    
