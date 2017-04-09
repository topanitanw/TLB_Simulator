
class Entry:
  # python cannot have multiple class constructors like Java or C++.
  # We can define the default values of each argument instead
  def __init__(self, valid=False, dirty=False, tag=0, lru=0):
    self.valid = valid
    self.dirty = dirty
    self.tag = tag
    self.lru = lru

  def __str__(self):
    return ("valid: %d dirty: %d tag: 0x%x lru: %d" \
            %(self.valid, self.dirty, self.tag, self.lru))
                  
  def get_dirty(self):
    return self.dirty
  def set_dirty(self, dirty):
    self.dirty = dirty    
  def get_lru(self):
    return self.lru
  def update_lru(self, lru):
    self.lru = lru
  def get_tag(self):
    return self.tag
  def set_tag(self, new_tag):
    self.tag = new_tag
  def get_valid(self):
    return self.valid
  def set_valid(self, vbit):
    self.valid = vbit
  
