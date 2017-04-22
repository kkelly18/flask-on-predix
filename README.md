# Flask on Predix
A codebook demonstrating details for pushing a Flask app on to Predix.

### Release History

v3.0 - Turn toy into production with Gunicorn WSGI server

v2.0 - Implement a Restful API as simply as possible, still using Flask Web Server (toy).

v1.0 - Simplest (toy) Flask application possible on Predix

#### Release v3.0
Turn toy into production with Gunicorn WSGI server.

Getting the app production ready is as simple as installing the gunicorn
package into your local environment and fixing up the run calls in the
manifest and proc files.

To get the response for the query endpoint you must assemble 
the URI from the URI provided by CF when it starts your app. It'll
be on the terminal console.

`https:<hostname and domain>/api/v1.0/` 

returns

`{
  "hello": "world"
}`

#### Release v2.0
Implement a Restful API as simply as possible, still using Flask Web Server (toy).

This release is a minimal implementation of Flask Blueprints. The "App" is the
simplest Restful API we could write. It has one route, the index, that responds
with a string of HTML text.  The goal is to have a minimal architecture seed for
our Flask apps.

The crux of the implementation is in the package constructors, `__init__.py`.
The module `manage.py` holds a global reference to the Flask app. It implements commands run
outside the app. Like `app.run()`!  This pattern seperates concerns of app initializion
from app operations.

App startup depends on `FLASK_CONFIG` set in the application's user environment.
The config options are in `config.py`. The script `setcf.sh` can be used to set the variable. If you're pushing the app
for the fist time, suggest using --no-start option.

`$cf push --no-start -b <link to buildpack>`

`$source setcf.sh`

`$cf start <app name>`

#### Release v1.0
Simplest (toy) Flask application possible on Predix.

If you're a Python dev using Flask as your web framework, this release is useful for smoke testing local Cloud Foundry (CF) configuration 
and getting your feet wet with CF deployment commands.

Replace the name (k2dark) in `manifest.yml` with your own.

The Predix Cloud Foundry instance is equipped with a default
python buildback. See it referenced in `manifest.yml`. 
You will want to investigate which versions
of Python it supports at present. We've found it convenient to 
apply the latest buildpack from the CloudFoundry github repo
to configure our app with later versions of Python 3.x.
Here's the technique:

`$ cf push -b https://github.com/cloudfoundry/buildpack-python.git`

You will need to set the python version spec in `runtime.txt` to match your own. 
The syntax is fiddly. If you direct the output of `$python --version` to `runtime.txt`, it'll be malformed. 
You'll get something like "Python 3.6.0". The buildpack demands
python-3.6.0. If CF deployment barks at you about MISSING-MANIFEST-DEPENDENCY 
it maybe the spec in runtime.txt.

CloudFoundry will issue your app a port to listen for requests on.
It's set in the PORT enviroment variable during app startup in CF.
Note in the `flask_app.py` how we're picking it out of the environment. When you
run the app locally on your desktop it should listen on localhost (127.0.0.1)
with the port you specify for your local machine, 4999 in our case. When running on
Predix, CF manages your host, domain and port (and a lot more).
The app.run command in flask_app.py is setting the host to 0.0.0.0 configuring the app
to listen on all IP addresses. CF deals with the routing. Route config is a bit fiddly, and since
configuration is rare activity for most developers, it's worth taking your time 
to work out how the app is configured differently for dev and production environements.

### Contact
This codebook is maintained by the GE Hitachi Digital team based in Wilmington NC.  
Where the beach is always calling!

Maintainer: \
kevin.c.kelly@ge.com

Authors:\
Kevin Kelly - GE Hitachi\
kevin.c.kelly@ge.com

Robin Wang -- GE Hitachi\
xuejun.wang@ge.com
