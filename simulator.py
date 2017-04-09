#import constant.constants as constants
from constant import constants

INPUT_FILE = "input/dinero4/cc1.din/cc1.din"

if __name__ == "__main__":
  print("mask tag: 0x%016x mask offset: 0x%016x" \
        % (constants.MASK_TAG, constants.MASK_OFFSET))