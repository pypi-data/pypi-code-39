import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudfront", "0.36.1", __name__, "aws-cloudfront@0.36.1.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _AliasConfiguration(jsii.compat.TypedDict, total=False):
    securityPolicy: "SecurityPolicyProtocol"
    """The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

    CloudFront serves your objects only to browsers or devices that support at
    least the SSL version that you specify.

    Default:
        - SSLv3 if sslMethod VIP, TLSv1 if sslMethod SNI

    Stability:
        experimental
    """
    sslMethod: "SSLMethod"
    """How CloudFront should serve HTTPS requests.

    See the notes on SSLMethod if you wish to use other SSL termination types.

    Default:
        SSLMethod.SNI

    See:
        https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_ViewerCertificate.html
    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.AliasConfiguration", jsii_struct_bases=[_AliasConfiguration])
class AliasConfiguration(_AliasConfiguration):
    """Configuration for custom domain names.

    CloudFront can use a custom domain that you provide instead of a
    "cloudfront.net" domain. To use this feature you must provide the list of
    additional domains, and the ACM Certificate that CloudFront should use for
    these additional domains.

    Stability:
        experimental
    """
    acmCertRef: str
    """ARN of an AWS Certificate Manager (ACM) certificate.

    Stability:
        experimental
    """

    names: typing.List[str]
    """Domain names on the certificate.

    Both main domain name and Subject Alternative Names.

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.Behavior", jsii_struct_bases=[])
class Behavior(jsii.compat.TypedDict, total=False):
    """A CloudFront behavior wrapper.

    Stability:
        experimental
    """
    allowedMethods: "CloudFrontAllowedMethods"
    """The method this CloudFront distribution responds do.

    Default:
        GET_HEAD

    Stability:
        experimental
    """

    cachedMethods: "CloudFrontAllowedCachedMethods"
    """Which methods are cached by CloudFront by default.

    Default:
        GET_HEAD

    Stability:
        experimental
    """

    compress: bool
    """If CloudFront should automatically compress some content types.

    Default:
        true

    Stability:
        experimental
    """

    defaultTtl: aws_cdk.core.Duration
    """The default amount of time CloudFront will cache an object.

    This value applies only when your custom origin does not add HTTP headers,
    such as Cache-Control max-age, Cache-Control s-maxage, and Expires to objects.

    Default:
        86400 (1 day)

    Stability:
        experimental
    """

    forwardedValues: "CfnDistribution.ForwardedValuesProperty"
    """The values CloudFront will forward to the origin when making a request.

    Default:
        none (no cookies - no headers)

    Stability:
        experimental
    """

    isDefaultBehavior: bool
    """If this behavior is the default behavior for the distribution.

    You must specify exactly one default distribution per CloudFront distribution.
    The default behavior is allowed to omit the "path" property.

    Stability:
        experimental
    """

    lambdaFunctionAssociations: typing.List["LambdaFunctionAssociation"]
    """Declares associated lambda@edge functions for this distribution behaviour.

    Default:
        No lambda function associated

    Stability:
        experimental
    """

    maxTtl: aws_cdk.core.Duration
    """The max amount of time you want objects to stay in the cache before CloudFront queries your origin.

    Default:
        Duration.seconds(31536000) (one year)

    Stability:
        experimental
    """

    minTtl: aws_cdk.core.Duration
    """The minimum amount of time that you want objects to stay in the cache before CloudFront queries your origin.

    Stability:
        experimental
    """

    pathPattern: str
    """The path this behavior responds to. Required for all non-default behaviors. (The default behavior implicitly has "*" as the path pattern. ).

    Stability:
        experimental
    """

    trustedSigners: typing.List[str]
    """Trusted signers is how CloudFront allows you to serve private content. The signers are the account IDs that are allowed to sign cookies/presigned URLs for this distribution.

    If you pass a non empty value, all requests for this behavior must be signed (no public access will be allowed)

    Stability:
        experimental
    """

