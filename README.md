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

Copy `./config/example/conf/client_secret.json.example` to `./config/example/conf/client_secret.json` and update `client_id` and `project_id`.

Copy `dotenv.example` to `dotenv` and set the `NOTIFY_HOME` and `NOTIFY_RECIPIENT` environment variables.

Create a symbolic link to the installation directory, e.g.:

```bash
sudo ln -s $(pwd) /opt/event-notify
```


## Templates

The code is designed so that it should be relatively easy to add a new Jinja2 template.  These are defined in `conf/config.yaml`, and implemented in `templates`  `templates/alert.j2` should serve as an example.  

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