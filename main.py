from angel_one_api import AngelOneClient

client = AngelOneClient()
profile = client.get_profile()

if profile:
    print("\n🎉 Profile Data:")
    print("Client Code:", profile.get("clientcode"))
    print("Name:", profile.get("name"))
    print("Exchanges:", profile.get("exchanges"))
else:
    print("\n⚠️ Failed to fetch profile.")