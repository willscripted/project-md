#!/usr/bin/python

import sys
import json
import pandocfilters


# In: project json
# Out: pandoc json

if __name__ == "__main__":
  doc = json.loads(sys.stdin.read())
  sys.stdout.write('# toMd! ')
