import enum

class Operation(enum.Enum):
  DATA_READ = 0
  DATA_WRITE = 1
  INSTRUCTION_FETCH = 2
  
