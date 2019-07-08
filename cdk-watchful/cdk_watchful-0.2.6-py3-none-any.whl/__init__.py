import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_cloudwatch_actions
import aws_cdk.aws_dynamodb
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("cdk-watchful", "0.2.6", __name__, "cdk-watchful@0.2.6.jsii.tgz")
@jsii.interface(jsii_type="cdk-watchful.IWatchful")
class IWatchful(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IWatchfulProxy

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.Alarm) -> None:
        """
        Arguments:
            alarm: -
        """
        ...

    @jsii.member(jsii_name="addSection")
    def add_section(self, title: str, *, links: typing.Optional[typing.List["QuickLink"]]=None) -> None:
        """
        Arguments:
            title: -
            options: -
            links: -
        """
        ...

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: aws_cdk.aws_cloudwatch.IWidget) -> None:
        """
        Arguments:
            widgets: -
        """
        ...


class _IWatchfulProxy():
    __jsii_type__ = "cdk-watchful.IWatchful"
    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.Alarm) -> None:
        """
        Arguments:
            alarm: -
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addSection")
    def add_section(self, title: str, *, links: typing.Optional[typing.List["QuickLink"]]=None) -> None:
        """
        Arguments:
            title: -
            options: -
            links: -
        """
        options: SectionOptions = {}

        if links is not None:
            options["links"] = links

        return jsii.invoke(self, "addSection", [title, options])

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: aws_cdk.aws_cloudwatch.IWidget) -> None:
        """
        Arguments:
            widgets: -
        """
        return jsii.invoke(self, "addWidgets", [*widgets])


@jsii.data_type(jsii_type="cdk-watchful.QuickLink", jsii_struct_bases=[])
class QuickLink(jsii.compat.TypedDict):
    title: str

    url: str

@jsii.data_type(jsii_type="cdk-watchful.SectionOptions", jsii_struct_bases=[])
class SectionOptions(jsii.compat.TypedDict, total=False):
    links: typing.List["QuickLink"]

class WatchApiGateway(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.WatchApiGateway"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, rest_api: aws_cdk.aws_apigateway.RestApi, title: str, watchful: "IWatchful", cache_graph: typing.Optional[bool]=None, server_error_threshold: typing.Optional[jsii.Number]=None, watched_operations: typing.Optional[typing.List["WatchedOperation"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            rest_api: The API Gateway REST API that is being watched.
            title: The title of this section.
            watchful: The Watchful instance to add widgets into.
            cache_graph: Include a dashboard graph for caching metrics. Default: false
            server_error_threshold: Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
            watched_operations: A list of operations to monitor separately. Default: - only API-level monitoring is added.
        """
        props: WatchApiGatewayProps = {"restApi": rest_api, "title": title, "watchful": watchful}

        if cache_graph is not None:
            props["cacheGraph"] = cache_graph

        if server_error_threshold is not None:
            props["serverErrorThreshold"] = server_error_threshold

        if watched_operations is not None:
            props["watchedOperations"] = watched_operations

        jsii.create(WatchApiGateway, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-watchful.WatchApiGatewayOptions", jsii_struct_bases=[])
class WatchApiGatewayOptions(jsii.compat.TypedDict, total=False):
    cacheGraph: bool
    """Include a dashboard graph for caching metrics.

    Default:
        false
    """

    serverErrorThreshold: jsii.Number
    """Alarm when 5XX errors reach this threshold over 5 minutes.

    Default:
        1 any 5xx HTTP response will trigger the alarm
    """

    watchedOperations: typing.List["WatchedOperation"]
    """A list of operations to monitor separately.

    Default:
        - only API-level monitoring is added.
    """

@jsii.data_type(jsii_type="cdk-watchful.WatchApiGatewayProps", jsii_struct_bases=[WatchApiGatewayOptions])
class WatchApiGatewayProps(WatchApiGatewayOptions, jsii.compat.TypedDict):
    restApi: aws_cdk.aws_apigateway.RestApi
    """The API Gateway REST API that is being watched."""

    title: str
    """The title of this section."""

    watchful: "IWatchful"
    """The Watchful instance to add widgets into."""

class WatchDynamoTable(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.WatchDynamoTable"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, table: aws_cdk.aws_dynamodb.Table, title: str, watchful: "IWatchful", read_capacity_threshold_percent: typing.Optional[jsii.Number]=None, write_capacity_threshold_percent: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            table: -
            title: -
            watchful: -
            read_capacity_threshold_percent: Threshold for read capacity alarm (percentage). Default: 80
            write_capacity_threshold_percent: Threshold for read capacity alarm (percentage). Default: 80
        """
        props: WatchDynamoTableProps = {"table": table, "title": title, "watchful": watchful}

        if read_capacity_threshold_percent is not None:
            props["readCapacityThresholdPercent"] = read_capacity_threshold_percent

        if write_capacity_threshold_percent is not None:
            props["writeCapacityThresholdPercent"] = write_capacity_threshold_percent

        jsii.create(WatchDynamoTable, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-watchful.WatchDynamoTableOptions", jsii_struct_bases=[])
class WatchDynamoTableOptions(jsii.compat.TypedDict, total=False):
    readCapacityThresholdPercent: jsii.Number
    """Threshold for read capacity alarm (percentage).

    Default:
        80
    """

    writeCapacityThresholdPercent: jsii.Number
    """Threshold for read capacity alarm (percentage).

    Default:
        80
    """

@jsii.data_type(jsii_type="cdk-watchful.WatchDynamoTableProps", jsii_struct_bases=[WatchDynamoTableOptions])
class WatchDynamoTableProps(WatchDynamoTableOptions, jsii.compat.TypedDict):
    table: aws_cdk.aws_dynamodb.Table

    title: str

    watchful: "IWatchful"

class WatchLambdaFunction(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.WatchLambdaFunction"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, fn: aws_cdk.aws_lambda.Function, title: str, watchful: "IWatchful", duration_threshold_percent: typing.Optional[jsii.Number]=None, errors_per_minute_threshold: typing.Optional[jsii.Number]=None, throttles_per_minute_threshold: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            fn: -
            title: -
            watchful: -
            duration_threshold_percent: Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
            errors_per_minute_threshold: Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
            throttles_per_minute_threshold: Number of allowed throttles per minute. Default: 0
        """
        props: WatchLambdaFunctionProps = {"fn": fn, "title": title, "watchful": watchful}

        if duration_threshold_percent is not None:
            props["durationThresholdPercent"] = duration_threshold_percent

        if errors_per_minute_threshold is not None:
            props["errorsPerMinuteThreshold"] = errors_per_minute_threshold

        if throttles_per_minute_threshold is not None:
            props["throttlesPerMinuteThreshold"] = throttles_per_minute_threshold

        jsii.create(WatchLambdaFunction, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-watchful.WatchLambdaFunctionOptions", jsii_struct_bases=[])
class WatchLambdaFunctionOptions(jsii.compat.TypedDict, total=False):
    durationThresholdPercent: jsii.Number
    """Threshold for the duration alarm as percentage of the function's timeout value.

    If this is set to 50%, the alarm will be set when p99 latency of the
    function exceeds 50% of the function's timeout setting.

    Default:
        80
    """

    errorsPerMinuteThreshold: jsii.Number
    """Number of allowed errors per minute.

    If there are more errors than that, an alarm will trigger.

    Default:
        0
    """

    throttlesPerMinuteThreshold: jsii.Number
    """Number of allowed throttles per minute.

    Default:
        0
    """

@jsii.data_type(jsii_type="cdk-watchful.WatchLambdaFunctionProps", jsii_struct_bases=[WatchLambdaFunctionOptions])
class WatchLambdaFunctionProps(WatchLambdaFunctionOptions, jsii.compat.TypedDict):
    fn: aws_cdk.aws_lambda.Function

    title: str

    watchful: "IWatchful"

@jsii.data_type(jsii_type="cdk-watchful.WatchedOperation", jsii_struct_bases=[])
class WatchedOperation(jsii.compat.TypedDict):
    """An operation (path and method) worth monitoring."""
    httpMethod: str
    """The HTTP method for the operation (GET, POST, ...)."""

    resourcePath: str
    """The REST API path for this operation (/, /resource/{id}, ...)."""

@jsii.implements(IWatchful)
class Watchful(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.Watchful"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, alarm_email: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            alarm_email: -
        """
        props: WatchfulProps = {}

        if alarm_email is not None:
            props["alarmEmail"] = alarm_email

        jsii.create(Watchful, self, [scope, id, props])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.Alarm) -> None:
        """
        Arguments:
            alarm: -
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addSection")
    def add_section(self, title: str, *, links: typing.Optional[typing.List["QuickLink"]]=None) -> None:
        """
        Arguments:
            title: -
            options: -
            links: -
        """
        options: SectionOptions = {}

        if links is not None:
            options["links"] = links

        return jsii.invoke(self, "addSection", [title, options])

    @jsii.member(jsii_name="addWidgets")
    def add_widgets(self, *widgets: aws_cdk.aws_cloudwatch.IWidget) -> None:
        """
        Arguments:
            widgets: -
        """
        return jsii.invoke(self, "addWidgets", [*widgets])

    @jsii.member(jsii_name="watchApiGateway")
    def watch_api_gateway(self, title: str, rest_api: aws_cdk.aws_apigateway.RestApi, *, cache_graph: typing.Optional[bool]=None, server_error_threshold: typing.Optional[jsii.Number]=None, watched_operations: typing.Optional[typing.List["WatchedOperation"]]=None) -> "WatchApiGateway":
        """
        Arguments:
            title: -
            rest_api: -
            options: -
            cache_graph: Include a dashboard graph for caching metrics. Default: false
            server_error_threshold: Alarm when 5XX errors reach this threshold over 5 minutes. Default: 1 any 5xx HTTP response will trigger the alarm
            watched_operations: A list of operations to monitor separately. Default: - only API-level monitoring is added.
        """
        options: WatchApiGatewayOptions = {}

        if cache_graph is not None:
            options["cacheGraph"] = cache_graph

        if server_error_threshold is not None:
            options["serverErrorThreshold"] = server_error_threshold

        if watched_operations is not None:
            options["watchedOperations"] = watched_operations

        return jsii.invoke(self, "watchApiGateway", [title, rest_api, options])

    @jsii.member(jsii_name="watchDynamoTable")
    def watch_dynamo_table(self, title: str, table: aws_cdk.aws_dynamodb.Table, *, read_capacity_threshold_percent: typing.Optional[jsii.Number]=None, write_capacity_threshold_percent: typing.Optional[jsii.Number]=None) -> "WatchDynamoTable":
        """
        Arguments:
            title: -
            table: -
            options: -
            read_capacity_threshold_percent: Threshold for read capacity alarm (percentage). Default: 80
            write_capacity_threshold_percent: Threshold for read capacity alarm (percentage). Default: 80
        """
        options: WatchDynamoTableOptions = {}

        if read_capacity_threshold_percent is not None:
            options["readCapacityThresholdPercent"] = read_capacity_threshold_percent

        if write_capacity_threshold_percent is not None:
            options["writeCapacityThresholdPercent"] = write_capacity_threshold_percent

        return jsii.invoke(self, "watchDynamoTable", [title, table, options])

    @jsii.member(jsii_name="watchLambdaFunction")
    def watch_lambda_function(self, title: str, fn: aws_cdk.aws_lambda.Function, *, duration_threshold_percent: typing.Optional[jsii.Number]=None, errors_per_minute_threshold: typing.Optional[jsii.Number]=None, throttles_per_minute_threshold: typing.Optional[jsii.Number]=None) -> "WatchLambdaFunction":
        """
        Arguments:
            title: -
            fn: -
            options: -
            duration_threshold_percent: Threshold for the duration alarm as percentage of the function's timeout value. If this is set to 50%, the alarm will be set when p99 latency of the function exceeds 50% of the function's timeout setting. Default: 80
            errors_per_minute_threshold: Number of allowed errors per minute. If there are more errors than that, an alarm will trigger. Default: 0
            throttles_per_minute_threshold: Number of allowed throttles per minute. Default: 0
        """
        options: WatchLambdaFunctionOptions = {}

        if duration_threshold_percent is not None:
            options["durationThresholdPercent"] = duration_threshold_percent

        if errors_per_minute_threshold is not None:
            options["errorsPerMinuteThreshold"] = errors_per_minute_threshold

        if throttles_per_minute_threshold is not None:
            options["throttlesPerMinuteThreshold"] = throttles_per_minute_threshold

        return jsii.invoke(self, "watchLambdaFunction", [title, fn, options])

    @jsii.member(jsii_name="watchScope")
    def watch_scope(self, scope: aws_cdk.core.Construct, *, api_gateway: typing.Optional[bool]=None, dynamodb: typing.Optional[bool]=None, lambda_: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            options: -
            api_gateway: Automatically watch API Gateway APIs in the scope. Default: true
            dynamodb: Automatically watch all Amazon DynamoDB tables in the scope. Default: true
            lambda_: Automatically watch AWS Lambda functions in the scope. Default: true
        """
        options: WatchfulAspectProps = {}

        if api_gateway is not None:
            options["apiGateway"] = api_gateway

        if dynamodb is not None:
            options["dynamodb"] = dynamodb

        if lambda_ is not None:
            options["lambda"] = lambda_

        return jsii.invoke(self, "watchScope", [scope, options])


@jsii.implements(aws_cdk.core.IAspect)
class WatchfulAspect(metaclass=jsii.JSIIMeta, jsii_type="cdk-watchful.WatchfulAspect"):
    """A CDK aspect that can automatically watch all resources within a scope."""
    def __init__(self, watchful: "Watchful", *, api_gateway: typing.Optional[bool]=None, dynamodb: typing.Optional[bool]=None, lambda_: typing.Optional[bool]=None) -> None:
        """Defines a watchful aspect.

        Arguments:
            watchful: The watchful to add those resources to.
            props: Options.
            api_gateway: Automatically watch API Gateway APIs in the scope. Default: true
            dynamodb: Automatically watch all Amazon DynamoDB tables in the scope. Default: true
            lambda_: Automatically watch AWS Lambda functions in the scope. Default: true
        """
        props: WatchfulAspectProps = {}

        if api_gateway is not None:
            props["apiGateway"] = api_gateway

        if dynamodb is not None:
            props["dynamodb"] = dynamodb

        if lambda_ is not None:
            props["lambda"] = lambda_

        jsii.create(WatchfulAspect, self, [watchful, props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        """All aspects can visit an IConstruct.

        Arguments:
            node: -
        """
        return jsii.invoke(self, "visit", [node])


@jsii.data_type(jsii_type="cdk-watchful.WatchfulAspectProps", jsii_struct_bases=[])
class WatchfulAspectProps(jsii.compat.TypedDict, total=False):
    apiGateway: bool
    """Automatically watch API Gateway APIs in the scope.

    Default:
        true
    """

    dynamodb: bool
    """Automatically watch all Amazon DynamoDB tables in the scope.

    Default:
        true
    """

    lambda_: bool
    """Automatically watch AWS Lambda functions in the scope.

    Default:
        true
    """

@jsii.data_type(jsii_type="cdk-watchful.WatchfulProps", jsii_struct_bases=[])
class WatchfulProps(jsii.compat.TypedDict, total=False):
    alarmEmail: str

__all__ = ["IWatchful", "QuickLink", "SectionOptions", "WatchApiGateway", "WatchApiGatewayOptions", "WatchApiGatewayProps", "WatchDynamoTable", "WatchDynamoTableOptions", "WatchDynamoTableProps", "WatchLambdaFunction", "WatchLambdaFunctionOptions", "WatchLambdaFunctionProps", "WatchedOperation", "Watchful", "WatchfulAspect", "WatchfulAspectProps", "WatchfulProps", "__jsii_assembly__"]

publication.publish()
