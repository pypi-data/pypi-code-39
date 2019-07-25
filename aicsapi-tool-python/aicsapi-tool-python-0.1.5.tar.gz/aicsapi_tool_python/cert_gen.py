from OpenSSL import crypto
from random import randint
import sys

def generate_v3cert(asus_account, certkey_name):
    '''
    Generates RSA private key along with self-signed X509v3 certificate under current directory.
    Saves key & cert pair in both PKCS12 (.pfx) & PEM format

    Parameters
    ----------
    asus_account : str
        account name in ASUS, used for credentials in certificate
    certkey_name : str
        file name of the combined key & cert pair
    '''
    # Generate private key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

    # Generate self-signed certificate
    cert = crypto.X509()
    cert.get_subject().C = "TW"
    cert.get_subject().ST = "Taiwan"
    cert.get_subject().L = "Taipei"
    cert.get_subject().O = "Asus Inc."
    cert.get_subject().OU = "AICS"
    cert.get_subject().CN = "asus.com"
    cert.get_subject().emailAddress = "{}@asus.com".format( asus_account )

    cert.set_version(2)
    cert.set_serial_number( randint(65537, 1e9+7) )
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # 10 years expiry date
    cert.set_issuer( cert.get_subject() )  # self-sign this certificate

    # For X509v3 extension, set CA: True in basicContraints
    cert.add_extensions([
      crypto.X509Extension(b"basicConstraints", True,
                                  b"CA:TRUE"),
      crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash",
                                  subject=cert),
      ])
    cert.add_extensions([
      crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always", issuer=cert)
      ])

    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # Write key & cert to file in PEM
    open("cert.pem", 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open("key.pem", 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    # Convert key & cert to PKCS12
    pkcs = crypto.PKCS12()
    pkcs.set_privatekey(k)
    pkcs.set_certificate(cert)
    with open('{}.pfx'.format( certkey_name ), 'wb') as pfx_file:
        pfx_file.write( pkcs.export() )

    # Combine key & cert in one PEM
    with open('{}.pem'.format( certkey_name ), 'wb') as pem_file:
        pem_file.write( open('cert.pem', 'rb').read() )
        pem_file.write( open('key.pem', 'rb').read() )

if __name__ == "__main__":
    generate_v3cert(sys.argv[1], sys.argv[2])