import unittest
import dinero4 as rinput
from Operation import Operation

class TestMemRequest(unittest.TestCase):
  def test_init_w(self):
    line = "2 408ed4"
    mr = rinput.MemRequest(line)
    self.assertEqual(mr.operation, Operation.DWRITE)
    self.assertEqual(mr.virtual_address, 0x408ed4)
                     
  def test_init_r(self):
    line = "0 10019d94"
    mr = rinput.MemRequest(line)
    self.assertEqual(mr.operation, Operation.DREAD)
    self.assertEqual(mr.virtual_address, 0x10019d94)

if __name__ == "__main__":
  unittest.main()
