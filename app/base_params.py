import os
import re
import datetime, pytz
from types import SimpleNamespace

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader

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
  def __init__(self, cfg):
    env_prefix = cfg.env.prefix
  
    self.home_path = os.environ.get(f"{env_prefix}_HOME", cfg.env.defaults.home or os.getcwd())

    timezone  = os.environ.get(f"{env_prefix}_TIMEZONE", cfg.env.defaults.timezone)
    self._tz  = pytz.timezone(timezone)

  @classmethod
  def from_path(cls, config_path):
    cfg = get_config(config_path)
    return cls(cfg)

  def path(self, *args):
    pth = os.path.sep.join([self.home_path] + list(args))
    return pth

  def now(self):
    return datetime.datetime.now(self._tz)

