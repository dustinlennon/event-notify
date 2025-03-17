import os
import datetime, pytz
from types import SimpleNamespace

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader

from app.dotenv_reader import DotenvReader

#- get_config -----------------------------------------------------------------

def get_config(config_path):
  with open(config_path) as f:
    config = yaml.load(f, Loader=Loader)
    if config is not None:
      config = _preprocess(config)
  return config

def _preprocess(d):
  obj = d
  if isinstance(d, list):
    dx = []
    for o in d:
      dx.append( _preprocess(o) )
    obj = dx
  elif isinstance(d, dict):
    dx = {}
    for k,v in d.items():
      dx[k] = _preprocess(v)
    obj = SimpleNamespace(**dx)

  return obj

#- BaseParams -----------------------------------------------------------------

class BaseParams(object):
  def __init__(self, *, prefix, cfg):
    self._app_path = os.environ.get(f"{prefix}_APP_PATH", cfg.env.app_path or os.getcwd())
    self._aux_path = os.environ.get(f"{prefix}_AUX_PATH", cfg.env.aux_path or os.getcwd())

    timezone  = os.environ.get(f"{prefix}_TIMEZONE", cfg.env.timezone)
    self._tz  = pytz.timezone(timezone)

  @classmethod
  def from_path(cls, prefix, config_path):
    instance = cls(
      prefix = prefix,
      cfg = get_config(config_path)
    )
    return instance
  
  @classmethod
  def from_dotenv(cls, prefix):
    result = DotenvReader([
      '/opt/event-notify/dotenv',
      'dotenv'
    ]).read()

    aux_path = result.get(f"{prefix}_AUX_PATH")
    config_path = os.path.sep.join(
      [p for p in [aux_path, "config.yaml"] if p]
    )

    instance = cls.from_path(prefix, config_path)
    return instance

  def app_path(self, *args):
    pth = os.path.sep.join([self._app_path] + list(args))
    return pth

  def aux_path(self, *args):
    pth = os.path.sep.join([self._aux_path] + list(args))
    return pth

  def now(self):
    return datetime.datetime.now(self._tz)

