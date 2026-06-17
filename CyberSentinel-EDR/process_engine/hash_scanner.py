import hashlib

path = input("Enter file path: ")

sha256 = hashlib.sha256()

try:
    with open(path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    print("\nSHA256 Hash:")
    print(sha256.hexdigest())

except Exception as e:
    print("Error:", e)