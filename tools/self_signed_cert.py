from socket import gethostname
from time import gmtime, mktime
from os.path import exists, join

from OpenSSL import crypto, SSL

CN = input("Input the hostname of the website the certificate is for: ")
CERT_FILE = "{}.crt".format(CN)
KEY_FILE = "{}.key".format(CN)


def create_self_signed_cert(cert_dir="."):
    C_F = join(cert_dir, CERT_FILE)
    K_F = join(cert_dir, KEY_FILE)

    if not exists(C_F) or not exists(K_F):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)
        cert = crypto.X509()
        cert.get_subject().C = input("Country: ")
        cert.get_subject().ST = input("State: ")
        cert.get_subject().L = input("City: ")
        cert.get_subject().O = input("Organization: ")
        cert.get_subject().OU = input("Organizational Unit: ")
        cert.get_subject().CN = CN

        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, "sha1")

        open(C_F, "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf8")
        )
        open(K_F, "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf8")
        )


def main():
    create_self_signed_cert()


if __name__ == "__main__":
    main()
