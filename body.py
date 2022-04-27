import os
import sys
import json

items = os.scandir(sys.argv[1])
body = {}
 
for entry in items:
    if not entry.is_dir():
        continue

    with open(os.path.join(sys.argv[1], entry.name, "score")) as f:
        a = json.load(f)

        for k, v in a.items():
            if k in body:
                body[k] += v
            else:
                body[k] = v

print(body)
