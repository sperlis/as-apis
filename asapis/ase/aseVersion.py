  
from asapis.services.aselib import ASE
from asapis.utils.printUtil import out

ase = ASE()

res = ase.get("version")
version = res.json()
out(f"ASE Version: {version['version']}")