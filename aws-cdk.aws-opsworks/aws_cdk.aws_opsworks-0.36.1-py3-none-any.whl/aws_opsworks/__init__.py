import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-opsworks", "0.36.1", __name__, "aws-opsworks@0.36.1.jsii.tgz")
class CfnApp(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnApp"):
    """A CloudFormation ``AWS::OpsWorks::App``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::App
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, stack_id: str, type: str, app_source: typing.Optional[typing.Union[typing.Optional["SourceProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, data_sources: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DataSourceProperty"]]]]]=None, description: typing.Optional[str]=None, domains: typing.Optional[typing.List[str]]=None, enable_ssl: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, environment: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EnvironmentVariableProperty"]]]]]=None, shortname: typing.Optional[str]=None, ssl_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SslConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::OpsWorks::App``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::OpsWorks::App.Name``.
            stack_id: ``AWS::OpsWorks::App.StackId``.
            type: ``AWS::OpsWorks::App.Type``.
            app_source: ``AWS::OpsWorks::App.AppSource``.
            attributes: ``AWS::OpsWorks::App.Attributes``.
            data_sources: ``AWS::OpsWorks::App.DataSources``.
            description: ``AWS::OpsWorks::App.Description``.
            domains: ``AWS::OpsWorks::App.Domains``.
            enable_ssl: ``AWS::OpsWorks::App.EnableSsl``.
            environment: ``AWS::OpsWorks::App.Environment``.
            shortname: ``AWS::OpsWorks::App.Shortname``.
            ssl_configuration: ``AWS::OpsWorks::App.SslConfiguration``.

        Stability:
            experimental
        """
        props: CfnAppProps = {"name": name, "stackId": stack_id, "type": type}

        if app_source is not None:
            props["appSource"] = app_source

        if attributes is not None:
            props["attributes"] = attributes

        if data_sources is not None:
            props["dataSources"] = data_sources

        if description is not None:
            props["description"] = description

        if domains is not None:
            props["domains"] = domains

        if enable_ssl is not None:
            props["enableSsl"] = enable_ssl

        if environment is not None:
            props["environment"] = environment

        if shortname is not None:
            props["shortname"] = shortname

        if ssl_configuration is not None:
            props["sslConfiguration"] = ssl_configuration

        jsii.create(CfnApp, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::OpsWorks::App.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
        Stability:
            stable
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """``AWS::OpsWorks::App.StackId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
        Stability:
            stable
        """
        return jsii.get(self, "stackId")

    @stack_id.setter
    def stack_id(self, value: str):
        return jsii.set(self, "stackId", value)

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::OpsWorks::App.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
        Stability:
            stable
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        return jsii.set(self, "type", value)

    @property
    @jsii.member(jsii_name="appSource")
    def app_source(self) -> typing.Optional[typing.Union[typing.Optional["SourceProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::App.AppSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
        Stability:
            stable
        """
        return jsii.get(self, "appSource")

    @app_source.setter
    def app_source(self, value: typing.Optional[typing.Union[typing.Optional["SourceProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "appSource", value)

    @property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::OpsWorks::App.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
        Stability:
            stable
        """
        return jsii.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        return jsii.set(self, "attributes", value)

    @property
    @jsii.member(jsii_name="dataSources")
    def data_sources(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DataSourceProperty"]]]]]:
        """``AWS::OpsWorks::App.DataSources``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
        Stability:
            stable
        """
        return jsii.get(self, "dataSources")

    @data_sources.setter
    def data_sources(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "DataSourceProperty"]]]]]):
        return jsii.set(self, "dataSources", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::App.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
        Stability:
            stable
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::App.Domains``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
        Stability:
            stable
        """
        return jsii.get(self, "domains")

    @domains.setter
    def domains(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "domains", value)

    @property
    @jsii.member(jsii_name="enableSsl")
    def enable_ssl(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::App.EnableSsl``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
        Stability:
            stable
        """
        return jsii.get(self, "enableSsl")

    @enable_ssl.setter
    def enable_ssl(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "enableSsl", value)

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EnvironmentVariableProperty"]]]]]:
        """``AWS::OpsWorks::App.Environment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
        Stability:
            stable
        """
        return jsii.get(self, "environment")

    @environment.setter
    def environment(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EnvironmentVariableProperty"]]]]]):
        return jsii.set(self, "environment", value)

    @property
    @jsii.member(jsii_name="shortname")
    def shortname(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::App.Shortname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
        Stability:
            stable
        """
        return jsii.get(self, "shortname")

    @shortname.setter
    def shortname(self, value: typing.Optional[str]):
        return jsii.set(self, "shortname", value)

    @property
    @jsii.member(jsii_name="sslConfiguration")
    def ssl_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SslConfigurationProperty"]]]:
        """``AWS::OpsWorks::App.SslConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "sslConfiguration")

    @ssl_configuration.setter
    def ssl_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SslConfigurationProperty"]]]):
        return jsii.set(self, "sslConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.DataSourceProperty", jsii_struct_bases=[])
    class DataSourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html
        Stability:
            stable
        """
        arn: str
        """``CfnApp.DataSourceProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-arn
        Stability:
            stable
        """

        databaseName: str
        """``CfnApp.DataSourceProperty.DatabaseName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-databasename
        Stability:
            stable
        """

        type: str
        """``CfnApp.DataSourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-type
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _EnvironmentVariableProperty(jsii.compat.TypedDict, total=False):
        secure: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnApp.EnvironmentVariableProperty.Secure``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-secure
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.EnvironmentVariableProperty", jsii_struct_bases=[_EnvironmentVariableProperty])
    class EnvironmentVariableProperty(_EnvironmentVariableProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html
        Stability:
            stable
        """
        key: str
        """``CfnApp.EnvironmentVariableProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-key
        Stability:
            stable
        """

        value: str
        """``CfnApp.EnvironmentVariableProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#value
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SourceProperty", jsii_struct_bases=[])
    class SourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
        Stability:
            stable
        """
        password: str
        """``CfnApp.SourceProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-pw
        Stability:
            stable
        """

        revision: str
        """``CfnApp.SourceProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
        Stability:
            stable
        """

        sshKey: str
        """``CfnApp.SourceProperty.SshKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
        Stability:
            stable
        """

        type: str
        """``CfnApp.SourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
        Stability:
            stable
        """

        url: str
        """``CfnApp.SourceProperty.Url``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
        Stability:
            stable
        """

        username: str
        """``CfnApp.SourceProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnApp.SslConfigurationProperty", jsii_struct_bases=[])
    class SslConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html
        Stability:
            stable
        """
        certificate: str
        """``CfnApp.SslConfigurationProperty.Certificate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-certificate
        Stability:
            stable
        """

        chain: str
        """``CfnApp.SslConfigurationProperty.Chain``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-chain
        Stability:
            stable
        """

        privateKey: str
        """``CfnApp.SslConfigurationProperty.PrivateKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-privatekey
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAppProps(jsii.compat.TypedDict, total=False):
    appSource: typing.Union["CfnApp.SourceProperty", aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::App.AppSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
    Stability:
        stable
    """
    attributes: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
    """``AWS::OpsWorks::App.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
    Stability:
        stable
    """
    dataSources: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.DataSourceProperty"]]]
    """``AWS::OpsWorks::App.DataSources``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
    Stability:
        stable
    """
    description: str
    """``AWS::OpsWorks::App.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
    Stability:
        stable
    """
    domains: typing.List[str]
    """``AWS::OpsWorks::App.Domains``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
    Stability:
        stable
    """
    enableSsl: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::App.EnableSsl``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
    Stability:
        stable
    """
    environment: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]
    """``AWS::OpsWorks::App.Environment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
    Stability:
        stable
    """
    shortname: str
    """``AWS::OpsWorks::App.Shortname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
    Stability:
        stable
    """
    sslConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnApp.SslConfigurationProperty"]
    """``AWS::OpsWorks::App.SslConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnAppProps", jsii_struct_bases=[_CfnAppProps])
class CfnAppProps(_CfnAppProps):
    """Properties for defining a ``AWS::OpsWorks::App``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    Stability:
        stable
    """
    name: str
    """``AWS::OpsWorks::App.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
    Stability:
        stable
    """

    stackId: str
    """``AWS::OpsWorks::App.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
    Stability:
        stable
    """

    type: str
    """``AWS::OpsWorks::App.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
    Stability:
        stable
    """

class CfnElasticLoadBalancerAttachment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachment"):
    """A CloudFormation ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::ElasticLoadBalancerAttachment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, elastic_load_balancer_name: str, layer_id: str) -> None:
        """Create a new ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            elastic_load_balancer_name: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.
            layer_id: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

        Stability:
            experimental
        """
        props: CfnElasticLoadBalancerAttachmentProps = {"elasticLoadBalancerName": elastic_load_balancer_name, "layerId": layer_id}

        jsii.create(CfnElasticLoadBalancerAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="elasticLoadBalancerName")
    def elastic_load_balancer_name(self) -> str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-elbname
        Stability:
            stable
        """
        return jsii.get(self, "elasticLoadBalancerName")

    @elastic_load_balancer_name.setter
    def elastic_load_balancer_name(self, value: str):
        return jsii.set(self, "elasticLoadBalancerName", value)

    @property
    @jsii.member(jsii_name="layerId")
    def layer_id(self) -> str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-layerid
        Stability:
            stable
        """
        return jsii.get(self, "layerId")

    @layer_id.setter
    def layer_id(self, value: str):
        return jsii.set(self, "layerId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachmentProps", jsii_struct_bases=[])
class CfnElasticLoadBalancerAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
    Stability:
        stable
    """
    elasticLoadBalancerName: str
    """``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-elbname
    Stability:
        stable
    """

    layerId: str
    """``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-layerid
    Stability:
        stable
    """

class CfnInstance(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnInstance"):
    """A CloudFormation ``AWS::OpsWorks::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::Instance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, instance_type: str, layer_ids: typing.List[str], stack_id: str, agent_version: typing.Optional[str]=None, ami_id: typing.Optional[str]=None, architecture: typing.Optional[str]=None, auto_scaling_type: typing.Optional[str]=None, availability_zone: typing.Optional[str]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, elastic_ips: typing.Optional[typing.List[str]]=None, hostname: typing.Optional[str]=None, install_updates_on_boot: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, os: typing.Optional[str]=None, root_device_type: typing.Optional[str]=None, ssh_key_name: typing.Optional[str]=None, subnet_id: typing.Optional[str]=None, tenancy: typing.Optional[str]=None, time_based_auto_scaling: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeBasedAutoScalingProperty"]]]=None, virtualization_type: typing.Optional[str]=None, volumes: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::OpsWorks::Instance``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            instance_type: ``AWS::OpsWorks::Instance.InstanceType``.
            layer_ids: ``AWS::OpsWorks::Instance.LayerIds``.
            stack_id: ``AWS::OpsWorks::Instance.StackId``.
            agent_version: ``AWS::OpsWorks::Instance.AgentVersion``.
            ami_id: ``AWS::OpsWorks::Instance.AmiId``.
            architecture: ``AWS::OpsWorks::Instance.Architecture``.
            auto_scaling_type: ``AWS::OpsWorks::Instance.AutoScalingType``.
            availability_zone: ``AWS::OpsWorks::Instance.AvailabilityZone``.
            block_device_mappings: ``AWS::OpsWorks::Instance.BlockDeviceMappings``.
            ebs_optimized: ``AWS::OpsWorks::Instance.EbsOptimized``.
            elastic_ips: ``AWS::OpsWorks::Instance.ElasticIps``.
            hostname: ``AWS::OpsWorks::Instance.Hostname``.
            install_updates_on_boot: ``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.
            os: ``AWS::OpsWorks::Instance.Os``.
            root_device_type: ``AWS::OpsWorks::Instance.RootDeviceType``.
            ssh_key_name: ``AWS::OpsWorks::Instance.SshKeyName``.
            subnet_id: ``AWS::OpsWorks::Instance.SubnetId``.
            tenancy: ``AWS::OpsWorks::Instance.Tenancy``.
            time_based_auto_scaling: ``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.
            virtualization_type: ``AWS::OpsWorks::Instance.VirtualizationType``.
            volumes: ``AWS::OpsWorks::Instance.Volumes``.

        Stability:
            experimental
        """
        props: CfnInstanceProps = {"instanceType": instance_type, "layerIds": layer_ids, "stackId": stack_id}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if ami_id is not None:
            props["amiId"] = ami_id

        if architecture is not None:
            props["architecture"] = architecture

        if auto_scaling_type is not None:
            props["autoScalingType"] = auto_scaling_type

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname is not None:
            props["hostname"] = hostname

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if os is not None:
            props["os"] = os

        if root_device_type is not None:
            props["rootDeviceType"] = root_device_type

        if ssh_key_name is not None:
            props["sshKeyName"] = ssh_key_name

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tenancy is not None:
            props["tenancy"] = tenancy

        if time_based_auto_scaling is not None:
            props["timeBasedAutoScaling"] = time_based_auto_scaling

        if virtualization_type is not None:
            props["virtualizationType"] = virtualization_type

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAvailabilityZone")
    def attr_availability_zone(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            AvailabilityZone
        """
        return jsii.get(self, "attrAvailabilityZone")

    @property
    @jsii.member(jsii_name="attrPrivateDnsName")
    def attr_private_dns_name(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            PrivateDnsName
        """
        return jsii.get(self, "attrPrivateDnsName")

    @property
    @jsii.member(jsii_name="attrPrivateIp")
    def attr_private_ip(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            PrivateIp
        """
        return jsii.get(self, "attrPrivateIp")

    @property
    @jsii.member(jsii_name="attrPublicDnsName")
    def attr_public_dns_name(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            PublicDnsName
        """
        return jsii.get(self, "attrPublicDnsName")

    @property
    @jsii.member(jsii_name="attrPublicIp")
    def attr_public_ip(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            PublicIp
        """
        return jsii.get(self, "attrPublicIp")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> str:
        """``AWS::OpsWorks::Instance.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
        Stability:
            stable
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter
    def instance_type(self, value: str):
        return jsii.set(self, "instanceType", value)

    @property
    @jsii.member(jsii_name="layerIds")
    def layer_ids(self) -> typing.List[str]:
        """``AWS::OpsWorks::Instance.LayerIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
        Stability:
            stable
        """
        return jsii.get(self, "layerIds")

    @layer_ids.setter
    def layer_ids(self, value: typing.List[str]):
        return jsii.set(self, "layerIds", value)

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """``AWS::OpsWorks::Instance.StackId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
        Stability:
            stable
        """
        return jsii.get(self, "stackId")

    @stack_id.setter
    def stack_id(self, value: str):
        return jsii.set(self, "stackId", value)

    @property
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.AgentVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
        Stability:
            stable
        """
        return jsii.get(self, "agentVersion")

    @agent_version.setter
    def agent_version(self, value: typing.Optional[str]):
        return jsii.set(self, "agentVersion", value)

    @property
    @jsii.member(jsii_name="amiId")
    def ami_id(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.AmiId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
        Stability:
            stable
        """
        return jsii.get(self, "amiId")

    @ami_id.setter
    def ami_id(self, value: typing.Optional[str]):
        return jsii.set(self, "amiId", value)

    @property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.Architecture``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
        Stability:
            stable
        """
        return jsii.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: typing.Optional[str]):
        return jsii.set(self, "architecture", value)

    @property
    @jsii.member(jsii_name="autoScalingType")
    def auto_scaling_type(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.AutoScalingType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
        Stability:
            stable
        """
        return jsii.get(self, "autoScalingType")

    @auto_scaling_type.setter
    def auto_scaling_type(self, value: typing.Optional[str]):
        return jsii.set(self, "autoScalingType", value)

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
        Stability:
            stable
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[str]):
        return jsii.set(self, "availabilityZone", value)

    @property
    @jsii.member(jsii_name="blockDeviceMappings")
    def block_device_mappings(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]:
        """``AWS::OpsWorks::Instance.BlockDeviceMappings``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
        Stability:
            stable
        """
        return jsii.get(self, "blockDeviceMappings")

    @block_device_mappings.setter
    def block_device_mappings(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "BlockDeviceMappingProperty"]]]]]):
        return jsii.set(self, "blockDeviceMappings", value)

    @property
    @jsii.member(jsii_name="ebsOptimized")
    def ebs_optimized(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Instance.EbsOptimized``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
        Stability:
            stable
        """
        return jsii.get(self, "ebsOptimized")

    @ebs_optimized.setter
    def ebs_optimized(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "ebsOptimized", value)

    @property
    @jsii.member(jsii_name="elasticIps")
    def elastic_ips(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::Instance.ElasticIps``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
        Stability:
            stable
        """
        return jsii.get(self, "elasticIps")

    @elastic_ips.setter
    def elastic_ips(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "elasticIps", value)

    @property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.Hostname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
        Stability:
            stable
        """
        return jsii.get(self, "hostname")

    @hostname.setter
    def hostname(self, value: typing.Optional[str]):
        return jsii.set(self, "hostname", value)

    @property
    @jsii.member(jsii_name="installUpdatesOnBoot")
    def install_updates_on_boot(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
        Stability:
            stable
        """
        return jsii.get(self, "installUpdatesOnBoot")

    @install_updates_on_boot.setter
    def install_updates_on_boot(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "installUpdatesOnBoot", value)

    @property
    @jsii.member(jsii_name="os")
    def os(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.Os``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
        Stability:
            stable
        """
        return jsii.get(self, "os")

    @os.setter
    def os(self, value: typing.Optional[str]):
        return jsii.set(self, "os", value)

    @property
    @jsii.member(jsii_name="rootDeviceType")
    def root_device_type(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.RootDeviceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
        Stability:
            stable
        """
        return jsii.get(self, "rootDeviceType")

    @root_device_type.setter
    def root_device_type(self, value: typing.Optional[str]):
        return jsii.set(self, "rootDeviceType", value)

    @property
    @jsii.member(jsii_name="sshKeyName")
    def ssh_key_name(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.SshKeyName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
        Stability:
            stable
        """
        return jsii.get(self, "sshKeyName")

    @ssh_key_name.setter
    def ssh_key_name(self, value: typing.Optional[str]):
        return jsii.set(self, "sshKeyName", value)

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
        Stability:
            stable
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: typing.Optional[str]):
        return jsii.set(self, "subnetId", value)

    @property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.Tenancy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
        Stability:
            stable
        """
        return jsii.get(self, "tenancy")

    @tenancy.setter
    def tenancy(self, value: typing.Optional[str]):
        return jsii.set(self, "tenancy", value)

    @property
    @jsii.member(jsii_name="timeBasedAutoScaling")
    def time_based_auto_scaling(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeBasedAutoScalingProperty"]]]:
        """``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
        Stability:
            stable
        """
        return jsii.get(self, "timeBasedAutoScaling")

    @time_based_auto_scaling.setter
    def time_based_auto_scaling(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["TimeBasedAutoScalingProperty"]]]):
        return jsii.set(self, "timeBasedAutoScaling", value)

    @property
    @jsii.member(jsii_name="virtualizationType")
    def virtualization_type(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Instance.VirtualizationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
        Stability:
            stable
        """
        return jsii.get(self, "virtualizationType")

    @virtualization_type.setter
    def virtualization_type(self, value: typing.Optional[str]):
        return jsii.set(self, "virtualizationType", value)

    @property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::Instance.Volumes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
        Stability:
            stable
        """
        return jsii.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "volumes", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.BlockDeviceMappingProperty", jsii_struct_bases=[])
    class BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html
        Stability:
            stable
        """
        deviceName: str
        """``CfnInstance.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-devicename
        Stability:
            stable
        """

        ebs: typing.Union[aws_cdk.core.IResolvable, "CfnInstance.EbsBlockDeviceProperty"]
        """``CfnInstance.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-ebs
        Stability:
            stable
        """

        noDevice: str
        """``CfnInstance.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-nodevice
        Stability:
            stable
        """

        virtualName: str
        """``CfnInstance.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-virtualname
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.EbsBlockDeviceProperty", jsii_struct_bases=[])
    class EbsBlockDeviceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html
        Stability:
            stable
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnInstance.EbsBlockDeviceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-deleteontermination
        Stability:
            stable
        """

        iops: jsii.Number
        """``CfnInstance.EbsBlockDeviceProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-iops
        Stability:
            stable
        """

        snapshotId: str
        """``CfnInstance.EbsBlockDeviceProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-snapshotid
        Stability:
            stable
        """

        volumeSize: jsii.Number
        """``CfnInstance.EbsBlockDeviceProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumesize
        Stability:
            stable
        """

        volumeType: str
        """``CfnInstance.EbsBlockDeviceProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumetype
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstance.TimeBasedAutoScalingProperty", jsii_struct_bases=[])
    class TimeBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html
        Stability:
            stable
        """
        friday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Friday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-friday
        Stability:
            stable
        """

        monday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Monday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-monday
        Stability:
            stable
        """

        saturday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Saturday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-saturday
        Stability:
            stable
        """

        sunday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Sunday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-sunday
        Stability:
            stable
        """

        thursday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Thursday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-thursday
        Stability:
            stable
        """

        tuesday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Tuesday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-tuesday
        Stability:
            stable
        """

        wednesday: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnInstance.TimeBasedAutoScalingProperty.Wednesday``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-wednesday
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnInstanceProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    """``AWS::OpsWorks::Instance.AgentVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
    Stability:
        stable
    """
    amiId: str
    """``AWS::OpsWorks::Instance.AmiId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
    Stability:
        stable
    """
    architecture: str
    """``AWS::OpsWorks::Instance.Architecture``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
    Stability:
        stable
    """
    autoScalingType: str
    """``AWS::OpsWorks::Instance.AutoScalingType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
    Stability:
        stable
    """
    availabilityZone: str
    """``AWS::OpsWorks::Instance.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
    Stability:
        stable
    """
    blockDeviceMappings: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.BlockDeviceMappingProperty"]]]
    """``AWS::OpsWorks::Instance.BlockDeviceMappings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
    Stability:
        stable
    """
    ebsOptimized: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Instance.EbsOptimized``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
    Stability:
        stable
    """
    elasticIps: typing.List[str]
    """``AWS::OpsWorks::Instance.ElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
    Stability:
        stable
    """
    hostname: str
    """``AWS::OpsWorks::Instance.Hostname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
    Stability:
        stable
    """
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
    Stability:
        stable
    """
    os: str
    """``AWS::OpsWorks::Instance.Os``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
    Stability:
        stable
    """
    rootDeviceType: str
    """``AWS::OpsWorks::Instance.RootDeviceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
    Stability:
        stable
    """
    sshKeyName: str
    """``AWS::OpsWorks::Instance.SshKeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
    Stability:
        stable
    """
    subnetId: str
    """``AWS::OpsWorks::Instance.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
    Stability:
        stable
    """
    tenancy: str
    """``AWS::OpsWorks::Instance.Tenancy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
    Stability:
        stable
    """
    timeBasedAutoScaling: typing.Union[aws_cdk.core.IResolvable, "CfnInstance.TimeBasedAutoScalingProperty"]
    """``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
    Stability:
        stable
    """
    virtualizationType: str
    """``AWS::OpsWorks::Instance.VirtualizationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
    Stability:
        stable
    """
    volumes: typing.List[str]
    """``AWS::OpsWorks::Instance.Volumes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnInstanceProps", jsii_struct_bases=[_CfnInstanceProps])
class CfnInstanceProps(_CfnInstanceProps):
    """Properties for defining a ``AWS::OpsWorks::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    Stability:
        stable
    """
    instanceType: str
    """``AWS::OpsWorks::Instance.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
    Stability:
        stable
    """

    layerIds: typing.List[str]
    """``AWS::OpsWorks::Instance.LayerIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
    Stability:
        stable
    """

    stackId: str
    """``AWS::OpsWorks::Instance.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
    Stability:
        stable
    """

class CfnLayer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnLayer"):
    """A CloudFormation ``AWS::OpsWorks::Layer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::Layer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, auto_assign_elastic_ips: typing.Union[bool, aws_cdk.core.IResolvable], auto_assign_public_ips: typing.Union[bool, aws_cdk.core.IResolvable], enable_auto_healing: typing.Union[bool, aws_cdk.core.IResolvable], name: str, shortname: str, stack_id: str, type: str, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, custom_instance_profile_arn: typing.Optional[str]=None, custom_json: typing.Any=None, custom_recipes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RecipesProperty"]]]=None, custom_security_group_ids: typing.Optional[typing.List[str]]=None, install_updates_on_boot: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, lifecycle_event_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleEventConfigurationProperty"]]]=None, load_based_auto_scaling: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBasedAutoScalingProperty"]]]=None, packages: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, use_ebs_optimized_instances: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, volume_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeConfigurationProperty"]]]]]=None) -> None:
        """Create a new ``AWS::OpsWorks::Layer``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            auto_assign_elastic_ips: ``AWS::OpsWorks::Layer.AutoAssignElasticIps``.
            auto_assign_public_ips: ``AWS::OpsWorks::Layer.AutoAssignPublicIps``.
            enable_auto_healing: ``AWS::OpsWorks::Layer.EnableAutoHealing``.
            name: ``AWS::OpsWorks::Layer.Name``.
            shortname: ``AWS::OpsWorks::Layer.Shortname``.
            stack_id: ``AWS::OpsWorks::Layer.StackId``.
            type: ``AWS::OpsWorks::Layer.Type``.
            attributes: ``AWS::OpsWorks::Layer.Attributes``.
            custom_instance_profile_arn: ``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.
            custom_json: ``AWS::OpsWorks::Layer.CustomJson``.
            custom_recipes: ``AWS::OpsWorks::Layer.CustomRecipes``.
            custom_security_group_ids: ``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.
            install_updates_on_boot: ``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.
            lifecycle_event_configuration: ``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.
            load_based_auto_scaling: ``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.
            packages: ``AWS::OpsWorks::Layer.Packages``.
            tags: ``AWS::OpsWorks::Layer.Tags``.
            use_ebs_optimized_instances: ``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.
            volume_configurations: ``AWS::OpsWorks::Layer.VolumeConfigurations``.

        Stability:
            experimental
        """
        props: CfnLayerProps = {"autoAssignElasticIps": auto_assign_elastic_ips, "autoAssignPublicIps": auto_assign_public_ips, "enableAutoHealing": enable_auto_healing, "name": name, "shortname": shortname, "stackId": stack_id, "type": type}

        if attributes is not None:
            props["attributes"] = attributes

        if custom_instance_profile_arn is not None:
            props["customInstanceProfileArn"] = custom_instance_profile_arn

        if custom_json is not None:
            props["customJson"] = custom_json

        if custom_recipes is not None:
            props["customRecipes"] = custom_recipes

        if custom_security_group_ids is not None:
            props["customSecurityGroupIds"] = custom_security_group_ids

        if install_updates_on_boot is not None:
            props["installUpdatesOnBoot"] = install_updates_on_boot

        if lifecycle_event_configuration is not None:
            props["lifecycleEventConfiguration"] = lifecycle_event_configuration

        if load_based_auto_scaling is not None:
            props["loadBasedAutoScaling"] = load_based_auto_scaling

        if packages is not None:
            props["packages"] = packages

        if tags is not None:
            props["tags"] = tags

        if use_ebs_optimized_instances is not None:
            props["useEbsOptimizedInstances"] = use_ebs_optimized_instances

        if volume_configurations is not None:
            props["volumeConfigurations"] = volume_configurations

        jsii.create(CfnLayer, self, [scope, id, props])

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
        """``AWS::OpsWorks::Layer.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="autoAssignElasticIps")
    def auto_assign_elastic_ips(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignElasticIps``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
        Stability:
            stable
        """
        return jsii.get(self, "autoAssignElasticIps")

    @auto_assign_elastic_ips.setter
    def auto_assign_elastic_ips(self, value: typing.Union[bool, aws_cdk.core.IResolvable]):
        return jsii.set(self, "autoAssignElasticIps", value)

    @property
    @jsii.member(jsii_name="autoAssignPublicIps")
    def auto_assign_public_ips(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignPublicIps``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
        Stability:
            stable
        """
        return jsii.get(self, "autoAssignPublicIps")

    @auto_assign_public_ips.setter
    def auto_assign_public_ips(self, value: typing.Union[bool, aws_cdk.core.IResolvable]):
        return jsii.set(self, "autoAssignPublicIps", value)

    @property
    @jsii.member(jsii_name="customJson")
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Layer.CustomJson``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
        Stability:
            stable
        """
        return jsii.get(self, "customJson")

    @custom_json.setter
    def custom_json(self, value: typing.Any):
        return jsii.set(self, "customJson", value)

    @property
    @jsii.member(jsii_name="enableAutoHealing")
    def enable_auto_healing(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.EnableAutoHealing``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
        Stability:
            stable
        """
        return jsii.get(self, "enableAutoHealing")

    @enable_auto_healing.setter
    def enable_auto_healing(self, value: typing.Union[bool, aws_cdk.core.IResolvable]):
        return jsii.set(self, "enableAutoHealing", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::OpsWorks::Layer.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
        Stability:
            stable
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="shortname")
    def shortname(self) -> str:
        """``AWS::OpsWorks::Layer.Shortname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
        Stability:
            stable
        """
        return jsii.get(self, "shortname")

    @shortname.setter
    def shortname(self, value: str):
        return jsii.set(self, "shortname", value)

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """``AWS::OpsWorks::Layer.StackId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
        Stability:
            stable
        """
        return jsii.get(self, "stackId")

    @stack_id.setter
    def stack_id(self, value: str):
        return jsii.set(self, "stackId", value)

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::OpsWorks::Layer.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
        Stability:
            stable
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        return jsii.set(self, "type", value)

    @property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::OpsWorks::Layer.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
        Stability:
            stable
        """
        return jsii.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        return jsii.set(self, "attributes", value)

    @property
    @jsii.member(jsii_name="customInstanceProfileArn")
    def custom_instance_profile_arn(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
        Stability:
            stable
        """
        return jsii.get(self, "customInstanceProfileArn")

    @custom_instance_profile_arn.setter
    def custom_instance_profile_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "customInstanceProfileArn", value)

    @property
    @jsii.member(jsii_name="customRecipes")
    def custom_recipes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RecipesProperty"]]]:
        """``AWS::OpsWorks::Layer.CustomRecipes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
        Stability:
            stable
        """
        return jsii.get(self, "customRecipes")

    @custom_recipes.setter
    def custom_recipes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["RecipesProperty"]]]):
        return jsii.set(self, "customRecipes", value)

    @property
    @jsii.member(jsii_name="customSecurityGroupIds")
    def custom_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
        Stability:
            stable
        """
        return jsii.get(self, "customSecurityGroupIds")

    @custom_security_group_ids.setter
    def custom_security_group_ids(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "customSecurityGroupIds", value)

    @property
    @jsii.member(jsii_name="installUpdatesOnBoot")
    def install_updates_on_boot(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
        Stability:
            stable
        """
        return jsii.get(self, "installUpdatesOnBoot")

    @install_updates_on_boot.setter
    def install_updates_on_boot(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "installUpdatesOnBoot", value)

    @property
    @jsii.member(jsii_name="lifecycleEventConfiguration")
    def lifecycle_event_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleEventConfigurationProperty"]]]:
        """``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "lifecycleEventConfiguration")

    @lifecycle_event_configuration.setter
    def lifecycle_event_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LifecycleEventConfigurationProperty"]]]):
        return jsii.set(self, "lifecycleEventConfiguration", value)

    @property
    @jsii.member(jsii_name="loadBasedAutoScaling")
    def load_based_auto_scaling(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBasedAutoScalingProperty"]]]:
        """``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
        Stability:
            stable
        """
        return jsii.get(self, "loadBasedAutoScaling")

    @load_based_auto_scaling.setter
    def load_based_auto_scaling(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBasedAutoScalingProperty"]]]):
        return jsii.set(self, "loadBasedAutoScaling", value)

    @property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::Layer.Packages``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
        Stability:
            stable
        """
        return jsii.get(self, "packages")

    @packages.setter
    def packages(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "packages", value)

    @property
    @jsii.member(jsii_name="useEbsOptimizedInstances")
    def use_ebs_optimized_instances(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
        Stability:
            stable
        """
        return jsii.get(self, "useEbsOptimizedInstances")

    @use_ebs_optimized_instances.setter
    def use_ebs_optimized_instances(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "useEbsOptimizedInstances", value)

    @property
    @jsii.member(jsii_name="volumeConfigurations")
    def volume_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeConfigurationProperty"]]]]]:
        """``AWS::OpsWorks::Layer.VolumeConfigurations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
        Stability:
            stable
        """
        return jsii.get(self, "volumeConfigurations")

    @volume_configurations.setter
    def volume_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeConfigurationProperty"]]]]]):
        return jsii.set(self, "volumeConfigurations", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.AutoScalingThresholdsProperty", jsii_struct_bases=[])
    class AutoScalingThresholdsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html
        Stability:
            stable
        """
        cpuThreshold: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.CpuThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-cputhreshold
        Stability:
            stable
        """

        ignoreMetricsTime: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.IgnoreMetricsTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-ignoremetricstime
        Stability:
            stable
        """

        instanceCount: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.InstanceCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-instancecount
        Stability:
            stable
        """

        loadThreshold: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.LoadThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-loadthreshold
        Stability:
            stable
        """

        memoryThreshold: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.MemoryThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-memorythreshold
        Stability:
            stable
        """

        thresholdsWaitTime: jsii.Number
        """``CfnLayer.AutoScalingThresholdsProperty.ThresholdsWaitTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-thresholdwaittime
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LifecycleEventConfigurationProperty", jsii_struct_bases=[])
    class LifecycleEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html
        Stability:
            stable
        """
        shutdownEventConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.ShutdownEventConfigurationProperty"]
        """``CfnLayer.LifecycleEventConfigurationProperty.ShutdownEventConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LoadBasedAutoScalingProperty", jsii_struct_bases=[])
    class LoadBasedAutoScalingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html
        Stability:
            stable
        """
        downScaling: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]
        """``CfnLayer.LoadBasedAutoScalingProperty.DownScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-downscaling
        Stability:
            stable
        """

        enable: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnLayer.LoadBasedAutoScalingProperty.Enable``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-enable
        Stability:
            stable
        """

        upScaling: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]
        """``CfnLayer.LoadBasedAutoScalingProperty.UpScaling``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-upscaling
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.RecipesProperty", jsii_struct_bases=[])
    class RecipesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html
        Stability:
            stable
        """
        configure: typing.List[str]
        """``CfnLayer.RecipesProperty.Configure``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-configure
        Stability:
            stable
        """

        deploy: typing.List[str]
        """``CfnLayer.RecipesProperty.Deploy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-deploy
        Stability:
            stable
        """

        setup: typing.List[str]
        """``CfnLayer.RecipesProperty.Setup``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-setup
        Stability:
            stable
        """

        shutdown: typing.List[str]
        """``CfnLayer.RecipesProperty.Shutdown``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-shutdown
        Stability:
            stable
        """

        undeploy: typing.List[str]
        """``CfnLayer.RecipesProperty.Undeploy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-undeploy
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.ShutdownEventConfigurationProperty", jsii_struct_bases=[])
    class ShutdownEventConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html
        Stability:
            stable
        """
        delayUntilElbConnectionsDrained: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnLayer.ShutdownEventConfigurationProperty.DelayUntilElbConnectionsDrained``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-delayuntilelbconnectionsdrained
        Stability:
            stable
        """

        executionTimeout: jsii.Number
        """``CfnLayer.ShutdownEventConfigurationProperty.ExecutionTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-executiontimeout
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayer.VolumeConfigurationProperty", jsii_struct_bases=[])
    class VolumeConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html
        Stability:
            stable
        """
        encrypted: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnLayer.VolumeConfigurationProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-encrypted
        Stability:
            stable
        """

        iops: jsii.Number
        """``CfnLayer.VolumeConfigurationProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-iops
        Stability:
            stable
        """

        mountPoint: str
        """``CfnLayer.VolumeConfigurationProperty.MountPoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-mountpoint
        Stability:
            stable
        """

        numberOfDisks: jsii.Number
        """``CfnLayer.VolumeConfigurationProperty.NumberOfDisks``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-numberofdisks
        Stability:
            stable
        """

        raidLevel: jsii.Number
        """``CfnLayer.VolumeConfigurationProperty.RaidLevel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-raidlevel
        Stability:
            stable
        """

        size: jsii.Number
        """``CfnLayer.VolumeConfigurationProperty.Size``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-size
        Stability:
            stable
        """

        volumeType: str
        """``CfnLayer.VolumeConfigurationProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-volumetype
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLayerProps(jsii.compat.TypedDict, total=False):
    attributes: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
    """``AWS::OpsWorks::Layer.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
    Stability:
        stable
    """
    customInstanceProfileArn: str
    """``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
    Stability:
        stable
    """
    customJson: typing.Any
    """``AWS::OpsWorks::Layer.CustomJson``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
    Stability:
        stable
    """
    customRecipes: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.RecipesProperty"]
    """``AWS::OpsWorks::Layer.CustomRecipes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
    Stability:
        stable
    """
    customSecurityGroupIds: typing.List[str]
    """``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
    Stability:
        stable
    """
    installUpdatesOnBoot: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
    Stability:
        stable
    """
    lifecycleEventConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LifecycleEventConfigurationProperty"]
    """``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
    Stability:
        stable
    """
    loadBasedAutoScaling: typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LoadBasedAutoScalingProperty"]
    """``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
    Stability:
        stable
    """
    packages: typing.List[str]
    """``AWS::OpsWorks::Layer.Packages``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
    Stability:
        stable
    """
    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::OpsWorks::Layer.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
    Stability:
        stable
    """
    useEbsOptimizedInstances: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
    Stability:
        stable
    """
    volumeConfigurations: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.VolumeConfigurationProperty"]]]
    """``AWS::OpsWorks::Layer.VolumeConfigurations``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnLayerProps", jsii_struct_bases=[_CfnLayerProps])
class CfnLayerProps(_CfnLayerProps):
    """Properties for defining a ``AWS::OpsWorks::Layer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    Stability:
        stable
    """
    autoAssignElasticIps: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Layer.AutoAssignElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
    Stability:
        stable
    """

    autoAssignPublicIps: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Layer.AutoAssignPublicIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
    Stability:
        stable
    """

    enableAutoHealing: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Layer.EnableAutoHealing``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
    Stability:
        stable
    """

    name: str
    """``AWS::OpsWorks::Layer.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
    Stability:
        stable
    """

    shortname: str
    """``AWS::OpsWorks::Layer.Shortname``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
    Stability:
        stable
    """

    stackId: str
    """``AWS::OpsWorks::Layer.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
    Stability:
        stable
    """

    type: str
    """``AWS::OpsWorks::Layer.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
    Stability:
        stable
    """

class CfnStack(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnStack"):
    """A CloudFormation ``AWS::OpsWorks::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::Stack
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_instance_profile_arn: str, name: str, service_role_arn: str, agent_version: typing.Optional[str]=None, attributes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]=None, chef_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ChefConfigurationProperty"]]]=None, clone_app_ids: typing.Optional[typing.List[str]]=None, clone_permissions: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, configuration_manager: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StackConfigurationManagerProperty"]]]=None, custom_cookbooks_source: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SourceProperty"]]]=None, custom_json: typing.Any=None, default_availability_zone: typing.Optional[str]=None, default_os: typing.Optional[str]=None, default_root_device_type: typing.Optional[str]=None, default_ssh_key_name: typing.Optional[str]=None, default_subnet_id: typing.Optional[str]=None, ecs_cluster_arn: typing.Optional[str]=None, elastic_ips: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticIpProperty"]]]]]=None, hostname_theme: typing.Optional[str]=None, rds_db_instances: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RdsDbInstanceProperty"]]]]]=None, source_stack_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, use_custom_cookbooks: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, use_opsworks_security_groups: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::Stack``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            default_instance_profile_arn: ``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.
            name: ``AWS::OpsWorks::Stack.Name``.
            service_role_arn: ``AWS::OpsWorks::Stack.ServiceRoleArn``.
            agent_version: ``AWS::OpsWorks::Stack.AgentVersion``.
            attributes: ``AWS::OpsWorks::Stack.Attributes``.
            chef_configuration: ``AWS::OpsWorks::Stack.ChefConfiguration``.
            clone_app_ids: ``AWS::OpsWorks::Stack.CloneAppIds``.
            clone_permissions: ``AWS::OpsWorks::Stack.ClonePermissions``.
            configuration_manager: ``AWS::OpsWorks::Stack.ConfigurationManager``.
            custom_cookbooks_source: ``AWS::OpsWorks::Stack.CustomCookbooksSource``.
            custom_json: ``AWS::OpsWorks::Stack.CustomJson``.
            default_availability_zone: ``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.
            default_os: ``AWS::OpsWorks::Stack.DefaultOs``.
            default_root_device_type: ``AWS::OpsWorks::Stack.DefaultRootDeviceType``.
            default_ssh_key_name: ``AWS::OpsWorks::Stack.DefaultSshKeyName``.
            default_subnet_id: ``AWS::OpsWorks::Stack.DefaultSubnetId``.
            ecs_cluster_arn: ``AWS::OpsWorks::Stack.EcsClusterArn``.
            elastic_ips: ``AWS::OpsWorks::Stack.ElasticIps``.
            hostname_theme: ``AWS::OpsWorks::Stack.HostnameTheme``.
            rds_db_instances: ``AWS::OpsWorks::Stack.RdsDbInstances``.
            source_stack_id: ``AWS::OpsWorks::Stack.SourceStackId``.
            tags: ``AWS::OpsWorks::Stack.Tags``.
            use_custom_cookbooks: ``AWS::OpsWorks::Stack.UseCustomCookbooks``.
            use_opsworks_security_groups: ``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.
            vpc_id: ``AWS::OpsWorks::Stack.VpcId``.

        Stability:
            experimental
        """
        props: CfnStackProps = {"defaultInstanceProfileArn": default_instance_profile_arn, "name": name, "serviceRoleArn": service_role_arn}

        if agent_version is not None:
            props["agentVersion"] = agent_version

        if attributes is not None:
            props["attributes"] = attributes

        if chef_configuration is not None:
            props["chefConfiguration"] = chef_configuration

        if clone_app_ids is not None:
            props["cloneAppIds"] = clone_app_ids

        if clone_permissions is not None:
            props["clonePermissions"] = clone_permissions

        if configuration_manager is not None:
            props["configurationManager"] = configuration_manager

        if custom_cookbooks_source is not None:
            props["customCookbooksSource"] = custom_cookbooks_source

        if custom_json is not None:
            props["customJson"] = custom_json

        if default_availability_zone is not None:
            props["defaultAvailabilityZone"] = default_availability_zone

        if default_os is not None:
            props["defaultOs"] = default_os

        if default_root_device_type is not None:
            props["defaultRootDeviceType"] = default_root_device_type

        if default_ssh_key_name is not None:
            props["defaultSshKeyName"] = default_ssh_key_name

        if default_subnet_id is not None:
            props["defaultSubnetId"] = default_subnet_id

        if ecs_cluster_arn is not None:
            props["ecsClusterArn"] = ecs_cluster_arn

        if elastic_ips is not None:
            props["elasticIps"] = elastic_ips

        if hostname_theme is not None:
            props["hostnameTheme"] = hostname_theme

        if rds_db_instances is not None:
            props["rdsDbInstances"] = rds_db_instances

        if source_stack_id is not None:
            props["sourceStackId"] = source_stack_id

        if tags is not None:
            props["tags"] = tags

        if use_custom_cookbooks is not None:
            props["useCustomCookbooks"] = use_custom_cookbooks

        if use_opsworks_security_groups is not None:
            props["useOpsworksSecurityGroups"] = use_opsworks_security_groups

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnStack, self, [scope, id, props])

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
        """``AWS::OpsWorks::Stack.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="customJson")
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Stack.CustomJson``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custjson
        Stability:
            stable
        """
        return jsii.get(self, "customJson")

    @custom_json.setter
    def custom_json(self, value: typing.Any):
        return jsii.set(self, "customJson", value)

    @property
    @jsii.member(jsii_name="defaultInstanceProfileArn")
    def default_instance_profile_arn(self) -> str:
        """``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprof
        Stability:
            stable
        """
        return jsii.get(self, "defaultInstanceProfileArn")

    @default_instance_profile_arn.setter
    def default_instance_profile_arn(self, value: str):
        return jsii.set(self, "defaultInstanceProfileArn", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::OpsWorks::Stack.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
        Stability:
            stable
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> str:
        """``AWS::OpsWorks::Stack.ServiceRoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
        Stability:
            stable
        """
        return jsii.get(self, "serviceRoleArn")

    @service_role_arn.setter
    def service_role_arn(self, value: str):
        return jsii.set(self, "serviceRoleArn", value)

    @property
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.AgentVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
        Stability:
            stable
        """
        return jsii.get(self, "agentVersion")

    @agent_version.setter
    def agent_version(self, value: typing.Optional[str]):
        return jsii.set(self, "agentVersion", value)

    @property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]:
        """``AWS::OpsWorks::Stack.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
        Stability:
            stable
        """
        return jsii.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.Mapping[str,str]]]]):
        return jsii.set(self, "attributes", value)

    @property
    @jsii.member(jsii_name="chefConfiguration")
    def chef_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ChefConfigurationProperty"]]]:
        """``AWS::OpsWorks::Stack.ChefConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "chefConfiguration")

    @chef_configuration.setter
    def chef_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ChefConfigurationProperty"]]]):
        return jsii.set(self, "chefConfiguration", value)

    @property
    @jsii.member(jsii_name="cloneAppIds")
    def clone_app_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::OpsWorks::Stack.CloneAppIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
        Stability:
            stable
        """
        return jsii.get(self, "cloneAppIds")

    @clone_app_ids.setter
    def clone_app_ids(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "cloneAppIds", value)

    @property
    @jsii.member(jsii_name="clonePermissions")
    def clone_permissions(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Stack.ClonePermissions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
        Stability:
            stable
        """
        return jsii.get(self, "clonePermissions")

    @clone_permissions.setter
    def clone_permissions(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "clonePermissions", value)

    @property
    @jsii.member(jsii_name="configurationManager")
    def configuration_manager(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StackConfigurationManagerProperty"]]]:
        """``AWS::OpsWorks::Stack.ConfigurationManager``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configmanager
        Stability:
            stable
        """
        return jsii.get(self, "configurationManager")

    @configuration_manager.setter
    def configuration_manager(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["StackConfigurationManagerProperty"]]]):
        return jsii.set(self, "configurationManager", value)

    @property
    @jsii.member(jsii_name="customCookbooksSource")
    def custom_cookbooks_source(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SourceProperty"]]]:
        """``AWS::OpsWorks::Stack.CustomCookbooksSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custcookbooksource
        Stability:
            stable
        """
        return jsii.get(self, "customCookbooksSource")

    @custom_cookbooks_source.setter
    def custom_cookbooks_source(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SourceProperty"]]]):
        return jsii.set(self, "customCookbooksSource", value)

    @property
    @jsii.member(jsii_name="defaultAvailabilityZone")
    def default_availability_zone(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultaz
        Stability:
            stable
        """
        return jsii.get(self, "defaultAvailabilityZone")

    @default_availability_zone.setter
    def default_availability_zone(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultAvailabilityZone", value)

    @property
    @jsii.member(jsii_name="defaultOs")
    def default_os(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.DefaultOs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
        Stability:
            stable
        """
        return jsii.get(self, "defaultOs")

    @default_os.setter
    def default_os(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultOs", value)

    @property
    @jsii.member(jsii_name="defaultRootDeviceType")
    def default_root_device_type(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.DefaultRootDeviceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
        Stability:
            stable
        """
        return jsii.get(self, "defaultRootDeviceType")

    @default_root_device_type.setter
    def default_root_device_type(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultRootDeviceType", value)

    @property
    @jsii.member(jsii_name="defaultSshKeyName")
    def default_ssh_key_name(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.DefaultSshKeyName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
        Stability:
            stable
        """
        return jsii.get(self, "defaultSshKeyName")

    @default_ssh_key_name.setter
    def default_ssh_key_name(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultSshKeyName", value)

    @property
    @jsii.member(jsii_name="defaultSubnetId")
    def default_subnet_id(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.DefaultSubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#defaultsubnet
        Stability:
            stable
        """
        return jsii.get(self, "defaultSubnetId")

    @default_subnet_id.setter
    def default_subnet_id(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultSubnetId", value)

    @property
    @jsii.member(jsii_name="ecsClusterArn")
    def ecs_cluster_arn(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.EcsClusterArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
        Stability:
            stable
        """
        return jsii.get(self, "ecsClusterArn")

    @ecs_cluster_arn.setter
    def ecs_cluster_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "ecsClusterArn", value)

    @property
    @jsii.member(jsii_name="elasticIps")
    def elastic_ips(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticIpProperty"]]]]]:
        """``AWS::OpsWorks::Stack.ElasticIps``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
        Stability:
            stable
        """
        return jsii.get(self, "elasticIps")

    @elastic_ips.setter
    def elastic_ips(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticIpProperty"]]]]]):
        return jsii.set(self, "elasticIps", value)

    @property
    @jsii.member(jsii_name="hostnameTheme")
    def hostname_theme(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.HostnameTheme``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
        Stability:
            stable
        """
        return jsii.get(self, "hostnameTheme")

    @hostname_theme.setter
    def hostname_theme(self, value: typing.Optional[str]):
        return jsii.set(self, "hostnameTheme", value)

    @property
    @jsii.member(jsii_name="rdsDbInstances")
    def rds_db_instances(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RdsDbInstanceProperty"]]]]]:
        """``AWS::OpsWorks::Stack.RdsDbInstances``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
        Stability:
            stable
        """
        return jsii.get(self, "rdsDbInstances")

    @rds_db_instances.setter
    def rds_db_instances(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "RdsDbInstanceProperty"]]]]]):
        return jsii.set(self, "rdsDbInstances", value)

    @property
    @jsii.member(jsii_name="sourceStackId")
    def source_stack_id(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.SourceStackId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
        Stability:
            stable
        """
        return jsii.get(self, "sourceStackId")

    @source_stack_id.setter
    def source_stack_id(self, value: typing.Optional[str]):
        return jsii.set(self, "sourceStackId", value)

    @property
    @jsii.member(jsii_name="useCustomCookbooks")
    def use_custom_cookbooks(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Stack.UseCustomCookbooks``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#usecustcookbooks
        Stability:
            stable
        """
        return jsii.get(self, "useCustomCookbooks")

    @use_custom_cookbooks.setter
    def use_custom_cookbooks(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "useCustomCookbooks", value)

    @property
    @jsii.member(jsii_name="useOpsworksSecurityGroups")
    def use_opsworks_security_groups(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
        Stability:
            stable
        """
        return jsii.get(self, "useOpsworksSecurityGroups")

    @use_opsworks_security_groups.setter
    def use_opsworks_security_groups(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "useOpsworksSecurityGroups", value)

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Stack.VpcId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
        Stability:
            stable
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[str]):
        return jsii.set(self, "vpcId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ChefConfigurationProperty", jsii_struct_bases=[])
    class ChefConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html
        Stability:
            stable
        """
        berkshelfVersion: str
        """``CfnStack.ChefConfigurationProperty.BerkshelfVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
        Stability:
            stable
        """

        manageBerkshelf: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnStack.ChefConfigurationProperty.ManageBerkshelf``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ElasticIpProperty(jsii.compat.TypedDict, total=False):
        name: str
        """``CfnStack.ElasticIpProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-name
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.ElasticIpProperty", jsii_struct_bases=[_ElasticIpProperty])
    class ElasticIpProperty(_ElasticIpProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html
        Stability:
            stable
        """
        ip: str
        """``CfnStack.ElasticIpProperty.Ip``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-ip
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.RdsDbInstanceProperty", jsii_struct_bases=[])
    class RdsDbInstanceProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html
        Stability:
            stable
        """
        dbPassword: str
        """``CfnStack.RdsDbInstanceProperty.DbPassword``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbpassword
        Stability:
            stable
        """

        dbUser: str
        """``CfnStack.RdsDbInstanceProperty.DbUser``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbuser
        Stability:
            stable
        """

        rdsDbInstanceArn: str
        """``CfnStack.RdsDbInstanceProperty.RdsDbInstanceArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-rdsdbinstancearn
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.SourceProperty", jsii_struct_bases=[])
    class SourceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
        Stability:
            stable
        """
        password: str
        """``CfnStack.SourceProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-password
        Stability:
            stable
        """

        revision: str
        """``CfnStack.SourceProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
        Stability:
            stable
        """

        sshKey: str
        """``CfnStack.SourceProperty.SshKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
        Stability:
            stable
        """

        type: str
        """``CfnStack.SourceProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
        Stability:
            stable
        """

        url: str
        """``CfnStack.SourceProperty.Url``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
        Stability:
            stable
        """

        username: str
        """``CfnStack.SourceProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStack.StackConfigurationManagerProperty", jsii_struct_bases=[])
    class StackConfigurationManagerProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html
        Stability:
            stable
        """
        name: str
        """``CfnStack.StackConfigurationManagerProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-name
        Stability:
            stable
        """

        version: str
        """``CfnStack.StackConfigurationManagerProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-version
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnStackProps(jsii.compat.TypedDict, total=False):
    agentVersion: str
    """``AWS::OpsWorks::Stack.AgentVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
    Stability:
        stable
    """
    attributes: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
    """``AWS::OpsWorks::Stack.Attributes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
    Stability:
        stable
    """
    chefConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnStack.ChefConfigurationProperty"]
    """``AWS::OpsWorks::Stack.ChefConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
    Stability:
        stable
    """
    cloneAppIds: typing.List[str]
    """``AWS::OpsWorks::Stack.CloneAppIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
    Stability:
        stable
    """
    clonePermissions: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Stack.ClonePermissions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
    Stability:
        stable
    """
    configurationManager: typing.Union[aws_cdk.core.IResolvable, "CfnStack.StackConfigurationManagerProperty"]
    """``AWS::OpsWorks::Stack.ConfigurationManager``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configmanager
    Stability:
        stable
    """
    customCookbooksSource: typing.Union[aws_cdk.core.IResolvable, "CfnStack.SourceProperty"]
    """``AWS::OpsWorks::Stack.CustomCookbooksSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custcookbooksource
    Stability:
        stable
    """
    customJson: typing.Any
    """``AWS::OpsWorks::Stack.CustomJson``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custjson
    Stability:
        stable
    """
    defaultAvailabilityZone: str
    """``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultaz
    Stability:
        stable
    """
    defaultOs: str
    """``AWS::OpsWorks::Stack.DefaultOs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
    Stability:
        stable
    """
    defaultRootDeviceType: str
    """``AWS::OpsWorks::Stack.DefaultRootDeviceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
    Stability:
        stable
    """
    defaultSshKeyName: str
    """``AWS::OpsWorks::Stack.DefaultSshKeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
    Stability:
        stable
    """
    defaultSubnetId: str
    """``AWS::OpsWorks::Stack.DefaultSubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#defaultsubnet
    Stability:
        stable
    """
    ecsClusterArn: str
    """``AWS::OpsWorks::Stack.EcsClusterArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
    Stability:
        stable
    """
    elasticIps: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ElasticIpProperty"]]]
    """``AWS::OpsWorks::Stack.ElasticIps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
    Stability:
        stable
    """
    hostnameTheme: str
    """``AWS::OpsWorks::Stack.HostnameTheme``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
    Stability:
        stable
    """
    rdsDbInstances: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.RdsDbInstanceProperty"]]]
    """``AWS::OpsWorks::Stack.RdsDbInstances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
    Stability:
        stable
    """
    sourceStackId: str
    """``AWS::OpsWorks::Stack.SourceStackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
    Stability:
        stable
    """
    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::OpsWorks::Stack.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
    Stability:
        stable
    """
    useCustomCookbooks: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Stack.UseCustomCookbooks``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#usecustcookbooks
    Stability:
        stable
    """
    useOpsworksSecurityGroups: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
    Stability:
        stable
    """
    vpcId: str
    """``AWS::OpsWorks::Stack.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnStackProps", jsii_struct_bases=[_CfnStackProps])
class CfnStackProps(_CfnStackProps):
    """Properties for defining a ``AWS::OpsWorks::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    Stability:
        stable
    """
    defaultInstanceProfileArn: str
    """``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprof
    Stability:
        stable
    """

    name: str
    """``AWS::OpsWorks::Stack.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
    Stability:
        stable
    """

    serviceRoleArn: str
    """``AWS::OpsWorks::Stack.ServiceRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
    Stability:
        stable
    """

class CfnUserProfile(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnUserProfile"):
    """A CloudFormation ``AWS::OpsWorks::UserProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::UserProfile
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, iam_user_arn: str, allow_self_management: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ssh_public_key: typing.Optional[str]=None, ssh_username: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::UserProfile``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            iam_user_arn: ``AWS::OpsWorks::UserProfile.IamUserArn``.
            allow_self_management: ``AWS::OpsWorks::UserProfile.AllowSelfManagement``.
            ssh_public_key: ``AWS::OpsWorks::UserProfile.SshPublicKey``.
            ssh_username: ``AWS::OpsWorks::UserProfile.SshUsername``.

        Stability:
            experimental
        """
        props: CfnUserProfileProps = {"iamUserArn": iam_user_arn}

        if allow_self_management is not None:
            props["allowSelfManagement"] = allow_self_management

        if ssh_public_key is not None:
            props["sshPublicKey"] = ssh_public_key

        if ssh_username is not None:
            props["sshUsername"] = ssh_username

        jsii.create(CfnUserProfile, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrSshUsername")
    def attr_ssh_username(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            SshUsername
        """
        return jsii.get(self, "attrSshUsername")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="iamUserArn")
    def iam_user_arn(self) -> str:
        """``AWS::OpsWorks::UserProfile.IamUserArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
        Stability:
            stable
        """
        return jsii.get(self, "iamUserArn")

    @iam_user_arn.setter
    def iam_user_arn(self, value: str):
        return jsii.set(self, "iamUserArn", value)

    @property
    @jsii.member(jsii_name="allowSelfManagement")
    def allow_self_management(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::OpsWorks::UserProfile.AllowSelfManagement``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
        Stability:
            stable
        """
        return jsii.get(self, "allowSelfManagement")

    @allow_self_management.setter
    def allow_self_management(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "allowSelfManagement", value)

    @property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::UserProfile.SshPublicKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
        Stability:
            stable
        """
        return jsii.get(self, "sshPublicKey")

    @ssh_public_key.setter
    def ssh_public_key(self, value: typing.Optional[str]):
        return jsii.set(self, "sshPublicKey", value)

    @property
    @jsii.member(jsii_name="sshUsername")
    def ssh_username(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::UserProfile.SshUsername``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
        Stability:
            stable
        """
        return jsii.get(self, "sshUsername")

    @ssh_username.setter
    def ssh_username(self, value: typing.Optional[str]):
        return jsii.set(self, "sshUsername", value)


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnUserProfileProps(jsii.compat.TypedDict, total=False):
    allowSelfManagement: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::OpsWorks::UserProfile.AllowSelfManagement``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
    Stability:
        stable
    """
    sshPublicKey: str
    """``AWS::OpsWorks::UserProfile.SshPublicKey``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
    Stability:
        stable
    """
    sshUsername: str
    """``AWS::OpsWorks::UserProfile.SshUsername``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnUserProfileProps", jsii_struct_bases=[_CfnUserProfileProps])
class CfnUserProfileProps(_CfnUserProfileProps):
    """Properties for defining a ``AWS::OpsWorks::UserProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    Stability:
        stable
    """
    iamUserArn: str
    """``AWS::OpsWorks::UserProfile.IamUserArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
    Stability:
        stable
    """

class CfnVolume(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-opsworks.CfnVolume"):
    """A CloudFormation ``AWS::OpsWorks::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    Stability:
        stable
    cloudformationResource:
        AWS::OpsWorks::Volume
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, ec2_volume_id: str, stack_id: str, mount_point: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::OpsWorks::Volume``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ec2_volume_id: ``AWS::OpsWorks::Volume.Ec2VolumeId``.
            stack_id: ``AWS::OpsWorks::Volume.StackId``.
            mount_point: ``AWS::OpsWorks::Volume.MountPoint``.
            name: ``AWS::OpsWorks::Volume.Name``.

        Stability:
            experimental
        """
        props: CfnVolumeProps = {"ec2VolumeId": ec2_volume_id, "stackId": stack_id}

        if mount_point is not None:
            props["mountPoint"] = mount_point

        if name is not None:
            props["name"] = name

        jsii.create(CfnVolume, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="ec2VolumeId")
    def ec2_volume_id(self) -> str:
        """``AWS::OpsWorks::Volume.Ec2VolumeId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
        Stability:
            stable
        """
        return jsii.get(self, "ec2VolumeId")

    @ec2_volume_id.setter
    def ec2_volume_id(self, value: str):
        return jsii.set(self, "ec2VolumeId", value)

    @property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> str:
        """``AWS::OpsWorks::Volume.StackId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
        Stability:
            stable
        """
        return jsii.get(self, "stackId")

    @stack_id.setter
    def stack_id(self, value: str):
        return jsii.set(self, "stackId", value)

    @property
    @jsii.member(jsii_name="mountPoint")
    def mount_point(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Volume.MountPoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
        Stability:
            stable
        """
        return jsii.get(self, "mountPoint")

    @mount_point.setter
    def mount_point(self, value: typing.Optional[str]):
        return jsii.set(self, "mountPoint", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::OpsWorks::Volume.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
        Stability:
            stable
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVolumeProps(jsii.compat.TypedDict, total=False):
    mountPoint: str
    """``AWS::OpsWorks::Volume.MountPoint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
    Stability:
        stable
    """
    name: str
    """``AWS::OpsWorks::Volume.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-opsworks.CfnVolumeProps", jsii_struct_bases=[_CfnVolumeProps])
class CfnVolumeProps(_CfnVolumeProps):
    """Properties for defining a ``AWS::OpsWorks::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    Stability:
        stable
    """
    ec2VolumeId: str
    """``AWS::OpsWorks::Volume.Ec2VolumeId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
    Stability:
        stable
    """

    stackId: str
    """``AWS::OpsWorks::Volume.StackId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
    Stability:
        stable
    """

__all__ = ["CfnApp", "CfnAppProps", "CfnElasticLoadBalancerAttachment", "CfnElasticLoadBalancerAttachmentProps", "CfnInstance", "CfnInstanceProps", "CfnLayer", "CfnLayerProps", "CfnStack", "CfnStackProps", "CfnUserProfile", "CfnUserProfileProps", "CfnVolume", "CfnVolumeProps", "__jsii_assembly__"]

publication.publish()
