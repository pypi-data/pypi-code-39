from google.cloud.storage.client import Client
import google.cloud.storage
import gzip
import srsly
from .binder import Binder

CLIENT = Client.create_anonymous_client()
BUCKET = CLIENT.get_bucket('spacyirl2019')


def gcs_list(path=None, bucket=BUCKET):
    """List the paths in the bucket, optionally by subpath."""
    for blob in bucket.list_blobs():
        if not path:
            yield blob
        elif blob.name.startswith(path):
            yield blob.name


def gcs_bytes(path, bucket=BUCKET):
    """Download a file from the bucket, and return the bytes."""
    blob = google.cloud.storage.Blob(path, bucket)
    return blob.download_as_string()


def gcs_binder(path, bucket=BUCKET):
    """Download and unpack a binder from the bucket."""
    data = gcs_bytes(path, bucket=bucket)
    return Binder(store_user_data=True).from_bytes(data)


def gcs_docs(vocab, path, bucket=BUCKET):
    """Download and unpack a collection of docs from the bucket."""
    binder = gcs_binder(path, bucket=bucket)
    for doc in binder.get_docs(vocab):
        yield doc


def gcs_jsonl(path, encoding="utf8", bucket=BUCKET):
    """Download a gzipped jsonl file from the bucket, and iterate over the records."""
    data = gzip.decompress(gcs_bytes(path, bucket=bucket))
    lines = data.decode(encoding).split("\n")
    for line in lines:
        print(line)
        yield srsly.json_loads(line)
