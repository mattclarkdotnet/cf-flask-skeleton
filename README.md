# A skeleton Flask app for continuous deployment to Cloud Foundry using Travis

While deploying to Cloud Foundry is incredibly easy once you get going it's not always so easy to get everything glued together.  This project contains files and scripts to get up and running with a basic Flask app as quickly as possible.  Out of the box the skeleton provides:

* a Flask app
* Unit tests
* Settings controlled though environment variables alone
* App deploys named by git commits
* Dev, Stage and Prod manifest files with a common base manifest
* Travis CI test and deployment integration
* setup scripts to:
  * set up a python 3 virtual environment correctly
  * create a 'runtime.txt' so that the CF buildpack uses the same python version as the virtualenv
  * install dependencies

## Quick start

_IMPORTANT: OS X users must install a more recent Python._  Cloud Foundry supports only the current and previous two minor python versions, so for python 2.7 only 2.7.8 2.7.9 and 2.7.10 are supported.  Since OS X still, bafflingly, comes with python 2.7.6, you need to install a more recent version, preferably Python 3.4.

For the quickstart you will need a Cloud Foundry account.  I'll assume we're using [Pivotal Web Services](http://run.pivotal.io/).

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

Make a local commit so that you get a unique app name:

    $ git commit --allow-empty -m "committing without changes to create unique commit ID"

Create a manifest.yml for your development space:

    $ ./make_manifest.sh development

And finally push the app:

    $ cf push
    
## Automated immutable builds

The quick start got us an app deployed, but to automate that deployment we'll need a few more things:

 * A forked git repo for Travis to pull from
 * the Travis command line client
 
### Travis client

If you don't already have the travis command line client installed, do:

`sudo gem install travis -v 1.8.0 --no-rdoc --no-ri`

### Forked repository

Fork the repository at https://github.com/mattclarkdotnet/cf-flask-skeleton

### Set up a new project in Travis

    $ git clone <your.forked.repo>
    $ cd <your.forked.repo>
    $ travis login
      ...
    $ travis enable

### Update the .travis.yml with your Cloud Foundry details

Open `.travis.yml` and in the `deploy:` section update the `username:` and `organization:` with your own settings.  Then run `travis encrypt --add deploy.password` to set your github password securely.

### Commit and push

Once you commit and push the new .travis.yml Travis will see the commit and start a build:

    $ git commit -a -m "updated .travis.yml with new account settings"
    $ git push
    
### Monitor your build

Either use the travis website or the `travis monitor` command to check the progress of your build.  Once it's done you will have a new app deployed in the staging space of your cloud foundry account.  You can get the URL of the newly deployed app with `travis logs .2 | grep urls`
    
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

### make_manifest.sh <space>

This script processes a template manifest (named template-manifest-<space>.yml) to create the 'manifest.yml' file that 'cf push' expects, with the name of the app set to the generic app name followed by the latest git commit ID.

### manifest_base.yml

This is where we specify the aspects of our app that are common across deployments.  A real app would probably have more differences between production and development in terms of scaling, but more common config for services.

### template_manifest_development.yml

We inherit the settings from `manifest_base.yml`, and add in some specific details.  An environment variable is set to trigger the app to set its log level to debug, and we set the name to APP_NAME which make_manifest.sh will replace with the real name later.

### template_manifest_staging.yml

Very similar to template_manifest_development, but without the APP_DEBUG environment variable set

### template_manifest_production.yml

Identical to the staging manifest template

### .travis.yml

Probably the most complex file in the project, this specifies to Travis CI how to build, test and deploy the application to staging.  Some points worth calling out are:

* `sudo: required` is needed because Travis' cloud foundry deployment mechanism can't run within a container.
* In the `before_deploy` section we set up the runtime.txt and run make_manifest.sh to create the manifest.yml.  Note that travis will run the 'cf push' itself.
* `edge: true` is required because the CF deployment is not available in mainline Travis.
* `space: staging` and the other cloud foundry settings in the 'deploy' section are essentially the arguments to `cf login`.
* Conditions are set so we only deploy the python 3.4 build, to avoid deploying the same app twice

See [the travis docs](http://docs.travis-ci.com/user/deployment/cloudfoundry/) for more information on integrating Travis with Cloud Foundry

### skeleton/skeleton.py

A fairly standard Flask app which renders a basic template, but note it gets all its config from environment variables

### skeleton/\_\_init.py\_\_

Python 2.7 requires this file to mark a directory as containing a python module.  Not needed if you are running Python 3 exclusively.

### skeleton/static/skeleton.css

A very minimal CSS file for demo purposes only

### skeleton/templates/main.html

A template file which actually doesn't have any variable parts, it's just here to show the principle of the thing.













    