class CfnCloudFrontOriginAccessIdentity(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity"):
    """A CloudFormation ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
    Stability:
        stable
    cloudformationResource:
        AWS::CloudFront::CloudFrontOriginAccessIdentity
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cloud_front_origin_access_identity_config: typing.Union["CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.core.IResolvable]) -> None:
        """Create a new ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            cloud_front_origin_access_identity_config: ``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

        Stability:
            experimental
        """
        props: CfnCloudFrontOriginAccessIdentityProps = {"cloudFrontOriginAccessIdentityConfig": cloud_front_origin_access_identity_config}

        jsii.create(CfnCloudFrontOriginAccessIdentity, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            props: -

        Stability:
            stable
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        Stability:
            stable
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrS3CanonicalUserId")
    def attr_s3_canonical_user_id(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            S3CanonicalUserId
        """
        return jsii.get(self, "attrS3CanonicalUserId")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="cloudFrontOriginAccessIdentityConfig")
    def cloud_front_origin_access_identity_config(self) -> typing.Union["CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig
        Stability:
            stable
        """
        return jsii.get(self, "cloudFrontOriginAccessIdentityConfig")

    @cloud_front_origin_access_identity_config.setter
    def cloud_front_origin_access_identity_config(self, value: typing.Union["CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "cloudFrontOriginAccessIdentityConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty", jsii_struct_bases=[])
    class CloudFrontOriginAccessIdentityConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html
        Stability:
            stable
        """
        comment: str
        """``CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig-comment
        Stability:
            stable
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnCloudFrontOriginAccessIdentityProps", jsii_struct_bases=[])
class CfnCloudFrontOriginAccessIdentityProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::CloudFront::CloudFrontOriginAccessIdentity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html
    Stability:
        stable
    """
    cloudFrontOriginAccessIdentityConfig: typing.Union["CfnCloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfigProperty", aws_cdk.core.IResolvable]
    """``AWS::CloudFront::CloudFrontOriginAccessIdentity.CloudFrontOriginAccessIdentityConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-cloudfrontoriginaccessidentity.html#cfn-cloudfront-cloudfrontoriginaccessidentity-cloudfrontoriginaccessidentityconfig
    Stability:
        stable
    """

class CfnDistribution(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution"):
    """A CloudFormation ``AWS::CloudFront::Distribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
    Stability:
        stable
    cloudformationResource:
        AWS::CloudFront::Distribution
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, distribution_config: typing.Union[aws_cdk.core.IResolvable, "DistributionConfigProperty"], tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::CloudFront::Distribution``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            distribution_config: ``AWS::CloudFront::Distribution.DistributionConfig``.
            tags: ``AWS::CloudFront::Distribution.Tags``.

        Stability:
            experimental
        """
        props: CfnDistributionProps = {"distributionConfig": distribution_config}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            props: -

        Stability:
            stable
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        Stability:
            stable
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            DomainName
        """
        return jsii.get(self, "attrDomainName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFront::Distribution.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="distributionConfig")
    def distribution_config(self) -> typing.Union[aws_cdk.core.IResolvable, "DistributionConfigProperty"]:
        """``AWS::CloudFront::Distribution.DistributionConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-distributionconfig
        Stability:
            stable
        """
        return jsii.get(self, "distributionConfig")

    @distribution_config.setter
    def distribution_config(self, value: typing.Union[aws_cdk.core.IResolvable, "DistributionConfigProperty"]):
        return jsii.set(self, "distributionConfig", value)

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.AllowedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-allowedmethods
        Stability:
            stable
        """
        cachedMethods: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.CachedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-cachedmethods
        Stability:
            stable
        """
        compress: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.CacheBehaviorProperty.Compress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-compress
        Stability:
            stable
        """
        defaultTtl: jsii.Number
        """``CfnDistribution.CacheBehaviorProperty.DefaultTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-defaultttl
        Stability:
            stable
        """
        fieldLevelEncryptionId: str
        """``CfnDistribution.CacheBehaviorProperty.FieldLevelEncryptionId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-fieldlevelencryptionid
        Stability:
            stable
        """
        lambdaFunctionAssociations: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        """``CfnDistribution.CacheBehaviorProperty.LambdaFunctionAssociations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-lambdafunctionassociations
        Stability:
            stable
        """
        maxTtl: jsii.Number
        """``CfnDistribution.CacheBehaviorProperty.MaxTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-maxttl
        Stability:
            stable
        """
        minTtl: jsii.Number
        """``CfnDistribution.CacheBehaviorProperty.MinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-minttl
        Stability:
            stable
        """
        smoothStreaming: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.CacheBehaviorProperty.SmoothStreaming``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-smoothstreaming
        Stability:
            stable
        """
        trustedSigners: typing.List[str]
        """``CfnDistribution.CacheBehaviorProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-trustedsigners
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CacheBehaviorProperty", jsii_struct_bases=[_CacheBehaviorProperty])
    class CacheBehaviorProperty(_CacheBehaviorProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html
        Stability:
            stable
        """
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.core.IResolvable]
        """``CfnDistribution.CacheBehaviorProperty.ForwardedValues``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-forwardedvalues
        Stability:
            stable
        """

        pathPattern: str
        """``CfnDistribution.CacheBehaviorProperty.PathPattern``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-pathpattern
        Stability:
            stable
        """

        targetOriginId: str
        """``CfnDistribution.CacheBehaviorProperty.TargetOriginId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-targetoriginid
        Stability:
            stable
        """

        viewerProtocolPolicy: str
        """``CfnDistribution.CacheBehaviorProperty.ViewerProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cachebehavior.html#cfn-cloudfront-distribution-cachebehavior-viewerprotocolpolicy
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CookiesProperty(jsii.compat.TypedDict, total=False):
        whitelistedNames: typing.List[str]
        """``CfnDistribution.CookiesProperty.WhitelistedNames``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-whitelistednames
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CookiesProperty", jsii_struct_bases=[_CookiesProperty])
    class CookiesProperty(_CookiesProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html
        Stability:
            stable
        """
        forward: str
        """``CfnDistribution.CookiesProperty.Forward``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-cookies.html#cfn-cloudfront-distribution-cookies-forward
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CustomErrorResponseProperty(jsii.compat.TypedDict, total=False):
        errorCachingMinTtl: jsii.Number
        """``CfnDistribution.CustomErrorResponseProperty.ErrorCachingMinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcachingminttl
        Stability:
            stable
        """
        responseCode: jsii.Number
        """``CfnDistribution.CustomErrorResponseProperty.ResponseCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsecode
        Stability:
            stable
        """
        responsePagePath: str
        """``CfnDistribution.CustomErrorResponseProperty.ResponsePagePath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-responsepagepath
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomErrorResponseProperty", jsii_struct_bases=[_CustomErrorResponseProperty])
    class CustomErrorResponseProperty(_CustomErrorResponseProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html
        Stability:
            stable
        """
        errorCode: jsii.Number
        """``CfnDistribution.CustomErrorResponseProperty.ErrorCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customerrorresponse.html#cfn-cloudfront-distribution-customerrorresponse-errorcode
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CustomOriginConfigProperty(jsii.compat.TypedDict, total=False):
        httpPort: jsii.Number
        """``CfnDistribution.CustomOriginConfigProperty.HTTPPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpport
        Stability:
            stable
        """
        httpsPort: jsii.Number
        """``CfnDistribution.CustomOriginConfigProperty.HTTPSPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-httpsport
        Stability:
            stable
        """
        originKeepaliveTimeout: jsii.Number
        """``CfnDistribution.CustomOriginConfigProperty.OriginKeepaliveTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originkeepalivetimeout
        Stability:
            stable
        """
        originReadTimeout: jsii.Number
        """``CfnDistribution.CustomOriginConfigProperty.OriginReadTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originreadtimeout
        Stability:
            stable
        """
        originSslProtocols: typing.List[str]
        """``CfnDistribution.CustomOriginConfigProperty.OriginSSLProtocols``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originsslprotocols
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.CustomOriginConfigProperty", jsii_struct_bases=[_CustomOriginConfigProperty])
    class CustomOriginConfigProperty(_CustomOriginConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html
        Stability:
            stable
        """
        originProtocolPolicy: str
        """``CfnDistribution.CustomOriginConfigProperty.OriginProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-customoriginconfig.html#cfn-cloudfront-distribution-customoriginconfig-originprotocolpolicy
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DefaultCacheBehaviorProperty(jsii.compat.TypedDict, total=False):
        allowedMethods: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.AllowedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-allowedmethods
        Stability:
            stable
        """
        cachedMethods: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.CachedMethods``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-cachedmethods
        Stability:
            stable
        """
        compress: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.DefaultCacheBehaviorProperty.Compress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-compress
        Stability:
            stable
        """
        defaultTtl: jsii.Number
        """``CfnDistribution.DefaultCacheBehaviorProperty.DefaultTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-defaultttl
        Stability:
            stable
        """
        fieldLevelEncryptionId: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.FieldLevelEncryptionId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-fieldlevelencryptionid
        Stability:
            stable
        """
        lambdaFunctionAssociations: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LambdaFunctionAssociationProperty"]]]
        """``CfnDistribution.DefaultCacheBehaviorProperty.LambdaFunctionAssociations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-lambdafunctionassociations
        Stability:
            stable
        """
        maxTtl: jsii.Number
        """``CfnDistribution.DefaultCacheBehaviorProperty.MaxTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-maxttl
        Stability:
            stable
        """
        minTtl: jsii.Number
        """``CfnDistribution.DefaultCacheBehaviorProperty.MinTTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-minttl
        Stability:
            stable
        """
        smoothStreaming: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.DefaultCacheBehaviorProperty.SmoothStreaming``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-smoothstreaming
        Stability:
            stable
        """
        trustedSigners: typing.List[str]
        """``CfnDistribution.DefaultCacheBehaviorProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-trustedsigners
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DefaultCacheBehaviorProperty", jsii_struct_bases=[_DefaultCacheBehaviorProperty])
    class DefaultCacheBehaviorProperty(_DefaultCacheBehaviorProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html
        Stability:
            stable
        """
        forwardedValues: typing.Union["CfnDistribution.ForwardedValuesProperty", aws_cdk.core.IResolvable]
        """``CfnDistribution.DefaultCacheBehaviorProperty.ForwardedValues``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-forwardedvalues
        Stability:
            stable
        """

        targetOriginId: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.TargetOriginId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-targetoriginid
        Stability:
            stable
        """

        viewerProtocolPolicy: str
        """``CfnDistribution.DefaultCacheBehaviorProperty.ViewerProtocolPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-defaultcachebehavior.html#cfn-cloudfront-distribution-defaultcachebehavior-viewerprotocolpolicy
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        """``CfnDistribution.DistributionConfigProperty.Aliases``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-aliases
        Stability:
            stable
        """
        cacheBehaviors: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CacheBehaviorProperty"]]]
        """``CfnDistribution.DistributionConfigProperty.CacheBehaviors``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-cachebehaviors
        Stability:
            stable
        """
        comment: str
        """``CfnDistribution.DistributionConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-comment
        Stability:
            stable
        """
        customErrorResponses: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnDistribution.CustomErrorResponseProperty", aws_cdk.core.IResolvable]]]
        """``CfnDistribution.DistributionConfigProperty.CustomErrorResponses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-customerrorresponses
        Stability:
            stable
        """
        defaultCacheBehavior: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DefaultCacheBehaviorProperty"]
        """``CfnDistribution.DistributionConfigProperty.DefaultCacheBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultcachebehavior
        Stability:
            stable
        """
        defaultRootObject: str
        """``CfnDistribution.DistributionConfigProperty.DefaultRootObject``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-defaultrootobject
        Stability:
            stable
        """
        httpVersion: str
        """``CfnDistribution.DistributionConfigProperty.HttpVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-httpversion
        Stability:
            stable
        """
        ipv6Enabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.DistributionConfigProperty.IPV6Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-ipv6enabled
        Stability:
            stable
        """
        logging: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.LoggingProperty"]
        """``CfnDistribution.DistributionConfigProperty.Logging``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-logging
        Stability:
            stable
        """
        origins: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginProperty"]]]
        """``CfnDistribution.DistributionConfigProperty.Origins``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-origins
        Stability:
            stable
        """
        priceClass: str
        """``CfnDistribution.DistributionConfigProperty.PriceClass``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-priceclass
        Stability:
            stable
        """
        restrictions: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.RestrictionsProperty"]
        """``CfnDistribution.DistributionConfigProperty.Restrictions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-restrictions
        Stability:
            stable
        """
        viewerCertificate: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.ViewerCertificateProperty"]
        """``CfnDistribution.DistributionConfigProperty.ViewerCertificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-viewercertificate
        Stability:
            stable
        """
        webAclId: str
        """``CfnDistribution.DistributionConfigProperty.WebACLId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-webaclid
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.DistributionConfigProperty", jsii_struct_bases=[_DistributionConfigProperty])
    class DistributionConfigProperty(_DistributionConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html
        Stability:
            stable
        """
        enabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.DistributionConfigProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-distributionconfig.html#cfn-cloudfront-distribution-distributionconfig-enabled
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ForwardedValuesProperty(jsii.compat.TypedDict, total=False):
        cookies: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CookiesProperty"]
        """``CfnDistribution.ForwardedValuesProperty.Cookies``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-cookies
        Stability:
            stable
        """
        headers: typing.List[str]
        """``CfnDistribution.ForwardedValuesProperty.Headers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-headers
        Stability:
            stable
        """
        queryStringCacheKeys: typing.List[str]
        """``CfnDistribution.ForwardedValuesProperty.QueryStringCacheKeys``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystringcachekeys
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ForwardedValuesProperty", jsii_struct_bases=[_ForwardedValuesProperty])
    class ForwardedValuesProperty(_ForwardedValuesProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html
        Stability:
            stable
        """
        queryString: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.ForwardedValuesProperty.QueryString``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-forwardedvalues.html#cfn-cloudfront-distribution-forwardedvalues-querystring
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _GeoRestrictionProperty(jsii.compat.TypedDict, total=False):
        locations: typing.List[str]
        """``CfnDistribution.GeoRestrictionProperty.Locations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-locations
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.GeoRestrictionProperty", jsii_struct_bases=[_GeoRestrictionProperty])
    class GeoRestrictionProperty(_GeoRestrictionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html
        Stability:
            stable
        """
        restrictionType: str
        """``CfnDistribution.GeoRestrictionProperty.RestrictionType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-georestriction.html#cfn-cloudfront-distribution-georestriction-restrictiontype
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LambdaFunctionAssociationProperty", jsii_struct_bases=[])
    class LambdaFunctionAssociationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html
        Stability:
            stable
        """
        eventType: str
        """``CfnDistribution.LambdaFunctionAssociationProperty.EventType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-eventtype
        Stability:
            stable
        """

        lambdaFunctionArn: str
        """``CfnDistribution.LambdaFunctionAssociationProperty.LambdaFunctionARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-lambdafunctionassociation.html#cfn-cloudfront-distribution-lambdafunctionassociation-lambdafunctionarn
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LoggingProperty(jsii.compat.TypedDict, total=False):
        includeCookies: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.LoggingProperty.IncludeCookies``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-includecookies
        Stability:
            stable
        """
        prefix: str
        """``CfnDistribution.LoggingProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-prefix
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.LoggingProperty", jsii_struct_bases=[_LoggingProperty])
    class LoggingProperty(_LoggingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html
        Stability:
            stable
        """
        bucket: str
        """``CfnDistribution.LoggingProperty.Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-logging.html#cfn-cloudfront-distribution-logging-bucket
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginCustomHeaderProperty", jsii_struct_bases=[])
    class OriginCustomHeaderProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html
        Stability:
            stable
        """
        headerName: str
        """``CfnDistribution.OriginCustomHeaderProperty.HeaderName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headername
        Stability:
            stable
        """

        headerValue: str
        """``CfnDistribution.OriginCustomHeaderProperty.HeaderValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origincustomheader.html#cfn-cloudfront-distribution-origincustomheader-headervalue
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OriginProperty(jsii.compat.TypedDict, total=False):
        customOriginConfig: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.CustomOriginConfigProperty"]
        """``CfnDistribution.OriginProperty.CustomOriginConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-customoriginconfig
        Stability:
            stable
        """
        originCustomHeaders: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.OriginCustomHeaderProperty"]]]
        """``CfnDistribution.OriginProperty.OriginCustomHeaders``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-origincustomheaders
        Stability:
            stable
        """
        originPath: str
        """``CfnDistribution.OriginProperty.OriginPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-originpath
        Stability:
            stable
        """
        s3OriginConfig: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.S3OriginConfigProperty"]
        """``CfnDistribution.OriginProperty.S3OriginConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-s3originconfig
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.OriginProperty", jsii_struct_bases=[_OriginProperty])
    class OriginProperty(_OriginProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html
        Stability:
            stable
        """
        domainName: str
        """``CfnDistribution.OriginProperty.DomainName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-domainname
        Stability:
            stable
        """

        id: str
        """``CfnDistribution.OriginProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-origin.html#cfn-cloudfront-distribution-origin-id
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.RestrictionsProperty", jsii_struct_bases=[])
    class RestrictionsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html
        Stability:
            stable
        """
        geoRestriction: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.GeoRestrictionProperty"]
        """``CfnDistribution.RestrictionsProperty.GeoRestriction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-restrictions.html#cfn-cloudfront-distribution-restrictions-georestriction
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.S3OriginConfigProperty", jsii_struct_bases=[])
    class S3OriginConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html
        Stability:
            stable
        """
        originAccessIdentity: str
        """``CfnDistribution.S3OriginConfigProperty.OriginAccessIdentity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-s3originconfig.html#cfn-cloudfront-distribution-s3originconfig-originaccessidentity
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistribution.ViewerCertificateProperty", jsii_struct_bases=[])
    class ViewerCertificateProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html
        Stability:
            stable
        """
        acmCertificateArn: str
        """``CfnDistribution.ViewerCertificateProperty.AcmCertificateArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-acmcertificatearn
        Stability:
            stable
        """

        cloudFrontDefaultCertificate: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnDistribution.ViewerCertificateProperty.CloudFrontDefaultCertificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-cloudfrontdefaultcertificate
        Stability:
            stable
        """

        iamCertificateId: str
        """``CfnDistribution.ViewerCertificateProperty.IamCertificateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-iamcertificateid
        Stability:
            stable
        """

        minimumProtocolVersion: str
        """``CfnDistribution.ViewerCertificateProperty.MinimumProtocolVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-minimumprotocolversion
        Stability:
            stable
        """

        sslSupportMethod: str
        """``CfnDistribution.ViewerCertificateProperty.SslSupportMethod``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-distribution-viewercertificate.html#cfn-cloudfront-distribution-viewercertificate-sslsupportmethod
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDistributionProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::CloudFront::Distribution.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-tags
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnDistributionProps", jsii_struct_bases=[_CfnDistributionProps])
class CfnDistributionProps(_CfnDistributionProps):
    """Properties for defining a ``AWS::CloudFront::Distribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html
    Stability:
        stable
    """
    distributionConfig: typing.Union[aws_cdk.core.IResolvable, "CfnDistribution.DistributionConfigProperty"]
    """``AWS::CloudFront::Distribution.DistributionConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-distribution.html#cfn-cloudfront-distribution-distributionconfig
    Stability:
        stable
    """

class CfnStreamingDistribution(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution"):
    """A CloudFormation ``AWS::CloudFront::StreamingDistribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
    Stability:
        stable
    cloudformationResource:
        AWS::CloudFront::StreamingDistribution
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, streaming_distribution_config: typing.Union[aws_cdk.core.IResolvable, "StreamingDistributionConfigProperty"], tags: typing.List[aws_cdk.core.CfnTag]) -> None:
        """Create a new ``AWS::CloudFront::StreamingDistribution``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            streaming_distribution_config: ``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.
            tags: ``AWS::CloudFront::StreamingDistribution.Tags``.

        Stability:
            experimental
        """
        props: CfnStreamingDistributionProps = {"streamingDistributionConfig": streaming_distribution_config, "tags": tags}

        jsii.create(CfnStreamingDistribution, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            props: -

        Stability:
            stable
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        Stability:
            stable
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            DomainName
        """
        return jsii.get(self, "attrDomainName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CloudFront::StreamingDistribution.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="streamingDistributionConfig")
    def streaming_distribution_config(self) -> typing.Union[aws_cdk.core.IResolvable, "StreamingDistributionConfigProperty"]:
        """``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig
        Stability:
            stable
        """
        return jsii.get(self, "streamingDistributionConfig")

    @streaming_distribution_config.setter
    def streaming_distribution_config(self, value: typing.Union[aws_cdk.core.IResolvable, "StreamingDistributionConfigProperty"]):
        return jsii.set(self, "streamingDistributionConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.LoggingProperty", jsii_struct_bases=[])
    class LoggingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html
        Stability:
            stable
        """
        bucket: str
        """``CfnStreamingDistribution.LoggingProperty.Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-bucket
        Stability:
            stable
        """

        enabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnStreamingDistribution.LoggingProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-enabled
        Stability:
            stable
        """

        prefix: str
        """``CfnStreamingDistribution.LoggingProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-logging.html#cfn-cloudfront-streamingdistribution-logging-prefix
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.S3OriginProperty", jsii_struct_bases=[])
    class S3OriginProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html
        Stability:
            stable
        """
        domainName: str
        """``CfnStreamingDistribution.S3OriginProperty.DomainName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-domainname
        Stability:
            stable
        """

        originAccessIdentity: str
        """``CfnStreamingDistribution.S3OriginProperty.OriginAccessIdentity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-s3origin.html#cfn-cloudfront-streamingdistribution-s3origin-originaccessidentity
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StreamingDistributionConfigProperty(jsii.compat.TypedDict, total=False):
        aliases: typing.List[str]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Aliases``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-aliases
        Stability:
            stable
        """
        logging: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.LoggingProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Logging``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-logging
        Stability:
            stable
        """
        priceClass: str
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.PriceClass``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-priceclass
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.StreamingDistributionConfigProperty", jsii_struct_bases=[_StreamingDistributionConfigProperty])
    class StreamingDistributionConfigProperty(_StreamingDistributionConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html
        Stability:
            stable
        """
        comment: str
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-comment
        Stability:
            stable
        """

        enabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-enabled
        Stability:
            stable
        """

        s3Origin: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.S3OriginProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.S3Origin``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-s3origin
        Stability:
            stable
        """

        trustedSigners: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.TrustedSignersProperty"]
        """``CfnStreamingDistribution.StreamingDistributionConfigProperty.TrustedSigners``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-streamingdistributionconfig.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig-trustedsigners
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TrustedSignersProperty(jsii.compat.TypedDict, total=False):
        awsAccountNumbers: typing.List[str]
        """``CfnStreamingDistribution.TrustedSignersProperty.AwsAccountNumbers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-awsaccountnumbers
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistribution.TrustedSignersProperty", jsii_struct_bases=[_TrustedSignersProperty])
    class TrustedSignersProperty(_TrustedSignersProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html
        Stability:
            stable
        """
        enabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnStreamingDistribution.TrustedSignersProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudfront-streamingdistribution-trustedsigners.html#cfn-cloudfront-streamingdistribution-trustedsigners-enabled
        Stability:
            stable
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CfnStreamingDistributionProps", jsii_struct_bases=[])
class CfnStreamingDistributionProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::CloudFront::StreamingDistribution``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html
    Stability:
        stable
    """
    streamingDistributionConfig: typing.Union[aws_cdk.core.IResolvable, "CfnStreamingDistribution.StreamingDistributionConfigProperty"]
    """``AWS::CloudFront::StreamingDistribution.StreamingDistributionConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-streamingdistributionconfig
    Stability:
        stable
    """

    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::CloudFront::StreamingDistribution.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudfront-streamingdistribution.html#cfn-cloudfront-streamingdistribution-tags
    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedCachedMethods")
class CloudFrontAllowedCachedMethods(enum.Enum):
    """Enums for the methods CloudFront can cache.

    Stability:
        experimental
    """
    GET_HEAD = "GET_HEAD"
    """
    Stability:
        experimental
    """
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    """
    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontAllowedMethods")
class CloudFrontAllowedMethods(enum.Enum):
    """An enum for the supported methods to a CloudFront distribution.

    Stability:
        experimental
    """
    GET_HEAD = "GET_HEAD"
    """
    Stability:
        experimental
    """
    GET_HEAD_OPTIONS = "GET_HEAD_OPTIONS"
    """
    Stability:
        experimental
    """
    ALL = "ALL"
    """
    Stability:
        experimental
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CloudFrontWebDistributionProps(jsii.compat.TypedDict, total=False):
    aliasConfiguration: "AliasConfiguration"
    """AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names.

    Default:
        - None.

    Stability:
        experimental
    """
    comment: str
    """A comment for this distribution in the CloudFront console.

    Default:
        - No comment is added to distribution.

    Stability:
        experimental
    """
    defaultRootObject: str
    """The default object to serve.

    Default:
        - "index.html" is served.

    Stability:
        experimental
    """
    enableIpV6: bool
    """If your distribution should have IPv6 enabled.

    Default:
        true

    Stability:
        experimental
    """
    errorConfigurations: typing.List["CfnDistribution.CustomErrorResponseProperty"]
    """How CloudFront should handle requests that are not successful (eg PageNotFound).

    By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range
    with custom error messages. CloudFront does not cache HTTP status codes.

    Default:
        - No custom error configuration.

    Stability:
        experimental
    """
    httpVersion: "HttpVersion"
    """The max supported HTTP Versions.

    Default:
        HttpVersion.HTTP2

    Stability:
        experimental
    """
    loggingConfig: "LoggingConfiguration"
    """Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled.

    Default:
        - no logging is enabled by default.

    Stability:
        experimental
    """
    priceClass: "PriceClass"
    """The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing).

    Default:
        PriceClass.PriceClass100 the cheapest option for CloudFront is picked by default.

    Stability:
        experimental
    """
    viewerProtocolPolicy: "ViewerProtocolPolicy"
    """The default viewer policy for incoming clients.

    Default:
        RedirectToHTTPs

    Stability:
        experimental
    """
    webACLId: str
    """Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

    Default:
        - No AWS Web Application Firewall web access control list (web ACL).

    See:
        https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html
    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistributionProps", jsii_struct_bases=[_CloudFrontWebDistributionProps])
class CloudFrontWebDistributionProps(_CloudFrontWebDistributionProps):
    """
    Stability:
        experimental
    """
    originConfigs: typing.List["SourceConfiguration"]
    """The origin configurations for this distribution.

    Behaviors are a part of the origin.

    Stability:
        experimental
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CustomOriginConfig(jsii.compat.TypedDict, total=False):
    allowedOriginSSLVersions: typing.List["OriginSslPolicy"]
    """The SSL versions to use when interacting with the origin.

    Default:
        OriginSslPolicy.TLSv1_2

    Stability:
        experimental
    """
    httpPort: jsii.Number
    """The origin HTTP port.

    Default:
        80

    Stability:
        experimental
    """
    httpsPort: jsii.Number
    """The origin HTTPS port.

    Default:
        443

    Stability:
        experimental
    """
    originKeepaliveTimeout: aws_cdk.core.Duration
    """The keep alive timeout when making calls in seconds.

    Default:
        Duration.seconds(5)

    Stability:
        experimental
    """
    originProtocolPolicy: "OriginProtocolPolicy"
    """The protocol (http or https) policy to use when interacting with the origin.

    Default:
        OriginProtocolPolicy.HttpsOnly

    Stability:
        experimental
    """
    originReadTimeout: aws_cdk.core.Duration
    """The read timeout when calling the origin in seconds.

    Default:
        Duration.seconds(30)

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.CustomOriginConfig", jsii_struct_bases=[_CustomOriginConfig])
class CustomOriginConfig(_CustomOriginConfig):
    """A custom origin configuration.

    Stability:
        experimental
    """
    domainName: str
    """The domain name of the custom origin.

    Should not include the path - that should be in the parent SourceConfiguration

    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.HttpVersion")
class HttpVersion(enum.Enum):
    """
    Stability:
        experimental
    """
    HTTP1_1 = "HTTP1_1"
    """
    Stability:
        experimental
    """
    HTTP2 = "HTTP2"
    """
    Stability:
        experimental
    """

@jsii.interface(jsii_type="@aws-cdk/aws-cloudfront.IDistribution")
class IDistribution(jsii.compat.Protocol):
    """Interface for CloudFront distributions.

    Stability:
        experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IDistributionProxy

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the distribution.

        Stability:
            experimental
        """
        ...


class _IDistributionProxy():
    """Interface for CloudFront distributions.

    Stability:
        experimental
    """
    __jsii_type__ = "@aws-cdk/aws-cloudfront.IDistribution"
    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the distribution.

        Stability:
            experimental
        """
        return jsii.get(self, "domainName")


@jsii.implements(IDistribution)
class CloudFrontWebDistribution(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront.CloudFrontWebDistribution"):
    """Amazon CloudFront is a global content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to your viewers with low latency and high transfer speeds. CloudFront fronts user provided content and caches it at edge locations across the world.

    Here's how you can use this construct::

       import { CloudFrontWebDistribution } from '@aws-cdk/aws-cloudfront'

       const sourceBucket = new Bucket(this, 'Bucket');

       const distribution = new CloudFrontWebDistribution(this, 'MyDistribution', {
         originConfigs: [
           {
             s3OriginSource: {
             s3BucketSource: sourceBucket
             },
             behaviors : [ {isDefaultBehavior: true}]
           }
         ]
       });

    This will create a CloudFront distribution that uses your S3Bucket as it's origin.

    You can customize the distribution using additional properties from the CloudFrontWebDistributionProps interface.

    Stability:
        experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, origin_configs: typing.List["SourceConfiguration"], alias_configuration: typing.Optional["AliasConfiguration"]=None, comment: typing.Optional[str]=None, default_root_object: typing.Optional[str]=None, enable_ip_v6: typing.Optional[bool]=None, error_configurations: typing.Optional[typing.List["CfnDistribution.CustomErrorResponseProperty"]]=None, http_version: typing.Optional["HttpVersion"]=None, logging_config: typing.Optional["LoggingConfiguration"]=None, price_class: typing.Optional["PriceClass"]=None, viewer_protocol_policy: typing.Optional["ViewerProtocolPolicy"]=None, web_acl_id: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            origin_configs: The origin configurations for this distribution. Behaviors are a part of the origin.
            alias_configuration: AliasConfiguration is used to configured CloudFront to respond to requests on custom domain names. Default: - None.
            comment: A comment for this distribution in the CloudFront console. Default: - No comment is added to distribution.
            default_root_object: The default object to serve. Default: - "index.html" is served.
            enable_ip_v6: If your distribution should have IPv6 enabled. Default: true
            error_configurations: How CloudFront should handle requests that are not successful (eg PageNotFound). By default, CloudFront does not replace HTTP status codes in the 4xx and 5xx range with custom error messages. CloudFront does not cache HTTP status codes. Default: - No custom error configuration.
            http_version: The max supported HTTP Versions. Default: HttpVersion.HTTP2
            logging_config: Optional - if we should enable logging. You can pass an empty object ({}) to have us auto create a bucket for logging. Omission of this property indicates no logging is to be enabled. Default: - no logging is enabled by default.
            price_class: The price class for the distribution (this impacts how many locations CloudFront uses for your distribution, and billing). Default: PriceClass.PriceClass100 the cheapest option for CloudFront is picked by default.
            viewer_protocol_policy: The default viewer policy for incoming clients. Default: RedirectToHTTPs
            web_acl_id: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. Default: - No AWS Web Application Firewall web access control list (web ACL).

        Stability:
            experimental
        """
        props: CloudFrontWebDistributionProps = {"originConfigs": origin_configs}

        if alias_configuration is not None:
            props["aliasConfiguration"] = alias_configuration

        if comment is not None:
            props["comment"] = comment

        if default_root_object is not None:
            props["defaultRootObject"] = default_root_object

        if enable_ip_v6 is not None:
            props["enableIpV6"] = enable_ip_v6

        if error_configurations is not None:
            props["errorConfigurations"] = error_configurations

        if http_version is not None:
            props["httpVersion"] = http_version

        if logging_config is not None:
            props["loggingConfig"] = logging_config

        if price_class is not None:
            props["priceClass"] = price_class

        if viewer_protocol_policy is not None:
            props["viewerProtocolPolicy"] = viewer_protocol_policy

        if web_acl_id is not None:
            props["webACLId"] = web_acl_id

        jsii.create(CloudFrontWebDistribution, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> str:
        """The distribution ID for this distribution.

        Stability:
            experimental
        """
        return jsii.get(self, "distributionId")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name created by CloudFront for this distribution. If you are using aliases for your distribution, this is the domainName your DNS records should point to. (In Route53, you could create an ALIAS record to this value, for example. ).

        Stability:
            experimental
        """
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="loggingBucket")
    def logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """The logging bucket for this CloudFront distribution. If logging is not enabled for this distribution - this property will be undefined.

        Stability:
            experimental
        """
        return jsii.get(self, "loggingBucket")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.LambdaEdgeEventType")
class LambdaEdgeEventType(enum.Enum):
    """
    Stability:
        experimental
    """
    ORIGIN_REQUEST = "ORIGIN_REQUEST"
    """The origin-request specifies the request to the origin location (e.g. S3).

    Stability:
        experimental
    """
    ORIGIN_RESPONSE = "ORIGIN_RESPONSE"
    """The origin-response specifies the response from the origin location (e.g. S3).

    Stability:
        experimental
    """
    VIEWER_REQUEST = "VIEWER_REQUEST"
    """The viewer-request specifies the incoming request.

    Stability:
        experimental
    """
    VIEWER_RESPONSE = "VIEWER_RESPONSE"
    """The viewer-response specifies the outgoing reponse.

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.LambdaFunctionAssociation", jsii_struct_bases=[])
class LambdaFunctionAssociation(jsii.compat.TypedDict):
    """
    Stability:
        experimental
    """
    eventType: "LambdaEdgeEventType"
    """The lambda event type defines at which event the lambda is called during the request lifecycle.

    Stability:
        experimental
    """

    lambdaFunction: aws_cdk.aws_lambda.IVersion
    """A version of the lambda to associate.

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.LoggingConfiguration", jsii_struct_bases=[])
class LoggingConfiguration(jsii.compat.TypedDict, total=False):
    """Logging configuration for incoming requests.

    Stability:
        experimental
    """
    bucket: aws_cdk.aws_s3.IBucket
    """Bucket to log requests to.

    Default:
        - A logging bucket is automatically created.

    Stability:
        experimental
    """

    includeCookies: bool
    """Whether to include the cookies in the logs.

    Default:
        false

    Stability:
        experimental
    """

    prefix: str
    """Where in the bucket to store logs.

    Default:
        - No prefix.

    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginProtocolPolicy")
class OriginProtocolPolicy(enum.Enum):
    """
    Stability:
        experimental
    """
    HTTP_ONLY = "HTTP_ONLY"
    """
    Stability:
        experimental
    """
    MATCH_VIEWER = "MATCH_VIEWER"
    """
    Stability:
        experimental
    """
    HTTPS_ONLY = "HTTPS_ONLY"
    """
    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.OriginSslPolicy")
class OriginSslPolicy(enum.Enum):
    """
    Stability:
        experimental
    """
    SSL_V3 = "SSL_V3"
    """
    Stability:
        experimental
    """
    TLS_V1 = "TLS_V1"
    """
    Stability:
        experimental
    """
    TLS_V1_1 = "TLS_V1_1"
    """
    Stability:
        experimental
    """
    TLS_V1_2 = "TLS_V1_2"
    """
    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.PriceClass")
class PriceClass(enum.Enum):
    """The price class determines how many edge locations CloudFront will use for your distribution.

    Stability:
        experimental
    """
    PRICE_CLASS_100 = "PRICE_CLASS_100"
    """
    Stability:
        experimental
    """
    PRICE_CLASS_200 = "PRICE_CLASS_200"
    """
    Stability:
        experimental
    """
    PRICE_CLASS_ALL = "PRICE_CLASS_ALL"
    """
    Stability:
        experimental
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _S3OriginConfig(jsii.compat.TypedDict, total=False):
    originAccessIdentityId: str
    """The optional ID of the origin identity cloudfront will use when calling your s3 bucket.

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.S3OriginConfig", jsii_struct_bases=[_S3OriginConfig])
class S3OriginConfig(_S3OriginConfig):
    """
    Stability:
        experimental
    """
    s3BucketSource: aws_cdk.aws_s3.IBucket
    """The source bucket to serve content from.

    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SSLMethod")
class SSLMethod(enum.Enum):
    """The SSL method CloudFront will use for your distribution.

    Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
    which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
    multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
    (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

    CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

    If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
    using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

    See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/

    Stability:
        experimental
    """
    SNI = "SNI"
    """
    Stability:
        experimental
    """
    VIP = "VIP"
    """
    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.SecurityPolicyProtocol")
class SecurityPolicyProtocol(enum.Enum):
    """The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify.

    Stability:
        experimental
    """
    SSL_V3 = "SSL_V3"
    """
    Stability:
        experimental
    """
    TLS_V1 = "TLS_V1"
    """
    Stability:
        experimental
    """
    TLS_V1_2016 = "TLS_V1_2016"
    """
    Stability:
        experimental
    """
    TLS_V1_1_2016 = "TLS_V1_1_2016"
    """
    Stability:
        experimental
    """
    TLS_V1_2_2018 = "TLS_V1_2_2018"
    """
    Stability:
        experimental
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SourceConfiguration(jsii.compat.TypedDict, total=False):
    customOriginSource: "CustomOriginConfig"
    """A custom origin source - for all non-s3 sources.

    Stability:
        experimental
    """
    originHeaders: typing.Mapping[str,str]
    """Any additional headers to pass to the origin.

    Default:
        - No additional headers are passed.

    Stability:
        experimental
    """
    originPath: str
    """The relative path to the origin root to use for sources.

    Default:
        /

    Stability:
        experimental
    """
    s3OriginSource: "S3OriginConfig"
    """An s3 origin source - if you're using s3 for your assets.

    Stability:
        experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudfront.SourceConfiguration", jsii_struct_bases=[_SourceConfiguration])
class SourceConfiguration(_SourceConfiguration):
    """A source configuration is a wrapper for CloudFront origins and behaviors. An origin is what CloudFront will "be in front of" - that is, CloudFront will pull it's assets from an origin.

    If you're using s3 as a source - pass the ``s3Origin`` property, otherwise, pass the ``customOriginSource`` property.

    One or the other must be passed, and it is invalid to pass both in the same SourceConfiguration.

    Stability:
        experimental
    """
    behaviors: typing.List["Behavior"]
    """The behaviors associated with this source. At least one (default) behavior must be included.

    Stability:
        experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudfront.ViewerProtocolPolicy")
class ViewerProtocolPolicy(enum.Enum):
    """How HTTPs should be handled with your distribution.

    Stability:
        experimental
    """
    HTTPS_ONLY = "HTTPS_ONLY"
    """
    Stability:
        experimental
    """
    REDIRECT_TO_HTTPS = "REDIRECT_TO_HTTPS"
    """
    Stability:
        experimental
    """
    ALLOW_ALL = "ALLOW_ALL"
    """
    Stability:
        experimental
    """

__all__ = ["AliasConfiguration", "Behavior", "CfnCloudFrontOriginAccessIdentity", "CfnCloudFrontOriginAccessIdentityProps", "CfnDistribution", "CfnDistributionProps", "CfnStreamingDistribution", "CfnStreamingDistributionProps", "CloudFrontAllowedCachedMethods", "CloudFrontAllowedMethods", "CloudFrontWebDistribution", "CloudFrontWebDistributionProps", "CustomOriginConfig", "HttpVersion", "IDistribution", "LambdaEdgeEventType", "LambdaFunctionAssociation", "LoggingConfiguration", "OriginProtocolPolicy", "OriginSslPolicy", "PriceClass", "S3OriginConfig", "SSLMethod", "SecurityPolicyProtocol", "SourceConfiguration", "ViewerProtocolPolicy", "__jsii_assembly__"]

publication.publish()
