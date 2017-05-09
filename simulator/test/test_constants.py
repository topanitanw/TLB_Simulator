import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import constants

class TestConstant(unittest.TestCase):
  def test_mask64(self):
    self.assertEqual(constants.get_offset(0xdeadbeefbeefdead), 0xead)
    self.assertEqual(constants.get_tag(0xdeadbeefbeefdead),
                     0xdeadbeefbeefd)  

  # def test_offset(self):
  #   vaddr = 0x408ed4
  #   self.assertEqual(constants.get_offset(vaddr), constants.getoffset(vaddr))

  # def test_tag(self):
  #   vaddr = 0x408ed4
  #   self.assertEqual(constants.get_tag(vaddr), constants.gettag(vaddr))

  # def test_index(self):
  #   vaddr = 0x408ed4
  #   self.assertEqual(constants.get_tag(vaddr), constants.gettag(vaddr))
if __name__ == "__main__":
  unittest.main()
