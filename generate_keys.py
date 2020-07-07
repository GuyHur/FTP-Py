from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_key_pair():
    """
    use:
    function generates the private key for the program
    :var private_key : public_exponent - use 65537, key_size = size of the key(considered to be breakable if 1024
    , use at least 2048) backend- rsa backend
    :return: private_key
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    with open("Desktop/PTF/private_key.pem", "wb") as pk_file:
        pk_file.write(pem_private)

    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open('public_key.pem', 'wb') as f:
        f.write(pem_public)
