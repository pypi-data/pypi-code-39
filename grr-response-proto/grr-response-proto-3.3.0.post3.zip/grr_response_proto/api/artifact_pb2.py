# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr_response_proto/api/artifact.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grr_response_proto import artifact_pb2 as grr__response__proto_dot_artifact__pb2
from grr_response_proto import semantic_pb2 as grr__response__proto_dot_semantic__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr_response_proto/api/artifact.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n%grr_response_proto/api/artifact.proto\x1a!grr_response_proto/artifact.proto\x1a!grr_response_proto/semantic.proto\"v\n\x14\x41piListArtifactsArgs\x12(\n\x06offset\x18\x01 \x01(\x03\x42\x18\xe2\xfc\xe3\xc4\x01\x12\x12\x10Starting offset.\x12\x34\n\x05\x63ount\x18\x02 \x01(\x03\x42%\xe2\xfc\xe3\xc4\x01\x1f\x12\x1dMax number of items to fetch.\"\x8b\x01\n\x16\x41piListArtifactsResult\x12=\n\x05items\x18\x01 \x03(\x0b\x32\x13.ArtifactDescriptorB\x19\xe2\xfc\xe3\xc4\x01\x13\x12\x11The flow results.\x12\x32\n\x0btotal_count\x18\x02 \x01(\x03\x42\x1d\xe2\xfc\xe3\xc4\x01\x17\x12\x15Total count of items.\"L\n\x15\x41piUploadArtifactArgs\x12\x33\n\x08\x61rtifact\x18\x01 \x01(\tB!\xe2\xfc\xe3\xc4\x01\x1b\x12\x19\x41rtifact YAML definition.\"V\n\x16\x41piDeleteArtifactsArgs\x12<\n\x05names\x18\x01 \x03(\tB-\xe2\xfc\xe3\xc4\x01\'\x12%Names of the artifacts to be deleted.')
  ,
  dependencies=[grr__response__proto_dot_artifact__pb2.DESCRIPTOR,grr__response__proto_dot_semantic__pb2.DESCRIPTOR,])




_APILISTARTIFACTSARGS = _descriptor.Descriptor(
  name='ApiListArtifactsArgs',
  full_name='ApiListArtifactsArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='offset', full_name='ApiListArtifactsArgs.offset', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\022\022\020Starting offset.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='ApiListArtifactsArgs.count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\037\022\035Max number of items to fetch.'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=229,
)


_APILISTARTIFACTSRESULT = _descriptor.Descriptor(
  name='ApiListArtifactsResult',
  full_name='ApiListArtifactsResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='ApiListArtifactsResult.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\023\022\021The flow results.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='ApiListArtifactsResult.total_count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\027\022\025Total count of items.'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=232,
  serialized_end=371,
)


_APIUPLOADARTIFACTARGS = _descriptor.Descriptor(
  name='ApiUploadArtifactArgs',
  full_name='ApiUploadArtifactArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifact', full_name='ApiUploadArtifactArgs.artifact', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\033\022\031Artifact YAML definition.'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=373,
  serialized_end=449,
)


_APIDELETEARTIFACTSARGS = _descriptor.Descriptor(
  name='ApiDeleteArtifactsArgs',
  full_name='ApiDeleteArtifactsArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='names', full_name='ApiDeleteArtifactsArgs.names', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\'\022%Names of the artifacts to be deleted.'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=451,
  serialized_end=537,
)

_APILISTARTIFACTSRESULT.fields_by_name['items'].message_type = grr__response__proto_dot_artifact__pb2._ARTIFACTDESCRIPTOR
DESCRIPTOR.message_types_by_name['ApiListArtifactsArgs'] = _APILISTARTIFACTSARGS
DESCRIPTOR.message_types_by_name['ApiListArtifactsResult'] = _APILISTARTIFACTSRESULT
DESCRIPTOR.message_types_by_name['ApiUploadArtifactArgs'] = _APIUPLOADARTIFACTARGS
DESCRIPTOR.message_types_by_name['ApiDeleteArtifactsArgs'] = _APIDELETEARTIFACTSARGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ApiListArtifactsArgs = _reflection.GeneratedProtocolMessageType('ApiListArtifactsArgs', (_message.Message,), dict(
  DESCRIPTOR = _APILISTARTIFACTSARGS,
  __module__ = 'grr_response_proto.api.artifact_pb2'
  # @@protoc_insertion_point(class_scope:ApiListArtifactsArgs)
  ))
_sym_db.RegisterMessage(ApiListArtifactsArgs)

ApiListArtifactsResult = _reflection.GeneratedProtocolMessageType('ApiListArtifactsResult', (_message.Message,), dict(
  DESCRIPTOR = _APILISTARTIFACTSRESULT,
  __module__ = 'grr_response_proto.api.artifact_pb2'
  # @@protoc_insertion_point(class_scope:ApiListArtifactsResult)
  ))
_sym_db.RegisterMessage(ApiListArtifactsResult)

ApiUploadArtifactArgs = _reflection.GeneratedProtocolMessageType('ApiUploadArtifactArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIUPLOADARTIFACTARGS,
  __module__ = 'grr_response_proto.api.artifact_pb2'
  # @@protoc_insertion_point(class_scope:ApiUploadArtifactArgs)
  ))
_sym_db.RegisterMessage(ApiUploadArtifactArgs)

ApiDeleteArtifactsArgs = _reflection.GeneratedProtocolMessageType('ApiDeleteArtifactsArgs', (_message.Message,), dict(
  DESCRIPTOR = _APIDELETEARTIFACTSARGS,
  __module__ = 'grr_response_proto.api.artifact_pb2'
  # @@protoc_insertion_point(class_scope:ApiDeleteArtifactsArgs)
  ))
_sym_db.RegisterMessage(ApiDeleteArtifactsArgs)


_APILISTARTIFACTSARGS.fields_by_name['offset']._options = None
_APILISTARTIFACTSARGS.fields_by_name['count']._options = None
_APILISTARTIFACTSRESULT.fields_by_name['items']._options = None
_APILISTARTIFACTSRESULT.fields_by_name['total_count']._options = None
_APIUPLOADARTIFACTARGS.fields_by_name['artifact']._options = None
_APIDELETEARTIFACTSARGS.fields_by_name['names']._options = None
# @@protoc_insertion_point(module_scope)
