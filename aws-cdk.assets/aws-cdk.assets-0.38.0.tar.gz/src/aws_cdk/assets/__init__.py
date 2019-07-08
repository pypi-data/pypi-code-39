import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets", "0.38.0", __name__, "assets@0.38.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/assets.CopyOptions", jsii_struct_bases=[], name_mapping={'exclude': 'exclude', 'follow': 'follow'})
class CopyOptions():
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None):
        """Obtains applied when copying directories into the staging location.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow

    @property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded
        """
        return self._values.get('exclude')

    @property
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never
        """
        return self._values.get('follow')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CopyOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/assets.FollowMode")
class FollowMode(enum.Enum):
    NEVER = "NEVER"
    """Never follow symlinks."""
    ALWAYS = "ALWAYS"
    """Materialize all symlinks, whether they are internal or external to the source directory."""
    EXTERNAL = "EXTERNAL"
    """Only follows symlinks that are external to the source directory."""
    BLOCK_EXTERNAL = "BLOCK_EXTERNAL"
    """Forbids source from having any symlinks pointing outside of the source tree.

    This is the safest mode of operation as it ensures that copy operations
    won't materialize files from the user's file system. Internal symlinks are
    not followed.

    If the copy operation runs into an external symlink, it will fail.
    """

@jsii.interface(jsii_type="@aws-cdk/assets.IAsset")
class IAsset(jsii.compat.Protocol):
    """Common interface for all assets."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAssetProxy

    @property
    @jsii.member(jsii_name="artifactHash")
    def artifact_hash(self) -> str:
        """A hash of the bundle for of this asset, which is only available at deployment time.

        As this is
        a late-bound token, it may not be used in construct IDs, but can be passed as a resource
        property in order to force a change on a resource when an asset is effectively updated. This is
        more reliable than ``sourceHash`` in particular for assets which bundling phase involve external
        resources that can change over time (such as Docker image builds).
        """
        ...

    @property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.
        """
        ...


class _IAssetProxy():
    """Common interface for all assets."""
    __jsii_type__ = "@aws-cdk/assets.IAsset"
    @property
    @jsii.member(jsii_name="artifactHash")
    def artifact_hash(self) -> str:
        """A hash of the bundle for of this asset, which is only available at deployment time.

        As this is
        a late-bound token, it may not be used in construct IDs, but can be passed as a resource
        property in order to force a change on a resource when an asset is effectively updated. This is
        more reliable than ``sourceHash`` in particular for assets which bundling phase involve external
        resources that can change over time (such as Docker image builds).
        """
        return jsii.get(self, "artifactHash")

    @property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.
        """
        return jsii.get(self, "sourceHash")


class Staging(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.Staging"):
    """Stages a file or directory from a location on the file system into a staging directory.

    This is controlled by the context key 'aws:cdk:asset-staging' and enabled
    by the CLI by default in order to ensure that when the CDK app exists, all
    assets are available for deployment. Otherwise, if an app references assets
    in temporary locations, those will not be available when it exists (see
    https://github.com/awslabs/aws-cdk/issues/1716).

    The ``stagedPath`` property is a stringified token that represents the location
    of the file or directory after staging. It will be resolved only during the
    "prepare" stage and may be either the original path or the staged path
    depending on the context setting.

    The file/directory are staged based on their content hash (fingerprint). This
    means that only if content was changed, copy will happen.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, source_path: str, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param source_path: 
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        """
        props = StagingProps(source_path=source_path, exclude=exclude, follow=follow)

        jsii.create(Staging, self, [scope, id, props])

    @jsii.member(jsii_name="synthesize")
    def _synthesize(self, session: aws_cdk.core.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -
        """
        return jsii.invoke(self, "synthesize", [session])

    @property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A cryptographic hash of the source document(s)."""
        return jsii.get(self, "sourceHash")

    @property
    @jsii.member(jsii_name="sourcePath")
    def source_path(self) -> str:
        """The path of the asset as it was referenced by the user."""
        return jsii.get(self, "sourcePath")

    @property
    @jsii.member(jsii_name="stagedPath")
    def staged_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.
        """
        return jsii.get(self, "stagedPath")


@jsii.data_type(jsii_type="@aws-cdk/assets.StagingProps", jsii_struct_bases=[CopyOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'source_path': 'sourcePath'})
class StagingProps(CopyOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional["FollowMode"]=None, source_path: str):
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param source_path: 
        """
        self._values = {
            'source_path': source_path,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow

    @property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded
        """
        return self._values.get('exclude')

    @property
    def follow(self) -> typing.Optional["FollowMode"]:
        """A strategy for how to handle symlinks.

        default
        :default: Never
        """
        return self._values.get('follow')

    @property
    def source_path(self) -> str:
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StagingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CopyOptions", "FollowMode", "IAsset", "Staging", "StagingProps", "__jsii_assembly__"]

publication.publish()
