from Operation import Operation

class MemRequest:
  def __init__(self, line):
    line = line.replace('\n', '').replace('\t', '').split(" ")
    print(line)
    
    self.virtual_addr = int(line[1], 16)
    if line[0] == '0':
      self.operation = Operation.DREAD
    elif line[0] == '1':
      self.operation = Operation.DWRITE
    elif line[0] == '2':
      self.operation = Operation.IFETCH
    else:
      raise ValueError("Unexpected Operations: ", line[0])

  def __str__(self):
    return "oper: %s vaddr: 0x%08x" % self.operation, self.virtual_addr
