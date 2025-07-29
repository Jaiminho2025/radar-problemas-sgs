import json

with open("credentials.json", "r") as f:
    data = json.load(f)

data["private_key"] = data["private_key"].replace("\n", "\\n")

print("[google]")
for key, value in data.items():
    print(f'{key} = "{value}"')
