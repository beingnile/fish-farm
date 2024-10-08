from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA private key
private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
)

# Serialize private key to PEM format
private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
)

# Save the private key to a file
with open("private_key.pem", "wb") as key_file:
        key_file.write(private_key_pem)

# Generate the public key
public_key = private_key.public_key()

# Serialize public key to PEM format
public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the public key to a file
with open("public_key.pem", "wb") as key_file:
    key_file.write(public_key_pem)

    print("RSA keys have been generated and saved.")

with open("public_key.pem", "rb") as key_file:
    public_key_pem = key_file.read()
    print(public_key_pem.decode())

