# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:19:46 2017

@author: PanitanW
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy.stats as stats
from parse_input.dinero4 import MemRequest, Operation
import cpu
import constants
import yaml

INPUT_FILE = "input/dinero4/cc1.din/cc1_200.din"
CONFIG_FILE = "config/intel_haswell.conf"

def print_stats(stats_lst, tlb_type):
  txt = ("++++++++++++++++ statistics of %s tlb ++++++++++++++++\n" % tlb_type)
  for i in range(len(stats_lst)):
    txt += "level: " + str(i) + "\n"
    txt += str(stats_lst[i])

  txt += (" %s overview: " % tlb_type) + "\n"
  txt += str(stats_lst[-1])
  print(txt)

def tag_graphs(tag_data, tag_instruction):
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
  plt.savefig("test.jpg")
  plt.show()

def read_config(file_name):
  config_file = open(file_name, 'r')
  yaml_config = yaml.load(config_file)
  config_file.close()
  return yaml_config

if __name__ == "__main__":
  print("----------------------------------------------------\n\n")
  yconfig = read_config(CONFIG_FILE)
  cpu1 = cpu.Cpu(yconfig)
  tag_data = list()
  tag_instruction = list()
  with open(INPUT_FILE, 'rt') as input_file:
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

  print_stats(cpu1.get_dtlb_stats(), "data")
  print_stats(cpu1.get_itlb_stats(), "instruction")
  tag_graphs(tag_data, tag_instruction)
