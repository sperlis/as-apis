from asapis.utils.printUtil import print_json
from asapis.services.asoclib import ASoC


asoc = ASoC()

res = asoc.get("Account/TenantInfo")

print_json("TenantInfo= ", res.json())

res = asoc.get("Account/SubscriptionInfo")

print_json("SubscriptionInfo= ", res.json())


