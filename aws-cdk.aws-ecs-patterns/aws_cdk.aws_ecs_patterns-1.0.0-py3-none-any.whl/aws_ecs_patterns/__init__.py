import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.aws_route53_targets
import aws_cdk.aws_sqs
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs-patterns", "1.0.0", __name__, "aws-ecs-patterns@1.0.0.jsii.tgz")
class LoadBalancedServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedServiceBase"):
    """Base class for load-balanced Fargate and ECS services.

    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _LoadBalancedServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false

        stability
        :stability: experimental
        """
        props = LoadBalancedServiceBaseProps(cluster=cluster, image=image, certificate=certificate, container_port=container_port, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_logging=enable_logging, environment=environment, load_balancer_type=load_balancer_type, public_load_balancer=public_load_balancer, public_tasks=public_tasks)

        jsii.create(LoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """
        :param service: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @property
    @jsii.member(jsii_name="listener")
    def listener(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationListener, aws_cdk.aws_elasticloadbalancingv2.NetworkListener]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "listener")

    @property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.BaseLoadBalancer:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancer")

    @property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> "LoadBalancerType":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancerType")

    @property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> typing.Union[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup, aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "targetGroup")

    @property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriver")


class _LoadBalancedServiceBaseProxy(LoadBalancedServiceBase):
    pass

class LoadBalancedEc2Service(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedEc2Service"):
    """A single task running on an ECS cluster fronted by a load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false

        stability
        :stability: experimental
        """
        props = LoadBalancedEc2ServiceProps(memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, cluster=cluster, image=image, certificate=certificate, container_port=container_port, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_logging=enable_logging, environment=environment, load_balancer_type=load_balancer_type, public_load_balancer=public_load_balancer, public_tasks=public_tasks)

        jsii.create(LoadBalancedEc2Service, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The ECS service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")


class LoadBalancedFargateService(LoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by a load balancer.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, container_name: typing.Optional[str]=None, cpu: typing.Optional[jsii.Number]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, service_name: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param container_name: Override value for the container name. Default: - No value
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param execution_role: Override for the Fargate Task Definition execution role. Default: - No value
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param service_name: Override value for the service name. Default: CloudFormation-generated name
        :param task_role: Override for the Fargate Task Definition task role. Default: - No value
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false

        stability
        :stability: experimental
        """
        props = LoadBalancedFargateServiceProps(container_name=container_name, cpu=cpu, execution_role=execution_role, memory_limit_mib=memory_limit_mib, service_name=service_name, task_role=task_role, cluster=cluster, image=image, certificate=certificate, container_port=container_port, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_logging=enable_logging, environment=environment, load_balancer_type=load_balancer_type, public_load_balancer=public_load_balancer, public_tasks=public_tasks)

        jsii.create(LoadBalancedFargateService, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedServiceBaseProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'image': 'image', 'certificate': 'certificate', 'container_port': 'containerPort', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_logging': 'enableLogging', 'environment': 'environment', 'load_balancer_type': 'loadBalancerType', 'public_load_balancer': 'publicLoadBalancer', 'public_tasks': 'publicTasks'})
class LoadBalancedServiceBaseProps():
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None):
        """Base properties for load-balanced Fargate and ECS services.

        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if container_port is not None: self._values["container_port"] = container_port
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if load_balancer_type is not None: self._values["load_balancer_type"] = load_balancer_type
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if public_tasks is not None: self._values["public_tasks"] = public_tasks

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443.

        default
        :default: - No certificate associated with the load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The container port of the application load balancer attached to your Fargate service.

        Corresponds to container port mapping.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @property
    def domain_name(self) -> typing.Optional[str]:
        """Domain name for the service, e.g. api.example.com.

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Whether to create an AWS log driver.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def load_balancer_type(self) -> typing.Optional["LoadBalancerType"]:
        """Whether to create an application load balancer or a network load balancer.

        default
        :default: application

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer_type')

    @property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Application Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @property
    def public_tasks(self) -> typing.Optional[bool]:
        """Determines whether your Fargate Service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('public_tasks')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancedServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedEc2ServiceProps", jsii_struct_bases=[LoadBalancedServiceBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'certificate': 'certificate', 'container_port': 'containerPort', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_logging': 'enableLogging', 'environment': 'environment', 'load_balancer_type': 'loadBalancerType', 'public_load_balancer': 'publicLoadBalancer', 'public_tasks': 'publicTasks', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class LoadBalancedEc2ServiceProps(LoadBalancedServiceBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None):
        """Properties for a LoadBalancedEc2Service.

        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if container_port is not None: self._values["container_port"] = container_port
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if load_balancer_type is not None: self._values["load_balancer_type"] = load_balancer_type
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if public_tasks is not None: self._values["public_tasks"] = public_tasks
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443.

        default
        :default: - No certificate associated with the load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The container port of the application load balancer attached to your Fargate service.

        Corresponds to container port mapping.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @property
    def domain_name(self) -> typing.Optional[str]:
        """Domain name for the service, e.g. api.example.com.

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Whether to create an AWS log driver.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def load_balancer_type(self) -> typing.Optional["LoadBalancerType"]:
        """Whether to create an application load balancer or a network load balancer.

        default
        :default: application

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer_type')

    @property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Application Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @property
    def public_tasks(self) -> typing.Optional[bool]:
        """Determines whether your Fargate Service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('public_tasks')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancedEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancedFargateServiceProps", jsii_struct_bases=[LoadBalancedServiceBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'certificate': 'certificate', 'container_port': 'containerPort', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_logging': 'enableLogging', 'environment': 'environment', 'load_balancer_type': 'loadBalancerType', 'public_load_balancer': 'publicLoadBalancer', 'public_tasks': 'publicTasks', 'container_name': 'containerName', 'cpu': 'cpu', 'execution_role': 'executionRole', 'memory_limit_mib': 'memoryLimitMiB', 'service_name': 'serviceName', 'task_role': 'taskRole'})
class LoadBalancedFargateServiceProps(LoadBalancedServiceBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, container_port: typing.Optional[jsii.Number]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, load_balancer_type: typing.Optional["LoadBalancerType"]=None, public_load_balancer: typing.Optional[bool]=None, public_tasks: typing.Optional[bool]=None, container_name: typing.Optional[str]=None, cpu: typing.Optional[jsii.Number]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, service_name: typing.Optional[str]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Properties for a LoadBalancedFargateService.

        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443. Default: - No certificate associated with the load balancer.
        :param container_port: The container port of the application load balancer attached to your Fargate service. Corresponds to container port mapping. Default: 80
        :param desired_count: Number of desired copies of running tasks. Default: 1
        :param domain_name: Domain name for the service, e.g. api.example.com. Default: - No domain name.
        :param domain_zone: Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_logging: Whether to create an AWS log driver. Default: true
        :param environment: Environment variables to pass to the container. Default: - No environment variables.
        :param load_balancer_type: Whether to create an application load balancer or a network load balancer. Default: application
        :param public_load_balancer: Determines whether the Application Load Balancer will be internet-facing. Default: true
        :param public_tasks: Determines whether your Fargate Service will be assigned a public IP address. Default: false
        :param container_name: Override value for the container name. Default: - No value
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param execution_role: Override for the Fargate Task Definition execution role. Default: - No value
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param service_name: Override value for the service name. Default: CloudFormation-generated name
        :param task_role: Override for the Fargate Task Definition task role. Default: - No value

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if container_port is not None: self._values["container_port"] = container_port
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if load_balancer_type is not None: self._values["load_balancer_type"] = load_balancer_type
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if public_tasks is not None: self._values["public_tasks"] = public_tasks
        if container_name is not None: self._values["container_name"] = container_name
        if cpu is not None: self._values["cpu"] = cpu
        if execution_role is not None: self._values["execution_role"] = execution_role
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if service_name is not None: self._values["service_name"] = service_name
        if task_role is not None: self._values["task_role"] = task_role

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer port to 443.

        default
        :default: - No certificate associated with the load balancer.

        stability
        :stability: experimental
        """
        return self._values.get('certificate')

    @property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The container port of the application load balancer attached to your Fargate service.

        Corresponds to container port mapping.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @property
    def domain_name(self) -> typing.Optional[str]:
        """Domain name for the service, e.g. api.example.com.

        default
        :default: - No domain name.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.

        stability
        :stability: experimental
        """
        return self._values.get('domain_zone')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Whether to create an AWS log driver.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """Environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def load_balancer_type(self) -> typing.Optional["LoadBalancerType"]:
        """Whether to create an application load balancer or a network load balancer.

        default
        :default: application

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer_type')

    @property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Application Load Balancer will be internet-facing.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('public_load_balancer')

    @property
    def public_tasks(self) -> typing.Optional[bool]:
        """Determines whether your Fargate Service will be assigned a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('public_tasks')

    @property
    def container_name(self) -> typing.Optional[str]:
        """Override value for the container name.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Override for the Fargate Task Definition execution role.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

        1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

        2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

        Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

        Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @property
    def service_name(self) -> typing.Optional[str]:
        """Override value for the service name.

        default
        :default: CloudFormation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Override for the Fargate Task Definition task role.

        default
        :default: - No value

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancedFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-ecs-patterns.LoadBalancerType")
class LoadBalancerType(enum.Enum):
    """
    stability
    :stability: experimental
    """
    APPLICATION = "APPLICATION"
    """
    stability
    :stability: experimental
    """
    NETWORK = "NETWORK"
    """
    stability
    :stability: experimental
    """

class QueueProcessingServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBase"):
    """Base class for a Fargate and ECS queue processing service.

    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _QueueProcessingServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        props = QueueProcessingServiceBaseProps(cluster=cluster, image=image, command=command, desired_task_count=desired_task_count, enable_logging=enable_logging, environment=environment, max_scaling_capacity=max_scaling_capacity, queue=queue, scaling_steps=scaling_steps)

        jsii.create(QueueProcessingServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="configureAutoscalingForService")
    def _configure_autoscaling_for_service(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Configure autoscaling based off of CPU utilization as well as the number of messages visible in the SQS queue.

        :param service: the ECS/Fargate service for which to apply the autoscaling rules to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "configureAutoscalingForService", [service])

    @property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The minimum number of tasks to run.

        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredCount")

    @property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[str,str]:
        """Environment variables that will include the queue name.

        stability
        :stability: experimental
        """
        return jsii.get(self, "environment")

    @property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        """The maximum number of instances for autoscaling to scale up to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "maxCapacity")

    @property
    @jsii.member(jsii_name="scalingSteps")
    def scaling_steps(self) -> typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]:
        """The scaling interval for autoscaling based off an SQS Queue size.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scalingSteps")

    @property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS queue that the service will process from.

        stability
        :stability: experimental
        """
        return jsii.get(self, "sqsQueue")

    @property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The AwsLogDriver to use for logging if logging is enabled.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriver")


class _QueueProcessingServiceBaseProxy(QueueProcessingServiceBase):
    pass

class QueueProcessingEc2Service(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2Service"):
    """Class to create a queue processing Ec2 service.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        props = QueueProcessingEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, cluster=cluster, image=image, command=command, desired_task_count=desired_task_count, enable_logging=enable_logging, environment=environment, max_scaling_capacity=max_scaling_capacity, queue=queue, scaling_steps=scaling_steps)

        jsii.create(QueueProcessingEc2Service, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The ECS service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")


class QueueProcessingFargateService(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateService"):
    """Class to create a queue processing Fargate service.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        props = QueueProcessingFargateServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, cluster=cluster, image=image, command=command, desired_task_count=desired_task_count, enable_logging=enable_logging, environment=environment, max_scaling_capacity=max_scaling_capacity, queue=queue, scaling_steps=scaling_steps)

        jsii.create(QueueProcessingFargateService, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct.

        stability
        :stability: experimental
        """
        return jsii.get(self, "service")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBaseProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'image': 'image', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_logging': 'enableLogging', 'environment': 'environment', 'max_scaling_capacity': 'maxScalingCapacity', 'queue': 'queue', 'scaling_steps': 'scalingSteps'})
class QueueProcessingServiceBaseProps():
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None):
        """Properties to define a queue processing service.

        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """Cluster where service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'.

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        see
        :see: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior.
        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2ServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_logging': 'enableLogging', 'environment': 'environment', 'max_scaling_capacity': 'maxScalingCapacity', 'queue': 'queue', 'scaling_steps': 'scalingSteps', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class QueueProcessingEc2ServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None):
        """Properties to define a queue processing Ec2 service.

        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """Cluster where service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'.

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        see
        :see: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior.
        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_logging': 'enableLogging', 'environment': 'environment', 'max_scaling_capacity': 'maxScalingCapacity', 'queue': 'queue', 'scaling_steps': 'scalingSteps', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class QueueProcessingFargateServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None):
        """Properties to define a queue processing Fargate service.

        :param cluster: Cluster where service will be deployed.
        :param image: The image to start.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: 'QUEUE_NAME: queue.queueName'
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """Cluster where service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enable_logging')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: 'QUEUE_NAME: queue.queueName'

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)

        stability
        :stability: experimental
        """
        return self._values.get('max_scaling_capacity')

    @property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'.

        default
        :default: 'SQSQueue with CloudFormation-generated name'

        see
        :see: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
        stability
        :stability: experimental
        """
        return self._values.get('queue')

    @property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior.
        https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]

        stability
        :stability: experimental
        """
        return self._values.get('scaling_steps')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

        1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

        2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

        Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

        Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScheduledTaskBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBase"):
    """A scheduled task base that will be initiated off of cloudwatch events.

    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ScheduledTaskBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none

        stability
        :stability: experimental
        """
        props = ScheduledTaskBaseProps(cluster=cluster, image=image, schedule=schedule, command=command, desired_task_count=desired_task_count, environment=environment)

        jsii.create(ScheduledTaskBase, self, [scope, id, props])

    @jsii.member(jsii_name="addTaskDefinitionToEventTarget")
    def _add_task_definition_to_event_target(self, task_definition: aws_cdk.aws_ecs.TaskDefinition) -> aws_cdk.aws_events_targets.EcsTask:
        """Create an ecs task using the task definition provided and add it to the scheduled event rule.

        :param task_definition: the TaskDefinition to add to the event rule.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addTaskDefinitionToEventTarget", [task_definition])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """Create an AWS Log Driver with the provided streamPrefix.

        :param prefix: the Cloudwatch logging prefix.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @property
    @jsii.member(jsii_name="desiredTaskCount")
    def desired_task_count(self) -> jsii.Number:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "desiredTaskCount")

    @property
    @jsii.member(jsii_name="eventRule")
    def event_rule(self) -> aws_cdk.aws_events.Rule:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "eventRule")


class _ScheduledTaskBaseProxy(ScheduledTaskBase):
    pass

class ScheduledEc2Task(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2Task"):
    """A scheduled Ec2 task that will be initiated off of cloudwatch events.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cpu: The minimum number of CPU units to reserve for the container. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none

        stability
        :stability: experimental
        """
        props = ScheduledEc2TaskProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, cluster=cluster, image=image, schedule=schedule, command=command, desired_task_count=desired_task_count, environment=environment)

        jsii.create(ScheduledEc2Task, self, [scope, id, props])


class ScheduledFargateTask(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTask"):
    """A scheduled Fargate task that will be initiated off of cloudwatch events.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: 512
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none

        stability
        :stability: experimental
        """
        props = ScheduledFargateTaskProps(cpu=cpu, memory_limit_mib=memory_limit_mib, cluster=cluster, image=image, schedule=schedule, command=command, desired_task_count=desired_task_count, environment=environment)

        jsii.create(ScheduledFargateTask, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBaseProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'image': 'image', 'schedule': 'schedule', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'environment': 'environment'})
class ScheduledTaskBaseProps():
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None):
        """
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
            'schedule': schedule,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if environment is not None: self._values["environment"] = environment

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon CloudWatch User Guide.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledTaskBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'schedule': 'schedule', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'environment': 'environment', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class ScheduledEc2TaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None):
        """
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none
        :param cpu: The minimum number of CPU units to reserve for the container. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
            'schedule': schedule,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if environment is not None: self._values["environment"] = environment
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon CloudWatch User Guide.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'cluster': 'cluster', 'image': 'image', 'schedule': 'schedule', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'environment': 'environment', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class ScheduledFargateTaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule: aws_cdk.aws_events.Schedule, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None):
        """
        :param cluster: The cluster where your service will be deployed.
        :param image: The image to start.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
        :param command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
        :param desired_task_count: Number of desired copies of running tasks. Default: 1
        :param environment: The environment variables to pass to the container. Default: none
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments. This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: 512

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'image': image,
            'schedule': schedule,
        }
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if environment is not None: self._values["environment"] = environment
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image to start.

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @property
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see Schedule Expression Syntax for
        Rules in the Amazon CloudWatch User Guide.

        see
        :see: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
        stability
        :stability: experimental
        """
        return self._values.get('schedule')

    @property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The CMD value to pass to the container.

        A string with commands delimited by commas.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """Number of desired copies of running tasks.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_task_count')

    @property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments.

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["LoadBalancedEc2Service", "LoadBalancedEc2ServiceProps", "LoadBalancedFargateService", "LoadBalancedFargateServiceProps", "LoadBalancedServiceBase", "LoadBalancedServiceBaseProps", "LoadBalancerType", "QueueProcessingEc2Service", "QueueProcessingEc2ServiceProps", "QueueProcessingFargateService", "QueueProcessingFargateServiceProps", "QueueProcessingServiceBase", "QueueProcessingServiceBaseProps", "ScheduledEc2Task", "ScheduledEc2TaskProps", "ScheduledFargateTask", "ScheduledFargateTaskProps", "ScheduledTaskBase", "ScheduledTaskBaseProps", "__jsii_assembly__"]

publication.publish()
