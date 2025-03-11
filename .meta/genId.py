import os

id = "ANE" + "0" + os.urandom(6).hex() + "0"
id = id.upper()

print(id)