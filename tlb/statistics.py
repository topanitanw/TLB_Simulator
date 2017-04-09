class Statistics:
  def __init__(self):
    self.total_request = 0
    self.hit_count = 0
    self.miss_count = 0

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
    return self.miss_count / float(self.total_count)
  
