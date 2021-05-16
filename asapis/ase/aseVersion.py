  
from asapis.services.aselib import ASE
from asapis.utils.printUtil import print_result

ase = ASE()

res = ase.get("version")
version = res.json()
print_result(f"ASE Version: {version['version']}")