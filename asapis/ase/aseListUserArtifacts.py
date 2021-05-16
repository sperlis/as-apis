from asapis.services.aselib import ASE
from asapis.utils.printUtil import print_json

ase = ASE()

# get current user information
res = ase.get("currentuser_v2")
user = res.json()
print_json("UserInfo =", user)

print_json("Templates =",ase.inventory.templates)
print_json("TestPolicies =", ase.inventory.test_policies)
print_json("Folders =", ase.inventory.folders)
print_json("Applications =",ase.inventory.applications)

