from cgi import test
from turtle import title
import yaml
import logging
import json
import re

# Colors, from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_yaml(filename):
    logging.info(bcolors.OKBLUE+'Loading YAML '+filename+bcolors.ENDC)
    with open(filename, 'r') as f:
        # Select YAML loader (needs PyYAML 5.1+ to be safe)
        if int(yaml.__version__.split('.')[0]) > 5 or (int(yaml.__version__.split('.')[0]) == 5 and int(yaml.__version__.split('.')[1]) >= 1):
            return yaml.load(f, Loader=yaml.FullLoader)
        return yaml.load(f)

def dump_yaml(filename,yaml_data):
    logging.info(bcolors.OKBLUE+'Dumping YAML '+filename+bcolors.ENDC)
    with open(filename, 'w') as f:
        f.write(yaml.dump(yaml_data, default_flow_style=False))
    return 0

def merge_default_current(default_dict,current_dict):
    # supports any nested levels
    updated_dict = default_dict
    if current_dict is not None:
        for num, item in enumerate(default_dict, start=0):
            if item['type'] == 'dict':
                updated_dict[num]['sub'] = merge_default_current(default_dict[num]['sub'],current_dict[item['name']])
            if 'default_value' in item:
                if item['name'] in current_dict:
                    updated_dict[num]['default_value'] = current_dict[item['name']]
    return updated_dict

def demultiplex(dict1):
    # supports only one nested level for now
    buffer_dict =  dict1.copy()
    for key, value in dict1.items():
        print(key)
        if "." in key:
            del(buffer_dict[key])
            if not key.split('.')[0] in buffer_dict:
                buffer_dict[key.split('.')[0]] = {}
            buffer_dict[key.split('.')[0]][key.split('.')[1]] = value
    return buffer_dict

def mergearrays(dict_in):
    '''
        This function merge an ImmutableMultiDict from an HTML form POST
        based on PHP/Ruby standard forms array styntax. It replaces enctype="application/json"
        without need of Javascript.

        in: dict_in as ImmutableMultiDict type
        out: buffer_dict as dict type
    '''
    dict1=dict_in.to_dict(flat=False)
    buffer_dict = {}
    for key, value in dict1.items():
        print('key ' + key)
        if len(value) == 1:
            value = value[0]
        print(value)
        print(buffer_dict)
        merge_subarrays(buffer_dict,key,value)
    return buffer_dict

def merge_subarrays(dict1,key,value):
    if not "[" in key: # End of main key
        dict1[key] = value
    else:
        current_key = key.split('[')[0]
        print('current key ' + current_key)
        if key.split('[')[1] == ']': # End list
            print('this is an end list')
            # user['arthur']['phone'][] -> phone[]
            if not current_key in dict1:
                dict1[current_key] = []
            if type(value) is list:
                dict1[current_key].extend(value)
            else:
                dict1[current_key].append(value)
        elif key.split('[')[1].replace(']','').replace("'",'').replace('"','').isnumeric(): # List
            list_index = key.split('[')[1].replace(']','').replace("'",'').replace('"','')
            if not current_key in dict1:
                dict1[current_key] = []
            # user['arthur']['phone'][0]  -> phone[0] (called end list)
            # user['arthur']['phone'][0]['other']  -> phone[0]['other']
            if len(key.split('[')) == 2: # End list
                # phone[0]
                dict1[current_key]=list_extend_and_add(dict1[current_key],int(list_index),value)
            else: # Not end list, so dict
                # phone[0]['other']
                next_key = key.replace(current_key,'',1) # [0]['other']
                next_key = re.sub('\[','', next_key,count=1) # 0]['other']
                next_key = re.sub('[0-9]+\]','', next_key,count=1) # ['other']
                next_key = re.sub('\[[\'"]','', next_key,count=1) # other']
                next_key = re.sub('[\'"]\]','', next_key,count=1) # other

                if (len(dict1[current_key]) - 1) >= int(list_index): # Entry already exist, update it
                    list_extend_and_add(dict1[current_key],int(list_index),merge_subarrays(dict1[current_key][int(list_index)],next_key,value))
                else: # Entry does not exist, create it with empty dict (cannot be a list since we are already in a list)
                    list_extend_and_add(dict1[current_key],int(list_index),merge_subarrays({},next_key,value))
        else: # Dict
            # user['arthur']['phone']
            next_key = key.replace(current_key,'',1) # ['arthur']['phone']
            next_key = re.sub('\[[\'"]','', next_key,count=1) # arthur']['phone']
            next_key = re.sub('[\'"]\]','', next_key,count=1) # arthur['phone']
            if not current_key in dict1:
                dict1[current_key] = {}
            merge_subarrays(dict1[current_key],next_key,value)
    return dict1

def list_extend_and_add(list1, index, value):
    list1.extend([None] * ((max(index.start, index.stop - 1) if isinstance(index, slice) else index) - len(list1) + 1))
    list1[index]=value
    return list1

# services_ip['pxe_ip']
# user ['arthur'] ['name']
# {"user":{"arthur":{"name":"value"}}}
# user['arthur']['phones'][0]=toto
# user['names'][0]['phones']=toto

def form_as_dict(dict1):
    buffer_dict = {}
    for key, value in dict1.items():
        print(key)
        if not "[" in key:
            buffer_dict[key] = value
        else:
            json_string = ""
            json_revert_string = ""
            for num, sub_key in enumerate(key.split('['),start=1):
                if sub_key.replace(']','').replace("'","").replace('"','').isnumeric():
                    #if num == len(key.split('[')):
                    json_string = json_string + '['
                    json_revert_string = ']' + json_revert_string
                else:
                    json_string = json_string + '{"' + sub_key.replace(']','').replace("'","").replace('"','') + '":'
                    json_revert_string = '}' + json_revert_string
            json_string = json_string + '"' + value + '"' + json_revert_string
            #for i in key.split('['):
            #    json_string = json_string + '}'
            print(json_string)
            buffer_dict = MergeDictList(buffer_dict,json.loads(json_string))
#            if re.search("\[[0-9]*\]",key) is not None:

    return buffer_dict

def MergeDictList(dict1, dict2):
   ''' Merge dictionaries and keep values keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2 and type(value) is list:
               value.extend(dict1[key])
               dict3[key] = value
   return dict3

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def load_page_navigation_data(page_navigation_data):
    # Gather navigation data from each blueprint
    for service in page_navigation_data:
        if service['sub_navigation']:
            page_navigation_data[0]['sub_navigation_elements'] = load_yaml(service['path'].replace('.','/').replace('main','navigation.yml'))
    return page_navigation_data

def update_yaml(yamlFile,yamlPath,data):
  """This function inserts yaml data into a file
  
  Args:
      yamlFile ([string]): path to the file to write to
      yamlPath ([String]): list of the path to get to the attribute
      data ([string]): data that you want to insert into the path in the file. 

      for example, if your file looks like this :       
        general_settings:
          root_path: 

      then insertFile("file.yml",['general_settings','root_path'],test)      
      will result in your file looking like this:
      general_settings:
          root_path: test

  """
  if(len(yamlPath)==2):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  elif(len(yamlPath)==3):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]][yamlPath[2]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  elif(len(yamlPath)==4):
    stream=open(yamlFile,'r')
    fileData=yaml.safe_load(stream)
    fileData[yamlPath[0]][yamlPath[1]][yamlPath[2]][yamlPath[3]]=data
    with open(yamlFile, 'w', encoding='utf8') as outfile:
      outfile.write(yaml.dump(fileData,default_flow_style=False))
  else:
    print("Path superior to 4 is not supported")
  