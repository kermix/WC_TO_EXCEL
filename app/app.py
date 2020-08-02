from api import wcapi

d = wcapi.get("products").json()

print(d)