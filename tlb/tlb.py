import statistics as stats
from structure import *
import entry as tlb_entry

class Tlb:
  def __init__(self, tlb_type, entry_num):
    self.stats = stats.Statistics()
    self.tlb_type = tlb_type
    self.entry_num = entry_num

    if tlb_type == Structure.FULLY_ASSOCIATIVE:
      self.content = [tlb_entry.Entry()] * entry_num
      self.set_num = 1
      
    elif tlb_type == Structure.SET2_ASSOCIATIVE:
      self.content = [[tlb_entry.Entry()] * 2] * entry_num
      self.set_num = 2
      
    elif tlb_type == Structure.SET4_ASSOCIATIVE:
      self.content = [[tlb_entry.Entry()] * 4] * entry_num
      self.set_num = 4

  def __str__(self):
    tlb_str = "\n\n-------------------- TLB Status --------------------\n"
    tlb_str += "tlb type: "+str(self.tlb_type)+" "
    tlb_str += "entry_num: "+str(self.entry_num)+"\n"
    tlb_str += self.print_content()
    tlb_str += "----------------------------------------------------\n"
    return tlb_str

  def print_content(self):
    content_str = ""
    if self.tlb_type == Structure.FULLY_ASSOCIATIVE:
      for i in range(self.entry_num):
        content_str += ("entry: %d %s\n" %(i, str(self.content[i])))
      
    else:
      for ientry in range(self.entry_num):
        content_str += ("entry: %d" % ientry)
        for jset in range(self.set_num):
          content_str += "\t%s" %(str(self.content[ientry][jset]))
        content_str += "\n"
    return content_str
    
  def get_hit_count(self):
    return self.stats.get_hit_count()
  def get_miss_count(self):
    return self.stats.get_miss_count()
  def get_total_request(self):
    return self.stats.get_total_request()
  def get_type(self):
    return self.tlb_type
  def get_entry_num(self):
    return self.entry_num
  def get_set_num(self):
    return self.set_num

  def lookup(self, dirty=False, tag=0, lru=0):
    if self.tlb_type == Structure.FULLY_ASSOCIATIVE:
      res = self.lookup_fa(dirty, tag, lru)
      self.stats.lookup_update(res)
      return res

  # TLB fully associative function  
  def lookup_fa(self, dirty=False, tag=0, lru=0):
    for i in range(self.entry_num):
      if self.content[i].get_valid():
        if self.content[i].get_tag() == tag:
          self.content[i].update_lru(lru)
          if dirty:
            self.content[i].set_dirty(dirty)
          return True # hit
        continue
        
      self.content[i] = tlb_entry.Entry(True, dirty, tag, lru)
      return False # miss

    self.evict_fa(dirty, tag, lru)
    return False

  def evict_fa(self, dirty, tag, lru):
    min_index = 0
    # python 3 does not have the max integer
    min_lru = float ("inf")
    for i in range(self.entry_num):
      if min_lru > self.content[i].get_lru():
        min_lru = self.content[i].get_lru()
        min_index = i
    print(min_index, min_lru)
    self.content[min_index] = tlb_entry.Entry(True, dirty, tag, lru)
    
  # flush_entire_tlb
  # flush_entry
