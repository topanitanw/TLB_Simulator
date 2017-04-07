import pylab as pl
import numpy as np

INPUT_FILE = "../input/rutger/input_1p.txt"

def dic_increase(dic, key):
  if key in dic:
    dic[key] += 1
  else:
    dic[key] = 1
    
if __name__ == "__main__":
  pid_count = {}
  ops_count = {'r' : 0, 'w' : 0}
  mem_addrd = {}
  total_line = 0
  with open(INPUT_FILE, 'r') as f:
    for line in f.readlines():
      total_line += 1
      line = line.replace('\n', '').split(", ")
      dic_increase(pid_count, line[0])
      dic_increase(ops_count, line[1].lower())
      dic_increase(mem_addrd, line[2])

  print("read: ", ops_count['r'], ops_count['r']/float(total_line))
  print("write: ", ops_count['w'], ops_count['w']/float(total_line))
  for pid in sorted(pid_count.keys()):
    print("pid: ", pid, pid_count[pid], pid_count[pid]/float(total_line))

  pl.hist(list(mem_addrd.values()))
  pl.show()
  
  
