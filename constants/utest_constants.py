import unittest
import constants

class TestConstant(unittest.TestCase):
  def test_mask64(self):
    self.assertEqual(constants.get_offset(0xdeadbeefbeefdead), 0xead)
    self.assertEqual(constants.get_tag(0xdeadbeefbeefdead),
                     0xdeadbeefbeefd)  

if __name__ == "__main__":
  unittest.main()
