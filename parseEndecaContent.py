import json
from collections.abc import Mapping
import os
LANGUAGE = 'pt_BR'
APP_PATH = 'C:/tmp/BKP-VM/parse_python'
FOLDER = 'content'
#FOLDER = 'pages'
#FOLDER = 'templates'
AUX_TEMPLATE = []

def update_prop(json, key, new_value):
  print(json)
  json[key] = new_value
  return json

def aux(json, log):
  if '@class' in json and json['@class'] == 'com.endeca.content.StringMap':
    if LANGUAGE in json:
      return True, json['pt_BR']
    elif (len(json) == 1):
      return True, ''
    else:
      strAux = ''
      for key in json:
        if key != '@class':
          strAux += str(key) + '=' + str(json[key]) + ','
      print('----------------- ATENCAO para item: ', strAux, file=log)
      return True, strAux

  if '@type' in json and json['@type'] == '_UNKNOWN_':
    new_dict = {}
    return True, new_dict

  if FOLDER == 'templates' and 'editor' in json and json['editor'] == 'editors/StringMapEditor':
    propertyName = json['propertyName']
    json['editor'] = 'editors/StringEditor'
    AUX_TEMPLATE.append(propertyName)
    return True, json

  return False, json

def aux_template_type(json, log):
  for key in AUX_TEMPLATE:
    json['typeInfo'][key]['@propertyType'] = 'String'
  return json

def process(json, log):
  if type(json) is dict:
    changed, new = aux(json, log)
    if changed:
      return new
    for key in json:
      json[key] = process(json[key], log)

  if type(json) is list:
    for idx, child in enumerate(json):
      json[idx] = process(child, log)

  return json

def migrate_file(file, log):
  global AUX_TEMPLATE
  AUX_TEMPLATE = []
  with open(file, encoding='UTF-8') as f:
    data = json.load(f)
    dump1 = json.dumps(data)
    process(data, log)
    dump2 = json.dumps(data)
    
    aux_template_type(data, log)

    if(len(dump1) == len(dump2)):
      print("migrate_file no changes...", file=log)
    else:
      with open(file, 'w') as f:
        json.dump(data, f, indent=4)      

def save(data):
  with open('new_template.json', 'w') as f:
    json.dump(data, f, indent=4)
  
def migrate_contents():
  print('Start parsing json, folder: ', FOLDER)
  with open('log_.txt', 'w') as log:
    for root, _, files in os.walk(os.path.join(APP_PATH, FOLDER)):
      for file in files:
        _, ext = os.path.splitext(file)
        if ext == '.json':
          auxFile = os.path.join(root, file)
          print(auxFile, file=log)
          #if (auxFile.find('RichRelevanceDiscoverResultsList') >= 0 or auxFile.find('RichRelevanceResultsList') >= 0 or auxFile.find('RichRelevanceDynamicExperiences') >= 0):
          #    print('Manual Changed', file=log)
          #    continue
          migrate_file(auxFile, log)


  print('End parsing json...')

migrate_contents()

#migrate_file('./new_menu.json')      