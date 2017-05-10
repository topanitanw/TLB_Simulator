# -*- coding: utf-8 -*-
import os                          # get the absolute file path
import sys                         # get the absolute file path
import yaml                        # read the yaml file
import numpy as np                 # plotting graphs
import matplotlib.pyplot as plt    # plotting graphs
import matplotlib.ticker as ticker # plotting graphs
import scipy.stats as stats        # plotting graphs
import datetime                    # filename
from parse_input.dinero4 import MemRequest, Operation
import cpu
import constants

INPUT_FILE = "input/dinero4/tex.din/tex.din"
CONFIG_FILE = "config/intel_haswell.conf"
EXPERIMENT_DIR = "./experiment_result"

# file/folder management --------------------------------------------------
def get_absolute_path(file_name):
  '''Get the absolute path of the file
  Args:
    file_name (string): the filename

  Return:
    (string): the absolute path of the filename
  '''
  # try to use the absolute path instead of the relative one.
  return os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))

def get_filename(path_name):
  '''Split the filename out of the file directory
  Args:
    path_name (string): the name of the file directory

  Return:
    string: the filename in that path without the file extension
  '''
  return os.path.basename(path_name).split('.')[0]

def create_folder(dir_name):
  '''Create a folder
  Args:
    dir_name (string): the name of directory

  Return:
    (string): the absolute path of the created directory
  '''
  absolute_path = get_absolute_path(dir_name)
  if not os.path.exists(absolute_path):
    os.makedirs(absolute_path)

  return absolute_path

def create_subexperiment_folder(dir_name):
  '''Create a sub experiment folder with a format name
  cc1_2017-05-15_11-34.

  Args:
    dir_name (string): the name of directory

  Return:
    (string): the absolute path to the created directory
  '''
  ex_path_dir = create_folder(dir_name)
  datetime_str = datetime.datetime.now().strftime('%y-%m-%d_%H-%M')
  subex_name = '_'.join([get_filename(INPUT_FILE), datetime_str])
  return create_folder(os.path.join(ex_path_dir, subex_name))
  
def save_stats(dtlb_stats, itlb_stats, dtag, itag):
  '''Save the statistics into a text file and a graph
  Args:
    dtlb_stats (a list of Stats Objects)
  '''
  print("save_stats fn")
  subex_path = create_subexperiment_folder(EXPERIMENT_DIR)
  
  input_filename = get_filename(INPUT_FILE)
  print("str_stats dtlb")
  dstats_str = str_stats(dtlb_stats, "data")
  print(dstats_str)
  print("str_stats itlb")  
  istats_str = str_stats(itlb_stats, "instruction")
  print(istats_str)
  file_stats = open(os.path.join(subex_path, input_filename + ".txt"), 'w+')
  file_stats.write(CONFIG_FILE + "\n")
  file_stats.write(istats_str)
  file_stats.write(dstats_str)
  file_stats.close()
  tag_graphs(dtag, itag, subex_path)
    
def str_stats(stats_lst, tlb_type):
  txt = ("++++++++++++++++ statistics of %s tlb ++++++++++++++++\n" % tlb_type)
  for i in range(len(stats_lst)):
    if i == len(stats_lst) - 1:
      txt += ("%s overview: " % tlb_type) + "\n"
      txt += str(stats_lst[i])
    else:
      txt += "level: " + str(i) + "\n"
      txt += str(stats_lst[i])

  return txt
  
def tag_graphs(tag_data, tag_instruction, save_dir):
  tag_data = [int(x) for x in tag_data]
  tag_instrution = [int(y) for y in tag_instruction]
  # tag = tag_data + tag_instruction
  # xmin = min(tag)
  # xmax = max(tag)
  
  plt.figure(1)
  plt.subplot(211)
  tag_data = sorted(tag_data)
  plt.hist(tag_data, alpha=0.5, color='r', rwidth=0.4, normed=True)
  #plt.xlim(xmin, xmax)
  plt.title('Tag Data')

  plt.subplot(212)
  tag_instruction = sorted(tag_instruction)
  plt.hist(tag_instruction, alpha=0.5, color='g', rwidth=0.4, normed=True)
  #plt.xlim(xmin, xmax)
  plt.title('Tag Instruction')
  plt.subplots_adjust(top=0.92, bottom=0.08, left=0.15,
                      right=0.95, hspace=0.4, wspace=0.35)
  file_name = '_'.join([get_filename(INPUT_FILE), "tag-distribution.jpg"])
  file_dir = os.path.join(save_dir, file_name)
  plt.savefig(file_dir)
  plt.show()

def read_config(file_name):
  file_path = get_absolute_path(CONFIG_FILE)
  file_config = open(file_path, 'r')
  yaml_config = yaml.load(file_config)
  file_config.close()
  return yaml_config

if __name__ == "__main__":
  print("----------------------------------------------------\n\n")
  yconfig = read_config(CONFIG_FILE)
  cpu1 = cpu.Cpu(yconfig)
  tag_data = list()
  tag_instruction = list()
  with open(get_absolute_path(INPUT_FILE), 'rt') as input_file:
    line_num = 0
    for line in input_file:
      mem_request = MemRequest(line)
      tag = constants.get_tag(mem_request.get_virtual_address())
      print(str(line_num) + " " + str(mem_request) + " tag: " + hex(tag))
      res = False
      if mem_request.get_operation() == Operation.DATA_READ or \
         mem_request.get_operation() == Operation.DATA_WRITE:
        tag_data.append(tag)
        if mem_request.get_operation() == Operation.DATA_READ:
          res = cpu1.dtlb_lookup(False, tag, line_num)

        elif mem_request.get_operation() == Operation.DATA_WRITE:
          res = cpu1.dtlb_lookup(True, tag, line_num)

        else:
          raise NotImplementedError("Wrong data type")

        cpu1.dlookup_update(res)

      elif mem_request.get_operation() == Operation.INSTRUCTION_FETCH:
        tag_instruction.append(tag)
        res = cpu1.itlb_lookup(tag, line_num)
        cpu1.ilookup_update(res)

      elif mem_request.get_operation() == Operation.IGNORE:
        print("ignore")

      else:
        raise NotImplementedError("Wrong Type")

      line_num += 1

  print("saving stats")
  save_stats(cpu1.get_dtlb_stats(), cpu1.get_itlb_stats(),
             tag_data, tag_instruction)
             
