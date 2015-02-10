#!/usr/bin/python

import sys
import json
import pandocfilters

# In: Pandoc Json
# Out: Project Json

if __name__ == "__main__":
  for line in sys.stdin:
    doc = json.loads(line)
    altered = {}
    for thing in doc[1]:
      if thing["t"] == "Header" and thing["c"][0] == 1:
        altered["name"] = pandocfilters.stringify(thing["c"])
        altered["type"] = "project"
        altered["description"] = ""
        altered["content"] = []
        json.dump(altered, sys.stdout)

  sys.stdout.flush()
  sys.stdout.close()
