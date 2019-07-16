import datetime
from M2Crypto import EVP
import base64
import urllib

"""
This is an example of signing a url in AWS Cloudfront for the purpose of
protecting the content. The keyfile and kaypair id are generated in the
AWS console.

The policy is just a canned policy that AWS hands out. It can be made to
be more complicated, but this just makes the URL valid for 1 hour. This
can be adjusted in the expires variable.
"""
baseurl = "https://dsxayjynapenv.cloudfront.net/DSCN0591.JPG"

expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
epoch = datetime.datetime.utcfromtimestamp(0)
expires = (expires - epoch).total_seconds()

policy = """
{
    "Statement": [
        {
            "Resource": "%s",
            "Condition": {
                "DateLessThan": {
                    "AWS:EpochTime": %d
                }
            }
        }
    ]
}
""" % (
    baseurl,
    expires,
)

policy = "".join(policy.split())

# print(policy)

key = EVP.load_key("pk-APKAJTEBPINAHERS5JXA.pem")
key.reset_context(md="sha1")
key.sign_init()
key.sign_update(policy)
signature = key.sign_final()
b64_signature = base64.b64encode(signature)
url_signature = urllib.quote(b64_signature)

keypair = "APKAJTEBPINAHERS5JXA"

fullurl = [
    "%s" % baseurl,  # base url of object
    "?",
    "",  # query string parameters
    "Expires=%d" % expires,  # hour from now
    "&Signature=%s" % url_signature,  # hashed and signed version of the policy statement
    "&Key-Pair-Id=%s" % keypair,  # from amazon crendentials
]

print("".join(fullurl))
