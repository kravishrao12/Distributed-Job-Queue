from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime

# Generate private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Create certificate subject and issuer
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Karnataka"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Bangalore"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PESU"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

# Create certificate
cert = x509.CertificateBuilder()\
    .subject_name(subject)\
    .issuer_name(issuer)\
    .public_key(key.public_key())\
    .serial_number(x509.random_serial_number())\
    .not_valid_before(datetime.datetime.utcnow())\
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
    .sign(key, hashes.SHA256(), default_backend())

# Write private key
with open("server.key", "wb") as f:
    f.write(
        key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        )
    )

# Write certificate
with open("server.crt", "wb") as f:
    f.write(cert.public_bytes(Encoding.PEM))

print("SSL certificate and key generated successfully.")