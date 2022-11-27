import json
import jinja2
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from helpers.profile import read_profile
from helpers.connection import get_credentials_from_profile

credentials = get_credentials_from_profile()

# To render the correct jinja template use target to look in the right directory
target = credentials['type']


print(target)

# profile = read_profile(profiles_dir="./")
# print(json.dumps(profile, indent=4))

templateLoader = jinja2.FileSystemLoader(
  encoding='utf-8-sig',
  searchpath=os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "jinja_templates")
)
templateEnv = jinja2.Environment(
  loader=templateLoader,
  extensions=['jinja2.ext.do']
)



