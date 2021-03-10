import json
from collections.abc import Mapping
import os
F_NAME = ''
LANGUAGE = 'pt_BR'
APP_FOLDER = ''


def parse_dict(dict):
  for key in dict.keys():
    print(key)
    if isinstance(dict[key], Mapping):
      cur_dict = dict[key]
      if '@class' in cur_dict and cur_dict['@class'] == 'com.endeca.content.StringMap':
        print(cur_dict)
        if LANGUAGE in cur_dict:
          dict[key] = cur_dict[LANGUAGE]
        else:
          dict[key] = ''
      else:
        parse_dict(dict[key])


def migrate_file(file):
  with open(F_NAME, encoding='UTF-8') as f:
    data = json.load(f)
    parse_dict(data)
    with open('c:/tmp/test.json', mode='w', encoding='UTF-8') as f1:
      json.dump(data, f1, indent=4)


def migrate_contents():
  for root, _, files in os.walk(os.path.join(APP_FOLDER, 'content')):
    for file in files:
      _, ext = os.path.splitext(file)
      if ext == '.json':
        print(os.path.join(root, file))


def test_content():
  print('Initialing parsing content')
  for root, _, files in os.walk(os.path.join(APP_FOLDER, 'content')):
    for file in files:
      _, ext = os.path.splitext(file)
      if ext == '.json':
        try:
          with open(os.path.join(root, file), encoding='UTF-8') as f:
            json.load(f)
        except:
          print('Error parsing ' + os.path.join(root, file))
  print('Finish parsing content...')

test_content()