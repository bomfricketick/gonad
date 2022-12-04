import json
import jinja2
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))



from profile import read_profile
profile = read_profile(profiles_dir="./")
print(json.dumps(profile, indent=4))

test = profile['project']['outputs']['test2']

print(json.dumps(test, indent=4))



templateLoader = jinja2.FileSystemLoader(
  encoding='utf-8-sig',
  searchpath=os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "jinja_templates"))
templateEnv = jinja2.Environment(
  loader=templateLoader,
  extensions=['jinja2.ext.do'])



_DISCOVER_TABLE = templateEnv.get_template("test.sql")
table = _DISCOVER_TABLE.render(macro=test, separator=',')

print(table)