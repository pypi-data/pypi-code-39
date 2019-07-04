import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_codebuild
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import aws_cdk.core
import aws_cdk.custom_resources
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events-targets", "0.37.0", __name__, "aws-events-targets@0.37.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodeBuildProject(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodeBuildProject"):
    """Start a CodeBuild build when an AWS CloudWatch events rule is triggered.

    Stability:
        stable
    """
    def __init__(self, project: aws_cdk.aws_codebuild.IProject) -> None:
        """
        Arguments:
            project: -

        Stability:
            stable
        """
        jsii.create(CodeBuildProject, self, [project])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using build projects as event rule targets.

        Arguments:
            _rule: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class CodePipeline(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodePipeline"):
    """Allows the pipeline to be used as a CloudWatch event rule target.

    Stability:
        stable
    """
    def __init__(self, pipeline: aws_cdk.aws_codepipeline.IPipeline) -> None:
        """
        Arguments:
            pipeline: -

        Stability:
            stable
        """
        jsii.create(CodePipeline, self, [pipeline])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns the rule target specification. NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        Arguments:
            _rule: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_rule])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ContainerOverride(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    """Command to run inside the container.

    Default:
        Default command

    Stability:
        stable
    """
    cpu: jsii.Number
    """The number of cpu units reserved for the container.

    Default:
        The default value from the task definition.

    Stability:
        stable
    """
    environment: typing.List["TaskEnvironmentVariable"]
    """Variables to set in the container's environment.

    Stability:
        stable
    """
    memoryLimit: jsii.Number
    """Hard memory limit on the container.

    Default:
        The default value from the task definition.

    Stability:
        stable
    """
    memoryReservation: jsii.Number
    """Soft memory limit on the container.

    Default:
        The default value from the task definition.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.ContainerOverride", jsii_struct_bases=[_ContainerOverride])
class ContainerOverride(_ContainerOverride):
    """
    Stability:
        stable
    """
    containerName: str
    """Name of the container inside the task definition.

    Stability:
        stable
    """

@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class EcsTask(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.EcsTask"):
    """Start a task on an ECS cluster.

    Stability:
        stable
    """
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, task_definition: aws_cdk.aws_ecs.TaskDefinition, container_overrides: typing.Optional[typing.List["ContainerOverride"]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, task_count: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            cluster: Cluster where service will be deployed.
            task_definition: Task Definition of the task that should be started.
            container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override.
            security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
            subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
            task_count: How many tasks should be started when this event is triggered. Default: 1

        Stability:
            stable
        """
        props: EcsTaskProps = {"cluster": cluster, "taskDefinition": task_definition}

        if container_overrides is not None:
            props["containerOverrides"] = container_overrides

        if security_group is not None:
            props["securityGroup"] = security_group

        if subnet_selection is not None:
            props["subnetSelection"] = subnet_selection

        if task_count is not None:
            props["taskCount"] = task_count

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Allows using tasks as target of CloudWatch events.

        Arguments:
            rule: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [rule])

    @property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "securityGroup")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _EcsTaskProps(jsii.compat.TypedDict, total=False):
    containerOverrides: typing.List["ContainerOverride"]
    """Container setting overrides.

    Key is the name of the container to override, value is the
    values you want to override.

    Stability:
        stable
    """
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    """Existing security group to use for the task's ENIs.

    (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

    Default:
        A new security group is created

    Stability:
        stable
    """
    subnetSelection: aws_cdk.aws_ec2.SubnetSelection
    """In what subnets to place the task's ENIs.

    (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

    Default:
        Private subnets

    Stability:
        stable
    """
    taskCount: jsii.Number
    """How many tasks should be started when this event is triggered.

    Default:
        1

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.EcsTaskProps", jsii_struct_bases=[_EcsTaskProps])
class EcsTaskProps(_EcsTaskProps):
    """Properties to define an ECS Event Task.

    Stability:
        stable
    """
    cluster: aws_cdk.aws_ecs.ICluster
    """Cluster where service will be deployed.

    Stability:
        stable
    """

    taskDefinition: aws_cdk.aws_ecs.TaskDefinition
    """Task Definition of the task that should be started.

    Stability:
        stable
    """

@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class LambdaFunction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.LambdaFunction"):
    """Use an AWS Lambda function as an event rule target.

    Stability:
        stable
    """
    def __init__(self, handler: aws_cdk.aws_lambda.IFunction, *, event: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        Arguments:
            handler: -
            props: -
            event: The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire CloudWatch event

        Stability:
            stable
        """
        props: LambdaFunctionProps = {}

        if event is not None:
            props["event"] = event

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this Lambda as a result from a CloudWatch event.

        Arguments:
            rule: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [rule])


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.LambdaFunctionProps", jsii_struct_bases=[])
class LambdaFunctionProps(jsii.compat.TypedDict, total=False):
    """Customize the SNS Topic Event Target.

    Stability:
        stable
    """
    event: aws_cdk.aws_events.RuleTargetInput
    """The event to send to the Lambda.

    This will be the payload sent to the Lambda Function.

    Default:
        the entire CloudWatch event

    Stability:
        stable
    """

