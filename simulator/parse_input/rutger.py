import enum

class Operation(enum.Enum):
  DATA_READ = 0
  DATA_WRITE = 1
  INSTRUCTION_FETCH = 2
  IGNORE = 3
  
  def __eq__(self, other):
    return self.value == other.value

class MemRequest:
  def __init__(self, line):
    line = line.replace('\n', '').replace('\t', '').split(", ")
    print(line)
    
    self.vaddr = int(line[2], 16)
    if line[1].lower() == 'r':
      self.oper = Operation.DATA_READ
    elif line[1].lower() == 'w':
      self.oper = Operation.DATA_WRITE
    else:
      raise ValueError("Unexpected Operations: ", line[1])

    self.pid = int(line[0])
    
    
      
  
