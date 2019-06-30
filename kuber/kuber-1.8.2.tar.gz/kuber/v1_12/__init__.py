import datetime as _datetime

from kuber import versioning

# Information about the kubernetes API library version associated with this
# package and kuber metadata around its creation and labeling within the
# kuber library.
KUBERNETES_VERSION = versioning.KubernetesVersion(
    label='v1.12',
    version='v1.12.9',
    major='1',
    minor='12',
    patch='9',
    pre_release='',
    build='',
    created_at=_datetime.datetime(2019, 6, 30),
    commit_sha='e09f5c40b55c91f681a46ee17f9bc447eeacee57'
)
