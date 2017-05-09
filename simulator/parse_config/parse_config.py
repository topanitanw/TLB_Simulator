import yaml

config_file = "../config/intel_haswell.conf"
print(yaml.dump(yaml.load(open(config_file, 'r'))))
config = yaml.load(open(config_file, 'r'))
print(str(config) + '\n')
print(yaml.dump(config["cpu"]))
print()
print(yaml.dump(config["cpu"]["tlb"]["data"]))
print()
print(type(config["cpu"]["tlb"]["data"][0]["level"]))

# class Config:
#   def __init__(self, file_name):
#     config_file = open(file_name, 'r')
#     self.yaml_config = yaml.load(config_file)
#     config_file.close()

#   def get_yaml(self):
#     return self.yaml_config

  
