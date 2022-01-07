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