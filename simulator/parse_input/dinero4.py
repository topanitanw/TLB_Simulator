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
    line = line.replace('\n', '').replace('\t', '').split(" ")
    
    self.virtual_address = int(line[1], 16)
    if int(line[0]) == 0:
      self.operation = Operation.DATA_READ
      
    elif int(line[0]) == 1:
      self.operation = Operation.DATA_WRITE
      
    elif int(line[0]) == 2:
      self.operation = Operation.INSTRUCTION_FETCH
      
    elif int(line[0]) == 3:
      self.operation = Operation.IGNORE
    else:
      raise ValueError("Unexpected Operations: ", line[0])

  def __str__(self):
    return "oper: %s vaddr: 0x%08x" % (self.operation, self.virtual_address)

  def get_operation(self):
    return self.operation
  def get_virtual_address(self):
    return self.virtual_address
