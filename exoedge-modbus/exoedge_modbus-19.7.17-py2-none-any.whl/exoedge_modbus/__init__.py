"""
    An ExoEdge source for interfacing with Modbus TCP devices.
"""
# pylint: disable=I0011,W0312,C0301,C0103,W0123,W1202,C0326,C0111,R0911,R0913,R0914
import sys
import time
import logging
import threading
from os import environ
from .__version__ import __version__
from exoedge_modbus.lib import \
    ExositeModbusTCP, \
    ExositeModbusRTU, \
    ExoEdgeModbusException, \
    REGISTER_NUMBER_MAP
from exoedge.sources import ExoEdgeSource
from exoedge import logger
from murano_client.client import WatchQueue
from pymodbus.exceptions import ModbusException
from pymodbus.constants import Endian

LOG = logger.getLogger(__name__, level=logging.getLogger('exoedge').getEffectiveLevel())

REGISTER_NUMBER_TO_ADDRESS_OFFSET=-1
class ModbusExoEdgeSource(ExoEdgeSource):
    """ Exoedge Modbus source."""

    def run(self):

        modbus_tcp_channels = {e.name: e for e in self.get_channels_by_application("Modbus_TCP")}
        modbus_rtu_channels = {e.name: e for e in self.get_channels_by_application("Modbus_RTU")}

        configured_applications = self.get_configured_applications()
        if modbus_rtu_channels:
            while not configured_applications:
                LOG.critical("Resource 'config_applications' not set for RTU channels.")
                configured_applications = self.get_configured_applications()
                time.sleep(1.0)

        for channel in modbus_tcp_channels.values():
            modbus_kwargs = {
                'ip_address': channel.protocol_config.app_specific_config['ip_address'],
                'port': int(channel.protocol_config.app_specific_config['port'])
            }
            setattr(
                channel,
                'client',
                # TODO: these modbus clients should be grouped
                # together better in a map and then referenced
                # by channels
                ExositeModbusTCP(**modbus_kwargs)
            )
            setattr(
                channel.client,
                'eval_kwargs',
                {
                    'data_address': REGISTER_NUMBER_MAP[
                        channel.protocol_config.app_specific_config['register_range']
                        ]['range'][0] + int(channel.protocol_config.app_specific_config['register_number']) + REGISTER_NUMBER_TO_ADDRESS_OFFSET,
                    'register_count': int(channel.protocol_config.app_specific_config['register_count']),
                    'value': None,  # not used/implimented for read operations
                    'byte_endianness': channel.protocol_config.app_specific_config['byte_endianness'],
                    'register_endianness': channel.protocol_config.app_specific_config['register_endianness'],
                    'evaluation_mode': channel.protocol_config.app_specific_config['evaluation_mode'],
                    'bitmask': channel.protocol_config.app_specific_config['bitmask'],
                }
            )
            LOG.critical("channel.client.eval_kwargs: {!r}".format(channel.client.eval_kwargs))

        for channel in modbus_rtu_channels.values():
            application_config = configured_applications.get('applications')
            modbus_rtu_configuration = application_config.get('Modbus_RTU')

            channel_modbus_kwargs = None
            for iface in modbus_rtu_configuration.get("interfaces"):
                if iface.get("interface") == channel.protocol_config.interface:
                    channel_modbus_kwargs = iface
            if not channel_modbus_kwargs:
                channel.put_channel_error("config_applications not configured for Modbus_RTU")
                break
            modbus_kwargs = {
                'slave_id': channel.protocol_config.app_specific_config['slave_id'],
            }
            modbus_kwargs.update(channel_modbus_kwargs)
            LOG.critical("modbus_kwargs: {}".format(modbus_kwargs))
            setattr(
                channel,
                'client',
                # TODO: these modbus clients should be grouped
                # together better in a map and then referenced
                # by channels?
                ExositeModbusRTU(**modbus_kwargs)
            )
            setattr(
                channel.client,
                'eval_kwargs',
                {
                    'data_address': REGISTER_NUMBER_MAP[
                        channel.protocol_config.app_specific_config['register_range']
                        ]['range'][0] + int(channel.protocol_config.app_specific_config['register_number']) + REGISTER_NUMBER_TO_ADDRESS_OFFSET,
                    'register_count': int(channel.protocol_config.app_specific_config['register_count']),
                    'value': None,  # not used/implimented for read operations
                    'byte_endianness': channel.protocol_config.app_specific_config['byte_endianness'],
                    'register_endianness': channel.protocol_config.app_specific_config['register_endianness'],
                    'evaluation_mode': channel.protocol_config.app_specific_config['evaluation_mode'],
                    'bitmask': channel.protocol_config.app_specific_config['bitmask'],
                }
            )
            LOG.critical("channel.client.eval_kwargs: {!r}".format(channel.client.eval_kwargs))

        all_channels = modbus_tcp_channels
        all_channels.update(modbus_rtu_channels)

        while not self.is_stopped():

            while not self._Q_DATA_OUT.empty():
                data_out_obj = self._Q_DATA_OUT.safe_get(timeout=0.1)
                LOG.info("GOT DATA_OUT: {}".format(data_out_obj))
                if data_out_obj:
                    channel = data_out_obj.channel
                    LOG.critical(
                        "Processing modbus data out: {}({}): {}"
                        .format(
                            channel.name,
                            channel.client.eval_kwargs['data_address'],
                            data_out_obj.data_out_value)
                    )
                    register_range = channel.protocol_config.app_specific_config['register_range']
                    response = None

                    if register_range in ["INPUT_COIL", "HOLDING_COIL"]:
                        try:
                            channel.client.eval_kwargs['value'] = data_out_obj.data_out_value
                            response = channel.client.write_coil(
                                channel.client.eval_kwargs['data_address'],
                                data_out_obj.data_out_value
                            )
                            LOG.warning(
                                "WRITE COIL RESPONSE: {}".format(response))
                        except ModbusException as exc:
                            LOG.exception("INPUT_COIL Write Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("INPUT_COIL Write EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("INPUT_COIL Write EXCEPTION")
                            channel.put_channel_error(exc)

                        # cleanup
                        channel.client.eval_kwargs['value'] = None

                    elif register_range in ["INPUT_REGISTER", "HOLDING_REGISTER"]:
                        try:
                            channel.client.eval_kwargs['value'] = data_out_obj.data_out_value
                            response = channel.client.write_registers(
                                channel.client.eval_kwargs
                            )
                        except ModbusException as exc:
                            LOG.exception("HOLDING_REGISTER Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("HOLDING_REGISTER EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("HOLDING_REGISTER General exception".format(format_exc=exc))
                            channel.put_channel_error(exc)

                        # cleanup
                        channel.client.eval_kwargs['value'] = None

            for channel in all_channels.values():
                if channel.is_sample_time():

                    LOG.info("POLLING MODBUS CHANNEL: {}".format(channel.name))
                    register_range = channel.protocol_config.app_specific_config['register_range']
                    response = None

                    if register_range == "INPUT_COIL":
                        try:
                            response = channel.client.read_discrete_inputs(
                                channel.client.eval_kwargs
                            )
                        except ModbusException as exc:
                            LOG.exception("INPUT_COIL Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("INPUT_COIL EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("INPUT_COIL EXCEPTION")
                            channel.put_channel_error(exc)

                    elif register_range == "HOLDING_COIL":
                        try:
                            response = channel.client.read_coils(
                                channel.client.eval_kwargs
                            )
                        except ModbusException as exc:
                            LOG.exception("HOLDING_COIL Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("HOLDING_COIL EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("HOLDING_COIL General exception".format(format_exc=exc))
                            channel.put_channel_error(exc)

                    elif register_range == "INPUT_REGISTER":
                        try:
                            response = channel.client.read_input_registers(
                                channel.client.eval_kwargs
                            )
                        except ModbusException as exc:
                            LOG.exception("INPUT_REGISTER Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("INPUT_REGISTER EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("INPUT_REGISTER General exception".format(format_exc=exc))
                            channel.put_channel_error(exc)

                    elif register_range == "HOLDING_REGISTER":
                        try:
                            response = channel.client.read_holding_registers(
                                channel.client.eval_kwargs
                            )
                        except ModbusException as exc:
                            LOG.exception("HOLDING_REGISTER Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                        except ExoEdgeModbusException as exc:
                            LOG.exception("HOLDING_REGISTER EXCEPTION")
                            channel.put_channel_error(exc)
                        except Exception as exc:
                            LOG.exception("HOLDING_REGISTER General exception".format(format_exc=exc))
                            channel.put_channel_error(exc)

                    if response is not None:
                        channel.put_sample(response)
                    LOG.debug("sleeping 0.01 sec after modbus read.")
                    time.sleep(0.01)
                LOG.debug("sleeping 0.01 sec after sweeping all channels.")
                time.sleep(0.01)

        for name, channel in all_channels.items():
            LOG.critical(
                "Closing client: {} :: {}"
                .format(channel, dir(channel.client))
            )
            channel.client.client.close()
        LOG.critical("{} HAS BEEN STOPPED.".format(self.name))

