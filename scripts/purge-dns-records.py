import os
import requests

# https://dash.cloudflare.com/4b8a0a194b32a8d44b27cbe8e188174d/subjs.in
zoneid = os.environ("ZONE_ID")

# https://dash.cloudflare.com/profile/api-tokens
bearer_token = os.environ("BEARER_TOKEN")

if input("Are you sure you want to delete ALL DNS records in this zone? (y/n)") != "y":
    exit()


# Fetch dns records from CloudFlare
record_rq = requests.get(
    "https://api.cloudflare.com/client/v4/zones/" + zoneid + "/dns_records",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + bearer_token,
    },
)
data = record_rq.json()
if data["success"] == False:
    print("Failed to fetch dns record:")
    print(data["errors"])
    quit()

# Delete dns records
for record in data["result"]:
    print("Deleting:", record["name"])
    rq = requests.delete(
        "https://api.cloudflare.com/client/v4/zones/"
        + zoneid
        + "/dns_records/"
        + record["id"],
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + bearer_token,
        },
    )
    print(rq.status_code, "\n")
