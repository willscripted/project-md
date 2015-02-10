#!/usr/bin/python

import sys
import json
import pandocfilters

from sh import pandoc


# In: project json
# Out: pandoc json

if __name__ == "__main__":
  for line in sys.stdin:
    project = json.loads(line)

    project_name = "# " + project["name"]
    for chunk in pandoc(["-f", "markdown", "-t", "json"], _in=project_name ):
      header = json.loads(chunk)[1][0]
      sys.stderr.write(str(header) + "\n#####")

    doc = [{"unMeta": {}}, [header]]
    json.dump(doc, sys.stdout)
  sys.stdout.flush()
  sys.stdout.close()
