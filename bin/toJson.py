#!/usr/bin/python

import sys
import json
import pandocfilters

# In: Pandoc Json
# Out: Project Json

if __name__ == "__main__":
  for line in sys.stdin:
    doc = json.loads(line)
    json.dump(doc, sys.stdout)

  sys.stdout.flush()
  sys.stdout.close()
