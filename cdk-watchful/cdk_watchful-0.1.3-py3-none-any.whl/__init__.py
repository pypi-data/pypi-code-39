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
__jsii_assembly__ = jsii.JSIIAssembly.load("cdk-watchful", "0.1.3", __name__, "cdk-watchful@0.1.3.jsii.tgz")
@jsii.interface(jsii_type="cdk-watchful.IWatchable")
class IWatchable(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IWatchableProxy

    @jsii.member(jsii_name="addToWatchful")
    def add_to_watchful(self, watchful: "IWatchful", title: str) -> None:
        """
        Arguments:
            watchful: -
            title: -
        """
        ...


class _IWatchableProxy():
    __jsii_type__ = "cdk-watchful.IWatchable"
    @jsii.member(jsii_name="addToWatchful")
    def add_to_watchful(self, watchful: "IWatchful", title: str) -> None:
        """
        Arguments:
            watchful: -
            title: -
        """
        return jsii.invoke(self, "addToWatchful", [watchful, title])


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

    @jsii.member(jsii_name="isWatchable")
    @classmethod
    def is_watchable(cls, obj: typing.Any) -> bool:
        """
        Arguments:
            obj: -
        """
        return jsii.sinvoke(cls, "isWatchable", [obj])

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

    @jsii.member(jsii_name="watch")
    def watch(self, title: str, obj: "IWatchable") -> None:
        """
        Arguments:
            title: -
            obj: -
        """
        return jsii.invoke(self, "watch", [title, obj])

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


@jsii.data_type(jsii_type="cdk-watchful.WatchfulProps", jsii_struct_bases=[])
class WatchfulProps(jsii.compat.TypedDict, total=False):
    alarmEmail: str

__all__ = ["IWatchable", "IWatchful", "QuickLink", "SectionOptions", "WatchDynamoTable", "WatchDynamoTableOptions", "WatchDynamoTableProps", "WatchLambdaFunction", "WatchLambdaFunctionOptions", "WatchLambdaFunctionProps", "Watchful", "WatchfulProps", "__jsii_assembly__"]

publication.publish()
