import sys
sys.path.append('.')
import statistics as stats
from structure import Structure
import entry as tlb_entry

class Tlb:
  '''
  TLB class
  '''
  def __init__(self, tlb_type, entry_num):
    self.stats = stats.Statistics()
    self.tlb_type = tlb_type
    self.entry_num = entry_num

    if tlb_type == Structure.FULLY_ASSOCIATIVE:
      self.content = [tlb_entry.Entry()] * entry_num
      # a fully associative cache has multiple sets, but only one entry.
      self.set_num = entry_num
      self.entry_num = 1

    elif tlb_type == Structure.SET2_ASSOCIATIVE:
      self.set_num = 2
      self.init_content_set()
    elif tlb_type == Structure.SET4_ASSOCIATIVE:
      self.set_num = 4
      self.init_content_set()
    else:
      raise NotImplementedError

  def __str__(self):
    '''
    String representation of the TLB class
    '''
    tlb_str = "\n\n-------------------- TLB Status --------------------\n"
    tlb_str += "tlb type: "+str(self.tlb_type)+" "
    tlb_str += "entry_num: "+str(self.entry_num)+"\n"
    tlb_str += self.print_content()
    tlb_str += "----------------------------------------------------\n"
    return tlb_str

  def print_content(self):
    '''
    String representation of the TLB content
    '''
    content_str = ""
    if self.tlb_type == Structure.FULLY_ASSOCIATIVE:
      for i in range(self.entry_num):
        content_str += ("entry: %d %s\n" %(i, str(self.content[i])))

    else:
      for ientry in range(self.entry_num):
        content_str += ("entry: %d " % ientry)
        for jset in range(self.set_num):
          content_str += "| %s \t|" %(str(self.content[ientry][jset]))
        content_str += "\n"
    return content_str

  def init_content_set(self):
    self.content = list()
    for _ in range(self.entry_num):
      entry = [tlb_entry.Entry()] * self.set_num
      self.content.append(entry)
      # does not work since every pointer entry will be pointing to the same
      # list entry [tlb_entry.Entry()] * entry_num
      # self.content = [[tlb_entry.Entry()] * 2] * entry_num
    
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
    '''
    TLB look up method

    return:
      True if TLB hits
      False if TLB misses
    '''
    if self.tlb_type == Structure.FULLY_ASSOCIATIVE:
      res = self.lookup_fa(dirty, tag, lru)
      self.stats.lookup_update(res)
      return res
    elif self.tlb_type == Structure.SET2_ASSOCIATIVE or \
         self.tlb_type == Structure.SET4_ASSOCIATIVE:
      entry_num = tag % self.entry_num
      res = self.lookup_set(entry_num, dirty, tag, lru)
      self.stats.lookup_update(res)
      return res
    else:
      raise NotImplementedError

  # TLB fully associative function
  def lookup_fa(self, dirty=False, tag=0, lru=0):
    for i in range(self.set_num):
      if self.content[i].get_valid():
        if self.content[i].get_tag() == tag:
          self.content[i].update_lru(lru)
          if dirty:
            self.content[i].set_dirty(dirty)
          return True # hit
        continue

      self.content[i] = tlb_entry.Entry(True, dirty, tag, lru)
      return False # miss

    self.evict_fa_lru(dirty, tag, lru)
    return False # miss

  def evict_fa_lru(self, dirty, tag, lru):
    '''
    TLB LRU replacement for fully associative TLB
    '''
    min_index = 0
    # python 3 does not have the max integer
    min_lru = float("inf")
    for i in range(self.set_num):
      if min_lru > self.content[i].get_lru():
        min_lru = self.content[i].get_lru()
        min_index = i

    self.content[min_index] = tlb_entry.Entry(True, dirty, tag, lru)


  def lookup_set(self, entry=0, dirty=False, tag=0, lru=0):
    '''
    TLB lookup method for the x-set associative TLB
    '''
    for iset in range(self.set_num):
      if self.content[entry][iset].get_valid():
        if self.content[entry][iset].get_tag() == tag:
          self.content[entry][iset].update_lru(lru)
          if dirty:
            # dirty |= new_dirty 
            self.content[entry][iset].set_dirty(dirty)
          return True # hit
        continue

      self.content[entry][iset] = tlb_entry.Entry(valid=True, dirty=dirty, tag=tag, lru=lru)
      return False # miss

    self.evict_set_lru(entry, dirty, tag, lru)
    return False

  def evict_set_lru(self, entry, dirty, tag, lru):
    '''
    TLB LRU replacement for fully associative TLB
    '''
    min_iset = 0
    # python 3 does not have the max integer
    min_lru = float("inf")
    for iset in range(self.set_num):
      if min_lru > self.content[entry][iset].get_lru():
        min_lru = self.content[entry][iset].get_lru()
        min_iset = iset

    self.content[entry][min_iset] = tlb_entry.Entry(True, dirty, tag, lru)

  # TODO
  # flush_entire_tlb
