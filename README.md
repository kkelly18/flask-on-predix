# flask_on_predix_spike

### Release 1
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

Maintainer: kevin.c.kelly@ge.com
Authors:
