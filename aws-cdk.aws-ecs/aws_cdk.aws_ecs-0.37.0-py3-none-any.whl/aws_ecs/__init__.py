import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_autoscaling
import aws_cdk.aws_autoscaling_hooktargets
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudformation
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_route53
import aws_cdk.aws_route53_targets
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_servicediscovery
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_ssm
import aws_cdk.core
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs", "0.37.0", __name__, "aws-ecs@0.37.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddAutoScalingGroupCapacityOptions", jsii_struct_bases=[])
class AddAutoScalingGroupCapacityOptions(jsii.compat.TypedDict, total=False):
    """The properties for adding an AutoScalingGroup.

    Stability:
        stable
    """
    canContainersAccessInstanceRole: bool
    """Specifies whether the containers can access the container instance role.

    Default:
        false

    Stability:
        stable
    """

    taskDrainTime: aws_cdk.core.Duration
    """The time period to wait before force terminating an instance that is draining.

    This creates a Lambda function that is used by a lifecycle hook for the
    AutoScalingGroup that will delay instance termination until all ECS tasks
    have drained from the instance. Set to 0 to disable task draining.

    Set to 0 to disable task draining.

    Default:
        Duration.minutes(5)

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[AddAutoScalingGroupCapacityOptions, aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps])
class _AddCapacityOptions(AddAutoScalingGroupCapacityOptions, aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps, jsii.compat.TypedDict, total=False):
    machineImage: aws_cdk.aws_ec2.IMachineImage
    """The ECS-optimized AMI variant to use.

    For more information, see Amazon ECS-optimized AMIs:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html]

    Default:
        - Amazon Linux 2

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AddCapacityOptions", jsii_struct_bases=[_AddCapacityOptions])
class AddCapacityOptions(_AddCapacityOptions):
    """The properties for adding instance capacity to an AutoScalingGroup.

    Stability:
        stable
    """
    instanceType: aws_cdk.aws_ec2.InstanceType
    """The EC2 instance type to use when launching instances into the AutoScalingGroup.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.AmiHardwareType")
class AmiHardwareType(enum.Enum):
    """The ECS-optimized AMI variant to use.

    For more information, see Amazon ECS-optimized AMIs:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html].

    Stability:
        stable
    """
    STANDARD = "STANDARD"
    """Use the Amazon ECS-optimized Amazon Linux 2 AMI.

    Stability:
        stable
    """
    GPU = "GPU"
    """Use the Amazon ECS GPU-optimized AMI.

    Stability:
        stable
    """
    ARM = "ARM"
    """Use the Amazon ECS-optimized Amazon Linux 2 (arm64) AMI.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AssetImageProps", jsii_struct_bases=[])
class AssetImageProps(jsii.compat.TypedDict, total=False):
    """The properties for building an AssetImage.

    Stability:
        stable
    """
    buildArgs: typing.Mapping[str,str]
    """The arguments to pass to the ``docker build`` command.

    Default:
        none

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _AwsLogDriverProps(jsii.compat.TypedDict, total=False):
    datetimeFormat: str
    """This option defines a multiline start pattern in Python strftime format.

    A log message consists of a line that matches the pattern and any
    following lines that don’t match the pattern. Thus the matched line is
    the delimiter between log messages.

    Default:
        - No multiline matching.

    Stability:
        stable
    """
    logGroup: aws_cdk.aws_logs.ILogGroup
    """The log group to log to.

    Default:
        - A log group is automatically created.

    Stability:
        stable
    """
    logRetention: aws_cdk.aws_logs.RetentionDays
    """The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct.

    Default:
        - Logs never expire.

    Stability:
        stable
    """
    multilinePattern: str
    """This option defines a multiline start pattern using a regular expression.

    A log message consists of a line that matches the pattern and any
    following lines that don’t match the pattern. Thus the matched line is
    the delimiter between log messages.

    This option is ignored if datetimeFormat is also configured.

    Default:
        - No multiline matching.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.AwsLogDriverProps", jsii_struct_bases=[_AwsLogDriverProps])
class AwsLogDriverProps(_AwsLogDriverProps):
    """Specifies the awslogs log driver configuration options.

    Stability:
        stable
    """
    streamPrefix: str
    """Prefix for the log streams.

    The awslogs-stream-prefix option allows you to associate a log stream
    with the specified prefix, the container name, and the ID of the Amazon
    ECS task to which the container belongs. If you specify a prefix with
    this option, then the log stream takes the following format::

        prefix-name/container-name/ecs-task-id

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BaseServiceOptions(jsii.compat.TypedDict, total=False):
    cloudMapOptions: "CloudMapOptions"
    """The options for configuring an Amazon ECS service to use service discovery.

    Default:
        - AWS Cloud Map service discovery is not enabled.

    Stability:
        stable
    """
    desiredCount: jsii.Number
    """The desired number of instantiations of the task definition to keep running on the service.

    Default:
        1

    Stability:
        stable
    """
    healthCheckGracePeriod: aws_cdk.core.Duration
    """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

    Default:
        - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

    Stability:
        stable
    """
    maxHealthyPercent: jsii.Number
    """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

    Default:
        - 100 if daemon, otherwise 200

    Stability:
        stable
    """
    minHealthyPercent: jsii.Number
    """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

    Default:
        - 0 if daemon, otherwise 50

    Stability:
        stable
    """
    serviceName: str
    """The name of the service.

    Default:
        - CloudFormation-generated name.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseServiceOptions", jsii_struct_bases=[_BaseServiceOptions])
class BaseServiceOptions(_BaseServiceOptions):
    """The properties for the base Ec2Service or FargateService service.

    Stability:
        stable
    """
    cluster: "ICluster"
    """The name of the cluster that hosts the service.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.BaseServiceProps", jsii_struct_bases=[BaseServiceOptions])
class BaseServiceProps(BaseServiceOptions, jsii.compat.TypedDict):
    """Complete base service properties that are required to be supplied by the implementation of the BaseService class.

    Stability:
        stable
    """
    launchType: "LaunchType"
    """The launch type on which to run your service.

    Valid values are: LaunchType.ECS or LaunchType.FARGATE

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.BinPackResource")
class BinPackResource(enum.Enum):
    """Instance resource used for bin packing.

    Stability:
        stable
    """
    CPU = "CPU"
    """Fill up hosts' CPU allocations first.

    Stability:
        stable
    """
    MEMORY = "MEMORY"
    """Fill up hosts' memory allocations first.

    Stability:
        stable
    """

class BuiltInAttributes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.BuiltInAttributes"):
    """The built-in container instance attributes.

    Stability:
        stable
    """
    def __init__(self) -> None:
        jsii.create(BuiltInAttributes, self, [])

    @classproperty
    @jsii.member(jsii_name="AMI_ID")
    def AMI_ID(cls) -> str:
        """The AMI id the instance is using.

        Stability:
            stable
        """
        return jsii.sget(cls, "AMI_ID")

    @classproperty
    @jsii.member(jsii_name="AVAILABILITY_ZONE")
    def AVAILABILITY_ZONE(cls) -> str:
        """The AvailabilityZone where the instance is running in.

        Stability:
            stable
        """
        return jsii.sget(cls, "AVAILABILITY_ZONE")

    @classproperty
    @jsii.member(jsii_name="INSTANCE_ID")
    def INSTANCE_ID(cls) -> str:
        """The id of the instance.

        Stability:
            stable
        """
        return jsii.sget(cls, "INSTANCE_ID")

    @classproperty
    @jsii.member(jsii_name="INSTANCE_TYPE")
    def INSTANCE_TYPE(cls) -> str:
        """The EC2 instance type.

        Stability:
            stable
        """
        return jsii.sget(cls, "INSTANCE_TYPE")

    @classproperty
    @jsii.member(jsii_name="OS_TYPE")
    def OS_TYPE(cls) -> str:
        """The operating system of the instance.

        Either 'linux' or 'windows'.

        Stability:
            stable
        """
        return jsii.sget(cls, "OS_TYPE")


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Capability")
class Capability(enum.Enum):
    """A Linux capability.

    Stability:
        stable
    """
    ALL = "ALL"
    """
    Stability:
        stable
    """
    AUDIT_CONTROL = "AUDIT_CONTROL"
    """
    Stability:
        stable
    """
    AUDIT_WRITE = "AUDIT_WRITE"
    """
    Stability:
        stable
    """
    BLOCK_SUSPEND = "BLOCK_SUSPEND"
    """
    Stability:
        stable
    """
    CHOWN = "CHOWN"
    """
    Stability:
        stable
    """
    DAC_OVERRIDE = "DAC_OVERRIDE"
    """
    Stability:
        stable
    """
    DAC_READ_SEARCH = "DAC_READ_SEARCH"
    """
    Stability:
        stable
    """
    FOWNER = "FOWNER"
    """
    Stability:
        stable
    """
    FSETID = "FSETID"
    """
    Stability:
        stable
    """
    IPC_LOCK = "IPC_LOCK"
    """
    Stability:
        stable
    """
    IPC_OWNER = "IPC_OWNER"
    """
    Stability:
        stable
    """
    KILL = "KILL"
    """
    Stability:
        stable
    """
    LEASE = "LEASE"
    """
    Stability:
        stable
    """
    LINUX_IMMUTABLE = "LINUX_IMMUTABLE"
    """
    Stability:
        stable
    """
    MAC_ADMIN = "MAC_ADMIN"
    """
    Stability:
        stable
    """
    MAC_OVERRIDE = "MAC_OVERRIDE"
    """
    Stability:
        stable
    """
    MKNOD = "MKNOD"
    """
    Stability:
        stable
    """
    NET_ADMIN = "NET_ADMIN"
    """
    Stability:
        stable
    """
    NET_BIND_SERVICE = "NET_BIND_SERVICE"
    """
    Stability:
        stable
    """
    NET_BROADCAST = "NET_BROADCAST"
    """
    Stability:
        stable
    """
    NET_RAW = "NET_RAW"
    """
    Stability:
        stable
    """
    SETFCAP = "SETFCAP"
    """
    Stability:
        stable
    """
    SETGID = "SETGID"
    """
    Stability:
        stable
    """
    SETPCAP = "SETPCAP"
    """
    Stability:
        stable
    """
    SETUID = "SETUID"
    """
    Stability:
        stable
    """
    SYS_ADMIN = "SYS_ADMIN"
    """
    Stability:
        stable
    """
    SYS_BOOT = "SYS_BOOT"
    """
    Stability:
        stable
    """
    SYS_CHROOT = "SYS_CHROOT"
    """
    Stability:
        stable
    """
    SYS_MODULE = "SYS_MODULE"
    """
    Stability:
        stable
    """
    SYS_NICE = "SYS_NICE"
    """
    Stability:
        stable
    """
    SYS_PACCT = "SYS_PACCT"
    """
    Stability:
        stable
    """
    SYS_PTRACE = "SYS_PTRACE"
    """
    Stability:
        stable
    """
    SYS_RAWIO = "SYS_RAWIO"
    """
    Stability:
        stable
    """
    SYS_RESOURCE = "SYS_RESOURCE"
    """
    Stability:
        stable
    """
    SYS_TIME = "SYS_TIME"
    """
    Stability:
        stable
    """
    SYS_TTY_CONFIG = "SYS_TTY_CONFIG"
    """
    Stability:
        stable
    """
    SYSLOG = "SYSLOG"
    """
    Stability:
        stable
    """
    WAKE_ALARM = "WAKE_ALARM"
    """
    Stability:
        stable
    """

class CfnCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnCluster"):
    """A CloudFormation ``AWS::ECS::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
    Stability:
        stable
    cloudformationResource:
        AWS::ECS::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ECS::Cluster``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            cluster_name: ``AWS::ECS::Cluster.ClusterName``.
            tags: ``AWS::ECS::Cluster.Tags``.

        Stability:
            stable
        """
        props: CfnClusterProps = {}

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "attrArn")

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
        """``AWS::ECS::Cluster.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Cluster.ClusterName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
        Stability:
            stable
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[str]):
        return jsii.set(self, "clusterName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnClusterProps", jsii_struct_bases=[])
class CfnClusterProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ECS::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
    Stability:
        stable
    """
    clusterName: str
    """``AWS::ECS::Cluster.ClusterName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
    Stability:
        stable
    """

    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::ECS::Cluster.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
    Stability:
        stable
    """

class CfnService(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnService"):
    """A CloudFormation ``AWS::ECS::Service``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
    Stability:
        stable
    cloudformationResource:
        AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: str, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union[typing.Optional["DeploymentConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["LoadBalancerProperty", aws_cdk.core.IResolvable]]]]]=None, network_configuration: typing.Optional[typing.Union[typing.Optional["NetworkConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementConstraintProperty", aws_cdk.core.IResolvable]]]]]=None, placement_strategies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementStrategyProperty", aws_cdk.core.IResolvable]]]]]=None, platform_version: typing.Optional[str]=None, propagate_tags: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ServiceRegistryProperty", aws_cdk.core.IResolvable]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::ECS::Service``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            task_definition: ``AWS::ECS::Service.TaskDefinition``.
            cluster: ``AWS::ECS::Service.Cluster``.
            deployment_configuration: ``AWS::ECS::Service.DeploymentConfiguration``.
            desired_count: ``AWS::ECS::Service.DesiredCount``.
            enable_ecs_managed_tags: ``AWS::ECS::Service.EnableECSManagedTags``.
            health_check_grace_period_seconds: ``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.
            launch_type: ``AWS::ECS::Service.LaunchType``.
            load_balancers: ``AWS::ECS::Service.LoadBalancers``.
            network_configuration: ``AWS::ECS::Service.NetworkConfiguration``.
            placement_constraints: ``AWS::ECS::Service.PlacementConstraints``.
            placement_strategies: ``AWS::ECS::Service.PlacementStrategies``.
            platform_version: ``AWS::ECS::Service.PlatformVersion``.
            propagate_tags: ``AWS::ECS::Service.PropagateTags``.
            role: ``AWS::ECS::Service.Role``.
            scheduling_strategy: ``AWS::ECS::Service.SchedulingStrategy``.
            service_name: ``AWS::ECS::Service.ServiceName``.
            service_registries: ``AWS::ECS::Service.ServiceRegistries``.
            tags: ``AWS::ECS::Service.Tags``.

        Stability:
            stable
        """
        props: CfnServiceProps = {"taskDefinition": task_definition}

        if cluster is not None:
            props["cluster"] = cluster

        if deployment_configuration is not None:
            props["deploymentConfiguration"] = deployment_configuration

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if enable_ecs_managed_tags is not None:
            props["enableEcsManagedTags"] = enable_ecs_managed_tags

        if health_check_grace_period_seconds is not None:
            props["healthCheckGracePeriodSeconds"] = health_check_grace_period_seconds

        if launch_type is not None:
            props["launchType"] = launch_type

        if load_balancers is not None:
            props["loadBalancers"] = load_balancers

        if network_configuration is not None:
            props["networkConfiguration"] = network_configuration

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if placement_strategies is not None:
            props["placementStrategies"] = placement_strategies

        if platform_version is not None:
            props["platformVersion"] = platform_version

        if propagate_tags is not None:
            props["propagateTags"] = propagate_tags

        if role is not None:
            props["role"] = role

        if scheduling_strategy is not None:
            props["schedulingStrategy"] = scheduling_strategy

        if service_name is not None:
            props["serviceName"] = service_name

        if service_registries is not None:
            props["serviceRegistries"] = service_registries

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnService, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        Stability:
            stable
        cloudformationAttribute:
            Name
        """
        return jsii.get(self, "attrName")

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
        """``AWS::ECS::Service.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> str:
        """``AWS::ECS::Service.TaskDefinition``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
        Stability:
            stable
        """
        return jsii.get(self, "taskDefinition")

    @task_definition.setter
    def task_definition(self, value: str):
        return jsii.set(self, "taskDefinition", value)

    @property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Cluster``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
        Stability:
            stable
        """
        return jsii.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: typing.Optional[str]):
        return jsii.set(self, "cluster", value)

    @property
    @jsii.member(jsii_name="deploymentConfiguration")
    def deployment_configuration(self) -> typing.Optional[typing.Union[typing.Optional["DeploymentConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECS::Service.DeploymentConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "deploymentConfiguration")

    @deployment_configuration.setter
    def deployment_configuration(self, value: typing.Optional[typing.Union[typing.Optional["DeploymentConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "deploymentConfiguration", value)

    @property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.DesiredCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
        Stability:
            stable
        """
        return jsii.get(self, "desiredCount")

    @desired_count.setter
    def desired_count(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "desiredCount", value)

    @property
    @jsii.member(jsii_name="enableEcsManagedTags")
    def enable_ecs_managed_tags(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECS::Service.EnableECSManagedTags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
        Stability:
            stable
        """
        return jsii.get(self, "enableEcsManagedTags")

    @enable_ecs_managed_tags.setter
    def enable_ecs_managed_tags(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "enableEcsManagedTags", value)

    @property
    @jsii.member(jsii_name="healthCheckGracePeriodSeconds")
    def health_check_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
        Stability:
            stable
        """
        return jsii.get(self, "healthCheckGracePeriodSeconds")

    @health_check_grace_period_seconds.setter
    def health_check_grace_period_seconds(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "healthCheckGracePeriodSeconds", value)

    @property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.LaunchType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
        Stability:
            stable
        """
        return jsii.get(self, "launchType")

    @launch_type.setter
    def launch_type(self, value: typing.Optional[str]):
        return jsii.set(self, "launchType", value)

    @property
    @jsii.member(jsii_name="loadBalancers")
    def load_balancers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["LoadBalancerProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::Service.LoadBalancers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
        Stability:
            stable
        """
        return jsii.get(self, "loadBalancers")

    @load_balancers.setter
    def load_balancers(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["LoadBalancerProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "loadBalancers", value)

    @property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(self) -> typing.Optional[typing.Union[typing.Optional["NetworkConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::ECS::Service.NetworkConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "networkConfiguration")

    @network_configuration.setter
    def network_configuration(self, value: typing.Optional[typing.Union[typing.Optional["NetworkConfigurationProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "networkConfiguration", value)

    @property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementConstraintProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::Service.PlacementConstraints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
        Stability:
            stable
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementConstraintProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "placementConstraints", value)

    @property
    @jsii.member(jsii_name="placementStrategies")
    def placement_strategies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementStrategyProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::Service.PlacementStrategies``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
        Stability:
            stable
        """
        return jsii.get(self, "placementStrategies")

    @placement_strategies.setter
    def placement_strategies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["PlacementStrategyProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "placementStrategies", value)

    @property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PlatformVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
        Stability:
            stable
        """
        return jsii.get(self, "platformVersion")

    @platform_version.setter
    def platform_version(self, value: typing.Optional[str]):
        return jsii.set(self, "platformVersion", value)

    @property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PropagateTags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
        Stability:
            stable
        """
        return jsii.get(self, "propagateTags")

    @propagate_tags.setter
    def propagate_tags(self, value: typing.Optional[str]):
        return jsii.set(self, "propagateTags", value)

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Role``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
        Stability:
            stable
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: typing.Optional[str]):
        return jsii.set(self, "role", value)

    @property
    @jsii.member(jsii_name="schedulingStrategy")
    def scheduling_strategy(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.SchedulingStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
        Stability:
            stable
        """
        return jsii.get(self, "schedulingStrategy")

    @scheduling_strategy.setter
    def scheduling_strategy(self, value: typing.Optional[str]):
        return jsii.set(self, "schedulingStrategy", value)

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.ServiceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
        Stability:
            stable
        """
        return jsii.get(self, "serviceName")

    @service_name.setter
    def service_name(self, value: typing.Optional[str]):
        return jsii.set(self, "serviceName", value)

    @property
    @jsii.member(jsii_name="serviceRegistries")
    def service_registries(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ServiceRegistryProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::Service.ServiceRegistries``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
        Stability:
            stable
        """
        return jsii.get(self, "serviceRegistries")

    @service_registries.setter
    def service_registries(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ServiceRegistryProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "serviceRegistries", value)

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AwsVpcConfigurationProperty(jsii.compat.TypedDict, total=False):
        assignPublicIp: str
        """``CfnService.AwsVpcConfigurationProperty.AssignPublicIp``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-assignpublicip
        Stability:
            stable
        """
        securityGroups: typing.List[str]
        """``CfnService.AwsVpcConfigurationProperty.SecurityGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-securitygroups
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.AwsVpcConfigurationProperty", jsii_struct_bases=[_AwsVpcConfigurationProperty])
    class AwsVpcConfigurationProperty(_AwsVpcConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html
        Stability:
            stable
        """
        subnets: typing.List[str]
        """``CfnService.AwsVpcConfigurationProperty.Subnets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-subnets
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.DeploymentConfigurationProperty", jsii_struct_bases=[])
    class DeploymentConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html
        Stability:
            stable
        """
        maximumPercent: jsii.Number
        """``CfnService.DeploymentConfigurationProperty.MaximumPercent``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-maximumpercent
        Stability:
            stable
        """

        minimumHealthyPercent: jsii.Number
        """``CfnService.DeploymentConfigurationProperty.MinimumHealthyPercent``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-minimumhealthypercent
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LoadBalancerProperty(jsii.compat.TypedDict, total=False):
        containerName: str
        """``CfnService.LoadBalancerProperty.ContainerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containername
        Stability:
            stable
        """
        loadBalancerName: str
        """``CfnService.LoadBalancerProperty.LoadBalancerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-loadbalancername
        Stability:
            stable
        """
        targetGroupArn: str
        """``CfnService.LoadBalancerProperty.TargetGroupArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-targetgrouparn
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.LoadBalancerProperty", jsii_struct_bases=[_LoadBalancerProperty])
    class LoadBalancerProperty(_LoadBalancerProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html
        Stability:
            stable
        """
        containerPort: jsii.Number
        """``CfnService.LoadBalancerProperty.ContainerPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containerport
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.NetworkConfigurationProperty", jsii_struct_bases=[])
    class NetworkConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html
        Stability:
            stable
        """
        awsvpcConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnService.AwsVpcConfigurationProperty"]
        """``CfnService.NetworkConfigurationProperty.AwsvpcConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html#cfn-ecs-service-networkconfiguration-awsvpcconfiguration
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _PlacementConstraintProperty(jsii.compat.TypedDict, total=False):
        expression: str
        """``CfnService.PlacementConstraintProperty.Expression``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-expression
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementConstraintProperty", jsii_struct_bases=[_PlacementConstraintProperty])
    class PlacementConstraintProperty(_PlacementConstraintProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html
        Stability:
            stable
        """
        type: str
        """``CfnService.PlacementConstraintProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-type
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _PlacementStrategyProperty(jsii.compat.TypedDict, total=False):
        field: str
        """``CfnService.PlacementStrategyProperty.Field``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-field
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.PlacementStrategyProperty", jsii_struct_bases=[_PlacementStrategyProperty])
    class PlacementStrategyProperty(_PlacementStrategyProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html
        Stability:
            stable
        """
        type: str
        """``CfnService.PlacementStrategyProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-type
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnService.ServiceRegistryProperty", jsii_struct_bases=[])
    class ServiceRegistryProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html
        Stability:
            stable
        """
        containerName: str
        """``CfnService.ServiceRegistryProperty.ContainerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containername
        Stability:
            stable
        """

        containerPort: jsii.Number
        """``CfnService.ServiceRegistryProperty.ContainerPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containerport
        Stability:
            stable
        """

        port: jsii.Number
        """``CfnService.ServiceRegistryProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-port
        Stability:
            stable
        """

        registryArn: str
        """``CfnService.ServiceRegistryProperty.RegistryArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-registryarn
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnServiceProps(jsii.compat.TypedDict, total=False):
    cluster: str
    """``AWS::ECS::Service.Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
    Stability:
        stable
    """
    deploymentConfiguration: typing.Union["CfnService.DeploymentConfigurationProperty", aws_cdk.core.IResolvable]
    """``AWS::ECS::Service.DeploymentConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
    Stability:
        stable
    """
    desiredCount: jsii.Number
    """``AWS::ECS::Service.DesiredCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
    Stability:
        stable
    """
    enableEcsManagedTags: typing.Union[bool, aws_cdk.core.IResolvable]
    """``AWS::ECS::Service.EnableECSManagedTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
    Stability:
        stable
    """
    healthCheckGracePeriodSeconds: jsii.Number
    """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
    Stability:
        stable
    """
    launchType: str
    """``AWS::ECS::Service.LaunchType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
    Stability:
        stable
    """
    loadBalancers: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnService.LoadBalancerProperty", aws_cdk.core.IResolvable]]]
    """``AWS::ECS::Service.LoadBalancers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
    Stability:
        stable
    """
    networkConfiguration: typing.Union["CfnService.NetworkConfigurationProperty", aws_cdk.core.IResolvable]
    """``AWS::ECS::Service.NetworkConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
    Stability:
        stable
    """
    placementConstraints: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnService.PlacementConstraintProperty", aws_cdk.core.IResolvable]]]
    """``AWS::ECS::Service.PlacementConstraints``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
    Stability:
        stable
    """
    placementStrategies: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnService.PlacementStrategyProperty", aws_cdk.core.IResolvable]]]
    """``AWS::ECS::Service.PlacementStrategies``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
    Stability:
        stable
    """
    platformVersion: str
    """``AWS::ECS::Service.PlatformVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
    Stability:
        stable
    """
    propagateTags: str
    """``AWS::ECS::Service.PropagateTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
    Stability:
        stable
    """
    role: str
    """``AWS::ECS::Service.Role``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
    Stability:
        stable
    """
    schedulingStrategy: str
    """``AWS::ECS::Service.SchedulingStrategy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
    Stability:
        stable
    """
    serviceName: str
    """``AWS::ECS::Service.ServiceName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
    Stability:
        stable
    """
    serviceRegistries: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnService.ServiceRegistryProperty", aws_cdk.core.IResolvable]]]
    """``AWS::ECS::Service.ServiceRegistries``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
    Stability:
        stable
    """
    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::ECS::Service.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnServiceProps", jsii_struct_bases=[_CfnServiceProps])
class CfnServiceProps(_CfnServiceProps):
    """Properties for defining a ``AWS::ECS::Service``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
    Stability:
        stable
    """
    taskDefinition: str
    """``AWS::ECS::Service.TaskDefinition``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
    Stability:
        stable
    """

class CfnTaskDefinition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition"):
    """A CloudFormation ``AWS::ECS::TaskDefinition``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
    Stability:
        stable
    cloudformationResource:
        AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, container_definitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]=None, proxy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]=None) -> None:
        """Create a new ``AWS::ECS::TaskDefinition``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            container_definitions: ``AWS::ECS::TaskDefinition.ContainerDefinitions``.
            cpu: ``AWS::ECS::TaskDefinition.Cpu``.
            execution_role_arn: ``AWS::ECS::TaskDefinition.ExecutionRoleArn``.
            family: ``AWS::ECS::TaskDefinition.Family``.
            memory: ``AWS::ECS::TaskDefinition.Memory``.
            network_mode: ``AWS::ECS::TaskDefinition.NetworkMode``.
            placement_constraints: ``AWS::ECS::TaskDefinition.PlacementConstraints``.
            proxy_configuration: ``AWS::ECS::TaskDefinition.ProxyConfiguration``.
            requires_compatibilities: ``AWS::ECS::TaskDefinition.RequiresCompatibilities``.
            tags: ``AWS::ECS::TaskDefinition.Tags``.
            task_role_arn: ``AWS::ECS::TaskDefinition.TaskRoleArn``.
            volumes: ``AWS::ECS::TaskDefinition.Volumes``.

        Stability:
            stable
        """
        props: CfnTaskDefinitionProps = {}

        if container_definitions is not None:
            props["containerDefinitions"] = container_definitions

        if cpu is not None:
            props["cpu"] = cpu

        if execution_role_arn is not None:
            props["executionRoleArn"] = execution_role_arn

        if family is not None:
            props["family"] = family

        if memory is not None:
            props["memory"] = memory

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if proxy_configuration is not None:
            props["proxyConfiguration"] = proxy_configuration

        if requires_compatibilities is not None:
            props["requiresCompatibilities"] = requires_compatibilities

        if tags is not None:
            props["tags"] = tags

        if task_role_arn is not None:
            props["taskRoleArn"] = task_role_arn

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnTaskDefinition, self, [scope, id, props])

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
        """``AWS::ECS::TaskDefinition.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="containerDefinitions")
    def container_definitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]:
        """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
        Stability:
            stable
        """
        return jsii.get(self, "containerDefinitions")

    @container_definitions.setter
    def container_definitions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union["ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]]]):
        return jsii.set(self, "containerDefinitions", value)

    @property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Cpu``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
        Stability:
            stable
        """
        return jsii.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: typing.Optional[str]):
        return jsii.set(self, "cpu", value)

    @property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
        Stability:
            stable
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "executionRoleArn", value)

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Family``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
        Stability:
            stable
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: typing.Optional[str]):
        return jsii.set(self, "family", value)

    @property
    @jsii.member(jsii_name="memory")
    def memory(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Memory``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
        Stability:
            stable
        """
        return jsii.get(self, "memory")

    @memory.setter
    def memory(self, value: typing.Optional[str]):
        return jsii.set(self, "memory", value)

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.NetworkMode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
        Stability:
            stable
        """
        return jsii.get(self, "networkMode")

    @network_mode.setter
    def network_mode(self, value: typing.Optional[str]):
        return jsii.set(self, "networkMode", value)

    @property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.PlacementConstraints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
        Stability:
            stable
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TaskDefinitionPlacementConstraintProperty"]]]]]):
        return jsii.set(self, "placementConstraints", value)

    @property
    @jsii.member(jsii_name="proxyConfiguration")
    def proxy_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]:
        """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
        Stability:
            stable
        """
        return jsii.get(self, "proxyConfiguration")

    @proxy_configuration.setter
    def proxy_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ProxyConfigurationProperty"]]]):
        return jsii.set(self, "proxyConfiguration", value)

    @property
    @jsii.member(jsii_name="requiresCompatibilities")
    def requires_compatibilities(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
        Stability:
            stable
        """
        return jsii.get(self, "requiresCompatibilities")

    @requires_compatibilities.setter
    def requires_compatibilities(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "requiresCompatibilities", value)

    @property
    @jsii.member(jsii_name="taskRoleArn")
    def task_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.TaskRoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
        Stability:
            stable
        """
        return jsii.get(self, "taskRoleArn")

    @task_role_arn.setter
    def task_role_arn(self, value: typing.Optional[str]):
        return jsii.set(self, "taskRoleArn", value)

    @property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]:
        """``AWS::ECS::TaskDefinition.Volumes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
        Stability:
            stable
        """
        return jsii.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "VolumeProperty"]]]]]):
        return jsii.set(self, "volumes", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ContainerDefinitionProperty", jsii_struct_bases=[])
    class ContainerDefinitionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html
        Stability:
            stable
        """
        command: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Command``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-command
        Stability:
            stable
        """

        cpu: jsii.Number
        """``CfnTaskDefinition.ContainerDefinitionProperty.Cpu``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-cpu
        Stability:
            stable
        """

        dependsOn: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ContainerDependencyProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DependsOn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dependson
        Stability:
            stable
        """

        disableNetworking: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DisableNetworking``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-disablenetworking
        Stability:
            stable
        """

        dnsSearchDomains: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DnsSearchDomains``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnssearchdomains
        Stability:
            stable
        """

        dnsServers: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DnsServers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnsservers
        Stability:
            stable
        """

        dockerLabels: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DockerLabels``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockerlabels
        Stability:
            stable
        """

        dockerSecurityOptions: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.DockerSecurityOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockersecurityoptions
        Stability:
            stable
        """

        entryPoint: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.EntryPoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-entrypoint
        Stability:
            stable
        """

        environment: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Environment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-environment
        Stability:
            stable
        """

        essential: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Essential``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-essential
        Stability:
            stable
        """

        extraHosts: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.HostEntryProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.ExtraHosts``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-extrahosts
        Stability:
            stable
        """

        healthCheck: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.HealthCheckProperty"]
        """``CfnTaskDefinition.ContainerDefinitionProperty.HealthCheck``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-healthcheck
        Stability:
            stable
        """

        hostname: str
        """``CfnTaskDefinition.ContainerDefinitionProperty.Hostname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-hostname
        Stability:
            stable
        """

        image: str
        """``CfnTaskDefinition.ContainerDefinitionProperty.Image``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-image
        Stability:
            stable
        """

        links: typing.List[str]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Links``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-links
        Stability:
            stable
        """

        linuxParameters: typing.Union["CfnTaskDefinition.LinuxParametersProperty", aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.LinuxParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-linuxparameters
        Stability:
            stable
        """

        logConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.LogConfigurationProperty"]
        """``CfnTaskDefinition.ContainerDefinitionProperty.LogConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration
        Stability:
            stable
        """

        memory: jsii.Number
        """``CfnTaskDefinition.ContainerDefinitionProperty.Memory``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memory
        Stability:
            stable
        """

        memoryReservation: jsii.Number
        """``CfnTaskDefinition.ContainerDefinitionProperty.MemoryReservation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memoryreservation
        Stability:
            stable
        """

        mountPoints: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.MountPointProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.MountPoints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints
        Stability:
            stable
        """

        name: str
        """``CfnTaskDefinition.ContainerDefinitionProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-name
        Stability:
            stable
        """

        portMappings: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.PortMappingProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.PortMappings``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-portmappings
        Stability:
            stable
        """

        privileged: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Privileged``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-privileged
        Stability:
            stable
        """

        readonlyRootFilesystem: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.ReadonlyRootFilesystem``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-readonlyrootfilesystem
        Stability:
            stable
        """

        repositoryCredentials: typing.Union["CfnTaskDefinition.RepositoryCredentialsProperty", aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.ContainerDefinitionProperty.RepositoryCredentials``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-repositorycredentials
        Stability:
            stable
        """

        resourceRequirements: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ResourceRequirementProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.ResourceRequirements``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-resourcerequirements
        Stability:
            stable
        """

        secrets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.SecretProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Secrets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-secrets
        Stability:
            stable
        """

        startTimeout: jsii.Number
        """``CfnTaskDefinition.ContainerDefinitionProperty.StartTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-starttimeout
        Stability:
            stable
        """

        stopTimeout: jsii.Number
        """``CfnTaskDefinition.ContainerDefinitionProperty.StopTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-stoptimeout
        Stability:
            stable
        """

        ulimits: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.UlimitProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.Ulimits``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-ulimits
        Stability:
            stable
        """

        user: str
        """``CfnTaskDefinition.ContainerDefinitionProperty.User``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-user
        Stability:
            stable
        """

        volumesFrom: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeFromProperty"]]]
        """``CfnTaskDefinition.ContainerDefinitionProperty.VolumesFrom``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom
        Stability:
            stable
        """

        workingDirectory: str
        """``CfnTaskDefinition.ContainerDefinitionProperty.WorkingDirectory``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-workingdirectory
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ContainerDependencyProperty", jsii_struct_bases=[])
    class ContainerDependencyProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html
        Stability:
            stable
        """
        condition: str
        """``CfnTaskDefinition.ContainerDependencyProperty.Condition``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-condition
        Stability:
            stable
        """

        containerName: str
        """``CfnTaskDefinition.ContainerDependencyProperty.ContainerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-containername
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DeviceProperty(jsii.compat.TypedDict, total=False):
        containerPath: str
        """``CfnTaskDefinition.DeviceProperty.ContainerPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-containerpath
        Stability:
            stable
        """
        permissions: typing.List[str]
        """``CfnTaskDefinition.DeviceProperty.Permissions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-permissions
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DeviceProperty", jsii_struct_bases=[_DeviceProperty])
    class DeviceProperty(_DeviceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html
        Stability:
            stable
        """
        hostPath: str
        """``CfnTaskDefinition.DeviceProperty.HostPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-hostpath
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.DockerVolumeConfigurationProperty", jsii_struct_bases=[])
    class DockerVolumeConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html
        Stability:
            stable
        """
        autoprovision: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Autoprovision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-autoprovision
        Stability:
            stable
        """

        driver: str
        """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Driver``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driver
        Stability:
            stable
        """

        driverOpts: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnTaskDefinition.DockerVolumeConfigurationProperty.DriverOpts``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driveropts
        Stability:
            stable
        """

        labels: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Labels``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-labels
        Stability:
            stable
        """

        scope: str
        """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-scope
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _HealthCheckProperty(jsii.compat.TypedDict, total=False):
        interval: jsii.Number
        """``CfnTaskDefinition.HealthCheckProperty.Interval``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-interval
        Stability:
            stable
        """
        retries: jsii.Number
        """``CfnTaskDefinition.HealthCheckProperty.Retries``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-retries
        Stability:
            stable
        """
        startPeriod: jsii.Number
        """``CfnTaskDefinition.HealthCheckProperty.StartPeriod``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-startperiod
        Stability:
            stable
        """
        timeout: jsii.Number
        """``CfnTaskDefinition.HealthCheckProperty.Timeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-timeout
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HealthCheckProperty", jsii_struct_bases=[_HealthCheckProperty])
    class HealthCheckProperty(_HealthCheckProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html
        Stability:
            stable
        """
        command: typing.List[str]
        """``CfnTaskDefinition.HealthCheckProperty.Command``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-command
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostEntryProperty", jsii_struct_bases=[])
    class HostEntryProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html
        Stability:
            stable
        """
        hostname: str
        """``CfnTaskDefinition.HostEntryProperty.Hostname``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-hostname
        Stability:
            stable
        """

        ipAddress: str
        """``CfnTaskDefinition.HostEntryProperty.IpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-ipaddress
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.HostVolumePropertiesProperty", jsii_struct_bases=[])
    class HostVolumePropertiesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html
        Stability:
            stable
        """
        sourcePath: str
        """``CfnTaskDefinition.HostVolumePropertiesProperty.SourcePath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html#cfn-ecs-taskdefinition-volumes-host-sourcepath
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KernelCapabilitiesProperty", jsii_struct_bases=[])
    class KernelCapabilitiesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html
        Stability:
            stable
        """
        add: typing.List[str]
        """``CfnTaskDefinition.KernelCapabilitiesProperty.Add``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-add
        Stability:
            stable
        """

        drop: typing.List[str]
        """``CfnTaskDefinition.KernelCapabilitiesProperty.Drop``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-drop
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.KeyValuePairProperty", jsii_struct_bases=[])
    class KeyValuePairProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html
        Stability:
            stable
        """
        name: str
        """``CfnTaskDefinition.KeyValuePairProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-name
        Stability:
            stable
        """

        value: str
        """``CfnTaskDefinition.KeyValuePairProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-value
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LinuxParametersProperty", jsii_struct_bases=[])
    class LinuxParametersProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html
        Stability:
            stable
        """
        capabilities: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KernelCapabilitiesProperty"]
        """``CfnTaskDefinition.LinuxParametersProperty.Capabilities``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-capabilities
        Stability:
            stable
        """

        devices: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.DeviceProperty"]]]
        """``CfnTaskDefinition.LinuxParametersProperty.Devices``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-devices
        Stability:
            stable
        """

        initProcessEnabled: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.LinuxParametersProperty.InitProcessEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-initprocessenabled
        Stability:
            stable
        """

        sharedMemorySize: jsii.Number
        """``CfnTaskDefinition.LinuxParametersProperty.SharedMemorySize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-sharedmemorysize
        Stability:
            stable
        """

        tmpfs: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TmpfsProperty"]]]
        """``CfnTaskDefinition.LinuxParametersProperty.Tmpfs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-tmpfs
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LogConfigurationProperty(jsii.compat.TypedDict, total=False):
        options: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[str,str]]
        """``CfnTaskDefinition.LogConfigurationProperty.Options``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-options
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.LogConfigurationProperty", jsii_struct_bases=[_LogConfigurationProperty])
    class LogConfigurationProperty(_LogConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html
        Stability:
            stable
        """
        logDriver: str
        """``CfnTaskDefinition.LogConfigurationProperty.LogDriver``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-logdriver
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.MountPointProperty", jsii_struct_bases=[])
    class MountPointProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html
        Stability:
            stable
        """
        containerPath: str
        """``CfnTaskDefinition.MountPointProperty.ContainerPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-containerpath
        Stability:
            stable
        """

        readOnly: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.MountPointProperty.ReadOnly``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-readonly
        Stability:
            stable
        """

        sourceVolume: str
        """``CfnTaskDefinition.MountPointProperty.SourceVolume``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-sourcevolume
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.PortMappingProperty", jsii_struct_bases=[])
    class PortMappingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html
        Stability:
            stable
        """
        containerPort: jsii.Number
        """``CfnTaskDefinition.PortMappingProperty.ContainerPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-containerport
        Stability:
            stable
        """

        hostPort: jsii.Number
        """``CfnTaskDefinition.PortMappingProperty.HostPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-readonly
        Stability:
            stable
        """

        protocol: str
        """``CfnTaskDefinition.PortMappingProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-sourcevolume
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ProxyConfigurationProperty(jsii.compat.TypedDict, total=False):
        proxyConfigurationProperties: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.KeyValuePairProperty"]]]
        """``CfnTaskDefinition.ProxyConfigurationProperty.ProxyConfigurationProperties``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-proxyconfigurationproperties
        Stability:
            stable
        """
        type: str
        """``CfnTaskDefinition.ProxyConfigurationProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-type
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ProxyConfigurationProperty", jsii_struct_bases=[_ProxyConfigurationProperty])
    class ProxyConfigurationProperty(_ProxyConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html
        Stability:
            stable
        """
        containerName: str
        """``CfnTaskDefinition.ProxyConfigurationProperty.ContainerName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-containername
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.RepositoryCredentialsProperty", jsii_struct_bases=[])
    class RepositoryCredentialsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html
        Stability:
            stable
        """
        credentialsParameter: str
        """``CfnTaskDefinition.RepositoryCredentialsProperty.CredentialsParameter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html#cfn-ecs-taskdefinition-repositorycredentials-credentialsparameter
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.ResourceRequirementProperty", jsii_struct_bases=[])
    class ResourceRequirementProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html
        Stability:
            stable
        """
        type: str
        """``CfnTaskDefinition.ResourceRequirementProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-type
        Stability:
            stable
        """

        value: str
        """``CfnTaskDefinition.ResourceRequirementProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-value
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.SecretProperty", jsii_struct_bases=[])
    class SecretProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html
        Stability:
            stable
        """
        name: str
        """``CfnTaskDefinition.SecretProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-name
        Stability:
            stable
        """

        valueFrom: str
        """``CfnTaskDefinition.SecretProperty.ValueFrom``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-valuefrom
        Stability:
            stable
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TaskDefinitionPlacementConstraintProperty(jsii.compat.TypedDict, total=False):
        expression: str
        """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Expression``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-expression
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty", jsii_struct_bases=[_TaskDefinitionPlacementConstraintProperty])
    class TaskDefinitionPlacementConstraintProperty(_TaskDefinitionPlacementConstraintProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html
        Stability:
            stable
        """
        type: str
        """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-type
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.TmpfsProperty", jsii_struct_bases=[])
    class TmpfsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html
        Stability:
            stable
        """
        containerPath: str
        """``CfnTaskDefinition.TmpfsProperty.ContainerPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-containerpath
        Stability:
            stable
        """

        mountOptions: typing.List[str]
        """``CfnTaskDefinition.TmpfsProperty.MountOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-mountoptions
        Stability:
            stable
        """

        size: jsii.Number
        """``CfnTaskDefinition.TmpfsProperty.Size``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-size
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.UlimitProperty", jsii_struct_bases=[])
    class UlimitProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html
        Stability:
            stable
        """
        hardLimit: jsii.Number
        """``CfnTaskDefinition.UlimitProperty.HardLimit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-hardlimit
        Stability:
            stable
        """

        name: str
        """``CfnTaskDefinition.UlimitProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-name
        Stability:
            stable
        """

        softLimit: jsii.Number
        """``CfnTaskDefinition.UlimitProperty.SoftLimit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-softlimit
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeFromProperty", jsii_struct_bases=[])
    class VolumeFromProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html
        Stability:
            stable
        """
        readOnly: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnTaskDefinition.VolumeFromProperty.ReadOnly``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-readonly
        Stability:
            stable
        """

        sourceContainer: str
        """``CfnTaskDefinition.VolumeFromProperty.SourceContainer``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-sourcecontainer
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinition.VolumeProperty", jsii_struct_bases=[])
    class VolumeProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html
        Stability:
            stable
        """
        dockerVolumeConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.DockerVolumeConfigurationProperty"]
        """``CfnTaskDefinition.VolumeProperty.DockerVolumeConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volume-dockervolumeconfiguration
        Stability:
            stable
        """

        host: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.HostVolumePropertiesProperty"]
        """``CfnTaskDefinition.VolumeProperty.Host``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-host
        Stability:
            stable
        """

        name: str
        """``CfnTaskDefinition.VolumeProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-name
        Stability:
            stable
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CfnTaskDefinitionProps", jsii_struct_bases=[])
class CfnTaskDefinitionProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::ECS::TaskDefinition``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
    Stability:
        stable
    """
    containerDefinitions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", aws_cdk.core.IResolvable]]]
    """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
    Stability:
        stable
    """

    cpu: str
    """``AWS::ECS::TaskDefinition.Cpu``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
    Stability:
        stable
    """

    executionRoleArn: str
    """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
    Stability:
        stable
    """

    family: str
    """``AWS::ECS::TaskDefinition.Family``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
    Stability:
        stable
    """

    memory: str
    """``AWS::ECS::TaskDefinition.Memory``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
    Stability:
        stable
    """

    networkMode: str
    """``AWS::ECS::TaskDefinition.NetworkMode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
    Stability:
        stable
    """

    placementConstraints: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty"]]]
    """``AWS::ECS::TaskDefinition.PlacementConstraints``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
    Stability:
        stable
    """

    proxyConfiguration: typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.ProxyConfigurationProperty"]
    """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
    Stability:
        stable
    """

    requiresCompatibilities: typing.List[str]
    """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
    Stability:
        stable
    """

    tags: typing.List[aws_cdk.core.CfnTag]
    """``AWS::ECS::TaskDefinition.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
    Stability:
        stable
    """

    taskRoleArn: str
    """``AWS::ECS::TaskDefinition.TaskRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
    Stability:
        stable
    """

    volumes: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTaskDefinition.VolumeProperty"]]]
    """``AWS::ECS::TaskDefinition.Volumes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CloudMapNamespaceOptions(jsii.compat.TypedDict, total=False):
    type: aws_cdk.aws_servicediscovery.NamespaceType
    """The type of CloudMap Namespace to create.

    Default:
        PrivateDns

    Stability:
        stable
    """
    vpc: aws_cdk.aws_ec2.IVpc
    """The VPC to associate the namespace with.

    This property is required for private DNS namespaces.

    Default:
        VPC of the cluster for Private DNS Namespace, otherwise none

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CloudMapNamespaceOptions", jsii_struct_bases=[_CloudMapNamespaceOptions])
class CloudMapNamespaceOptions(_CloudMapNamespaceOptions):
    """The options for creating an AWS Cloud Map namespace.

    Stability:
        stable
    """
    name: str
    """The name of the namespace, such as example.com.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CloudMapOptions", jsii_struct_bases=[])
class CloudMapOptions(jsii.compat.TypedDict, total=False):
    """The options to enabling AWS Cloud Map for an Amazon ECS service.

    Stability:
        stable
    """
    dnsRecordType: aws_cdk.aws_servicediscovery.DnsRecordType
    """The DNS record type that you want AWS Cloud Map to create.

    The supported record types are A or SRV.

    Default:
        : A

    Stability:
        stable
    """

    dnsTtl: aws_cdk.core.Duration
    """The amount of time that you want DNS resolvers to cache the settings for this record.

    Default:
        60

    Stability:
        stable
    """

    failureThreshold: jsii.Number
    """The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance.

    NOTE: This is used for HealthCheckCustomConfig

    Stability:
        stable
    """

    name: str
    """The name of the Cloud Map service to attach to the ECS service.

    Default:
        CloudFormation-generated name

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ClusterAttributes(jsii.compat.TypedDict, total=False):
    clusterArn: str
    """The Amazon Resource Name (ARN) that identifies the cluster.

    Default:
        Derived from clusterName

    Stability:
        stable
    """
    defaultCloudMapNamespace: aws_cdk.aws_servicediscovery.INamespace
    """The AWS Cloud Map namespace to associate with the cluster.

    Default:
        - No default namespace

    Stability:
        stable
    """
    hasEc2Capacity: bool
    """Specifies whether the cluster has EC2 instance capacity.

    Default:
        true

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterAttributes", jsii_struct_bases=[_ClusterAttributes])
class ClusterAttributes(_ClusterAttributes):
    """The properties to import from the ECS cluster.

    Stability:
        stable
    """
    clusterName: str
    """The name of the cluster.

    Stability:
        stable
    """

    securityGroups: typing.List[aws_cdk.aws_ec2.ISecurityGroup]
    """The security groups associated with the container instances registered to the cluster.

    Stability:
        stable
    """

    vpc: aws_cdk.aws_ec2.IVpc
    """The VPC associated with the cluster.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ClusterProps(jsii.compat.TypedDict, total=False):
    clusterName: str
    """The name for the cluster.

    Default:
        CloudFormation-generated name

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ClusterProps", jsii_struct_bases=[_ClusterProps])
class ClusterProps(_ClusterProps):
    """The properties used to define an ECS cluster.

    Stability:
        stable
    """
    vpc: aws_cdk.aws_ec2.IVpc
    """The VPC to associate with the cluster.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CommonTaskDefinitionProps", jsii_struct_bases=[])
class CommonTaskDefinitionProps(jsii.compat.TypedDict, total=False):
    """The common properties for all task definitions.

    For more information, see Task Definition Parameters:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html]

    Stability:
        stable
    """
    executionRole: aws_cdk.aws_iam.IRole
    """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

    The role will be used to retrieve container images from ECR and create CloudWatch log groups.

    Default:
        - An execution role will be automatically created if you use ECR images in your task definition.

    Stability:
        stable
    """

    family: str
    """The name of a family that this task definition is registered to.

    A family groups multiple versions of a task definition.

    Default:
        - Automatically generated name.

    Stability:
        stable
    """

    taskRole: aws_cdk.aws_iam.IRole
    """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

    Default:
        - A task role is automatically created for you.

    Stability:
        stable
    """

    volumes: typing.List["Volume"]
    """The list of volume definitions for the task.

    For more information, see Task Definition Parameter Volumes:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes]

    Default:
        - No volumes are passed to the Docker daemon on a container instance.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Compatibility")
class Compatibility(enum.Enum):
    """The task launch type compatibility requirement.

    Stability:
        stable
    """
    EC2 = "EC2"
    """The task should specify the EC2 launch type.

    Stability:
        stable
    """
    FARGATE = "FARGATE"
    """The task should specify the Fargate launch type.

    Stability:
        stable
    """
    EC2_AND_FARGATE = "EC2_AND_FARGATE"
    """The task can specify either the EC2 or Fargate launch types.

    Stability:
        stable
    """

class ContainerDefinition(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ContainerDefinition"):
    """A container definition is used in a task definition to describe the containers that are launched as part of a task.

    Stability:
        stable
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the ContainerDefinition class.

        Arguments:
            scope: -
            id: -
            props: -
            task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
            image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
            command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
            cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
            disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
            dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
            dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
            docker_labels: A key/value map of labels to add to the container. Default: - No labels.
            docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
            entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
            environment: The environment variables to pass to the container. Default: - No environment variables.
            essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
            extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
            health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
            hostname: The hostname to use for your container. Default: - Automatic hostname.
            linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see KernelCapabilities. [https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html]. Default: - No Linux paramters.
            logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
            memory_limit_mi_b: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
            memory_reservation_mi_b: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
            privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
            readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
            user: The user name to use inside the container. Default: root
            working_directory: The working directory in which to run commands inside the container. Default: /

        Stability:
            stable
        """
        props: ContainerDefinitionProps = {"taskDefinition": task_definition, "image": image}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if disable_networking is not None:
            props["disableNetworking"] = disable_networking

        if dns_search_domains is not None:
            props["dnsSearchDomains"] = dns_search_domains

        if dns_servers is not None:
            props["dnsServers"] = dns_servers

        if docker_labels is not None:
            props["dockerLabels"] = docker_labels

        if docker_security_options is not None:
            props["dockerSecurityOptions"] = docker_security_options

        if entry_point is not None:
            props["entryPoint"] = entry_point

        if environment is not None:
            props["environment"] = environment

        if essential is not None:
            props["essential"] = essential

        if extra_hosts is not None:
            props["extraHosts"] = extra_hosts

        if health_check is not None:
            props["healthCheck"] = health_check

        if hostname is not None:
            props["hostname"] = hostname

        if linux_parameters is not None:
            props["linuxParameters"] = linux_parameters

        if logging is not None:
            props["logging"] = logging

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if privileged is not None:
            props["privileged"] = privileged

        if readonly_root_filesystem is not None:
            props["readonlyRootFilesystem"] = readonly_root_filesystem

        if user is not None:
            props["user"] = user

        if working_directory is not None:
            props["workingDirectory"] = working_directory

        jsii.create(ContainerDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addLink")
    def add_link(self, container: "ContainerDefinition", alias: typing.Optional[str]=None) -> None:
        """This method adds a link which allows containers to communicate with each other without the need for port mappings.

        This parameter is only supported if the task definition is using the bridge network mode.
        Warning: The --link flag is a legacy feature of Docker. It may eventually be removed.

        Arguments:
            container: -
            alias: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addLink", [container, alias])

    @jsii.member(jsii_name="addMountPoints")
    def add_mount_points(self, *, container_path: str, read_only: bool, source_volume: str) -> None:
        """This method adds one or more mount points for data volumes to the container.

        Arguments:
            mount_points: -
            container_path: The path on the container to mount the host volume at.
            read_only: Specifies whether to give the container read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
            source_volume: The name of the volume to mount. Must be a volume name referenced in the name parameter of task definition volume.

        Stability:
            stable
        """
        mount_points: MountPoint = {"containerPath": container_path, "readOnly": read_only, "sourceVolume": source_volume}

        return jsii.invoke(self, "addMountPoints", [*mount_points])

    @jsii.member(jsii_name="addPortMappings")
    def add_port_mappings(self, *, container_port: jsii.Number, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> None:
        """This method adds one or more port mappings to the container.

        Arguments:
            port_mappings: -
            container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. For more information, see hostPort. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.
            host_port: The port number on the container instance to reserve for your container. If you are using containers in a task with the awsvpc or host network mode, the hostPort can either be left blank or set to the same value as the containerPort. If you are using containers in a task with the bridge network mode, you can specify a non-reserved host port for your container port mapping, or you can omit the hostPort (or set it to 0) while specifying a containerPort and your container automatically receives a port in the ephemeral port range for your container instance operating system and Docker version.
            protocol: The protocol used for the port mapping. Valid values are Protocol.TCP and Protocol.UDP. Default: TCP

        Stability:
            stable
        """
        port_mappings: PortMapping = {"containerPort": container_port}

        if host_port is not None:
            port_mappings["hostPort"] = host_port

        if protocol is not None:
            port_mappings["protocol"] = protocol

        return jsii.invoke(self, "addPortMappings", [*port_mappings])

    @jsii.member(jsii_name="addScratch")
    def add_scratch(self, *, container_path: str, name: str, read_only: bool, source_path: str) -> None:
        """This method mounts temporary disk space to the container.

        This adds the correct container mountPoint and task definition volume.

        Arguments:
            scratch: -
            container_path: The path on the container to mount the scratch volume at.
            name: The name of the scratch volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
            read_only: Specifies whether to give the container read-only access to the scratch volume. If this value is true, the container has read-only access to the scratch volume. If this value is false, then the container can write to the scratch volume.
            source_path: 

        Stability:
            stable
        """
        scratch: ScratchSpace = {"containerPath": container_path, "name": name, "readOnly": read_only, "sourcePath": source_path}

        return jsii.invoke(self, "addScratch", [scratch])

    @jsii.member(jsii_name="addToExecutionPolicy")
    def add_to_execution_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """This method adds the specified statement to the IAM task execution policy in the task definition.

        Arguments:
            statement: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addToExecutionPolicy", [statement])

    @jsii.member(jsii_name="addUlimits")
    def add_ulimits(self, *, hard_limit: jsii.Number, name: "UlimitName", soft_limit: jsii.Number) -> None:
        """This method adds one or more ulimits to the container.

        Arguments:
            ulimits: -
            hard_limit: The hard limit for the ulimit type.
            name: The type of the ulimit. For more information, see UlimitName: [https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName]
            soft_limit: The soft limit for the ulimit type.

        Stability:
            stable
        """
        ulimits: Ulimit = {"hardLimit": hard_limit, "name": name, "softLimit": soft_limit}

        return jsii.invoke(self, "addUlimits", [*ulimits])

    @jsii.member(jsii_name="addVolumesFrom")
    def add_volumes_from(self, *, read_only: bool, source_container: str) -> None:
        """This method adds one or more volumes to the container.

        Arguments:
            volumes_from: -
            read_only: Specifies whether the container has read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
            source_container: The name of another container within the same task definition from which to mount volumes.

        Stability:
            stable
        """
        volumes_from: VolumeFrom = {"readOnly": read_only, "sourceContainer": source_container}

        return jsii.invoke(self, "addVolumesFrom", [*volumes_from])

    @jsii.member(jsii_name="renderContainerDefinition")
    def render_container_definition(self) -> "CfnTaskDefinition.ContainerDefinitionProperty":
        """Render this container definition to a CloudFormation object.

        Stability:
            stable
        """
        return jsii.invoke(self, "renderContainerDefinition", [])

    @property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        """The port the container will listen on.

        Stability:
            stable
        """
        return jsii.get(self, "containerPort")

    @property
    @jsii.member(jsii_name="essential")
    def essential(self) -> bool:
        """Specifies whether the container will be marked essential.

        If the essential parameter of a container is marked as true, and that container
        fails or stops for any reason, all other containers that are part of the task are
        stopped. If the essential parameter of a container is marked as false, then its
        failure does not affect the rest of the containers in a task.

        If this parameter isomitted, a container is assumed to be essential.

        Stability:
            stable
        """
        return jsii.get(self, "essential")

    @property
    @jsii.member(jsii_name="ingressPort")
    def ingress_port(self) -> jsii.Number:
        """The inbound rules associated with the security group the task or service will use.

        This property is only used for tasks that use the awsvpc network mode.

        Stability:
            stable
        """
        return jsii.get(self, "ingressPort")

    @property
    @jsii.member(jsii_name="memoryLimitSpecified")
    def memory_limit_specified(self) -> bool:
        """Whether there was at least one memory limit specified in this definition.

        Stability:
            stable
        """
        return jsii.get(self, "memoryLimitSpecified")

    @property
    @jsii.member(jsii_name="mountPoints")
    def mount_points(self) -> typing.List["MountPoint"]:
        """The mount points for data volumes in your container.

        Stability:
            stable
        """
        return jsii.get(self, "mountPoints")

    @property
    @jsii.member(jsii_name="portMappings")
    def port_mappings(self) -> typing.List["PortMapping"]:
        """The list of port mappings for the container.

        Port mappings allow containers to access ports
        on the host container instance to send or receive traffic.

        Stability:
            stable
        """
        return jsii.get(self, "portMappings")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition.

        Stability:
            stable
        """
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        """An array of ulimits to set in the container.

        Stability:
            stable
        """
        return jsii.get(self, "ulimits")

    @property
    @jsii.member(jsii_name="volumesFrom")
    def volumes_from(self) -> typing.List["VolumeFrom"]:
        """The data volumes to mount from another container in the same task definition.

        Stability:
            stable
        """
        return jsii.get(self, "volumesFrom")

    @property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """The Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        Stability:
            stable
        """
        return jsii.get(self, "linuxParameters")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ContainerDefinitionOptions(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    """The command that is passed to the container.

    If you provide a shell command as a single string, you have to quote command-line arguments.

    Default:
        - CMD value built into container image.

    Stability:
        stable
    """
    cpu: jsii.Number
    """The minimum number of CPU units to reserve for the container.

    Default:
        - No minimum CPU units reserved.

    Stability:
        stable
    """
    disableNetworking: bool
    """Specifies whether networking is disabled within the container.

    When this parameter is true, networking is disabled within the container.

    Default:
        false

    Stability:
        stable
    """
    dnsSearchDomains: typing.List[str]
    """A list of DNS search domains that are presented to the container.

    Default:
        - No search domains.

    Stability:
        stable
    """
    dnsServers: typing.List[str]
    """A list of DNS servers that are presented to the container.

    Default:
        - Default DNS servers.

    Stability:
        stable
    """
    dockerLabels: typing.Mapping[str,str]
    """A key/value map of labels to add to the container.

    Default:
        - No labels.

    Stability:
        stable
    """
    dockerSecurityOptions: typing.List[str]
    """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

    Default:
        - No security labels.

    Stability:
        stable
    """
    entryPoint: typing.List[str]
    """The ENTRYPOINT value to pass to the container.

    Default:
        - Entry point configured in container.

    See:
        https://docs.docker.com/engine/reference/builder/#entrypoint
    Stability:
        stable
    """
    environment: typing.Mapping[str,str]
    """The environment variables to pass to the container.

    Default:
        - No environment variables.

    Stability:
        stable
    """
    essential: bool
    """Specifies whether the container is marked essential.

    If the essential parameter of a container is marked as true, and that container fails
    or stops for any reason, all other containers that are part of the task are stopped.
    If the essential parameter of a container is marked as false, then its failure does not
    affect the rest of the containers in a task. All tasks must have at least one essential container.

    If this parameter is omitted, a container is assumed to be essential.

    Default:
        true

    Stability:
        stable
    """
    extraHosts: typing.Mapping[str,str]
    """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

    Default:
        - No extra hosts.

    Stability:
        stable
    """
    healthCheck: "HealthCheck"
    """The health check command and associated configuration parameters for the container.

    Default:
        - Health check configuration from container.

    Stability:
        stable
    """
    hostname: str
    """The hostname to use for your container.

    Default:
        - Automatic hostname.

    Stability:
        stable
    """
    linuxParameters: "LinuxParameters"
    """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see KernelCapabilities. [https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html].

    Default:
        - No Linux paramters.

    Stability:
        stable
    """
    logging: "LogDriver"
    """The log configuration specification for the container.

    Default:
        - Containers use the same logging driver that the Docker daemon uses.

    Stability:
        stable
    """
    memoryLimitMiB: jsii.Number
    """The amount (in MiB) of memory to present to the container.

    If your container attempts to exceed the allocated memory, the container
    is terminated.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory limit.

    Stability:
        stable
    """
    memoryReservationMiB: jsii.Number
    """The soft limit (in MiB) of memory to reserve for the container.

    When system memory is under heavy contention, Docker attempts to keep the
    container memory to this soft limit. However, your container can consume more
    memory when it needs to, up to either the hard limit specified with the memory
    parameter (if applicable), or all of the available memory on the container
    instance, whichever comes first.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory reserved.

    Stability:
        stable
    """
    privileged: bool
    """Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

    Default:
        false

    Stability:
        stable
    """
    readonlyRootFilesystem: bool
    """When this parameter is true, the container is given read-only access to its root file system.

    Default:
        false

    Stability:
        stable
    """
    user: str
    """The user name to use inside the container.

    Default:
        root

    Stability:
        stable
    """
    workingDirectory: str
    """The working directory in which to run commands inside the container.

    Default:
        /

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionOptions", jsii_struct_bases=[_ContainerDefinitionOptions])
class ContainerDefinitionOptions(_ContainerDefinitionOptions):
    """The options for creating a container definition.

    Stability:
        stable
    """
    image: "ContainerImage"
    """The image used to start a container.

    This string is passed directly to the Docker daemon.
    Images in the Docker Hub registry are available by default.
    Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
    TODO: Update these to specify using classes of IContainerImage

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerDefinitionProps", jsii_struct_bases=[ContainerDefinitionOptions])
class ContainerDefinitionProps(ContainerDefinitionOptions, jsii.compat.TypedDict):
    """The properties in a container definition.

    Stability:
        stable
    """
    taskDefinition: "TaskDefinition"
    """The name of the task definition that includes this container definition.

    [disable-awslint:ref-via-interface]

    Stability:
        stable
    """

class ContainerImage(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.ContainerImage"):
    """Constructs for types of container images.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ContainerImageProxy

    def __init__(self) -> None:
        jsii.create(ContainerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @classmethod
    def from_asset(cls, directory: str, *, build_args: typing.Optional[typing.Mapping[str,str]]=None) -> "AssetImage":
        """Reference an image that's constructed directly from sources on disk.

        Arguments:
            directory: The directory containing the Dockerfile.
            props: -
            build_args: The arguments to pass to the ``docker build`` command. Default: none

        Stability:
            stable
        """
        props: AssetImageProps = {}

        if build_args is not None:
            props["buildArgs"] = build_args

        return jsii.sinvoke(cls, "fromAsset", [directory, props])

    @jsii.member(jsii_name="fromEcrRepository")
    @classmethod
    def from_ecr_repository(cls, repository: aws_cdk.aws_ecr.IRepository, tag: typing.Optional[str]=None) -> "EcrImage":
        """Reference an image in an ECR repository.

        Arguments:
            repository: -
            tag: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromRegistry")
    @classmethod
    def from_registry(cls, name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> "RepositoryImage":
        """Reference an image on DockerHub or another online registry.

        Arguments:
            name: -
            props: -
            credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

        Stability:
            stable
        """
        props: RepositoryImageProps = {}

        if credentials is not None:
            props["credentials"] = credentials

        return jsii.sinvoke(cls, "fromRegistry", [name, props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        ...


class _ContainerImageProxy(ContainerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


class AssetImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AssetImage"):
    """An image that will be built from a local directory with a Dockerfile.

    Stability:
        stable
    """
    def __init__(self, directory: str, *, build_args: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        """Constructs a new instance of the AssetImage class.

        Arguments:
            directory: The directory containing the Dockerfile.
            props: -
            build_args: The arguments to pass to the ``docker build`` command. Default: none

        Stability:
            stable
        """
        props: AssetImageProps = {}

        if build_args is not None:
            props["buildArgs"] = build_args

        jsii.create(AssetImage, self, [directory, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ContainerImageConfig(jsii.compat.TypedDict, total=False):
    repositoryCredentials: "CfnTaskDefinition.RepositoryCredentialsProperty"
    """Specifies the credentials used to access the image repository.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ContainerImageConfig", jsii_struct_bases=[_ContainerImageConfig])
class ContainerImageConfig(_ContainerImageConfig):
    """The configuration for creating a container image.

    Stability:
        stable
    """
    imageName: str
    """Specifies the name of the container image.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.CpuUtilizationScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps])
class CpuUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    """The properties for enabling scaling based on CPU utilization.

    Stability:
        stable
    """
    targetUtilizationPercent: jsii.Number
    """The target value for CPU utilization across all tasks in the service.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _Device(jsii.compat.TypedDict, total=False):
    containerPath: str
    """The path inside the container at which to expose the host device.

    Default:
        Same path as the host

    Stability:
        stable
    """
    permissions: typing.List["DevicePermission"]
    """The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device.

    Default:
        Readonly

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Device", jsii_struct_bases=[_Device])
class Device(_Device):
    """A container instance host device.

    Stability:
        stable
    """
    hostPath: str
    """The path for the device on the host container instance.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.DevicePermission")
class DevicePermission(enum.Enum):
    """Permissions for device access.

    Stability:
        stable
    """
    READ = "READ"
    """Read.

    Stability:
        stable
    """
    WRITE = "WRITE"
    """Write.

    Stability:
        stable
    """
    MKNOD = "MKNOD"
    """Make a node.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _DockerVolumeConfiguration(jsii.compat.TypedDict, total=False):
    autoprovision: bool
    """Specifies whether the Docker volume should be created if it does not already exist. If true is specified, the Docker volume will be created for you.

    Default:
        false

    Stability:
        stable
    """
    driverOpts: typing.List[str]
    """A map of Docker driver-specific options passed through.

    Default:
        No options

    Stability:
        stable
    """
    labels: typing.List[str]
    """Custom metadata to add to your Docker volume.

    Default:
        No labels

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.DockerVolumeConfiguration", jsii_struct_bases=[_DockerVolumeConfiguration])
class DockerVolumeConfiguration(_DockerVolumeConfiguration):
    """The configuration for a Docker volume.

    Docker volumes are only supported when you are using the EC2 launch type.

    Stability:
        stable
    """
    driver: str
    """The Docker volume driver to use.

    Stability:
        stable
    """

    scope: "Scope"
    """The scope for the Docker volume that determines its lifecycle.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[BaseServiceOptions])
class _Ec2ServiceProps(BaseServiceOptions, jsii.compat.TypedDict, total=False):
    assignPublicIp: bool
    """Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address.

    This property is only used for tasks that use the awsvpc network mode.

    Default:
        - Use subnet default.

    Stability:
        stable
    """
    daemon: bool
    """Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster.

    When you are using this strategy, do not specify a desired number of tasks orany task placement strategies.

    Default:
        false

    Stability:
        stable
    """
    placementConstraints: typing.List["PlacementConstraint"]
    """The placement constraints to use for tasks in the service.

    For more information, see Amazon ECS Task Placement Constraints:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html]

    Default:
        - No constraints.

    Stability:
        stable
    """
    placementStrategies: typing.List["PlacementStrategy"]
    """The placement strategies to use for tasks in the service.

    For more information, see Amazon ECS Task Placement Constraints:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html]

    Default:
        - No strategies.

    Stability:
        stable
    """
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    """The security groups to associate with the service.

    If you do not specify a security group, the default security group for the VPC is used.

    This property is only used for tasks that use the awsvpc network mode.

    Default:
        - A new security group is created.

    Stability:
        stable
    """
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """The subnets to associate with the service.

    This property is only used for tasks that use the awsvpc network mode.

    Default:
        - Private subnets.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2ServiceProps", jsii_struct_bases=[_Ec2ServiceProps])
class Ec2ServiceProps(_Ec2ServiceProps):
    """The properties for defining a service using the EC2 launch type.

    Stability:
        stable
    """
    taskDefinition: "TaskDefinition"
    """The task definition to use for tasks in the service.

    [disable-awslint:ref-via-interface]

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps])
class Ec2TaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    """The properties for a task definition run on an EC2 cluster.

    Stability:
        stable
    """
    networkMode: "NetworkMode"
    """The Docker networking mode to use for the containers in the task.

    The valid values are none, bridge, awsvpc, and host.

    Default:
        - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.

    Stability:
        stable
    """

    placementConstraints: typing.List["PlacementConstraint"]
    """An array of placement constraint objects to use for the task.

    You can
    specify a maximum of 10 constraints per task (this limit includes
    constraints in the task definition and those specified at run time).

    Default:
        - No placement constraints.

    Stability:
        stable
    """

class EcrImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcrImage"):
    """An image from an Amazon ECR repository.

    Stability:
        stable
    """
    def __init__(self, repository: aws_cdk.aws_ecr.IRepository, tag: str) -> None:
        """Constructs a new instance of the EcrImage class.

        Arguments:
            repository: -
            tag: -

        Stability:
            stable
        """
        jsii.create(EcrImage, self, [repository, tag])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        Arguments:
            _scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_scope, container_definition])

    @property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        """The image name. Images in Amazon ECR repositories can be specified by either using the full registry/repository:tag or registry/repository@digest.

        For example, 012345678910.dkr.ecr..amazonaws.com/:latest or
        012345678910.dkr.ecr..amazonaws.com/@sha256:94afd1f2e64d908bc90dbca0035a5b567EXAMPLE.

        Stability:
            stable
        """
        return jsii.get(self, "imageName")


@jsii.implements(aws_cdk.aws_ec2.IMachineImage)
class EcsOptimizedAmi(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmi"):
    """Construct a Linux machine image from the latest ECS Optimized AMI published in SSM.

    Stability:
        stable
    """
    def __init__(self, *, generation: typing.Optional[aws_cdk.aws_ec2.AmazonLinuxGeneration]=None, hardware_type: typing.Optional["AmiHardwareType"]=None) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        Arguments:
            props: -
            generation: The Amazon Linux generation to use. Default: AmazonLinuxGeneration.AmazonLinux2
            hardware_type: The ECS-optimized AMI variant to use. Default: AmiHardwareType.Standard

        Stability:
            stable
        """
        props: EcsOptimizedAmiProps = {}

        if generation is not None:
            props["generation"] = generation

        if hardware_type is not None:
            props["hardwareType"] = hardware_type

        jsii.create(EcsOptimizedAmi, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.MachineImageConfig:
        """Return the correct image.

        Arguments:
            scope: -

        Stability:
            stable
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.EcsOptimizedAmiProps", jsii_struct_bases=[])
class EcsOptimizedAmiProps(jsii.compat.TypedDict, total=False):
    """The properties that define which ECS-optimized AMI is used.

    Stability:
        stable
    """
    generation: aws_cdk.aws_ec2.AmazonLinuxGeneration
    """The Amazon Linux generation to use.

    Default:
        AmazonLinuxGeneration.AmazonLinux2

    Stability:
        stable
    """

    hardwareType: "AmiHardwareType"
    """The ECS-optimized AMI variant to use.

    Default:
        AmiHardwareType.Standard

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.FargatePlatformVersion")
class FargatePlatformVersion(enum.Enum):
    """The platform version on which to run your service.

    See:
        https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
    Stability:
        stable
    """
    LATEST = "LATEST"
    """The latest, recommended platform version.

    Stability:
        stable
    """
    VERSION1_3 = "VERSION1_3"
    """Version 1.3.0.

    Supports secrets, task recycling.

    Stability:
        stable
    """
    VERSION1_2 = "VERSION1_2"
    """Version 1.2.0.

    Supports private registries.

    Stability:
        stable
    """
    VERSION1_1 = "VERSION1_1"
    """Version 1.1.0.

    Supports task metadata, health checks, service discovery.

    Stability:
        stable
    """
    VERSION1_0 = "VERSION1_0"
    """Initial release.

    Based on Amazon Linux 2017.09.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[BaseServiceOptions])
class _FargateServiceProps(BaseServiceOptions, jsii.compat.TypedDict, total=False):
    assignPublicIp: bool
    """Specifies whether the task's elastic network interface receives a public IP address.

    If true, each task will receive a public IP address.

    Default:
        - Use subnet default.

    Stability:
        stable
    """
    platformVersion: "FargatePlatformVersion"
    """The platform version on which to run your service.

    If one is not specified, the LATEST platform version is used by default. For more information, see AWS Fargate Platform Versions:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html] in the Amazon Elastic Container Service Developer Guide.

    Default:
        Latest

    Stability:
        stable
    """
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    """The security groups to associate with the service.

    If you do not specify a security group, the default security group for the VPC is used.

    Default:
        - A new security group is created.

    Stability:
        stable
    """
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """The subnets to associate with the service.

    Default:
        - Private subnets.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateServiceProps", jsii_struct_bases=[_FargateServiceProps])
class FargateServiceProps(_FargateServiceProps):
    """The properties for defining a service using the Fargate launch type.

    Stability:
        stable
    """
    taskDefinition: "TaskDefinition"
    """The task definition to use for tasks in the service.

    [disable-awslint:ref-via-interface]

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps])
class FargateTaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    """The properties for a task definition.

    Stability:
        stable
    """
    cpu: jsii.Number
    """The number of cpu units used by the task.

    For tasks using the Fargate launch type,
    this field is required and you must use one of the following values,
    which determines your range of valid values for the memory parameter:

    256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
    512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
    1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
    2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
    4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

    Default:
        256

    Stability:
        stable
    """

    memoryLimitMiB: jsii.Number
    """The amount (in MiB) of memory used by the task.

    For tasks using the Fargate launch type,
    this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

    512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
    1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
    2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
    Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
    Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

    Default:
        512

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _HealthCheck(jsii.compat.TypedDict, total=False):
    interval: aws_cdk.core.Duration
    """The time period in seconds between each health check execution.

    You may specify between 5 and 300 seconds.

    Default:
        Duration.seconds(30)

    Stability:
        stable
    """
    retries: jsii.Number
    """The number of times to retry a failed health check before the container is considered unhealthy.

    You may specify between 1 and 10 retries.

    Default:
        3

    Stability:
        stable
    """
    startPeriod: aws_cdk.core.Duration
    """The optional grace period within which to provide containers time to bootstrap before failed health checks count towards the maximum number of retries.

    You may specify between 0 and 300 seconds.

    Default:
        No start period

    Stability:
        stable
    """
    timeout: aws_cdk.core.Duration
    """The time period in seconds to wait for a health check to succeed before it is considered a failure.

    You may specify between 2 and 60 seconds.

    Default:
        Duration.seconds(5)

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.HealthCheck", jsii_struct_bases=[_HealthCheck])
class HealthCheck(_HealthCheck):
    """The health check command and associated configuration parameters for the container.

    Stability:
        stable
    """
    command: typing.List[str]
    """A string array representing the command that the container runs to determine if it is healthy. The string array must start with CMD to execute the command arguments directly, or CMD-SHELL to run the command with the container's default shell.

    For example: [ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Host", jsii_struct_bases=[])
class Host(jsii.compat.TypedDict, total=False):
    """The details on a container instance bind mount host volume.

    Stability:
        stable
    """
    sourcePath: str
    """Specifies the path on the host container instance that is presented to the container. If the sourcePath value does not exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported.

    This property is not supported for tasks that use the Fargate launch type.

    Stability:
        stable
    """

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ICluster")
class ICluster(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        Stability:
            stable
        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        Stability:
            stable
        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The AWS Cloud Map namespace to associate with the cluster.

        Stability:
            stable
        """
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.ICluster"
    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups.

        Stability:
            stable
        """
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity.

        Stability:
            stable
        """
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster.

        Stability:
            stable
        """
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """The AWS Cloud Map namespace to associate with the cluster.

        Stability:
            stable
        """
        return jsii.get(self, "defaultCloudMapNamespace")


@jsii.implements(ICluster)
class Cluster(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Cluster"):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    Stability:
        stable
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, cluster_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the Cluster class.

        Arguments:
            scope: -
            id: -
            props: -
            vpc: The VPC to associate with the cluster.
            cluster_name: The name for the cluster. Default: CloudFormation-generated name

        Stability:
            stable
        """
        props: ClusterProps = {"vpc": vpc}

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @classmethod
    def from_cluster_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, cluster_name: str, security_groups: typing.List[aws_cdk.aws_ec2.ISecurityGroup], vpc: aws_cdk.aws_ec2.IVpc, cluster_arn: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional[aws_cdk.aws_servicediscovery.INamespace]=None, has_ec2_capacity: typing.Optional[bool]=None) -> "ICluster":
        """This method adds attributes from a specified cluster to this cluster.

        Arguments:
            scope: -
            id: -
            attrs: -
            cluster_name: The name of the cluster.
            security_groups: The security groups associated with the container instances registered to the cluster.
            vpc: The VPC associated with the cluster.
            cluster_arn: The Amazon Resource Name (ARN) that identifies the cluster. Default: Derived from clusterName
            default_cloud_map_namespace: The AWS Cloud Map namespace to associate with the cluster. Default: - No default namespace
            has_ec2_capacity: Specifies whether the cluster has EC2 instance capacity. Default: true

        Stability:
            stable
        """
        attrs: ClusterAttributes = {"clusterName": cluster_name, "securityGroups": security_groups, "vpc": vpc}

        if cluster_arn is not None:
            attrs["clusterArn"] = cluster_arn

        if default_cloud_map_namespace is not None:
            attrs["defaultCloudMapNamespace"] = default_cloud_map_namespace

        if has_ec2_capacity is not None:
            attrs["hasEc2Capacity"] = has_ec2_capacity

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: aws_cdk.aws_autoscaling.AutoScalingGroup, *, can_containers_access_instance_role: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """This method adds compute capacity to a cluster using the specified AutoScalingGroup.

        Arguments:
            auto_scaling_group: the ASG to add to this cluster. [disable-awslint:ref-via-interface] is needed in order to install the ECS agent by updating the ASGs user data.
            options: -
            can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
            task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)

        Stability:
            stable
        """
        options: AddAutoScalingGroupCapacityOptions = {}

        if can_containers_access_instance_role is not None:
            options["canContainersAccessInstanceRole"] = can_containers_access_instance_role

        if task_drain_time is not None:
            options["taskDrainTime"] = task_drain_time

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage]=None, can_containers_access_instance_role: typing.Optional[bool]=None, task_drain_time: typing.Optional[aws_cdk.core.Duration]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """This method adds compute capacity to a cluster by creating an AutoScalingGroup with the specified options.

        Returns the AutoScalingGroup so you can add autoscaling settings to it.

        Arguments:
            id: -
            options: -
            instance_type: The EC2 instance type to use when launching instances into the AutoScalingGroup.
            machine_image: The ECS-optimized AMI variant to use. For more information, see Amazon ECS-optimized AMIs: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html] Default: - Amazon Linux 2
            can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
            task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
            allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
            associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
            cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
            desired_capacity: Initial amount of instances in the fleet. Default: 1
            ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
            key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
            max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
            min_capacity: Minimum number of instances in the fleet. Default: 1
            notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
            replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
            resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
            resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
            rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
            spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
            update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
            vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.

        Stability:
            stable
        """
        options: AddCapacityOptions = {"instanceType": instance_type}

        if machine_image is not None:
            options["machineImage"] = machine_image

        if can_containers_access_instance_role is not None:
            options["canContainersAccessInstanceRole"] = can_containers_access_instance_role

        if task_drain_time is not None:
            options["taskDrainTime"] = task_drain_time

        if allow_all_outbound is not None:
            options["allowAllOutbound"] = allow_all_outbound

        if associate_public_ip_address is not None:
            options["associatePublicIpAddress"] = associate_public_ip_address

        if cooldown is not None:
            options["cooldown"] = cooldown

        if desired_capacity is not None:
            options["desiredCapacity"] = desired_capacity

        if ignore_unmodified_size_properties is not None:
            options["ignoreUnmodifiedSizeProperties"] = ignore_unmodified_size_properties

        if key_name is not None:
            options["keyName"] = key_name

        if max_capacity is not None:
            options["maxCapacity"] = max_capacity

        if min_capacity is not None:
            options["minCapacity"] = min_capacity

        if notifications_topic is not None:
            options["notificationsTopic"] = notifications_topic

        if replacing_update_min_successful_instances_percent is not None:
            options["replacingUpdateMinSuccessfulInstancesPercent"] = replacing_update_min_successful_instances_percent

        if resource_signal_count is not None:
            options["resourceSignalCount"] = resource_signal_count

        if resource_signal_timeout is not None:
            options["resourceSignalTimeout"] = resource_signal_timeout

        if rolling_update_configuration is not None:
            options["rollingUpdateConfiguration"] = rolling_update_configuration

        if spot_price is not None:
            options["spotPrice"] = spot_price

        if update_type is not None:
            options["updateType"] = update_type

        if vpc_subnets is not None:
            options["vpcSubnets"] = vpc_subnets

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addDefaultCloudMapNamespace")
    def add_default_cloud_map_namespace(self, *, name: str, type: typing.Optional[aws_cdk.aws_servicediscovery.NamespaceType]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_servicediscovery.INamespace:
        """Add an AWS Cloud Map DNS namespace for this cluster. NOTE: HttpNamespaces are not supported, as ECS always requires a DNSConfig when registering an instance to a Cloud Map service.

        Arguments:
            options: -
            name: The name of the namespace, such as example.com.
            type: The type of CloudMap Namespace to create. Default: PrivateDns
            vpc: The VPC to associate the namespace with. This property is required for private DNS namespaces. Default: VPC of the cluster for Private DNS Namespace, otherwise none

        Stability:
            stable
        """
        options: CloudMapNamespaceOptions = {"name": name}

        if type is not None:
            options["type"] = type

        if vpc is not None:
            options["vpc"] = vpc

        return jsii.invoke(self, "addDefaultCloudMapNamespace", [options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the specifed CloudWatch metric for this cluster.

        Arguments:
            metric_name: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuReservation")
    def metric_cpu_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters CPU reservation.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            average over 5 minutes

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricCpuReservation", [props])

    @jsii.member(jsii_name="metricMemoryReservation")
    def metric_memory_reservation(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters memory reservation.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            average over 5 minutes

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricMemoryReservation", [props])

    @property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        Stability:
            stable
        """
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        Stability:
            stable
        """
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage the allowed network connections for the cluster with Security Groups.

        Stability:
            stable
        """
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Whether the cluster has EC2 capacity associated with it.

        Stability:
            stable
        """
        return jsii.get(self, "hasEc2Capacity")

    @property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC associated with the cluster.

        Stability:
            stable
        """
        return jsii.get(self, "vpc")

    @property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[aws_cdk.aws_servicediscovery.INamespace]:
        """Getter for namespace added to cluster.

        Stability:
            stable
        """
        return jsii.get(self, "defaultCloudMapNamespace")


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IService")
class IService(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The interface for a service.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IServiceProxy

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        Stability:
            stable
        attribute:
            true
        """
        ...


class _IServiceProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The interface for a service.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.IService"
    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "serviceArn")


@jsii.implements(IService, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class BaseService(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.BaseService"):
    """The base class for Ec2Service and FargateService services.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseServiceProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, props: "BaseServiceProps", additional_props: typing.Any, task_definition: "TaskDefinition") -> None:
        """Constructs a new instance of the BaseService class.

        Arguments:
            scope: -
            id: -
            props: -
            additional_props: -
            task_definition: -

        Stability:
            stable
        """
        jsii.create(BaseService, self, [scope, id, props, additional_props, task_definition])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """This method is called to attach this service to an Application Load Balancer.

        Don't call this function directly. Instead, call listener.addTarget()
        to add this service to a load balancer.

        Arguments:
            target_group: -

        Stability:
            stable
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """This method is called to attach this service to a Network Load Balancer.

        Don't call this function directly. Instead, call listener.addTarget()
        to add this service to a load balancer.

        Arguments:
            target_group: -

        Stability:
            stable
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="autoScaleTaskCount")
    def auto_scale_task_count(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> "ScalableTaskCount":
        """An attribute representing the minimum and maximum task count for an AutoScalingGroup.

        Arguments:
            props: -
            max_capacity: Maximum capacity to scale to.
            min_capacity: Minimum capacity to scale to. Default: 1

        Stability:
            stable
        """
        props: aws_cdk.aws_applicationautoscaling.EnableScalingProps = {"maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        return jsii.invoke(self, "autoScaleTaskCount", [props])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(self, vpc: aws_cdk.aws_ec2.IVpc, assign_public_ip: typing.Optional[bool]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        """This method is called to create a networkConfiguration.

        Arguments:
            vpc: -
            assign_public_ip: -
            vpc_subnets: -
            security_group: -

        Stability:
            stable
        """
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, vpc_subnets, security_group])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the specified CloudWatch metric name for this service.

        Arguments:
            metric_name: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuUtilization")
    def metric_cpu_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters CPU utilization.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            average over 5 minutes

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricCpuUtilization", [props])

    @jsii.member(jsii_name="metricMemoryUtilization")
    def metric_memory_utilization(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[aws_cdk.core.Duration]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """This method returns the CloudWatch metric for this clusters memory utilization.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            average over 5 minutes

        Stability:
            stable
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricMemoryUtilization", [props])

    @property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        Stability:
            stable
        """
        return jsii.get(self, "cluster")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups which manage the allowed network traffic for the service.

        Stability:
            stable
        """
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        Stability:
            stable
        """
        return jsii.get(self, "serviceArn")

    @property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """The name of the service.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "serviceName")

    @property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        Stability:
            stable
        """
        return jsii.get(self, "taskDefinition")

    @property
    @jsii.member(jsii_name="loadBalancers")
    def _load_balancers(self) -> typing.List["CfnService.LoadBalancerProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer.

        Stability:
            stable
        """
        return jsii.get(self, "loadBalancers")

    @_load_balancers.setter
    def _load_balancers(self, value: typing.List["CfnService.LoadBalancerProperty"]):
        return jsii.set(self, "loadBalancers", value)

    @property
    @jsii.member(jsii_name="serviceRegistries")
    def _service_registries(self) -> typing.List["CfnService.ServiceRegistryProperty"]:
        """The details of the service discovery registries to assign to this service. For more information, see Service Discovery.

        Stability:
            stable
        """
        return jsii.get(self, "serviceRegistries")

    @_service_registries.setter
    def _service_registries(self, value: typing.List["CfnService.ServiceRegistryProperty"]):
        return jsii.set(self, "serviceRegistries", value)

    @property
    @jsii.member(jsii_name="cloudmapService")
    def _cloudmap_service(self) -> typing.Optional[aws_cdk.aws_servicediscovery.Service]:
        """The details of the AWS Cloud Map service.

        Stability:
            stable
        """
        return jsii.get(self, "cloudmapService")

    @_cloudmap_service.setter
    def _cloudmap_service(self, value: typing.Optional[aws_cdk.aws_servicediscovery.Service]):
        return jsii.set(self, "cloudmapService", value)

    @property
    @jsii.member(jsii_name="networkConfiguration")
    def _network_configuration(self) -> typing.Optional["CfnService.NetworkConfigurationProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer.

        Stability:
            stable
        """
        return jsii.get(self, "networkConfiguration")

    @_network_configuration.setter
    def _network_configuration(self, value: typing.Optional["CfnService.NetworkConfigurationProperty"]):
        return jsii.set(self, "networkConfiguration", value)


class _BaseServiceProxy(BaseService, jsii.proxy_for(aws_cdk.core.Resource)):
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IEc2Service")
class IEc2Service(IService, jsii.compat.Protocol):
    """The interface for a service using the EC2 launch type on an ECS cluster.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IEc2ServiceProxy

    pass

class _IEc2ServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the EC2 launch type on an ECS cluster.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.IEc2Service"
    pass

@jsii.implements(IEc2Service, aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget)
class Ec2Service(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2Service"):
    """This creates a service using the EC2 launch type on an ECS cluster.

    Stability:
        stable
    resource:
        AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, daemon: typing.Optional[bool]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, placement_strategies: typing.Optional[typing.List["PlacementStrategy"]]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the Ec2Service class.

        Arguments:
            scope: -
            id: -
            props: -
            task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
            assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. This property is only used for tasks that use the awsvpc network mode. Default: - Use subnet default.
            daemon: Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster. When you are using this strategy, do not specify a desired number of tasks orany task placement strategies. Default: false
            placement_constraints: The placement constraints to use for tasks in the service. For more information, see Amazon ECS Task Placement Constraints: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html] Default: - No constraints.
            placement_strategies: The placement strategies to use for tasks in the service. For more information, see Amazon ECS Task Placement Constraints: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html] Default: - No strategies.
            security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
            vpc_subnets: The subnets to associate with the service. This property is only used for tasks that use the awsvpc network mode. Default: - Private subnets.
            cluster: The name of the cluster that hosts the service.
            cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
            desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
            health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
            max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
            min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
            service_name: The name of the service. Default: - CloudFormation-generated name.

        Stability:
            stable
        """
        props: Ec2ServiceProps = {"taskDefinition": task_definition, "cluster": cluster}

        if assign_public_ip is not None:
            props["assignPublicIp"] = assign_public_ip

        if daemon is not None:
            props["daemon"] = daemon

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if placement_strategies is not None:
            props["placementStrategies"] = placement_strategies

        if security_group is not None:
            props["securityGroup"] = security_group

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if cloud_map_options is not None:
            props["cloudMapOptions"] = cloud_map_options

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if health_check_grace_period is not None:
            props["healthCheckGracePeriod"] = health_check_grace_period

        if max_healthy_percent is not None:
            props["maxHealthyPercent"] = max_healthy_percent

        if min_healthy_percent is not None:
            props["minHealthyPercent"] = min_healthy_percent

        if service_name is not None:
            props["serviceName"] = service_name

        jsii.create(Ec2Service, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2ServiceArn")
    @classmethod
    def from_ec2_service_arn(cls, scope: aws_cdk.core.Construct, id: str, ec2_service_arn: str) -> "IEc2Service":
        """Imports from the specified service ARN.

        Arguments:
            scope: -
            id: -
            ec2_service_arn: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromEc2ServiceArn", [scope, id, ec2_service_arn])

    @jsii.member(jsii_name="addPlacementConstraints")
    def add_placement_constraints(self, *constraints: "PlacementConstraint") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see Amazon ECS Task Placement Constraints:
        [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html]

        Arguments:
            constraints: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addPlacementConstraints", [*constraints])

    @jsii.member(jsii_name="addPlacementStrategies")
    def add_placement_strategies(self, *strategies: "PlacementStrategy") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see Amazon ECS Task Placement Strategies:
        [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html]

        Arguments:
            strategies: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addPlacementStrategies", [*strategies])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        """Registers the service as a target of a Classic Load Balancer (CLB).

        Don't call this. Call ``loadBalancer.addTarget()`` instead.

        Arguments:
            load_balancer: -

        Stability:
            stable
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates this Ec2Service.

        Stability:
            stable
        """
        return jsii.invoke(self, "validate", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IFargateService")
class IFargateService(IService, jsii.compat.Protocol):
    """The interface for a service using the Fargate launch type on an ECS cluster.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IFargateServiceProxy

    pass

class _IFargateServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the Fargate launch type on an ECS cluster.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.IFargateService"
    pass

@jsii.implements(IFargateService)
class FargateService(BaseService, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateService"):
    """This creates a service using the Fargate launch type on an ECS cluster.

    Stability:
        stable
    resource:
        AWS::ECS::Service
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, desired_count: typing.Optional[jsii.Number]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FargateService class.

        Arguments:
            scope: -
            id: -
            props: -
            task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
            assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: - Use subnet default.
            platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see AWS Fargate Platform Versions: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html] in the Amazon Elastic Container Service Developer Guide. Default: Latest
            security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
            vpc_subnets: The subnets to associate with the service. Default: - Private subnets.
            cluster: The name of the cluster that hosts the service.
            cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
            desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
            health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
            max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
            min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
            service_name: The name of the service. Default: - CloudFormation-generated name.

        Stability:
            stable
        """
        props: FargateServiceProps = {"taskDefinition": task_definition, "cluster": cluster}

        if assign_public_ip is not None:
            props["assignPublicIp"] = assign_public_ip

        if platform_version is not None:
            props["platformVersion"] = platform_version

        if security_group is not None:
            props["securityGroup"] = security_group

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if cloud_map_options is not None:
            props["cloudMapOptions"] = cloud_map_options

        if desired_count is not None:
            props["desiredCount"] = desired_count

        if health_check_grace_period is not None:
            props["healthCheckGracePeriod"] = health_check_grace_period

        if max_healthy_percent is not None:
            props["maxHealthyPercent"] = max_healthy_percent

        if min_healthy_percent is not None:
            props["minHealthyPercent"] = min_healthy_percent

        if service_name is not None:
            props["serviceName"] = service_name

        jsii.create(FargateService, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateServiceArn")
    @classmethod
    def from_fargate_service_arn(cls, scope: aws_cdk.core.Construct, id: str, fargate_service_arn: str) -> "IFargateService":
        """Import a task definition from the specified task definition ARN.

        Arguments:
            scope: -
            id: -
            fargate_service_arn: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromFargateServiceArn", [scope, id, fargate_service_arn])


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ITaskDefinition")
class ITaskDefinition(aws_cdk.core.IResource, jsii.compat.Protocol):
    """The interface for all task definitions.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionProxy

    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        Stability:
            stable
        """
        ...

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        Stability:
            stable
        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition.

        Stability:
            stable
        """
        ...


class _ITaskDefinitionProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """The interface for all task definitions.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.ITaskDefinition"
    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with.

        Stability:
            stable
        """
        return jsii.get(self, "compatibility")

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        Stability:
            stable
        """
        return jsii.get(self, "isEc2Compatible")

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        Stability:
            stable
        """
        return jsii.get(self, "isFargateCompatible")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "taskDefinitionArn")

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition.

        Stability:
            stable
        """
        return jsii.get(self, "executionRole")


@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IEc2TaskDefinition")
class IEc2TaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on an EC2 cluster.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IEc2TaskDefinitionProxy

    pass

class _IEc2TaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on an EC2 cluster.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.IEc2TaskDefinition"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.IFargateTaskDefinition")
class IFargateTaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on a Fargate cluster.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IFargateTaskDefinitionProxy

    pass

class _IFargateTaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on a Fargate cluster.

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.IFargateTaskDefinition"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ecs.ITaskDefinitionExtension")
class ITaskDefinitionExtension(jsii.compat.Protocol):
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionExtensionProxy

    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        Arguments:
            task_definition: [disable-awslint:ref-via-interface].

        Stability:
            stable
        """
        ...


class _ITaskDefinitionExtensionProxy():
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));

    Stability:
        stable
    """
    __jsii_type__ = "@aws-cdk/aws-ecs.ITaskDefinitionExtension"
    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        Arguments:
            task_definition: [disable-awslint:ref-via-interface].

        Stability:
            stable
        """
        return jsii.invoke(self, "extend", [task_definition])


@jsii.enum(jsii_type="@aws-cdk/aws-ecs.LaunchType")
class LaunchType(enum.Enum):
    """The launch type of an ECS service.

    Stability:
        stable
    """
    EC2 = "EC2"
    """The service will be launched using the EC2 launch type.

    Stability:
        stable
    """
    FARGATE = "FARGATE"
    """The service will be launched using the FARGATE launch type.

    Stability:
        stable
    """

class LinuxParameters(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.LinuxParameters"):
    """Linux-specific options that are applied to the container.

    Stability:
        stable
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, init_process_enabled: typing.Optional[bool]=None, shared_memory_size: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the LinuxParameters class.

        Arguments:
            scope: -
            id: -
            props: -
            init_process_enabled: Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
            shared_memory_size: The value for the size (in MiB) of the /dev/shm volume. Default: No shared memory.

        Stability:
            stable
        """
        props: LinuxParametersProps = {}

        if init_process_enabled is not None:
            props["initProcessEnabled"] = init_process_enabled

        if shared_memory_size is not None:
            props["sharedMemorySize"] = shared_memory_size

        jsii.create(LinuxParameters, self, [scope, id, props])

    @jsii.member(jsii_name="addCapabilities")
    def add_capabilities(self, *cap: "Capability") -> None:
        """Adds one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        Arguments:
            cap: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addCapabilities", [*cap])

    @jsii.member(jsii_name="addDevices")
    def add_devices(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List["DevicePermission"]]=None) -> None:
        """Adds one or more host devices to a container.

        Arguments:
            device: -
            host_path: The path for the device on the host container instance.
            container_path: The path inside the container at which to expose the host device. Default: Same path as the host
            permissions: The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device. Default: Readonly

        Stability:
            stable
        """
        device: Device = {"hostPath": host_path}

        if container_path is not None:
            device["containerPath"] = container_path

        if permissions is not None:
            device["permissions"] = permissions

        return jsii.invoke(self, "addDevices", [*device])

    @jsii.member(jsii_name="addTmpfs")
    def add_tmpfs(self, *, container_path: str, size: jsii.Number, mount_options: typing.Optional[typing.List["TmpfsMountOption"]]=None) -> None:
        """Specifies the container path, mount options, and size (in MiB) of the tmpfs mount for a container.

        Only works with EC2 launch type.

        Arguments:
            tmpfs: -
            container_path: The absolute file path where the tmpfs volume is to be mounted.
            size: The size (in MiB) of the tmpfs volume.
            mount_options: The list of tmpfs volume mount options. For more information, see TmpfsMountOptions: [https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html]

        Stability:
            stable
        """
        tmpfs: Tmpfs = {"containerPath": container_path, "size": size}

        if mount_options is not None:
            tmpfs["mountOptions"] = mount_options

        return jsii.invoke(self, "addTmpfs", [*tmpfs])

    @jsii.member(jsii_name="dropCapabilities")
    def drop_capabilities(self, *cap: "Capability") -> None:
        """Removes one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        Arguments:
            cap: -

        Stability:
            stable
        """
        return jsii.invoke(self, "dropCapabilities", [*cap])

    @jsii.member(jsii_name="renderLinuxParameters")
    def render_linux_parameters(self) -> "CfnTaskDefinition.LinuxParametersProperty":
        """Renders the Linux parameters to a CloudFormation object.

        Stability:
            stable
        """
        return jsii.invoke(self, "renderLinuxParameters", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LinuxParametersProps", jsii_struct_bases=[])
class LinuxParametersProps(jsii.compat.TypedDict, total=False):
    """The properties for defining Linux-specific options that are applied to the container.

    Stability:
        stable
    """
    initProcessEnabled: bool
    """Specifies whether to run an init process inside the container that forwards signals and reaps processes.

    Default:
        false

    Stability:
        stable
    """

    sharedMemorySize: jsii.Number
    """The value for the size (in MiB) of the /dev/shm volume.

    Default:
        No shared memory.

    Stability:
        stable
    """

class LogDriver(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs.LogDriver"):
    """The base class for log drivers.

    Stability:
        stable
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _LogDriverProxy

    def __init__(self) -> None:
        jsii.create(LogDriver, self, [])

    @jsii.member(jsii_name="awsLogs")
    @classmethod
    def aws_logs(cls, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to CloudWatch Logs.

        Arguments:
            props: -
            stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
            datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
            log_group: The log group to log to. Default: - A log group is automatically created.
            log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
            multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        Stability:
            stable
        """
        props: AwsLogDriverProps = {"streamPrefix": stream_prefix}

        if datetime_format is not None:
            props["datetimeFormat"] = datetime_format

        if log_group is not None:
            props["logGroup"] = log_group

        if log_retention is not None:
            props["logRetention"] = log_retention

        if multiline_pattern is not None:
            props["multilinePattern"] = multiline_pattern

        return jsii.sinvoke(cls, "awsLogs", [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        ...


class _LogDriverProxy(LogDriver):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


class AwsLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.AwsLogDriver"):
    """A log driver that sends log information to CloudWatch Logs.

    Stability:
        stable
    """
    def __init__(self, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, multiline_pattern: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the AwsLogDriver class.

        Arguments:
            props: the awslogs log driver configuration options.
            stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
            datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
            log_group: The log group to log to. Default: - A log group is automatically created.
            log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
            multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        Stability:
            stable
        """
        props: AwsLogDriverProps = {"streamPrefix": stream_prefix}

        if datetime_format is not None:
            props["datetimeFormat"] = datetime_format

        if log_group is not None:
            props["logGroup"] = log_group

        if log_retention is not None:
            props["logRetention"] = log_retention

        if multiline_pattern is not None:
            props["multilinePattern"] = multiline_pattern

        jsii.create(AwsLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        Arguments:
            scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [scope, container_definition])

    @property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        """The log group to send log streams to.

        Only available after the LogDriver has been bound to a ContainerDefinition.

        Stability:
            stable
        """
        return jsii.get(self, "logGroup")

    @log_group.setter
    def log_group(self, value: typing.Optional[aws_cdk.aws_logs.ILogGroup]):
        return jsii.set(self, "logGroup", value)


@jsii.data_type_optionals(jsii_struct_bases=[])
class _LogDriverConfig(jsii.compat.TypedDict, total=False):
    options: typing.Mapping[str,str]
    """The configuration options to send to the log driver.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.LogDriverConfig", jsii_struct_bases=[_LogDriverConfig])
class LogDriverConfig(_LogDriverConfig):
    """The configuration to use when creating a log driver.

    Stability:
        stable
    """
    logDriver: str
    """The log driver to use for the container.

    The valid values listed for this parameter are log drivers
    that the Amazon ECS container agent can communicate with by default.

    For tasks using the Fargate launch type, the supported log drivers are awslogs and splunk.
    For tasks using the EC2 launch type, the supported log drivers are awslogs, syslog, gelf, fluentd, splunk, journald, and json-file.

    For more information about using the awslogs log driver, see Using the awslogs Log Driver:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html] in the Amazon Elastic Container Service Developer Guide.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MemoryUtilizationScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps])
class MemoryUtilizationScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    """The properties for enabling scaling based on memory utilization.

    Stability:
        stable
    """
    targetUtilizationPercent: jsii.Number
    """The target value for memory utilization across all tasks in the service.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.MountPoint", jsii_struct_bases=[])
class MountPoint(jsii.compat.TypedDict):
    """The details of data volume mount points for a container.

    Stability:
        stable
    """
    containerPath: str
    """The path on the container to mount the host volume at.

    Stability:
        stable
    """

    readOnly: bool
    """Specifies whether to give the container read-only access to the volume.

    If this value is true, the container has read-only access to the volume.
    If this value is false, then the container can write to the volume.

    Stability:
        stable
    """

    sourceVolume: str
    """The name of the volume to mount.

    Must be a volume name referenced in the name parameter of task definition volume.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.NetworkMode")
class NetworkMode(enum.Enum):
    """The networking mode to use for the containers in the task.

    Stability:
        stable
    """
    NONE = "NONE"
    """The task's containers do not have external connectivity and port mappings can't be specified in the container definition.

    Stability:
        stable
    """
    BRIDGE = "BRIDGE"
    """The task utilizes Docker's built-in virtual network which runs inside each container instance.

    Stability:
        stable
    """
    AWS_VPC = "AWS_VPC"
    """The task is allocated an elastic network interface.

    Stability:
        stable
    """
    HOST = "HOST"
    """The task bypasses Docker's built-in virtual network and maps container ports directly to the EC2 instance's network interface directly.

    In this mode, you can't run multiple instantiations of the same task on a
    single container instance when port mappings are used.

    Stability:
        stable
    """

class PlacementConstraint(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.PlacementConstraint"):
    """The placement constraints to use for tasks in the service. For more information, see Amazon ECS Task Placement Constraints. [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html].

    Tasks will only be placed on instances that match these rules.

    Stability:
        stable
    """
    @jsii.member(jsii_name="distinctInstances")
    @classmethod
    def distinct_instances(cls) -> "PlacementConstraint":
        """Use distinctInstance to ensure that each task in a particular group is running on a different container instance.

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "distinctInstances", [])

    @jsii.member(jsii_name="memberOf")
    @classmethod
    def member_of(cls, *expressions: str) -> "PlacementConstraint":
        """Use memberOf to restrict the selection to a group of valid candidates specified by a query expression.

        Multiple expressions can be specified. For more information, see Cluster Query Language:
        [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html]

        You can specify multiple expressions in one call. The tasks will only be placed on instances matching all expressions.

        Arguments:
            expressions: -

        See:
            https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html
        Stability:
            stable
        """
        return jsii.sinvoke(cls, "memberOf", [*expressions])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementConstraintProperty"]:
        """Return the placement JSON.

        Stability:
            stable
        """
        return jsii.invoke(self, "toJson", [])


class PlacementStrategy(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.PlacementStrategy"):
    """The placement strategies to use for tasks in the service. For more information, see Amazon ECS Task Placement Strategies: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html].

    Tasks will preferentially be placed on instances that match these rules.

    Stability:
        stable
    """
    @jsii.member(jsii_name="packedBy")
    @classmethod
    def packed_by(cls, resource: "BinPackResource") -> "PlacementStrategy":
        """Places tasks on the container instances with the least available capacity of the specified resource.

        Arguments:
            resource: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "packedBy", [resource])

    @jsii.member(jsii_name="packedByCpu")
    @classmethod
    def packed_by_cpu(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of CPU capacity.

        This minimizes the number of instances in use.

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "packedByCpu", [])

    @jsii.member(jsii_name="packedByMemory")
    @classmethod
    def packed_by_memory(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of memory capacity.

        This minimizes the number of instances in use.

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "packedByMemory", [])

    @jsii.member(jsii_name="randomly")
    @classmethod
    def randomly(cls) -> "PlacementStrategy":
        """Places tasks randomly.

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "randomly", [])

    @jsii.member(jsii_name="spreadAcross")
    @classmethod
    def spread_across(cls, *fields: str) -> "PlacementStrategy":
        """Places tasks evenly based on the specified value.

        You can use one of the built-in attributes found on ``BuiltInAttributes``
        or supply your own custom instance attributes. If more than one attribute
        is supplied, spreading is done in order.

        Arguments:
            fields: -

        Default:
            attributes instanceId

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "spreadAcross", [*fields])

    @jsii.member(jsii_name="spreadAcrossInstances")
    @classmethod
    def spread_across_instances(cls) -> "PlacementStrategy":
        """Places tasks evenly across all container instances in the cluster.

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "spreadAcrossInstances", [])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementStrategyProperty"]:
        """Return the placement JSON.

        Stability:
            stable
        """
        return jsii.invoke(self, "toJson", [])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _PortMapping(jsii.compat.TypedDict, total=False):
    hostPort: jsii.Number
    """The port number on the container instance to reserve for your container.

    If you are using containers in a task with the awsvpc or host network mode,
    the hostPort can either be left blank or set to the same value as the containerPort.

    If you are using containers in a task with the bridge network mode,
    you can specify a non-reserved host port for your container port mapping, or
    you can omit the hostPort (or set it to 0) while specifying a containerPort and
    your container automatically receives a port in the ephemeral port range for
    your container instance operating system and Docker version.

    Stability:
        stable
    """
    protocol: "Protocol"
    """The protocol used for the port mapping.

    Valid values are Protocol.TCP and Protocol.UDP.

    Default:
        TCP

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.PortMapping", jsii_struct_bases=[_PortMapping])
class PortMapping(_PortMapping):
    """Port mappings allow containers to access ports on the host container instance to send or receive traffic.

    Stability:
        stable
    """
    containerPort: jsii.Number
    """The port number on the container that is bound to the user-specified or automatically assigned host port.

    If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
    If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
    your container automatically receives a host port in the ephemeral port range.

    For more information, see hostPort.
    Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Protocol")
class Protocol(enum.Enum):
    """Network protocol.

    Stability:
        stable
    """
    TCP = "TCP"
    """TCP.

    Stability:
        stable
    """
    UDP = "UDP"
    """UDP.

    Stability:
        stable
    """

class RepositoryImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.RepositoryImage"):
    """An image hosted in a public or private repository.

    For images hosted in Amazon ECR, see EcrImage:
    [https://docs.aws.amazon.com/AmazonECR/latest/userguide/images.html]

    Stability:
        stable
    """
    def __init__(self, image_name: str, *, credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret]=None) -> None:
        """Constructs a new instance of the RepositoryImage class.

        Arguments:
            image_name: -
            props: -
            credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

        Stability:
            stable
        """
        props: RepositoryImageProps = {}

        if credentials is not None:
            props["credentials"] = credentials

        jsii.create(RepositoryImage, self, [image_name, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        Arguments:
            _scope: -
            container_definition: -

        Stability:
            stable
        """
        return jsii.invoke(self, "bind", [_scope, container_definition])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RepositoryImageProps", jsii_struct_bases=[])
class RepositoryImageProps(jsii.compat.TypedDict, total=False):
    """The properties for an image hosted in a public or private repository.

    Stability:
        stable
    """
    credentials: aws_cdk.aws_secretsmanager.ISecret
    """The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.RequestCountScalingProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps])
class RequestCountScalingProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    """The properties for enabling scaling based on Application Load Balancer (ALB) request counts.

    Stability:
        stable
    """
    requestsPerTarget: jsii.Number
    """The number of ALB requests per target.

    Stability:
        stable
    """

    targetGroup: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup
    """The ALB target group name.

    Stability:
        stable
    """

class ScalableTaskCount(aws_cdk.aws_applicationautoscaling.BaseScalableAttribute, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.ScalableTaskCount"):
    """The scalable attribute representing task count.

    Stability:
        stable
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: aws_cdk.aws_applicationautoscaling.ServiceNamespace, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the ScalableTaskCount class.

        Arguments:
            scope: -
            id: -
            props: -
            dimension: Scalable dimension of the attribute.
            resource_id: Resource ID of the attribute.
            role: Role to use for scaling.
            service_namespace: Service namespace of the scalable attribute.
            max_capacity: Maximum capacity to scale to.
            min_capacity: Minimum capacity to scale to. Default: 1

        Stability:
            stable
        """
        props: ScalableTaskCountProps = {"dimension": dimension, "resourceId": resource_id, "role": role, "serviceNamespace": service_namespace, "maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        jsii.create(ScalableTaskCount, self, [scope, id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target CPU utilization.

        Arguments:
            id: -
            props: -
            target_utilization_percent: The target value for CPU utilization across all tasks in the service.
            disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policy_name: A name for the scaling policy. Default: - Automatically generated name.
            scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.

        Stability:
            stable
        """
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown is not None:
            props["scaleInCooldown"] = scale_in_cooldown

        if scale_out_cooldown is not None:
            props["scaleOutCooldown"] = scale_out_cooldown

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMemoryUtilization")
    def scale_on_memory_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target memory utilization.

        Arguments:
            id: -
            props: -
            target_utilization_percent: The target value for memory utilization across all tasks in the service.
            disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policy_name: A name for the scaling policy. Default: - Automatically generated name.
            scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.

        Stability:
            stable
        """
        props: MemoryUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown is not None:
            props["scaleInCooldown"] = scale_in_cooldown

        if scale_out_cooldown is not None:
            props["scaleOutCooldown"] = scale_out_cooldown

        return jsii.invoke(self, "scaleOnMemoryUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, scaling_steps: typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval], adjustment_type: typing.Optional[aws_cdk.aws_applicationautoscaling.AdjustmentType]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """Scales in or out based on a specified metric value.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
            min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect

        Stability:
            stable
        """
        props: aws_cdk.aws_applicationautoscaling.BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown is not None:
            props["cooldown"] = cooldown

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, requests_per_target: jsii.Number, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target Application Load Balancer request count per target.

        Arguments:
            id: -
            props: -
            requests_per_target: The number of ALB requests per target.
            target_group: The ALB target group name.
            disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policy_name: A name for the scaling policy. Default: - Automatically generated name.
            scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.

        Stability:
            stable
        """
        props: RequestCountScalingProps = {"requestsPerTarget": requests_per_target, "targetGroup": target_group}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown is not None:
            props["scaleInCooldown"] = scale_in_cooldown

        if scale_out_cooldown is not None:
            props["scaleOutCooldown"] = scale_out_cooldown

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scales in or out based on a specified scheduled time.

        Arguments:
            id: -
            props: -
            schedule: When to perform this action.
            end_time: When this scheduled action expires. Default: The rule never expires.
            max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
            min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
            start_time: When this scheduled action becomes active. Default: The rule is activate immediately

        Stability:
            stable
        """
        props: aws_cdk.aws_applicationautoscaling.ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackCustomMetric")
    def scale_to_track_custom_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.IMetric, target_value: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[aws_cdk.core.Duration]=None, scale_out_cooldown: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Scales in or out to achieve a target on a custom metric.

        Arguments:
            id: -
            props: -
            metric: The custom CloudWatch metric to track. The metric must represent utilization; that is, you will always get the following behavior: - metric > targetValue => scale out - metric < targetValue => scale in
            target_value: The target value for the custom CloudWatch metric.
            disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policy_name: A name for the scaling policy. Default: - Automatically generated name.
            scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.

        Stability:
            stable
        """
        props: TrackCustomMetricProps = {"metric": metric, "targetValue": target_value}

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown is not None:
            props["scaleInCooldown"] = scale_in_cooldown

        if scale_out_cooldown is not None:
            props["scaleOutCooldown"] = scale_out_cooldown

        return jsii.invoke(self, "scaleToTrackCustomMetric", [id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ScalableTaskCountProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseScalableAttributeProps])
class ScalableTaskCountProps(aws_cdk.aws_applicationautoscaling.BaseScalableAttributeProps, jsii.compat.TypedDict):
    """The properties of a scalable attribute representing task count.

    Stability:
        stable
    """
    pass

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.Scope")
class Scope(enum.Enum):
    """The scope for the Docker volume that determines its lifecycle. Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops. Docker volumes that are scoped as shared persist after the task stops.

    Stability:
        stable
    """
    TASK = "TASK"
    """Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops.

    Stability:
        stable
    """
    SHARED = "SHARED"
    """Docker volumes that are scoped as shared persist after the task stops.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.ScratchSpace", jsii_struct_bases=[])
class ScratchSpace(jsii.compat.TypedDict):
    """The temporary disk space mounted to the container.

    Stability:
        stable
    """
    containerPath: str
    """The path on the container to mount the scratch volume at.

    Stability:
        stable
    """

    name: str
    """The name of the scratch volume to mount.

    Must be a volume name referenced in the name parameter of task definition volume.

    Stability:
        stable
    """

    readOnly: bool
    """Specifies whether to give the container read-only access to the scratch volume.

    If this value is true, the container has read-only access to the scratch volume.
    If this value is false, then the container can write to the scratch volume.

    Stability:
        stable
    """

    sourcePath: str
    """
    Stability:
        stable
    """

@jsii.implements(ITaskDefinition)
class TaskDefinition(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.TaskDefinition"):
    """The base class for all task definitions.

    Stability:
        stable
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, compatibility: "Compatibility", cpu: typing.Optional[str]=None, memory_mi_b: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the TaskDefinition class.

        Arguments:
            scope: -
            id: -
            props: -
            compatibility: The task launch type compatiblity requirement.
            cpu: The number of cpu units used by the task. If you are using the EC2 launch type, this field is optional and any value can be used. If you are using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: - CPU units are not specified.
            memory_mi_b: The amount (in MiB) of memory used by the task. If using the EC2 launch type, this field is optional and any value can be used. If using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: - Memory used by task is not specified.
            network_mode: The networking mode to use for the containers in the task. On Fargate, the only supported networking mode is AwsVpc. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
            placement_constraints: The placement constraints to use for tasks in the service. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Not supported in Fargate. Default: - No placement constraints.
            execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
            family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
            task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
            volumes: The list of volume definitions for the task. For more information, see Task Definition Parameter Volumes: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes] Default: - No volumes are passed to the Docker daemon on a container instance.

        Stability:
            stable
        """
        props: TaskDefinitionProps = {"compatibility": compatibility}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_mi_b is not None:
            props["memoryMiB"] = memory_mi_b

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromTaskDefinitionArn")
    @classmethod
    def from_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, task_definition_arn: str) -> "ITaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        The task will have a compatibility of EC2+Fargate.

        Arguments:
            scope: -
            id: -
            task_definition_arn: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromTaskDefinitionArn", [scope, id, task_definition_arn])

    @jsii.member(jsii_name="addContainer")
    def add_container(self, id: str, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str,str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str,str]]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> "ContainerDefinition":
        """Adds a new container to the task definition.

        Arguments:
            id: -
            props: -
            image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
            command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
            cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
            disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
            dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
            dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
            docker_labels: A key/value map of labels to add to the container. Default: - No labels.
            docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
            entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
            environment: The environment variables to pass to the container. Default: - No environment variables.
            essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
            extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
            health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
            hostname: The hostname to use for your container. Default: - Automatic hostname.
            linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see KernelCapabilities. [https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html]. Default: - No Linux paramters.
            logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
            memory_limit_mi_b: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
            memory_reservation_mi_b: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
            privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
            readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
            user: The user name to use inside the container. Default: root
            working_directory: The working directory in which to run commands inside the container. Default: /

        Stability:
            stable
        """
        props: ContainerDefinitionOptions = {"image": image}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if disable_networking is not None:
            props["disableNetworking"] = disable_networking

        if dns_search_domains is not None:
            props["dnsSearchDomains"] = dns_search_domains

        if dns_servers is not None:
            props["dnsServers"] = dns_servers

        if docker_labels is not None:
            props["dockerLabels"] = docker_labels

        if docker_security_options is not None:
            props["dockerSecurityOptions"] = docker_security_options

        if entry_point is not None:
            props["entryPoint"] = entry_point

        if environment is not None:
            props["environment"] = environment

        if essential is not None:
            props["essential"] = essential

        if extra_hosts is not None:
            props["extraHosts"] = extra_hosts

        if health_check is not None:
            props["healthCheck"] = health_check

        if hostname is not None:
            props["hostname"] = hostname

        if linux_parameters is not None:
            props["linuxParameters"] = linux_parameters

        if logging is not None:
            props["logging"] = logging

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        if privileged is not None:
            props["privileged"] = privileged

        if readonly_root_filesystem is not None:
            props["readonlyRootFilesystem"] = readonly_root_filesystem

        if user is not None:
            props["user"] = user

        if working_directory is not None:
            props["workingDirectory"] = working_directory

        return jsii.invoke(self, "addContainer", [id, props])

    @jsii.member(jsii_name="addExtension")
    def add_extension(self, extension: "ITaskDefinitionExtension") -> None:
        """Adds the specified extention to the task definition.

        Extension can be used to apply a packaged modification to
        a task definition.

        Arguments:
            extension: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addExtension", [extension])

    @jsii.member(jsii_name="addPlacementConstraint")
    def add_placement_constraint(self, constraint: "PlacementConstraint") -> None:
        """Adds the specified placement constraint to the task definition.

        Arguments:
            constraint: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addPlacementConstraint", [constraint])

    @jsii.member(jsii_name="addToExecutionRolePolicy")
    def add_to_execution_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a policy statement to the task execution IAM role.

        Arguments:
            statement: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addToExecutionRolePolicy", [statement])

    @jsii.member(jsii_name="addToTaskRolePolicy")
    def add_to_task_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a policy statement to the task IAM role.

        Arguments:
            statement: -

        Stability:
            stable
        """
        return jsii.invoke(self, "addToTaskRolePolicy", [statement])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None) -> None:
        """Adds a volume to the task definition.

        Arguments:
            volume: -
            name: The name of the volume. Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed. This name is referenced in the sourceVolume parameter of container definition mountPoints.
            docker_volume_configuration: This property is specified when you are using Docker volumes. Docker volumes are only supported when you are using the EC2 launch type. Windows containers only support the use of the local driver. To use bind mounts, specify a host instead.
            host: This property is specified when you are using bind mount host volumes. Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types. The contents of the host parameter determine whether your bind mount host volume persists on the host container instance and where it is stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data is not guaranteed to persist after the containers associated with it stop running.

        Stability:
            stable
        """
        volume: Volume = {"name": name}

        if docker_volume_configuration is not None:
            volume["dockerVolumeConfiguration"] = docker_volume_configuration

        if host is not None:
            volume["host"] = host

        return jsii.invoke(self, "addVolume", [volume])

    @jsii.member(jsii_name="obtainExecutionRole")
    def obtain_execution_role(self) -> aws_cdk.aws_iam.IRole:
        """Creates the task execution IAM role if it doesn't already exist.

        Stability:
            stable
        """
        return jsii.invoke(self, "obtainExecutionRole", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates the task definition.

        Stability:
            stable
        """
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """The task launch type compatiblity requirement.

        Stability:
            stable
        """
        return jsii.get(self, "compatibility")

    @property
    @jsii.member(jsii_name="containers")
    def _containers(self) -> typing.List["ContainerDefinition"]:
        """The container definitions.

        Stability:
            stable
        """
        return jsii.get(self, "containers")

    @property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """The name of a family that this task definition is registered to. A family groups multiple versions of a task definition.

        Stability:
            stable
        """
        return jsii.get(self, "family")

    @property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        Stability:
            stable
        """
        return jsii.get(self, "isEc2Compatible")

    @property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        Stability:
            stable
        """
        return jsii.get(self, "isFargateCompatible")

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The networking mode to use for the containers in the task.

        Stability:
            stable
        """
        return jsii.get(self, "networkMode")

    @property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """The full Amazon Resource Name (ARN) of the task definition.

        Stability:
            stable
        attribute:
            true
        """
        return jsii.get(self, "taskDefinitionArn")

    @property
    @jsii.member(jsii_name="taskRole")
    def task_role(self) -> aws_cdk.aws_iam.IRole:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        Stability:
            stable
        """
        return jsii.get(self, "taskRole")

    @property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role for this task definition.

        Stability:
            stable
        """
        return jsii.get(self, "executionRole")

    @property
    @jsii.member(jsii_name="defaultContainer")
    def default_container(self) -> typing.Optional["ContainerDefinition"]:
        """Default container for this task.

        Load balancers will send traffic to this container. The first
        essential container that is added to this task will become the default
        container.

        Stability:
            stable
        """
        return jsii.get(self, "defaultContainer")

    @default_container.setter
    def default_container(self, value: typing.Optional["ContainerDefinition"]):
        return jsii.set(self, "defaultContainer", value)


@jsii.implements(IEc2TaskDefinition)
class Ec2TaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.Ec2TaskDefinition"):
    """The details of a task definition run on an EC2 cluster.

    Stability:
        stable
    resource:
        AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, network_mode: typing.Optional["NetworkMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the Ec2TaskDefinition class.

        Arguments:
            scope: -
            id: -
            props: -
            network_mode: The Docker networking mode to use for the containers in the task. The valid values are none, bridge, awsvpc, and host. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
            placement_constraints: An array of placement constraint objects to use for the task. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Default: - No placement constraints.
            execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
            family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
            task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
            volumes: The list of volume definitions for the task. For more information, see Task Definition Parameter Volumes: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes] Default: - No volumes are passed to the Docker daemon on a container instance.

        Stability:
            stable
        """
        props: Ec2TaskDefinitionProps = {}

        if network_mode is not None:
            props["networkMode"] = network_mode

        if placement_constraints is not None:
            props["placementConstraints"] = placement_constraints

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(Ec2TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2TaskDefinitionArn")
    @classmethod
    def from_ec2_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, ec2_task_definition_arn: str) -> "IEc2TaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        Arguments:
            scope: -
            id: -
            ec2_task_definition_arn: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromEc2TaskDefinitionArn", [scope, id, ec2_task_definition_arn])


@jsii.implements(IFargateTaskDefinition)
class FargateTaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs.FargateTaskDefinition"):
    """The details of a task definition run on a Fargate cluster.

    Stability:
        stable
    resource:
        AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the FargateTaskDefinition class.

        Arguments:
            scope: -
            id: -
            props: -
            cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 256
            memory_limit_mi_b: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 512
            execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
            family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
            task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
            volumes: The list of volume definitions for the task. For more information, see Task Definition Parameter Volumes: [https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes] Default: - No volumes are passed to the Docker daemon on a container instance.

        Stability:
            stable
        """
        props: FargateTaskDefinitionProps = {}

        if cpu is not None:
            props["cpu"] = cpu

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if execution_role is not None:
            props["executionRole"] = execution_role

        if family is not None:
            props["family"] = family

        if task_role is not None:
            props["taskRole"] = task_role

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(FargateTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateTaskDefinitionArn")
    @classmethod
    def from_fargate_task_definition_arn(cls, scope: aws_cdk.core.Construct, id: str, fargate_task_definition_arn: str) -> "IFargateTaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        Arguments:
            scope: -
            id: -
            fargate_task_definition_arn: -

        Stability:
            stable
        """
        return jsii.sinvoke(cls, "fromFargateTaskDefinitionArn", [scope, id, fargate_task_definition_arn])

    @property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The Docker networking mode to use for the containers in the task.

        Fargate tasks require the awsvpc network mode.

        Stability:
            stable
        """
        return jsii.get(self, "networkMode")


@jsii.data_type_optionals(jsii_struct_bases=[CommonTaskDefinitionProps])
class _TaskDefinitionProps(CommonTaskDefinitionProps, jsii.compat.TypedDict, total=False):
    cpu: str
    """The number of cpu units used by the task.

    If you are using the EC2 launch type, this field is optional and any value can be used.
    If you are using the Fargate launch type, this field is required and you must use one of the following values,
    which determines your range of valid values for the memory parameter:

    256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
    512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
    1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
    2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
    4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

    Default:
        - CPU units are not specified.

    Stability:
        stable
    """
    memoryMiB: str
    """The amount (in MiB) of memory used by the task.

    If using the EC2 launch type, this field is optional and any value can be used.
    If using the Fargate launch type, this field is required and you must use one of the following values,
    which determines your range of valid values for the cpu parameter:

    512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
    1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
    2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
    Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
    Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

    Default:
        - Memory used by task is not specified.

    Stability:
        stable
    """
    networkMode: "NetworkMode"
    """The networking mode to use for the containers in the task.

    On Fargate, the only supported networking mode is AwsVpc.

    Default:
        - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.

    Stability:
        stable
    """
    placementConstraints: typing.List["PlacementConstraint"]
    """The placement constraints to use for tasks in the service.

    You can specify a maximum of 10 constraints per task (this limit includes
    constraints in the task definition and those specified at run time).

    Not supported in Fargate.

    Default:
        - No placement constraints.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TaskDefinitionProps", jsii_struct_bases=[_TaskDefinitionProps])
class TaskDefinitionProps(_TaskDefinitionProps):
    """The properties for task definitions.

    Stability:
        stable
    """
    compatibility: "Compatibility"
    """The task launch type compatiblity requirement.

    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _Tmpfs(jsii.compat.TypedDict, total=False):
    mountOptions: typing.List["TmpfsMountOption"]
    """The list of tmpfs volume mount options.

    For more information, see TmpfsMountOptions:
    [https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html]

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Tmpfs", jsii_struct_bases=[_Tmpfs])
class Tmpfs(_Tmpfs):
    """The details of a tmpfs mount for a container.

    Stability:
        stable
    """
    containerPath: str
    """The absolute file path where the tmpfs volume is to be mounted.

    Stability:
        stable
    """

    size: jsii.Number
    """The size (in MiB) of the tmpfs volume.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.TmpfsMountOption")
class TmpfsMountOption(enum.Enum):
    """The supported options for a tmpfs mount for a container.

    Stability:
        stable
    """
    DEFAULTS = "DEFAULTS"
    """
    Stability:
        stable
    """
    RO = "RO"
    """
    Stability:
        stable
    """
    RW = "RW"
    """
    Stability:
        stable
    """
    SUID = "SUID"
    """
    Stability:
        stable
    """
    NOSUID = "NOSUID"
    """
    Stability:
        stable
    """
    DEV = "DEV"
    """
    Stability:
        stable
    """
    NODEV = "NODEV"
    """
    Stability:
        stable
    """
    EXEC = "EXEC"
    """
    Stability:
        stable
    """
    NOEXEC = "NOEXEC"
    """
    Stability:
        stable
    """
    SYNC = "SYNC"
    """
    Stability:
        stable
    """
    ASYNC = "ASYNC"
    """
    Stability:
        stable
    """
    DIRSYNC = "DIRSYNC"
    """
    Stability:
        stable
    """
    REMOUNT = "REMOUNT"
    """
    Stability:
        stable
    """
    MAND = "MAND"
    """
    Stability:
        stable
    """
    NOMAND = "NOMAND"
    """
    Stability:
        stable
    """
    ATIME = "ATIME"
    """
    Stability:
        stable
    """
    NOATIME = "NOATIME"
    """
    Stability:
        stable
    """
    DIRATIME = "DIRATIME"
    """
    Stability:
        stable
    """
    NODIRATIME = "NODIRATIME"
    """
    Stability:
        stable
    """
    BIND = "BIND"
    """
    Stability:
        stable
    """
    RBIND = "RBIND"
    """
    Stability:
        stable
    """
    UNBINDABLE = "UNBINDABLE"
    """
    Stability:
        stable
    """
    RUNBINDABLE = "RUNBINDABLE"
    """
    Stability:
        stable
    """
    PRIVATE = "PRIVATE"
    """
    Stability:
        stable
    """
    RPRIVATE = "RPRIVATE"
    """
    Stability:
        stable
    """
    SHARED = "SHARED"
    """
    Stability:
        stable
    """
    RSHARED = "RSHARED"
    """
    Stability:
        stable
    """
    SLAVE = "SLAVE"
    """
    Stability:
        stable
    """
    RSLAVE = "RSLAVE"
    """
    Stability:
        stable
    """
    RELATIME = "RELATIME"
    """
    Stability:
        stable
    """
    NORELATIME = "NORELATIME"
    """
    Stability:
        stable
    """
    STRICTATIME = "STRICTATIME"
    """
    Stability:
        stable
    """
    NOSTRICTATIME = "NOSTRICTATIME"
    """
    Stability:
        stable
    """
    MODE = "MODE"
    """
    Stability:
        stable
    """
    UID = "UID"
    """
    Stability:
        stable
    """
    GID = "GID"
    """
    Stability:
        stable
    """
    NR_INODES = "NR_INODES"
    """
    Stability:
        stable
    """
    NR_BLOCKS = "NR_BLOCKS"
    """
    Stability:
        stable
    """
    MPOL = "MPOL"
    """
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.TrackCustomMetricProps", jsii_struct_bases=[aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps])
class TrackCustomMetricProps(aws_cdk.aws_applicationautoscaling.BaseTargetTrackingProps, jsii.compat.TypedDict):
    """The properties for enabling target tracking scaling based on a custom CloudWatch metric.

    Stability:
        stable
    """
    metric: aws_cdk.aws_cloudwatch.IMetric
    """The custom CloudWatch metric to track.

    The metric must represent utilization; that is, you will always get the following behavior:

    - metric > targetValue => scale out
    - metric < targetValue => scale in

    Stability:
        stable
    """

    targetValue: jsii.Number
    """The target value for the custom CloudWatch metric.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Ulimit", jsii_struct_bases=[])
class Ulimit(jsii.compat.TypedDict):
    """The ulimit settings to pass to the container.

    NOTE: Does not work for Windows containers.

    Stability:
        stable
    """
    hardLimit: jsii.Number
    """The hard limit for the ulimit type.

    Stability:
        stable
    """

    name: "UlimitName"
    """The type of the ulimit.

    For more information, see UlimitName:
    [https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName]

    Stability:
        stable
    """

    softLimit: jsii.Number
    """The soft limit for the ulimit type.

    Stability:
        stable
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ecs.UlimitName")
class UlimitName(enum.Enum):
    """Type of resource to set a limit on.

    Stability:
        stable
    """
    CORE = "CORE"
    """
    Stability:
        stable
    """
    CPU = "CPU"
    """
    Stability:
        stable
    """
    DATA = "DATA"
    """
    Stability:
        stable
    """
    FSIZE = "FSIZE"
    """
    Stability:
        stable
    """
    LOCKS = "LOCKS"
    """
    Stability:
        stable
    """
    MEMLOCK = "MEMLOCK"
    """
    Stability:
        stable
    """
    MSGQUEUE = "MSGQUEUE"
    """
    Stability:
        stable
    """
    NICE = "NICE"
    """
    Stability:
        stable
    """
    NOFILE = "NOFILE"
    """
    Stability:
        stable
    """
    NPROC = "NPROC"
    """
    Stability:
        stable
    """
    RSS = "RSS"
    """
    Stability:
        stable
    """
    RTPRIO = "RTPRIO"
    """
    Stability:
        stable
    """
    RTTIME = "RTTIME"
    """
    Stability:
        stable
    """
    SIGPENDING = "SIGPENDING"
    """
    Stability:
        stable
    """
    STACK = "STACK"
    """
    Stability:
        stable
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _Volume(jsii.compat.TypedDict, total=False):
    dockerVolumeConfiguration: "DockerVolumeConfiguration"
    """This property is specified when you are using Docker volumes.

    Docker volumes are only supported when you are using the EC2 launch type.
    Windows containers only support the use of the local driver.
    To use bind mounts, specify a host instead.

    Stability:
        stable
    """
    host: "Host"
    """This property is specified when you are using bind mount host volumes.

    Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types.
    The contents of the host parameter determine whether your bind mount host volume persists on the
    host container instance and where it is stored. If the host parameter is empty, then the Docker
    daemon assigns a host path for your data volume. However, the data is not guaranteed to persist
    after the containers associated with it stop running.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.Volume", jsii_struct_bases=[_Volume])
class Volume(_Volume):
    """A data volume used in a task definition.

    For tasks that use a Docker volume, specify a DockerVolumeConfiguration.
    For tasks that use a bind mount host volume, specify a host and optional sourcePath.

    For more information, see Using Data Volumes in Tasks:
    [https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html]

    Stability:
        stable
    """
    name: str
    """The name of the volume.

    Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed.
    This name is referenced in the sourceVolume parameter of container definition mountPoints.

    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs.VolumeFrom", jsii_struct_bases=[])
class VolumeFrom(jsii.compat.TypedDict):
    """The details on a data volume from another container in the same task definition.

    Stability:
        stable
    """
    readOnly: bool
    """Specifies whether the container has read-only access to the volume.

    If this value is true, the container has read-only access to the volume.
    If this value is false, then the container can write to the volume.

    Stability:
        stable
    """

    sourceContainer: str
    """The name of another container within the same task definition from which to mount volumes.

    Stability:
        stable
    """

__all__ = ["AddAutoScalingGroupCapacityOptions", "AddCapacityOptions", "AmiHardwareType", "AssetImage", "AssetImageProps", "AwsLogDriver", "AwsLogDriverProps", "BaseService", "BaseServiceOptions", "BaseServiceProps", "BinPackResource", "BuiltInAttributes", "Capability", "CfnCluster", "CfnClusterProps", "CfnService", "CfnServiceProps", "CfnTaskDefinition", "CfnTaskDefinitionProps", "CloudMapNamespaceOptions", "CloudMapOptions", "Cluster", "ClusterAttributes", "ClusterProps", "CommonTaskDefinitionProps", "Compatibility", "ContainerDefinition", "ContainerDefinitionOptions", "ContainerDefinitionProps", "ContainerImage", "ContainerImageConfig", "CpuUtilizationScalingProps", "Device", "DevicePermission", "DockerVolumeConfiguration", "Ec2Service", "Ec2ServiceProps", "Ec2TaskDefinition", "Ec2TaskDefinitionProps", "EcrImage", "EcsOptimizedAmi", "EcsOptimizedAmiProps", "FargatePlatformVersion", "FargateService", "FargateServiceProps", "FargateTaskDefinition", "FargateTaskDefinitionProps", "HealthCheck", "Host", "ICluster", "IEc2Service", "IEc2TaskDefinition", "IFargateService", "IFargateTaskDefinition", "IService", "ITaskDefinition", "ITaskDefinitionExtension", "LaunchType", "LinuxParameters", "LinuxParametersProps", "LogDriver", "LogDriverConfig", "MemoryUtilizationScalingProps", "MountPoint", "NetworkMode", "PlacementConstraint", "PlacementStrategy", "PortMapping", "Protocol", "RepositoryImage", "RepositoryImageProps", "RequestCountScalingProps", "ScalableTaskCount", "ScalableTaskCountProps", "Scope", "ScratchSpace", "TaskDefinition", "TaskDefinitionProps", "Tmpfs", "TmpfsMountOption", "TrackCustomMetricProps", "Ulimit", "UlimitName", "Volume", "VolumeFrom", "__jsii_assembly__"]

publication.publish()
