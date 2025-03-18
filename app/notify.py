#
#  Ref:
#   https://github.com/googleapis/google-api-python-client/blob/main/docs/client-secrets.md
#   https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth-installed.md
#

import os, stat
from types import SimpleNamespace
import base64
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.message import EmailMessage

from app.base_params import BaseParams

# build parser ----------------------------------------------------------------

import argparse
class NotifyParams(BaseParams):
  _prefix = "NOTIFY"
  _opt_path = "/opt/event-notify"

  def __init__(self, *, cfg, **kws):
    super().__init__(
      prefix = self._prefix,
      cfg = cfg
    )

    self._templates = cfg.templates
    self.scopes     = cfg.scopes
    self.message    = cfg.message

  @classmethod
  def from_dotenv(cls):
    instance = super().from_dotenv(cls._prefix, cls._opt_path)
    return instance

  def parse_args(self) -> SimpleNamespace:
    main_parser = argparse.ArgumentParser()

    subparsers = main_parser.add_subparsers(dest='cmd')
    subparsers.required = True
    for template in self._templates:
      template_name = template.name
      template_args = template.args
      template_file = f"{template_name}.j2"
      
      parser = subparsers.add_parser(template_name)
      parser.add_argument("--recipient", required = True)
      parser.add_argument("--template", default = template_file, help=argparse.SUPPRESS)
      for targs in template_args:
        name  = targs.name_or_flags
        kws   = targs.kws
        parser.add_argument(name, **vars(kws))

    args = main_parser.parse_args()
    return args


# get_credentials -------------------------------------------------------------

def get_credentials(np : NotifyParams):
  creds = None

  token_path  = np.aux_path("secrets/token.json")
  cs_path     = np.aux_path("secrets/client_secret.json")

  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, np.scopes)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(cs_path, np.scopes)
      creds = flow.run_local_server(port=0)

    with open(token_path, "w") as token:
      token.write(creds.to_json())

    # limit permissions on token.json
    os.chmod(token_path, stat.S_IRUSR | stat.S_IWUSR)

  return creds

# notify ----------------------------------------------------------------------

def notify(service, notification_kws):
  (
    service
      .users()
      .messages()
      .send(**notification_kws)
      .execute()
  )

# get_email -------------------------------------------------------------------


def get_email(service):
  profile = (
    service
      .users()
      .getProfile(userId = "me")
      .execute()
  )

  return profile['emailAddress']


# create_notification ---------------------------------------------------------

def create_notification(np : NotifyParams, content, sender, recipient):

  message = EmailMessage()
  message.set_content(content)
  message["From"]     = sender
  message["To"]       = recipient
  message["Subject"]  = np.message.subject

  kws = {
    'userId' : "me",
    'body' : {
      "raw" : base64.urlsafe_b64encode(message.as_bytes().strip()).decode()
    }
  }

  return kws


# main ------------------------------------------------------------------------

if __name__ == '__main__':
  from jinja2 import Environment, FileSystemLoader

  aux_path = os.environ.get("NOTIFY_AUX_PATH")
  if aux_path:
    params = NotifyParams.from_path("NOTIFY", f"{aux_path}/config.yaml")
  else:
    params = NotifyParams.from_dotenv()

  args = params.parse_args()
  kws = vars(args)

  # jinja setup
  j2env = Environment(
    loader = FileSystemLoader(params.aux_path("templates")),
    autoescape = True
  )
  j2env.globals['now'] = params.now

  # generate notification content
  template = kws.pop('template')
  content = (
    j2env
    .get_template(template)
    .render(**kws)
  )

  # send notification
  credentials = get_credentials(params)
  service = build("gmail", "v1", credentials=credentials)
  sender = get_email(service)

  notification_kws = create_notification(params, content, sender, args.recipient)
  notify(service, notification_kws)
