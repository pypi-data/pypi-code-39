from dataclasses import field, asdict
from typing import Optional, Any
from pydantic import validator
from pydantic.dataclasses import dataclass
from netapi.metadata import Metadata, DataConfig, HidePrivateAttrs
from netapi.units import unit_validator
from netapi.probe.utils import addresser
from netaddr import IPAddress


def default_ping_analysis(packet_loss):
    result = {}
    if packet_loss < 1.0:
        if packet_loss != 0.0:
            result.update(status="warning", status_up=True, status_code=1)
        else:
            result.update(status="ok", status_up=True, status_code=0)
    else:
        result.update(status="critical", status_up=False, status_code=2)

    return result


@dataclass(unsafe_hash=True, config=DataConfig)  # type: ignore
class PingResult:
    """
    Ping results from execution.

    Attributes:

    - `probes_sent`: (int) Number of probes sent
    - `probes_received`: (int) Number of probes received
    - `packet_loss`: (float) percentage of packet loss on the ping execution. /100
    - `rtt_min`: (float) Minimum RTT encountered
    - `rtt_avg`: (float) Average RTT encountered
    - `rtt_max`: (float) Maximum RTT encountered
    - `warning_thld` (int) Percentage when the ping execution packet loss is considered
    warning. i.e. 80 (meaning 80%)
    - `critical_thld` (int) Percentage when the ping execution packet loss is considered
    critical. i.e. 80 (meaning 80%)
    - `status`: (str) ok/warning/critical/no-route reflecting the status of the result
    - `status_code`: (int) same as `status` but in numbers for visualization (0/1/2/3).
    Result of analysis applied
    - `status_up`: (bool) Flag if the ping was successful in overall. Result of analysis
    applied
    """

    probes_sent: int
    probes_received: int
    packet_loss: float
    rtt_min: Optional[float] = None
    rtt_avg: Optional[float] = None
    rtt_max: Optional[float] = None
    warning_thld: Optional[int] = None
    critical_thld: Optional[int] = None
    status: Optional[str] = None
    status_up: Optional[bool] = None
    status_code: Optional[int] = None
    apply_analysis: bool = False

    @validator("packet_loss")
    def valid_packet_loss(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("Packet loss must be between 0.0 and 1.0")
        return v

    @validator("apply_analysis")
    def applies_result_analysis(cls, v, values):
        if v is True:
            _warning = values.get("warning_thld")
            _critical = values.get("critical_thld")
            if _warning is None and _critical is None:
                values.update(**default_ping_analysis(values["packet_loss"]))
            else:
                _analysed = False
                if _critical:
                    if values["packet_loss"] * 100 > _critical:
                        values.update(status="critical", status_up=False, status_code=2)
                        _analysed = True
                if _warning and not _analysed:
                    if values["packet_loss"] * 100 > _warning:
                        values.update(status="warning", status_up=True, status_code=1)
                        _analysed = True
                    else:
                        if not _analysed:
                            values.update(status="ok", status_up=True, status_code=0)
                            _analysed = True
                if not _analysed:
                    values.update(**default_ping_analysis(values["packet_loss"]))
        return v


@dataclass(unsafe_hash=True, config=DataConfig)  # type: ignore
class PingBase:
    """
    Ping instance creator. It creates a ping object based on parameters passed to it for
    construction.

    Attributes:
    - `target` (str): IP or Host target
    - `target_ip` (IPAddress): IP address of target (Optional)
    - `target_name` (str): Hostname of target (Optional)
    - `resolve_target` (bool): Resolve IP address and name assigned to attributes
    - for the likes of `target_ip` and `target_name`
    - `source` (str): Interface/Name source of the request
    - `source_ip` (IPAddress): IP Address of the source of the request
    - `instance` (str): instance/vrf for the ping object
    - `count` (int): Number of probes
    - `timeout` (int): Timeout for when a probe is marked as unreachable
    - `size` (int): Packet size of the ping probes
    - `df_bit` (bool): Do not fragment bit to be set
    - `interval` (float): Time interval between each probe
    - `ttl` (int): Time-to-live value for the probes
    - `result`: (PingResult) result object of the execution
    - `connector`: Device object used to perform the necessary connection.
    - `metadata`: Metadata object which contains information about the current object.
    - `ping_cmd`: Ping command to be used for execution
    """

    target: str
    target_ip: Optional[Any] = None
    target_name: Optional[str] = None
    resolve_target: bool = False
    source: Optional[str] = None
    source_ip: Optional[Any] = None
    instance: Optional[str] = None
    count: int = 5
    timeout: int = 2
    size: int = 692
    df_bit: bool = False
    interval: float = 1.0
    ttl: Optional[int] = None
    result: Optional[PingResult] = None
    connector: Optional[Any] = field(default=None, repr=False)
    metadata: Optional[Any] = field(default=None, repr=False)
    ping_cmd: Optional[Any] = field(default=None, repr=False)

    @validator("source_ip", "target_ip")
    def valid_ip(cls, value):
        return unit_validator("netaddr.ip.IPAddress", "IPAddress", value)

    @validator("resolve_target")
    def valid_resolve_targets(cls, v, values):
        """
        It sets `target_ip` and `target_name` if any one of them is not set and
        `resolve_target` is True
        """
        if v is True:
            if values.get("target_ip") is None or values.get("target_name") is None:
                _ip, values["target_name"] = addresser(
                    values["target"], dns_query_attempt=3
                )
                values["target_ip"] = IPAddress(_ip)
        return v

    def __post_init__(self, **_ignore):
        self.metadata = Metadata(name="ping", type="entity")
        if self.connector:
            if not hasattr(self.connector, "metadata"):
                raise ValueError(
                    f"It does not contain metadata attribute: {self.connector}"
                )
            if self.connector.metadata.name != "device":
                raise ValueError(
                    f"It is not a valid connector object: {self.connector}"
                )

    def to_dict(self):
        return asdict(self, dict_factory=HidePrivateAttrs)


class PingsBase:
    ENTITY = "ping"

    def __init__(self, *args, **kwargs):
        super().__init__(entity=self.ENTITY, *args, **kwargs)
        self.metadata = Metadata(name="pings", type="collection")

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, entity=self.ENTITY, **kwargs)
