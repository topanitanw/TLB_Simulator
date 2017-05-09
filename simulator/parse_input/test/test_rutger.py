import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from rutger import Operation, MemRequest

class TestMemRequest(unittest.TestCase):
  def test_init_w(self):
    line = "0, W, 0x0000a1bc"
    mr = MemRequest(line)
    self.assertEqual(mr.pid, 0)
    self.assertEqual(mr.oper, Operation.DATA_WRITE)
    self.assertEqual(mr.vaddr, 0x0000a1bc)
                     
  def test_init_r(self):
    line = "10, R, 0x00001594"
    mr = MemRequest(line)
    self.assertEqual(mr.pid, 10)
    self.assertEqual(mr.oper, Operation.DATA_READ)
    self.assertEqual(mr.vaddr, 0x00001594)

if __name__ == "__main__":
  unittest.main()
