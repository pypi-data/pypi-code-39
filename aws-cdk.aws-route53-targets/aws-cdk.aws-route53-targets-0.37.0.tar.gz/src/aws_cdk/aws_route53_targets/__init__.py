import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_cloudfront
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53-targets", "0.37.0", __name__, "aws-route53-targets@0.37.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class ApiGatewayDomain(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.ApiGatewayDomain"):
    """Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined throug the ``RestApiProps.domainName`` prop.

    Stability:
        stable
    """
    def __init__(self, domain_name: aws_cdk.aws_apigateway.IDomainName) -> None:
        """
        Arguments:
            domain_name: -

        Stability:
            stable
        """
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        Arguments:
            _record: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_record])


class ApiGateway(ApiGatewayDomain, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.ApiGateway"):
    """Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.

    Stability:
        stable
    """
    def __init__(self, api: aws_cdk.aws_apigateway.RestApi) -> None:
        """
        Arguments:
            api: -

        Stability:
            stable
        """
        jsii.create(ApiGateway, self, [api])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class CloudFrontTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.CloudFrontTarget"):
    """Use a CloudFront Distribution as an alias record target.

    Stability:
        stable
    """
    def __init__(self, distribution: aws_cdk.aws_cloudfront.CloudFrontWebDistribution) -> None:
        """
        Arguments:
            distribution: -

        Stability:
            stable
        """
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        Arguments:
            _record: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_record])


@jsii.implements(aws_cdk.aws_route53.IAliasRecordTarget)
class LoadBalancerTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53-targets.LoadBalancerTarget"):
    """Use an ELBv2 as an alias record target.

    Stability:
        stable
    """
    def __init__(self, load_balancer: aws_cdk.aws_elasticloadbalancingv2.ILoadBalancerV2) -> None:
        """
        Arguments:
            load_balancer: -

        Stability:
            stable
        """
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: aws_cdk.aws_route53.IRecordSet) -> aws_cdk.aws_route53.AliasRecordTargetConfig:
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        Arguments:
            _record: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_record])


__all__ = ["ApiGateway", "ApiGatewayDomain", "CloudFrontTarget", "LoadBalancerTarget", "__jsii_assembly__"]

publication.publish()
