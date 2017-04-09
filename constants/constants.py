import math

# general settings
MACHINE_TYPE = 64

# general constants
MASK64 = 0xffffffffffffffff
MASK32 = 0xffffffff
PAGE_SIZE4K = 4 * 1024

# simulated machine 
PAGE_SIZE = PAGE_SIZE4K
MASK_MACHINE = MASK64

MASK_TAG = (MASK64 << int(math.log(PAGE_SIZE, 2))) & MASK_MACHINE
MASK_OFFSET = (~(MASK64 << int(math.log(PAGE_SIZE, 2)))) & MASK_MACHINE

def get_offset(vaddr):
  return (MASK_OFFSET & vaddr)

def get_tag(vaddr):
  return (MASK_TAG & vaddr) >> int(math.log(PAGE_SIZE, 2))
