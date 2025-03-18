event-notify
====

`event-notify` provides dockerized machinery to generate alerts from the command line.  These alerts are delivered through Google's Gmail API.  One use case is to generate a text message through an SMS gateway.


## Sending Alerts

```bash
./event-notify.sh alert --timestamp --message "my first alert"
```


## Setup

### Google Gloud Config

You'll need to create a google project that enables the Gmail API.  Relevant documentation is here:

+ [create gmail project](https://console.cloud.google.com/projectcreate)
+ [gmail api guide](https://developers.google.com/gmail/api/guides)


### Local Config

Copy `./aux/example/secrets/client_secret.json.example` to `./aux/example/secrets/client_secret.json` and update `client_id` and `project_id`.

Copy `dotenv.example` to `dotenv` and set the `NOTIFY_HOME` and `NOTIFY_RECIPIENT` environment variables.

<!-- Create a symbolic link to the installation directory, e.g.:

```bash
sudo ln -s $(pwd) /opt/event-notify
``` -->

### Pipenv Run

After making the configuration changes, and invoking from the installation directory:

```bash
# install
pipenv install

# this should generate a usage message
PYTHONPATH=. pipenv run python3 app/notify.py

# send an email alert (adjust --recipient and --message as needed)
PYTHONPATH=. pipenv run python3 app/notify.py alert --recipient user@example.com --message "Hi user@example.com.  Welcome to my new alerting service!"
```

The first time you send an alert, the Gmail API will load up a browser and ask for you to confirm access.  If approved, this will create a persistent local token `./aux/example/secrets/token.json` and send the message.


### Dockerized Run

```bash
# build the docker container
docker build . --tag event-notify

# run the container
docker run -it --rm \
	-v $(pwd)/aux/example:/home/notify/aux \
	event-notify
```

### config.yaml and auxilliary files

event-notify determines the location of its configuration, `config.yaml`, using a fallback strategy.  This enables some nice features.  

In particular, auxilliary files, including secrets and templates, are easily separated from the code.  The `config.yaml` file provides defaults for other environmental variables.  It also provides a way to register dynamically available templates.

Moreover, the underlying parameterization machinery / configuration is intended to be general.  One should be able to easily reuse these components in another project.

#### fallback strategy

Finding `config.yaml` proceeds by first checking the environment variable `NOTIFY_AUX_PATH`.  If that is unset, it looks for a `dotenv` file in a known location:  first `/opt/event-notify/dotenv`, then `./dotenv`.

One reason to prefer a `dotenv` file is that, when deploying a service via `systemd`, it can be specified as an `EnvironmentFile`.  This provides a workaround for symbolic links, which tend to be problematic for docker.  Hence, `/opt/event-notify` could be a symbolic link to an arbitrary installation location while `/opt/event-notify/dotenv` would contain a Docker-friendly or absolute path to the installation directory.

## Templates

The code is designed so that it should be relatively easy to add a new Jinja2 template.  These are defined in `./aux/example/config.yaml`, and implemented in `./aux/example/templates`  `templates/alert.j2` should serve as an example.  

For reference, see the python argparse documentation; specifically, [add_argument](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument).



Appendix: SMS Gateway Domains
----

A list of SMS gateways is available on [wikipedia: sms gateway](https://en.wikipedia.org/wiki/SMS_gateway).


| mobile carrier     | sms gateway              |
| ------------------ | -------------------------|
| Alltel             | sms.alltelwireless.com   |
| AT&T               | txt.att.net              |
| Boost Mobile       | sms.myboostmobile.com    |
| Consumer Cellular  | mailmymobile.net         |
| Cricket Wireless   | mms.cricketwireless.net  |
| FirstNet           | sms.firstnet.com         |
| Google Fi Wireless | msg.fi.google.com        |
| MetroPCS           | mymetropcs.com           |
| Republic Wireless  | text.republicwireless.com|
| Sprint             | messaging.sprintpcs.com  |
| T-Mobile           | tmomail.net              |
| Ting               | message.ting.com         |
| U.S. Cellular      | email.uscc.net           |
| Verizon Wireless   | vtext.com                |
| Virgin Mobile      | vmobl.com                |
| XFinity Mobile     | vtext.com                |