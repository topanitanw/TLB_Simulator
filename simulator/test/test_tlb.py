import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from tlb import Tlb, Structure
import constants

class TestTlb(unittest.TestCase):
  def test_init_set2_64(self):
    tlb = Tlb(Structure.SET2_ASSOCIATIVE, 64)
    self.assertEqual(tlb.get_type(), Structure.SET2_ASSOCIATIVE)
    self.assertEqual(tlb.get_set_index(), 32)
    self.assertEqual(tlb.set_num, 2)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)
    for i in range(tlb.get_set_index()):
      for j in range(tlb.get_set_num()):
        self.assertFalse(tlb.content[i][j].get_valid())
        self.assertFalse(tlb.content[i][j].get_dirty())
        self.assertEqual(tlb.content[i][j].get_lru(), 0)
        self.assertEqual(tlb.content[i][j].get_tag(), 0)
  
  def test_init_set4_64(self):
    tlb = Tlb(Structure.SET4_ASSOCIATIVE, 64)
    self.assertEqual(tlb.get_type(), Structure.SET4_ASSOCIATIVE)
    self.assertEqual(tlb.get_set_index(), 16)
    self.assertEqual(tlb.set_num, 4)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)
    for i in range(tlb.get_set_index()):
      for j in range(tlb.get_set_num()):
        self.assertFalse(tlb.content[i][j].get_valid())
        self.assertFalse(tlb.content[i][j].get_dirty())
        self.assertEqual(tlb.content[i][j].get_lru(), 0)
        self.assertEqual(tlb.content[i][j].get_tag(), 0)
  
  def test_init_full_64(self):
    tlb = Tlb(Structure.FULLY_ASSOCIATIVE, 64)
    self.assertEqual(tlb.get_type(), Structure.FULLY_ASSOCIATIVE)
    self.assertEqual(tlb.get_set_index(), 1)
    self.assertEqual(tlb.get_set_num(), 64)
    self.assertEqual(tlb.get_hit_count(), 0)
    self.assertEqual(tlb.get_total_request(), 0)
    for i in range(tlb.get_set_index()):
      self.assertFalse(tlb.content[i].get_valid())
      self.assertFalse(tlb.content[i].get_dirty())
      self.assertEqual(tlb.content[i].get_lru(), 0)
      self.assertEqual(tlb.content[i].get_tag(), 0)
  
  def test_lookup_fa(self):
    tlb = Tlb(Structure.FULLY_ASSOCIATIVE, 2)
    # print(tlb)
    
    self.assertFalse(tlb.lookup(True, constants.get_tag(0x408ed4), 10))
    # print(tlb)
    self.assertEqual(tlb.content[0].get_valid(), True)
    self.assertEqual(tlb.content[0].get_dirty(), True)
    self.assertEqual(tlb.content[0].get_tag(), 0x408)
    self.assertEqual(tlb.content[0].get_lru(), 10)
    
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x10019d94), 11))
    # print(tlb)
    self.assertEqual(tlb.content[1].get_valid(), True)
    self.assertEqual(tlb.content[1].get_dirty(), False)
    self.assertEqual(tlb.content[1].get_tag(), 0x10019)
    self.assertEqual(tlb.content[1].get_lru(), 11)
    
    self.assertTrue(tlb.lookup(False, constants.get_tag(0x408ed4), 12))
    # print(tlb)
    self.assertEqual(tlb.content[0].get_valid(), True)
    self.assertEqual(tlb.content[0].get_dirty(), True)
    self.assertEqual(tlb.content[0].get_tag(), 0x408)
    self.assertEqual(tlb.content[0].get_lru(), 12)
    
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x409ed8), 15))
    # print(tlb)
    self.assertEqual(tlb.content[1].get_valid(), True)
    self.assertEqual(tlb.content[1].get_dirty(), False)
    self.assertEqual(tlb.content[1].get_tag(), 0x409)
    self.assertEqual(tlb.content[1].get_lru(), 15)
  
  def test_lookup_set2(self):
    tlb = Tlb(Structure.SET2_ASSOCIATIVE, 4)
    # print(tlb)
    # miss [0][0] 0x408
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x408ed4), 9))
    self.assertEqual(tlb.content[0][0].get_valid(), True)
    self.assertEqual(tlb.content[0][0].get_dirty(), False)
    print(tlb.content[0][0].get_tag())
    self.assertEqual(tlb.content[0][0].get_tag(), int(0x408 / 2))
    self.assertEqual(tlb.content[0][0].get_lru(), 9)
    
    # make sure that there is no effect of the init in other entries
    # make sure that we do not have the same data inserted in
    # any entry
    self.assertEqual(tlb.content[1][0].get_valid(), False)
    self.assertEqual(tlb.content[1][0].get_dirty(), False)
    self.assertEqual(tlb.content[1][0].get_tag(), 0)
    self.assertEqual(tlb.content[1][0].get_lru(), 0)
    # make sure that data in the same set is not initialized
    self.assertEqual(tlb.content[0][1].get_valid(), False)
    self.assertEqual(tlb.content[0][1].get_dirty(), False)
    self.assertEqual(tlb.content[0][1].get_tag(), 0)
    self.assertEqual(tlb.content[0][1].get_lru(), 0)
    # end other entries
    
    # dirty bit and lru testing
    # dirty false -> true
    # hit [0][0] tag 0x408 dirty True, but tlb[0][0].dirty = True
    self.assertTrue(tlb.lookup(True, constants.get_tag(0x408ed4), 10))
    self.assertEqual(tlb.content[0][0].get_lru(), 10)
    self.assertEqual(tlb.content[0][0].get_dirty(), True)
    
    # miss [0][1] tag 0x40a, dirty +  true = true
    self.assertFalse(tlb.lookup(True, constants.get_tag(0x40aed4), 12))
    self.assertEqual(tlb.content[0][1].get_valid(), True)
    self.assertEqual(tlb.content[0][1].get_dirty(), True)
    self.assertEqual(tlb.content[0][1].get_tag(), int(0x40a / 2))
    self.assertEqual(tlb.content[0][1].get_lru(), 12)
    
    # dirty bit testing true + false = true
    self.assertTrue(tlb.lookup(False, constants.get_tag(0x40aed4), 12))
    self.assertEqual(tlb.content[0][1].get_dirty(), True)
    # end testing dirty bit
    
    # miss [1][0] tag 0x10019
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x10019d94), 11))
    self.assertEqual(tlb.content[1][0].get_valid(), True)
    self.assertEqual(tlb.content[1][0].get_dirty(), False)
    self.assertEqual(tlb.content[1][0].get_tag(), int(0x10019 / 2))
    self.assertEqual(tlb.content[1][0].get_lru(), 11)
    
    # miss [1][1] tag 0x10021
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x10021d94), 13))
    self.assertEqual(tlb.content[1][1].get_valid(), True)
    self.assertEqual(tlb.content[1][1].get_dirty(), False)
    self.assertEqual(tlb.content[1][1].get_tag(), int(0x10021 / 2))
    self.assertEqual(tlb.content[1][1].get_lru(), 13)
    
    # testing lru
    # hit [0][0] lru = 14
    self.assertTrue(tlb.lookup(True, constants.get_tag(0x408ed4), 14))
    self.assertEqual(tlb.content[0][0].get_valid(), True)
    self.assertEqual(tlb.content[0][0].get_dirty(), True)
    self.assertEqual(tlb.content[0][0].get_tag(), int(0x408 / 2))
    self.assertEqual(tlb.content[0][0].get_lru(), 14)
    
    # miss [1][0] lru = 15
    self.assertFalse(tlb.lookup(False, constants.get_tag(0x10023d94), 15))
    self.assertEqual(tlb.content[1][0].get_valid(), True)
    self.assertEqual(tlb.content[1][0].get_dirty(), False)
    self.assertEqual(tlb.content[1][0].get_tag(), int(0x10023 / 2))
    self.assertEqual(tlb.content[1][0].get_lru(), 15)

if __name__ == "__main__":
  unittest.main()
