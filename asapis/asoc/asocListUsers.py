from asapis.utils.printUtil import print_json
from asapis.services.asoclib import ASoC

asoc = ASoC()

res = asoc.get("Users")

users = res.json()

print_json("Users:", users)