@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SfnStateMachine(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SfnStateMachine"):
    """Use a StepFunctions state machine as a target for AWS CloudWatch event rules.

    Stability:
        stable
    """
    def __init__(self, machine: aws_cdk.aws_stepfunctions.IStateMachine, *, input: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        Arguments:
            machine: -
            props: -
            input: The input to the state machine execution. Default: the entire CloudWatch event

        Stability:
            stable
        """
        props: SfnStateMachineProps = {}

        if input is not None:
            props["input"] = input

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a properties that are used in an Rule to trigger this State Machine.

        Arguments:
            _rule: -

        See:
            https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/resource-based-policies-cwe.html#sns-permissions
        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_rule])

    @property
    @jsii.member(jsii_name="machine")
    def machine(self) -> aws_cdk.aws_stepfunctions.IStateMachine:
        """
        Stability:
            stable
        """
        return jsii.get(self, "machine")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SfnStateMachineProps", jsii_struct_bases=[])
class SfnStateMachineProps(jsii.compat.TypedDict, total=False):
    """Customize the Step Functions State Machine target.

    Stability:
        stable
    """
    input: aws_cdk.aws_events.RuleTargetInput
    """The input to the state machine execution.

    Default:
        the entire CloudWatch event

    Stability:
        stable
    """

@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SnsTopic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SnsTopic"):
    """Use an SNS topic as a target for AWS CloudWatch event rules.

    Stability:
        stable

    Example::
           // publish to an SNS topic every time code is committed
           // to a CodeCommit repository
           repository.onCommit(new targets.SnsTopic(topic));
    """
    def __init__(self, topic: aws_cdk.aws_sns.ITopic, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None) -> None:
        """
        Arguments:
            topic: -
            props: -
            message: The message to send to the topic. Default: the entire CloudWatch event

        Stability:
            stable
        """
        props: SnsTopicProps = {}

        if message is not None:
            props["message"] = message

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SNS topic as a result from a CloudWatch event.

        Arguments:
            _rule: -

        See:
            https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/resource-based-policies-cwe.html#sns-permissions
        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_rule])

    @property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        """
        Stability:
            stable
        """
        return jsii.get(self, "topic")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SnsTopicProps", jsii_struct_bases=[])
class SnsTopicProps(jsii.compat.TypedDict, total=False):
    """Customize the SNS Topic Event Target.

    Stability:
        stable
    """
    message: aws_cdk.aws_events.RuleTargetInput
    """The message to send to the topic.

    Default:
        the entire CloudWatch event

    Stability:
        stable
    """

@jsii.implements(aws_cdk.aws_events.IRuleTarget)
class SqsQueue(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SqsQueue"):
    """Use an SQS Queue as a target for AWS CloudWatch event rules.

    Stability:
        stable

    Example::
           // publish to an SQS queue every time code is committed
           // to a CodeCommit repository
           repository.onCommit(new targets.SqsQueue(queue));
    """
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, message: typing.Optional[aws_cdk.aws_events.RuleTargetInput]=None, message_group_id: typing.Optional[str]=None) -> None:
        """
        Arguments:
            queue: -
            props: -
            message: The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire CloudWatch event
            message_group_id: Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        Stability:
            stable
        """
        props: SqsQueueProps = {}

        if message is not None:
            props["message"] = message

        if message_group_id is not None:
            props["messageGroupId"] = message_group_id

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: aws_cdk.aws_events.IRule) -> aws_cdk.aws_events.RuleTargetConfig:
        """Returns a RuleTarget that can be used to trigger this SQS queue as a result from a CloudWatch event.

        Arguments:
            rule: -

        See:
            https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/resource-based-policies-cwe.html#sqs-permissions
        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [rule])

    @property
    @jsii.member(jsii_name="queue")
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        """
        Stability:
            stable
        """
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.SqsQueueProps", jsii_struct_bases=[])
class SqsQueueProps(jsii.compat.TypedDict, total=False):
    """Customize the SQS Queue Event Target.

    Stability:
        stable
    """
    message: aws_cdk.aws_events.RuleTargetInput
    """The message to send to the queue.

    Must be a valid JSON text passed to the target queue.

    Default:
        the entire CloudWatch event

    Stability:
        stable
    """

    messageGroupId: str
    """Message Group ID for messages sent to this queue.

    Required for FIFO queues, leave empty for regular queues.

    Default:
        - no message group ID (regular queue)

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-events-targets.TaskEnvironmentVariable", jsii_struct_bases=[])
class TaskEnvironmentVariable(jsii.compat.TypedDict):
    """An environment variable to be set in the container run as a task.

    Stability:
        stable
    """
    name: str
    """Name for the environment variable.

    Exactly one of ``name`` and ``namePath`` must be specified.

    Stability:
        stable
    """

    value: str
    """Value of the environment variable.

    Exactly one of ``value`` and ``valuePath`` must be specified.

    Stability:
        stable
    """

__all__ = ["CodeBuildProject", "CodePipeline", "ContainerOverride", "EcsTask", "EcsTaskProps", "LambdaFunction", "LambdaFunctionProps", "SfnStateMachine", "SfnStateMachineProps", "SnsTopic", "SnsTopicProps", "SqsQueue", "SqsQueueProps", "TaskEnvironmentVariable", "__jsii_assembly__"]

publication.publish()
