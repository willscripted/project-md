#!/usr/bin/python

import sys
import json
import pandocfilters

# In: Pandoc Json
# Out: Project Json
if __name__ == "__main__":
  doc = sys.stdin.read()
  json.dump({"to": "json"}, sys.stdout)
