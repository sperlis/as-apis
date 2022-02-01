from asapis.utils.printUtil import print_result
from asapis.services.aselib import ASE

ase = ASE()

if "Create" in ase.config:
    res = ase.post("account/apikey",json={})
    api_key = res.json()
    print_result(api_key)
else:
    res = ase.get("account/getapikey")
    api_key = res.json()
    print_result(api_key)

