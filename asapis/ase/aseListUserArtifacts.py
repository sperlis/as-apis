import json
from asapis.services.aselib import ASE
from asapis.utils.printUtil import out

ase = ASE()

# get current user information
res = ase.get("currentuser_v2")
user = res.json()
out("UserInfo ="  + json.dumps(user, indent=2))

out("Templates ="  + json.dumps(ase.inventory.templates, indent=2))
out("TestPolicies ="  + json.dumps(ase.inventory.test_policies, indent=2))
out("Folders ="  + json.dumps(ase.inventory.folders, indent=2))
out("Applications ="  + json.dumps(ase.inventory.applications, indent=2))

