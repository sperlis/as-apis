from asapis.utils.printUtil import out
from asapis.services.asoclib import ASoC


asoc = ASoC()


res = asoc.get("Account/TenantInfo")

out(res.json())

res = asoc.get("Account/SubscriptionInfo")

out(res.json())

out(asoc.get("Users").json())

