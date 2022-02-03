import yaml
import logging

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
        f.write(yaml.dump(yaml_data))
    return 0


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
  