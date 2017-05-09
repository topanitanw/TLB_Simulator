import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tlb import Tlb, Structure
from stats import Statistics

class Cpu:
  def __init__(self, yconfig):
    self.itlb = list()
    self.dtlb = list()
    # start hard coding the tlbs
    self.dtlb_total_level = len(yconfig['cpu']['tlb']['data'])
    self.itlb_total_level = len(yconfig['cpu']['tlb']['instruction'])
    # stats[0..1] are the statistics for individual tlbs
    # stats[-1] is for the overall instruction or data tlbs
    self.itlb_stats = list()
    self.dtlb_stats = list()
    self.init_tlb(self.dtlb, self.dtlb_total_level,
                  self.dtlb_stats, yconfig['cpu']['tlb']['data'])
    self.init_tlb(self.itlb, self.itlb_total_level,
                  self.itlb_stats, yconfig['cpu']['tlb']['instruction'],
                  False)

  def init_tlb(self, tlb_lst, tlb_len, tlb_stats, yconfig, data=True):
    for l in range(tlb_len):
      if yconfig[l]['private'] or data:
        if yconfig[l]['type'] == 'fully-associative':
          tlb_lst.append(Tlb(Structure.FULLY_ASSOCIATIVE, yconfig[l]['entry']))
        elif yconfig[l]['type'] == '2-way':
          tlb_lst.append(Tlb(Structure.SET2_ASSOCIATIVE, yconfig[l]['entry']))
        elif yconfig[l]['type'] == '4-way':
          tlb_lst.append(Tlb(Structure.SET4_ASSOCIATIVE, yconfig[l]['entry']))
        else:
          raise NotImplementedError("unimplemented tlb type")

        tlb_stats.append(Statistics())
        tlb_lst[-1].set_stats(tlb_stats[-1])
      else:
        # shared tlb -> let the data and instruction tlbs have
        # the same object.
        tlb_lst.append(self.dtlb[l])
        tlb_stats.append(self.dtlb_stats[l])

  def dtlb_lookup(self, dirty=False, tag=0, lru=0):
    return self.tlb_lookup(self.dtlb, self.dtlb_total_level, \
                           dirty, tag, lru)

  def itlb_lookup(self, tag=0, lru=0):
    return self.tlb_lookup(self.itlb, self.itlb_total_level, \
                           False, tag, lru)

  def tlb_lookup(self, tlb, level, dirty=False, tag=0, lru=0):
    hit = False
    for l in range(level):
      hit = tlb[l].lookup(dirty, tag, lru)
      if hit:
        break
    return hit

  def dlookup_update(self, res):
    self.dtlb_stats[-1].lookup_update(res)

  def ilookup_update(self, res):
    self.itlb_stats[-1].lookup_update(res)

  # generic getter/setter
  def get_dtlb(self, i):
    return self.dtlb[i]
  def get_itlb(self, i):
    return self.itlb[i]
  def get_dtlb_total_level(self):
    return self.dtlb_total_level
  def get_itlb_total_level(self):
    return self.itlb_total_level
  def get_dtlb_istats(self, i):
    return self.dtlb_stats[i]
  def get_itlb_istats(self, i):
    return self.itlb_stats[i]
  def get_dtlb_stats(self):
    return self.dtlb_stats
  def get_itlb_stats(self):
    return self.itlb_stats
