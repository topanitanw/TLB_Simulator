import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from dinero4 import Operation, MemRequest

class TestMemRequest(unittest.TestCase):
  def test_init_w(self):
    line = "1 408ed4"
    mr = MemRequest(line)
    print(mr)
    self.assertEqual(mr.get_operation(), Operation.DATA_WRITE)
    self.assertEqual(mr.get_virtual_address(), 0x408ed4)
                     
  def test_init_r(self):
    line = "0 10019d94"
    mr = MemRequest(line)
    self.assertEqual(mr.get_operation(), Operation.DATA_READ)
    self.assertEqual(mr.get_virtual_address(), 0x10019d94)
    
  def test_init_if(self):
    line = "2 408ed8"
    mr = MemRequest(line)
    self.assertEqual(mr.get_operation(), Operation.INSTRUCTION_FETCH)
    self.assertEqual(mr.get_virtual_address(), 0x408ed8)

  def test_init_if(self):
    line = "3 408ed8"
    mr = MemRequest(line)
    self.assertEqual(mr.get_operation(), Operation.IGNORE)
    self.assertEqual(mr.get_virtual_address(), 0x408ed8)
    
if __name__ == "__main__":
  unittest.main()
