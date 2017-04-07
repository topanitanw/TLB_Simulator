import unittest
import rutger_input as rinput
from Operation import Operation

class TestMemRequest(unittest.TestCase):
  def test_init_w(self):
    line = "0, W, 0x0000a1bc"
    mr = rinput.MemRequest(line)
    self.assertEqual(mr.pid, 0)
    self.assertEqual(mr.oper, Operation.WRITE)
    self.assertEqual(mr.vaddr, 0x0000a1bc)
                     
  def test_init_r(self):
    line = "10, R, 0x00001594"
    mr = rinput.MemRequest(line)
    self.assertEqual(mr.pid, 10)
    self.assertEqual(mr.oper, Operation.READ)
    self.assertEqual(mr.vaddr, 0x00001594)




if __name__ == "__main__":
  unittest.main()
