# A minimal Flask app for deployment to Cloud Foundry

While deploying to Cloud Foundry is incredibly easy once you get going, there are a few little gotchas sometimes.  
This project contains files and scripts to get up and running with a basic Flask app as quickly as possible.  Out of 
the box the skeleton app provides:

* a Flask app in a subdirectory with an \_\_init\_\_.py for Python 2 compatibility
* example unit tests
* all settings controlled though environment variables alone
* separate application log debug and flask debug settings
* a CF manifest
* Travis CI test and deployment integration
* setup scripts to:
  * set up a python 3 virtual environment correctly
  * create a 'runtime.txt' so that the CF buildpack uses the same python version as the virtualenv
  * install dependencies


Begin by checking out the repository

    $ git clone https://github.com/mattclarkdotnet/cf-flask-skeleton.git
    $ cd cf-flask-skeleton

Then run the setup script to create a python 3 virtual environment and install dependencies:
  
    $ ./setup_venv.sh
    
Check that the app works correctly locally:

    $ source env_local
    $ ./runlocal.sh &
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
    $ kill $!
    
If you are not already logged in to a Cloud Foundry platform, do it now:

    $ cf login
    
Make sure CF knows what Python runtime you want to use by creating a 'runtime.txt' file:

    $ ./setup_runtime.sh

And finally push the app:

    $ cf push -f manifest-development.yml
    

    
