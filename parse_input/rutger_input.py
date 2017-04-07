from Operation import Operation

class MemRequest:
  def __init__(self, line):
    line = line.replace('\n', '').replace('\t', '').split(", ")
    print(line)
    
    self.vaddr = int(line[2], 16)
    if line[1].lower() == 'r':
      self.oper = Operation.READ
    elif line[1].lower() == 'w':
      self.oper = Operation.WRITE
    else:
      raise ValueError("Unexpected Operations: ", line[1])

    self.pid = int(line[0])
    
    
      
  
