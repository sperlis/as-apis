from asapis.services.asoclib import ASoC


asoc = ASoC()


res = asoc.get("Account/TenantInfo")

print(res.json())

res = asoc.get("Account/SubscriptionInfo")

print(res.json())

print(asoc.get("Users").json())

