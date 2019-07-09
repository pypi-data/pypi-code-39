import valispace

api = valispace.API("http://127.0.0.1:8000", "admin", "12345678")
assert api, "Connection error"

print("All tests passed.")
