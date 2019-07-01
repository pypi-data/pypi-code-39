# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SetpointSensorPair.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import brewblox_pb2 as brewblox__pb2
import nanopb_pb2 as nanopb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='SetpointSensorPair.proto',
  package='blox',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18SetpointSensorPair.proto\x12\x04\x62lox\x1a\x0e\x62rewblox.proto\x1a\x0cnanopb.proto\"\xbc\x04\n\x12SetpointSensorPair\x12\x1d\n\x08sensorId\x18\x02 \x01(\rB\x0b\x8a\xb5\x18\x02\x18\x02\x92?\x02\x38\x10\x12/\n\x07setting\x18\x05 \x01(\x11\x42\x1e\x8a\xb5\x18\x02\x30\x01\x8a\xb5\x18\x02\x08\x01\x8a\xb5\x18\x03\x10\x80 \x92?\x02\x38 \x8a\xb5\x18\x02(\x01\x12-\n\x05value\x18\x06 \x01(\x11\x42\x1e\x8a\xb5\x18\x02\x30\x01\x8a\xb5\x18\x02\x08\x01\x8a\xb5\x18\x03\x10\x80 \x92?\x02\x38 \x8a\xb5\x18\x02(\x01\x12\x16\n\x0esettingEnabled\x18\x07 \x01(\x08\x12/\n\rstoredSetting\x18\x08 \x01(\x11\x42\x18\x8a\xb5\x18\x02\x30\x00\x8a\xb5\x18\x02\x08\x01\x8a\xb5\x18\x03\x10\x80 \x92?\x02\x38 \x12\x35\n\x06\x66ilter\x18\t \x01(\x0e\x32%.blox.SetpointSensorPair.FilterChoice\x12+\n\x0f\x66ilterThreshold\x18\n \x01(\x11\x42\x12\x8a\xb5\x18\x02\x08\x02\x8a\xb5\x18\x03\x10\x80 \x92?\x02\x38 \x12\x37\n\x0fvalueUnfiltered\x18\x0b \x01(\x11\x42\x1e\x8a\xb5\x18\x02\x30\x01\x8a\xb5\x18\x02\x08\x01\x8a\xb5\x18\x03\x10\x80 \x92?\x02\x38 \x8a\xb5\x18\x02(\x01\x12\x13\n\x0bresetFilter\x18\x0c \x01(\x08\x12(\n\x0estrippedFields\x18\x63 \x03(\rB\x10\x8a\xb5\x18\x02(\x01\x92?\x02\x38\x10\x92?\x02\x10\x03\"m\n\x0c\x46ilterChoice\x12\x0c\n\x08\x46ILT_30s\x10\x00\x12\x0b\n\x07\x46ILT_1m\x10\x01\x12\x0b\n\x07\x46ILT_3m\x10\x02\x12\x0b\n\x07\x46ILT_5m\x10\x03\x12\x0c\n\x08\x46ILT_10m\x10\x04\x12\x0c\n\x08\x46ILT_20m\x10\x05\x12\x0c\n\x08\x46ILT_45m\x10\x06:\x13\x8a\xb5\x18\x03\x18\xaf\x02\x8a\xb5\x18\x02H\x01\x8a\xb5\x18\x02H\x04\x62\x06proto3')
  ,
  dependencies=[brewblox__pb2.DESCRIPTOR,nanopb__pb2.DESCRIPTOR,])



_SETPOINTSENSORPAIR_FILTERCHOICE = _descriptor.EnumDescriptor(
  name='FilterChoice',
  full_name='blox.SetpointSensorPair.FilterChoice',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FILT_30s', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_1m', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_3m', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_5m', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_10m', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_20m', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILT_45m', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=507,
  serialized_end=616,
)
_sym_db.RegisterEnumDescriptor(_SETPOINTSENSORPAIR_FILTERCHOICE)


_SETPOINTSENSORPAIR = _descriptor.Descriptor(
  name='SetpointSensorPair',
  full_name='blox.SetpointSensorPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sensorId', full_name='blox.SetpointSensorPair.sensorId', index=0,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\002\030\002\222?\0028\020'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='setting', full_name='blox.SetpointSensorPair.setting', index=1,
      number=5, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\0020\001\212\265\030\002\010\001\212\265\030\003\020\200 \222?\0028 \212\265\030\002(\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='blox.SetpointSensorPair.value', index=2,
      number=6, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\0020\001\212\265\030\002\010\001\212\265\030\003\020\200 \222?\0028 \212\265\030\002(\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='settingEnabled', full_name='blox.SetpointSensorPair.settingEnabled', index=3,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='storedSetting', full_name='blox.SetpointSensorPair.storedSetting', index=4,
      number=8, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\0020\000\212\265\030\002\010\001\212\265\030\003\020\200 \222?\0028 '), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter', full_name='blox.SetpointSensorPair.filter', index=5,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filterThreshold', full_name='blox.SetpointSensorPair.filterThreshold', index=6,
      number=10, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\002\010\002\212\265\030\003\020\200 \222?\0028 '), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='valueUnfiltered', full_name='blox.SetpointSensorPair.valueUnfiltered', index=7,
      number=11, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\0020\001\212\265\030\002\010\001\212\265\030\003\020\200 \222?\0028 \212\265\030\002(\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resetFilter', full_name='blox.SetpointSensorPair.resetFilter', index=8,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strippedFields', full_name='blox.SetpointSensorPair.strippedFields', index=9,
      number=99, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\212\265\030\002(\001\222?\0028\020\222?\002\020\003'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SETPOINTSENSORPAIR_FILTERCHOICE,
  ],
  serialized_options=_b('\212\265\030\003\030\257\002\212\265\030\002H\001\212\265\030\002H\004'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=637,
)

_SETPOINTSENSORPAIR.fields_by_name['filter'].enum_type = _SETPOINTSENSORPAIR_FILTERCHOICE
_SETPOINTSENSORPAIR_FILTERCHOICE.containing_type = _SETPOINTSENSORPAIR
DESCRIPTOR.message_types_by_name['SetpointSensorPair'] = _SETPOINTSENSORPAIR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetpointSensorPair = _reflection.GeneratedProtocolMessageType('SetpointSensorPair', (_message.Message,), dict(
  DESCRIPTOR = _SETPOINTSENSORPAIR,
  __module__ = 'SetpointSensorPair_pb2'
  # @@protoc_insertion_point(class_scope:blox.SetpointSensorPair)
  ))
_sym_db.RegisterMessage(SetpointSensorPair)


_SETPOINTSENSORPAIR.fields_by_name['sensorId']._options = None
_SETPOINTSENSORPAIR.fields_by_name['setting']._options = None
_SETPOINTSENSORPAIR.fields_by_name['value']._options = None
_SETPOINTSENSORPAIR.fields_by_name['storedSetting']._options = None
_SETPOINTSENSORPAIR.fields_by_name['filterThreshold']._options = None
_SETPOINTSENSORPAIR.fields_by_name['valueUnfiltered']._options = None
_SETPOINTSENSORPAIR.fields_by_name['strippedFields']._options = None
_SETPOINTSENSORPAIR._options = None
# @@protoc_insertion_point(module_scope)
