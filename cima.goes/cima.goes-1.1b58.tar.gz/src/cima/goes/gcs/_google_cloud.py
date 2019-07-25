import os
import io
import netCDF4
from collections import namedtuple
import google.cloud.storage as gcs
from google.colab import drive
import cima.goes.utils._file_names as fn
import cima.goes as Bands

GOES_PUBLIC_BUCKET = 'gcp-public-data-goes-16'


def list_blobs(bucket, gcs_prefix, gcs_patterns):
    bucket = gcs.Client().get_bucket(bucket)
    blobs = bucket.list_blobs(prefix=gcs_prefix, delimiter='/')
    result = []
    if gcs_patterns == None or len(gcs_patterns) == 0:
        for b in blobs:
            result.append(b)
    else:
        for b in blobs:
            match = True
            for pattern in gcs_patterns:
                if not pattern in b.path:
                    match = False
            if match:
                result.append(b)
    return result


def band_blobs(band: int, year: int, day_of_year: int, hour: int):
  return list_blobs(
      GOES_PUBLIC_BUCKET,
      fn.PATH_PREFIX.format(year=year, day_of_year=day_of_year, hour=hour),
      [fn.FILE_PATTERN.format(band=band)])


def group_blobs(named_blobs: dict):
    blobs_by_start = {}
    names = [n for n, _ in named_blobs.items()]
    for name, blobs in named_blobs.items():
      for blob in blobs:
          key = blob.name[fn.SLICE_OBS_START]
          if key not in blobs_by_start:
              blobs_by_start[key] = {n: None for n in names}
          blobs_by_start[key][name] = blob
    BlobsGroup = namedtuple('BlobsGroup', ['start'] + names)
    result = []
    for k, v in blobs_by_start.items():
        result.append(BlobsGroup(**{'start':k, **{kk: vv for kk, vv in v.items()}}))
    return result


def get_blobs(year: int, day_of_year: int, hour: int, bands: Bands):
    named_blobs = {}
    for band in bands:
        named_blobs[band.name] = band_blobs(band.value, year, day_of_year, hour)
    return group_blobs(named_blobs)


def get_datasets(year: int, day_of_year: int, hour: int, bands: Bands):
    blobs = get_blobs(year, day_of_year, hour, bands)
    Datasets = namedtuple('Datasets', ['start'] + [band.name for band in bands])
    for blob in blobs:
        data = {band.name: get_dataset_from_blob(getattr(blob, band.name)) for band in bands}
        yield Datasets(start=blob.start, **data)


def close_dataset(dataset):
    dataset.close()


def close_datasets(datasets):
    ds = datasets._asdict()
    for k in datasets._fields:
        if k != 'start':
            close_dataset(datasets._asdict()[k])


def get_dataset_from_blob(blob):
    in_memory_file = io.BytesIO()
    blob.download_to_file(in_memory_file)
    in_memory_file.seek(0)
    ds = netCDF4.Dataset("in_memory_file", mode='r', memory=in_memory_file.read())
    return ds


def mount_colab():
    drive.mount('/content/gdrive')


def set_credentials(credential_filepath):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_filepath
