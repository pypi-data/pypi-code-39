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


def gcs_jsonl(path, compression=None, encoding="utf8", bucket=BUCKET):
    """Download a gzipped jsonl file from the bucket, and iterate over the records."""
    if compressed is None:
        compressed = path.parts[-1].endswith("gz")
        
    data = gcs_bytes(path, bucket=bucket)
    if compressed:
        data = gzip.decompress(data)
    lines = data.decode(encoding).split("\n")
    for line in lines:
        yield srsly.json_loads(line)


def reddit_docs(vocab):
    yield from gcs_docs(vocab, "parses/reddit/RC_2019-01-0.spacy")


def reddit_lines():
    yield from gcs_jsonl("jsonl/reddit/RC_2019-01-0.jsonl.gz")


def sec10k_lines():
    yield from gcs_jsonl("jsonl/sec-10k/2019q1.jsonl.gz")


def share(key, path, bucket=BUCKET):
    """Upload a file (by path) so that someone else can retrieve it."""
    blob = bucket.blob(os.path.join("shares", key))
    blob.upload_from_filename(source_file_name)


def get_shared(key, path=None, bucket=BUCKET):
    """Download a path someone else has shared."""
    data = gcs_bytes(os.path.join("shares", key), bucket=bucket)
    if path is not None:
        with open(str(path), mode="wb") as file_:
            file_.write(data)
