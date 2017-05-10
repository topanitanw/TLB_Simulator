import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import cpu as mCpu
import tlb as mTlb
import constants as mConstants
import yaml as mYaml

FILE_NAME1 = "../config/test/conf_test1.conf"
FILE_NAME2 = "../config/test/conf_test2.conf"
FILE_NAME3 = "../config/test/conf_test3.conf"

def read_config(file_name):
  # try to use the absolute path instead of the relative one.
  file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
  config_file = open(file_path, 'r')
  yaml_config = mYaml.load(config_file)
  config_file.close()
  return yaml_config

class TestCpu(unittest.TestCase):
  def test_init_config(self):
    yaml_config = read_config(FILE_NAME1)
    self.assertEqual(len(yaml_config['cpu']['tlb']['data']), 2)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['level'], 1)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['private'], True)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['type'], "4-way" )
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['replacement'], "lru" )

    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['level'], 2)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['private'], True)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['type'], "4-way" )
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['replacement'], "lru" )

    self.assertEqual(len(yaml_config['cpu']['tlb']['instruction']), 2)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['level'], 1)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['private'], True)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['entry'], 4)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['type'], "2-way" )
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['replacement'], "lru" )

    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['level'], 2)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['private'], True)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['entry'], 4)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['type'], "2-way" )
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['replacement'], "lru" )

  def test_init_tlb_private(self):
    yaml_config = read_config(FILE_NAME1)
    cpui = mCpu.Cpu(yaml_config)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['entry'],
                     cpui.dtlb[0].get_set_index() * 4)
    self.assertEqual(cpui.dtlb[0].get_set_num(), 4)
    self.assertIsNot(cpui.dtlb[0], cpui.itlb[0])

    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['entry'],
                     cpui.dtlb[1].get_set_index() * 4)
    self.assertEqual(cpui.dtlb[1].get_set_num(), 4)
    self.assertIsNot(cpui.dtlb[1], cpui.itlb[1])

    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['entry'], 4)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['entry'],
                     cpui.itlb[0].get_set_index() * 2)
    self.assertEqual(cpui.itlb[0].get_set_num(), 2)
    self.assertIsNot(cpui.itlb[0], cpui.dtlb[0])

    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['entry'], 4)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['entry'],
                     cpui.itlb[1].get_set_index() * 2)
    self.assertEqual(cpui.itlb[1].get_set_num(), 2)
    self.assertIsNot(cpui.itlb[1], cpui.dtlb[1])

  def test_init_tlb_shared(self):
    yaml_config = read_config(FILE_NAME2)
    cpui = mCpu.Cpu(yaml_config)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][0]['entry'],
                     cpui.dtlb[0].get_set_index() * 4)
    self.assertEqual(cpui.dtlb[0].get_set_num(), 4)
    self.assertIsNot(cpui.dtlb[0], cpui.itlb[0])

    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['data'][1]['entry'],
                     cpui.dtlb[1].get_set_index() * 4)
    self.assertEqual(cpui.dtlb[1].get_set_num(), 4)
    self.assertIs(cpui.dtlb[1], cpui.itlb[1])

    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][0]['entry'],
                     cpui.itlb[0].get_set_index() * 4)
    self.assertEqual(cpui.itlb[0].get_set_num(), 4)
    self.assertIsNot(cpui.itlb[0], cpui.dtlb[0])

    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['entry'], 16)
    self.assertEqual(yaml_config['cpu']['tlb']['instruction'][1]['entry'],
                     cpui.itlb[1].get_set_index() * 4)
    self.assertEqual(cpui.itlb[1].get_set_num(), 4)
    self.assertIs(cpui.itlb[1], cpui.dtlb[1])

  def test_tlb_private(self):
    yaml_config = read_config(FILE_NAME3)
    cpui = mCpu.Cpu(yaml_config)
    # test miss L1/L2
    self.assertEqual(cpui.dtlb_lookup(False, 0x408ed4, 0), False)
    self.assertEqual(cpui.dtlb[0].content[0][0].tag, int(0x408ed4 / 2))
    self.assertEqual(cpui.dtlb[0].content[0][0].dirty, False)
    self.assertEqual(cpui.dtlb[1].content[0][0].tag, int(0x408ed4 / 2))
    self.assertEqual(cpui.dtlb[1].content[0][0].dirty, False)
    self.assertEqual(cpui.get_dtlb_istats(0).get_hit_count(), 0)
    self.assertEqual(cpui.get_dtlb_istats(0).get_miss_count(), 1)
    self.assertEqual(cpui.get_dtlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_dtlb_istats(1).get_miss_count(), 1)

    # test hit L1 dtlb
    self.assertEqual(cpui.dtlb_lookup(True, 0x408ed4, 0), True)
    self.assertEqual(cpui.dtlb[0].content[0][0].dirty, True)
    self.assertEqual(cpui.dtlb[1].content[0][0].dirty, False)    
    self.assertEqual(cpui.get_dtlb_istats(0).get_hit_count(), 1)
    self.assertEqual(cpui.get_dtlb_istats(0).get_miss_count(), 1)
    self.assertEqual(cpui.get_dtlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_dtlb_istats(1).get_miss_count(), 1)

    # test miss L1/L2 dtlb
    self.assertEqual(cpui.dtlb_lookup(False, 0x408ed8, 0), False)
    self.assertEqual(cpui.dtlb[0].content[0][1].tag, int(0x408ed8 / 2))
    self.assertEqual(cpui.dtlb[0].content[0][1].dirty, False)
    self.assertEqual(cpui.dtlb[1].content[0][1].tag, int(0x408ed8 / 2))
    self.assertEqual(cpui.dtlb[1].content[0][1].dirty, False)
    self.assertEqual(cpui.get_dtlb_istats(0).get_hit_count(), 1)
    self.assertEqual(cpui.get_dtlb_istats(0).get_miss_count(), 2)
    self.assertEqual(cpui.get_dtlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_dtlb_istats(1).get_miss_count(), 2)

    # ITLB
    # test miss L1/L2 itlb 0x10019d90
    self.assertEqual(cpui.itlb_lookup(0x10019d90, 0), False)
    self.assertEqual(cpui.itlb[0].content[0][0].tag, int(0x10019d90 / 2))
    self.assertEqual(cpui.itlb[0].content[0][0].dirty, False)
    self.assertEqual(cpui.itlb[1].content[0][0].tag, int(0x10019d90 / 2))
    self.assertEqual(cpui.itlb[1].content[0][0].dirty, False)
    self.assertEqual(cpui.get_itlb_istats(0).get_hit_count(), 0)
    self.assertEqual(cpui.get_itlb_istats(0).get_miss_count(), 1)
    self.assertEqual(cpui.get_itlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_itlb_istats(1).get_miss_count(), 1)

    # test miss L1/L2 itlb
    self.assertEqual(cpui.itlb_lookup(0x10019d94, 0), False)
    self.assertEqual(cpui.itlb[0].content[0][1].tag, int(0x10019d94 / 2))
    self.assertEqual(cpui.itlb[0].content[0][1].dirty, False)
    self.assertEqual(cpui.itlb[1].content[0][1].tag, int(0x10019d94 / 2))
    self.assertEqual(cpui.itlb[1].content[0][1].dirty, False)
    self.assertEqual(cpui.get_itlb_istats(0).get_hit_count(), 0)
    self.assertEqual(cpui.get_itlb_istats(0).get_miss_count(), 2)
    self.assertEqual(cpui.get_itlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_itlb_istats(1).get_miss_count(), 2)

    # test hit L1 itlb
    self.assertEqual(cpui.itlb_lookup(0x10019d90, 0), True)
    self.assertEqual(cpui.itlb[0].content[0][0].dirty, False)
    self.assertEqual(cpui.itlb[1].content[0][0].dirty, False)
    self.assertEqual(cpui.get_itlb_istats(0).get_hit_count(), 1)
    self.assertEqual(cpui.get_itlb_istats(0).get_miss_count(), 2)
    self.assertEqual(cpui.get_itlb_istats(1).get_hit_count(), 0)
    self.assertEqual(cpui.get_itlb_istats(1).get_miss_count(), 2)
    
if __name__ == "__main__":
  unittest.main()
