import stats as stats
import entry as tlb_entry
import enum

class Structure(enum.Enum):
  FULLY_ASSOCIATIVE = 0
  # TODO the direct map tlb/cache is not implemented yet.
  DIRECT_MAP = 1
  SET2_ASSOCIATIVE = 2
  SET4_ASSOCIATIVE = 4
  
  def __eq__(self, other):
    # problem when compare the class
    if self.__class__ == other.__class__:
      return self.value == other.value
    else:
      return False  


class Tlb:
  '''
  TLB class
  '''  
  def __init__(self, tlb_type, entry_num):
    self.stats = stats.Statistics()
    self.tlb_type = tlb_type
    if tlb_type == Structure.FULLY_ASSOCIATIVE:
      # a fully associative cache has multiple blocks in one set
      self.set_num = entry_num
      # We do not need an index for a fully-associative tlb/cache
      self.set_index = 1
      self.content = [tlb_entry.Entry()] * entry_num

    elif tlb_type == Structure.DIRECT_MAP:
      self.set_num = 1
      # the index =
      # the total number of entries / N (number of sets)
      self.set_index = int(entry_num / 2)
      self.init_content_set()
      
    elif tlb_type == Structure.SET2_ASSOCIATIVE:
      self.set_num = 2
      # the index =
      # the total number of entries / N (number of sets)
      self.set_index = int(entry_num / 2)
      self.init_content_set()
    
    elif tlb_type == Structure.SET4_ASSOCIATIVE:
      self.set_num = 4
      self.set_index = int(entry_num / 4)
      self.init_content_set()
    
    else:
      raise NotImplementedError("unimplemented tlb type")
  
  def __str__(self):
    '''
    String representation of the TLB class
    '''
    tlb_str = "\n\n-------------------- TLB Status --------------------\n"
    tlb_str += "tlb type: " + str(self.tlb_type) + " "
    tlb_str += "entry_num: " + str(self.set_num) + "\n"
    tlb_str += self.print_content()
    tlb_str += "----------------------------------------------------\n"
    return tlb_str
  
  def print_content(self):
    '''
    String representation of the TLB content
    '''
    content_str = ""
    if self.tlb_type == Structure.FULLY_ASSOCIATIVE:
      for i in range(self.set_num):
        content_str += ("entry: %d %s\n" % (i, str(self.content[i])))
    
    else:
      for index in range(self.set_index):
        content_str += ("index: %d " % index)
        for jset in range(self.set_num):
          content_str += "| %s \t|" % (str(self.content[index][jset]))
        content_str += "\n"
    return content_str
  
  def init_content_set(self):
    self.content = list()
    # does not work since every pointer entry will be pointing to the same
    # list entry [tlb_entry.Entry()] * entry_num
    # self.content = [[tlb_entry.Entry()] * 2] * entry_num    
    # tlb_type contain 
    for _ in range(self.set_index):
      entry = [tlb_entry.Entry()] * self.set_num
      self.content.append(entry)

  # generic getter/setter of the private variable
  def get_hit_count(self):
    return self.stats.get_hit_count()
  
  def get_miss_count(self):
    return self.stats.get_miss_count()
  
  def get_total_request(self):
    return self.stats.get_total_request()
  
  def get_type(self):
    return self.tlb_type
  
  def get_set_index(self):
    return self.set_index
  
  def get_set_num(self):
    return self.set_num
  
  def set_stats(self, tlb_stats):
    self.stats = tlb_stats
  
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
      # TODO define how to find the tag an index more formally
      index = tag % self.set_index
      tag = int(tag / self.set_index)
      res = self.lookup_set(index, dirty, tag, lru)
      self.stats.lookup_update(res)
      return res
    else:
      raise NotImplementedError("unimplemented tlb type")
  
  # TLB fully associative function
  def lookup_fa(self, dirty=False, tag=0, lru=0):
    for i in range(self.set_num):
      if self.content[i].get_valid():
        if self.content[i].get_tag() == tag:
          self.content[i].update_lru(lru)
          if dirty:
            self.content[i].set_dirty(dirty)
          return True  # hit
        continue
      
      self.content[i] = tlb_entry.Entry(True, dirty, tag, lru)
      return False  # miss
    
    self.evict_fa_lru(dirty, tag, lru)
    return False  # miss
  
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
  
  def lookup_set(self, index=0, dirty=False, tag=0, lru=0):
    '''
    TLB lookup method for the x-set associative TLB
    '''
    for iset in range(self.set_index):
      if self.content[index][iset].get_valid():
        if self.content[index][iset].get_tag() == tag:
          self.content[index][iset].update_lru(lru)
          # dirty |= new_dirty
          if dirty:
            self.content[index][iset].set_dirty(dirty)
          return True  # hit
        continue
      
      self.content[index][iset] = tlb_entry.Entry(True, dirty, tag, lru)
      return False  # miss
    
    self.evict_set_lru(index, dirty, tag, lru)
    return False
  
  def evict_set_lru(self, index, dirty, tag, lru):
    '''
    TLB LRU replacement for fully associative TLB
    '''
    min_iset = 0
    # python 3 does not have the max integer
    min_lru = float("inf")
    for iset in range(self.set_num):
      if min_lru > self.content[index][iset].get_lru():
        min_lru = self.content[index][iset].get_lru()
        min_iset = iset
    
    self.content[index][min_iset] = tlb_entry.Entry(True, dirty, tag, lru)\

    # TODO
    # direct map tlb
    # flush_entire_tlb
