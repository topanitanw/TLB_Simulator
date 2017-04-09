import unittest
from tlb import Tlb
from structure import Structure
import sys
sys.path.append('..')
#from constant import constants
import constants.constants as Constants


class TestTlb(unittest.TestCase):
  def test_init_tlb_set2_64(self):
    tlb = Tlb(Structure.SET2_ASSOCIATIVE, 64)
    self.assertEqual(tlb.get_type(), Structure.SET2_ASSOCIATIVE)
    self.assertEqual(tlb.get_entry_num(), 64)
    self.assertEqual(tlb.set_num, 2)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)        
    for i in range(tlb.get_entry_num()):
      for j in range(tlb.get_set_num()):
        self.assertFalse(tlb.content[i][j].get_valid())
        self.assertFalse(tlb.content[i][j].get_dirty())
        self.assertEqual(tlb.content[i][j].get_lru(), 0)
        self.assertEqual(tlb.content[i][j].get_tag(), 0)
        
  def test_init_tlb_set4_64(self):
    tlb = Tlb(Structure.SET4_ASSOCIATIVE, 64)
    self.assertEqual(tlb.get_type(), Structure.SET4_ASSOCIATIVE)
    self.assertEqual(tlb.get_entry_num(), 64)
    self.assertEqual(tlb.set_num, 4)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)
    for i in range(tlb.get_entry_num()):
      for j in range(tlb.get_set_num()):
        self.assertFalse(tlb.content[i][j].get_valid())
        self.assertFalse(tlb.content[i][j].get_dirty())
        self.assertEqual(tlb.content[i][j].get_lru(), 0)
        self.assertEqual(tlb.content[i][j].get_tag(), 0)
        
  def test_init_tlb_full_64(self):
    tlb = Tlb(Structure.FULLY_ASSOCIATIVE , 64)
    self.assertEqual(tlb.get_type(), Structure.FULLY_ASSOCIATIVE)
    self.assertEqual(tlb.get_entry_num(), 64)
    self.assertEqual(tlb.set_num, 1)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)
    for i in range(tlb.get_entry_num()):
      self.assertFalse(tlb.content[i].get_valid())
      self.assertFalse(tlb.content[i].get_dirty())
      self.assertEqual(tlb.content[i].get_lru(), 0)
      self.assertEqual(tlb.content[i].get_tag(), 0)
      
  def test_tlb_fa(self):
    tlb = Tlb(Structure.FULLY_ASSOCIATIVE, 2)
    print(tlb)
    
    self.assertFalse(tlb.lookup(True, Constants.get_tag(0x408ed4), 10))
    print(tlb)
    self.assertEqual(tlb.content[0].get_valid(), True)
    self.assertEqual(tlb.content[0].get_dirty(), True)
    self.assertEqual(tlb.content[0].get_tag(), 0x408)
    self.assertEqual(tlb.content[0].get_lru(), 10)
    
    self.assertFalse(tlb.lookup(False, Constants.get_tag(0x10019d94), 11))
    print(tlb)
    self.assertEqual(tlb.content[1].get_valid(), True)
    self.assertEqual(tlb.content[1].get_dirty(), False)
    self.assertEqual(tlb.content[1].get_tag(), 0x10019)
    self.assertEqual(tlb.content[1].get_lru(), 11)    

    self.assertTrue(tlb.lookup(False, Constants.get_tag(0x408ed4), 12))
    print(tlb)
    self.assertEqual(tlb.content[0].get_valid(), True)
    self.assertEqual(tlb.content[0].get_dirty(), True)
    self.assertEqual(tlb.content[0].get_tag(), 0x408)
    self.assertEqual(tlb.content[0].get_lru(), 12)    

    print(1)
    self.assertFalse(tlb.lookup(False, Constants.get_tag(0x409ed8), 15))
    print(tlb)
    self.assertEqual(tlb.content[1].get_valid(), True)
    self.assertEqual(tlb.content[1].get_dirty(), False)
    self.assertEqual(tlb.content[1].get_tag(), 0x409)
    self.assertEqual(tlb.content[1].get_lru(), 15)    
        
if __name__ == "__main__":
  unittest.main()