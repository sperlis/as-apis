from asapis.utils.printUtil import out
from asapis.services.aselib import ASE

ase = ASE()

res = ase.post("account/apikey",json={})
api_key = res.json()
out(api_key)

