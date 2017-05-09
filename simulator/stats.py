class Statistics:
  def __init__(self):
    self.total_request = 0
    self.hit_count = 0
    self.miss_count = 0
  
  def __str__(self):
    text = "-------------------- stats --------------------\n"
    text += "total request: " + str(self.total_request)
    text += " hit: " + str(self.hit_count)
    text += " miss: " + str(self.miss_count) + "\n"
    text += "hit ratio: %.2f" % (self.get_hit_ratio())
    text += (" miss ratio: %.2f" % (self.get_miss_ratio())) + "\n\n"
    return text
  
  def lookup_update(self, res):
    self.total_request += 1
    if res:
      self.hit_count += 1
    else:
      self.miss_count += 1
  
  def get_hit_count(self):
    return self.hit_count
  
  def get_miss_count(self):
    return self.miss_count
  
  def get_total_request(self):
    return self.total_request
  
  def get_hit_ratio(self):
    return self.hit_count / float(self.total_request)
  
  def get_miss_ratio(self):
    return self.miss_count / float(self.total_request)

