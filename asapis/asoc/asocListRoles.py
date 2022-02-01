from asapis.utils.printUtil import print_json
from asapis.services.asoclib import ASoC

asoc = ASoC()

res = asoc.get("Roles")
roles = res.json()
firstRole = roles[0]
for key in firstRole:
    if key == "Capabilities":
        for cap in firstRole["Capabilities"]:
            print(cap, end =",")
    else:
        print(key, end =",")
print()
for role in roles:
    for field in role:
        if field == "Capabilities":
            for cap in role["Capabilities"]:
                print(role["Capabilities"][cap], end =",")
        else:
            value = role[field]
            if type(value) is str:
                value = value.replace(",",";")
            print(value, end =",")
    print()
