# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr_response_proto/tests.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grr_response_proto import export_pb2 as grr__response__proto_dot_export__pb2
from grr_response_proto import jobs_pb2 as grr__response__proto_dot_jobs__pb2
from grr_response_proto import semantic_pb2 as grr__response__proto_dot_semantic__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr_response_proto/tests.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x1egrr_response_proto/tests.proto\x1a\x1fgrr_response_proto/export.proto\x1a\x1dgrr_response_proto/jobs.proto\x1a!grr_response_proto/semantic.proto\"@\n\x16\x43lientActionRunnerArgs\x12&\n\x06\x61\x63tion\x18\x01 \x01(\tB\x16\xe2\xfc\xe3\xc4\x01\x10\x12\x0e\x41\x63tion to run.\"+\n\x10\x42\x61\x64\x41rgsFlow1Args\x12\x17\n\x04\x61rg1\x18\x01 \x01(\x0b\x32\t.PathSpec\"(\n\x0fSendingFlowArgs\x12\x15\n\rmessage_count\x18\x01 \x01(\x04\"M\n\x1d\x44ummyCronHuntOutputPluginArgs\x12\x13\n\x0boutput_path\x18\x01 \x01(\t\x12\x17\n\x0f\x63ollection_name\x18\x02 \x01(\t\"&\n\x15RecursiveTestFlowArgs\x12\r\n\x05\x64\x65pth\x18\x01 \x01(\x04\"[\n\x18MultiGetFileTestFlowArgs\x12?\n\nfile_limit\x18\x01 \x01(\x04:\x01\x33\x42(\xe2\xfc\xe3\xc4\x01\"\x12 The number of files to retrieve.\"\xbc\x03\n\x1e\x44\x61taAgnosticConverterTestValue\x12\x14\n\x0cstring_value\x18\x01 \x01(\t\x12\x11\n\tint_value\x18\x02 \x01(\x04\x12\x12\n\nbool_value\x18\x03 \x01(\x08\x12\x1d\n\x15repeated_string_value\x18\x04 \x03(\t\x12(\n\rmessage_value\x18\x05 \x01(\x0b\x32\x11.ExportedMetadata\x12H\n\nenum_value\x18\x06 \x01(\x0e\x32*.DataAgnosticConverterTestValue.EnumOption:\x08OPTION_1\x12P\n\x12\x61nother_enum_value\x18\x07 \x01(\x0e\x32*.DataAgnosticConverterTestValue.EnumOption:\x08OPTION_2\x12!\n\turn_value\x18\x08 \x01(\tB\x0e\xe2\xfc\xe3\xc4\x01\x08\n\x06RDFURN\x12+\n\x0e\x64\x61tetime_value\x18\t \x01(\x04\x42\x13\xe2\xfc\xe3\xc4\x01\r\n\x0bRDFDatetime\"(\n\nEnumOption\x12\x0c\n\x08OPTION_1\x10\x00\x12\x0c\n\x08OPTION_2\x10\x01\"M\n*DataAgnosticConverterTestValueWithMetadata\x12\x10\n\x08metadata\x18\x01 \x01(\x04\x12\r\n\x05value\x18\x02 \x01(\t\"\x87\x03\n\x17\x44\x65\x66\x61ultArgsTestFlowArgs\x12\x14\n\x0cstring_value\x18\x01 \x01(\t\x12\x11\n\tint_value\x18\x02 \x01(\x04\x12\x12\n\nbool_value\x18\x03 \x01(\x08\x12\x37\n\nenum_value\x18\x04 \x01(\x0e\x32#.DefaultArgsTestFlowArgs.EnumOption\x12\x31\n\x19string_value_with_default\x18\x05 \x01(\t:\x0e\x64\x65\x66\x61ult string\x12\"\n\x16int_value_with_default\x18\x06 \x01(\x04:\x02\x34\x32\x12%\n\x17\x62ool_value_with_default\x18\x07 \x01(\x08:\x04true\x12N\n\x17\x65num_value_with_default\x18\x08 \x01(\x0e\x32#.DefaultArgsTestFlowArgs.EnumOption:\x08OPTION_2\"(\n\nEnumOption\x12\x0c\n\x08OPTION_1\x10\x00\x12\x0c\n\x08OPTION_2\x10\x01\"1\n\x14SampleGetHandlerArgs\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0b\n\x03\x66oo\x18\x02 \x01(\t\"C\n\x16SampleGetHandlerResult\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0b\n\x03\x66oo\x18\x03 \x01(\t\"o\n\x1f\x41piRDFProtoStructRendererSample\x12$\n\x05index\x18\x01 \x01(\x04\x42\x15\xe2\xfc\xe3\xc4\x01\x0f\x12\rSample index.\x12&\n\x06values\x18\x02 \x03(\tB\x16\xe2\xfc\xe3\xc4\x01\x10\x12\x0eSample values.\".\n\x17SampleDeleteHandlerArgs\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"=\n\x19SampleDeleteHandlerResult\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\"-\n\x16SamplePatchHandlerArgs\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\"<\n\x18SamplePatchHandlerResult\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\"K\n/DummyAuthManagerTestConfigurableApiRouterParams\x12\x0b\n\x03\x66oo\x18\x01 \x01(\t\x12\x0b\n\x03\x62\x61r\x18\x02 \x01(\x04')
  ,
  dependencies=[grr__response__proto_dot_export__pb2.DESCRIPTOR,grr__response__proto_dot_jobs__pb2.DESCRIPTOR,grr__response__proto_dot_semantic__pb2.DESCRIPTOR,])



_DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION = _descriptor.EnumDescriptor(
  name='EnumOption',
  full_name='DataAgnosticConverterTestValue.EnumOption',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OPTION_1', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPTION_2', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=903,
  serialized_end=943,
)
_sym_db.RegisterEnumDescriptor(_DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION)

_DEFAULTARGSTESTFLOWARGS_ENUMOPTION = _descriptor.EnumDescriptor(
  name='EnumOption',
  full_name='DefaultArgsTestFlowArgs.EnumOption',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OPTION_1', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPTION_2', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=903,
  serialized_end=943,
)
_sym_db.RegisterEnumDescriptor(_DEFAULTARGSTESTFLOWARGS_ENUMOPTION)


_CLIENTACTIONRUNNERARGS = _descriptor.Descriptor(
  name='ClientActionRunnerArgs',
  full_name='ClientActionRunnerArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='ClientActionRunnerArgs.action', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\020\022\016Action to run.'), file=DESCRIPTOR),
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
  serialized_start=133,
  serialized_end=197,
)


_BADARGSFLOW1ARGS = _descriptor.Descriptor(
  name='BadArgsFlow1Args',
  full_name='BadArgsFlow1Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arg1', full_name='BadArgsFlow1Args.arg1', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=199,
  serialized_end=242,
)


_SENDINGFLOWARGS = _descriptor.Descriptor(
  name='SendingFlowArgs',
  full_name='SendingFlowArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_count', full_name='SendingFlowArgs.message_count', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=244,
  serialized_end=284,
)


_DUMMYCRONHUNTOUTPUTPLUGINARGS = _descriptor.Descriptor(
  name='DummyCronHuntOutputPluginArgs',
  full_name='DummyCronHuntOutputPluginArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='output_path', full_name='DummyCronHuntOutputPluginArgs.output_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection_name', full_name='DummyCronHuntOutputPluginArgs.collection_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=286,
  serialized_end=363,
)


_RECURSIVETESTFLOWARGS = _descriptor.Descriptor(
  name='RecursiveTestFlowArgs',
  full_name='RecursiveTestFlowArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='depth', full_name='RecursiveTestFlowArgs.depth', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=365,
  serialized_end=403,
)


_MULTIGETFILETESTFLOWARGS = _descriptor.Descriptor(
  name='MultiGetFileTestFlowArgs',
  full_name='MultiGetFileTestFlowArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_limit', full_name='MultiGetFileTestFlowArgs.file_limit', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=3,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\"\022 The number of files to retrieve.'), file=DESCRIPTOR),
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
  serialized_start=405,
  serialized_end=496,
)


_DATAAGNOSTICCONVERTERTESTVALUE = _descriptor.Descriptor(
  name='DataAgnosticConverterTestValue',
  full_name='DataAgnosticConverterTestValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_value', full_name='DataAgnosticConverterTestValue.string_value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='DataAgnosticConverterTestValue.int_value', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='DataAgnosticConverterTestValue.bool_value', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='repeated_string_value', full_name='DataAgnosticConverterTestValue.repeated_string_value', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message_value', full_name='DataAgnosticConverterTestValue.message_value', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_value', full_name='DataAgnosticConverterTestValue.enum_value', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='another_enum_value', full_name='DataAgnosticConverterTestValue.another_enum_value', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='urn_value', full_name='DataAgnosticConverterTestValue.urn_value', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\010\n\006RDFURN'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='datetime_value', full_name='DataAgnosticConverterTestValue.datetime_value', index=8,
      number=9, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\r\n\013RDFDatetime'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=499,
  serialized_end=943,
)


_DATAAGNOSTICCONVERTERTESTVALUEWITHMETADATA = _descriptor.Descriptor(
  name='DataAgnosticConverterTestValueWithMetadata',
  full_name='DataAgnosticConverterTestValueWithMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='DataAgnosticConverterTestValueWithMetadata.metadata', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='DataAgnosticConverterTestValueWithMetadata.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=945,
  serialized_end=1022,
)


_DEFAULTARGSTESTFLOWARGS = _descriptor.Descriptor(
  name='DefaultArgsTestFlowArgs',
  full_name='DefaultArgsTestFlowArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_value', full_name='DefaultArgsTestFlowArgs.string_value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='DefaultArgsTestFlowArgs.int_value', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='DefaultArgsTestFlowArgs.bool_value', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_value', full_name='DefaultArgsTestFlowArgs.enum_value', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_value_with_default', full_name='DefaultArgsTestFlowArgs.string_value_with_default', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("default string").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_value_with_default', full_name='DefaultArgsTestFlowArgs.int_value_with_default', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=42,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value_with_default', full_name='DefaultArgsTestFlowArgs.bool_value_with_default', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_value_with_default', full_name='DefaultArgsTestFlowArgs.enum_value_with_default', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEFAULTARGSTESTFLOWARGS_ENUMOPTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1025,
  serialized_end=1416,
)


_SAMPLEGETHANDLERARGS = _descriptor.Descriptor(
  name='SampleGetHandlerArgs',
  full_name='SampleGetHandlerArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='SampleGetHandlerArgs.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='foo', full_name='SampleGetHandlerArgs.foo', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1418,
  serialized_end=1467,
)


_SAMPLEGETHANDLERRESULT = _descriptor.Descriptor(
  name='SampleGetHandlerResult',
  full_name='SampleGetHandlerResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='SampleGetHandlerResult.method', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='SampleGetHandlerResult.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='foo', full_name='SampleGetHandlerResult.foo', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1469,
  serialized_end=1536,
)


_APIRDFPROTOSTRUCTRENDERERSAMPLE = _descriptor.Descriptor(
  name='ApiRDFProtoStructRendererSample',
  full_name='ApiRDFProtoStructRendererSample',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='ApiRDFProtoStructRendererSample.index', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\017\022\rSample index.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='ApiRDFProtoStructRendererSample.values', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\020\022\016Sample values.'), file=DESCRIPTOR),
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
  serialized_start=1538,
  serialized_end=1649,
)


_SAMPLEDELETEHANDLERARGS = _descriptor.Descriptor(
  name='SampleDeleteHandlerArgs',
  full_name='SampleDeleteHandlerArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='SampleDeleteHandlerArgs.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1651,
  serialized_end=1697,
)


_SAMPLEDELETEHANDLERRESULT = _descriptor.Descriptor(
  name='SampleDeleteHandlerResult',
  full_name='SampleDeleteHandlerResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='SampleDeleteHandlerResult.method', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource', full_name='SampleDeleteHandlerResult.resource', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1699,
  serialized_end=1760,
)


_SAMPLEPATCHHANDLERARGS = _descriptor.Descriptor(
  name='SamplePatchHandlerArgs',
  full_name='SamplePatchHandlerArgs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='SamplePatchHandlerArgs.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1762,
  serialized_end=1807,
)


_SAMPLEPATCHHANDLERRESULT = _descriptor.Descriptor(
  name='SamplePatchHandlerResult',
  full_name='SamplePatchHandlerResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='SamplePatchHandlerResult.method', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource', full_name='SamplePatchHandlerResult.resource', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1809,
  serialized_end=1869,
)


_DUMMYAUTHMANAGERTESTCONFIGURABLEAPIROUTERPARAMS = _descriptor.Descriptor(
  name='DummyAuthManagerTestConfigurableApiRouterParams',
  full_name='DummyAuthManagerTestConfigurableApiRouterParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo', full_name='DummyAuthManagerTestConfigurableApiRouterParams.foo', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bar', full_name='DummyAuthManagerTestConfigurableApiRouterParams.bar', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1871,
  serialized_end=1946,
)

_BADARGSFLOW1ARGS.fields_by_name['arg1'].message_type = grr__response__proto_dot_jobs__pb2._PATHSPEC
_DATAAGNOSTICCONVERTERTESTVALUE.fields_by_name['message_value'].message_type = grr__response__proto_dot_export__pb2._EXPORTEDMETADATA
_DATAAGNOSTICCONVERTERTESTVALUE.fields_by_name['enum_value'].enum_type = _DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION
_DATAAGNOSTICCONVERTERTESTVALUE.fields_by_name['another_enum_value'].enum_type = _DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION
_DATAAGNOSTICCONVERTERTESTVALUE_ENUMOPTION.containing_type = _DATAAGNOSTICCONVERTERTESTVALUE
_DEFAULTARGSTESTFLOWARGS.fields_by_name['enum_value'].enum_type = _DEFAULTARGSTESTFLOWARGS_ENUMOPTION
_DEFAULTARGSTESTFLOWARGS.fields_by_name['enum_value_with_default'].enum_type = _DEFAULTARGSTESTFLOWARGS_ENUMOPTION
_DEFAULTARGSTESTFLOWARGS_ENUMOPTION.containing_type = _DEFAULTARGSTESTFLOWARGS
DESCRIPTOR.message_types_by_name['ClientActionRunnerArgs'] = _CLIENTACTIONRUNNERARGS
DESCRIPTOR.message_types_by_name['BadArgsFlow1Args'] = _BADARGSFLOW1ARGS
DESCRIPTOR.message_types_by_name['SendingFlowArgs'] = _SENDINGFLOWARGS
DESCRIPTOR.message_types_by_name['DummyCronHuntOutputPluginArgs'] = _DUMMYCRONHUNTOUTPUTPLUGINARGS
DESCRIPTOR.message_types_by_name['RecursiveTestFlowArgs'] = _RECURSIVETESTFLOWARGS
DESCRIPTOR.message_types_by_name['MultiGetFileTestFlowArgs'] = _MULTIGETFILETESTFLOWARGS
DESCRIPTOR.message_types_by_name['DataAgnosticConverterTestValue'] = _DATAAGNOSTICCONVERTERTESTVALUE
DESCRIPTOR.message_types_by_name['DataAgnosticConverterTestValueWithMetadata'] = _DATAAGNOSTICCONVERTERTESTVALUEWITHMETADATA
DESCRIPTOR.message_types_by_name['DefaultArgsTestFlowArgs'] = _DEFAULTARGSTESTFLOWARGS
DESCRIPTOR.message_types_by_name['SampleGetHandlerArgs'] = _SAMPLEGETHANDLERARGS
DESCRIPTOR.message_types_by_name['SampleGetHandlerResult'] = _SAMPLEGETHANDLERRESULT
DESCRIPTOR.message_types_by_name['ApiRDFProtoStructRendererSample'] = _APIRDFPROTOSTRUCTRENDERERSAMPLE
DESCRIPTOR.message_types_by_name['SampleDeleteHandlerArgs'] = _SAMPLEDELETEHANDLERARGS
DESCRIPTOR.message_types_by_name['SampleDeleteHandlerResult'] = _SAMPLEDELETEHANDLERRESULT
DESCRIPTOR.message_types_by_name['SamplePatchHandlerArgs'] = _SAMPLEPATCHHANDLERARGS
DESCRIPTOR.message_types_by_name['SamplePatchHandlerResult'] = _SAMPLEPATCHHANDLERRESULT
DESCRIPTOR.message_types_by_name['DummyAuthManagerTestConfigurableApiRouterParams'] = _DUMMYAUTHMANAGERTESTCONFIGURABLEAPIROUTERPARAMS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ClientActionRunnerArgs = _reflection.GeneratedProtocolMessageType('ClientActionRunnerArgs', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTACTIONRUNNERARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:ClientActionRunnerArgs)
  ))
_sym_db.RegisterMessage(ClientActionRunnerArgs)

BadArgsFlow1Args = _reflection.GeneratedProtocolMessageType('BadArgsFlow1Args', (_message.Message,), dict(
  DESCRIPTOR = _BADARGSFLOW1ARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:BadArgsFlow1Args)
  ))
_sym_db.RegisterMessage(BadArgsFlow1Args)

SendingFlowArgs = _reflection.GeneratedProtocolMessageType('SendingFlowArgs', (_message.Message,), dict(
  DESCRIPTOR = _SENDINGFLOWARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SendingFlowArgs)
  ))
_sym_db.RegisterMessage(SendingFlowArgs)

DummyCronHuntOutputPluginArgs = _reflection.GeneratedProtocolMessageType('DummyCronHuntOutputPluginArgs', (_message.Message,), dict(
  DESCRIPTOR = _DUMMYCRONHUNTOUTPUTPLUGINARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:DummyCronHuntOutputPluginArgs)
  ))
_sym_db.RegisterMessage(DummyCronHuntOutputPluginArgs)

RecursiveTestFlowArgs = _reflection.GeneratedProtocolMessageType('RecursiveTestFlowArgs', (_message.Message,), dict(
  DESCRIPTOR = _RECURSIVETESTFLOWARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:RecursiveTestFlowArgs)
  ))
_sym_db.RegisterMessage(RecursiveTestFlowArgs)

MultiGetFileTestFlowArgs = _reflection.GeneratedProtocolMessageType('MultiGetFileTestFlowArgs', (_message.Message,), dict(
  DESCRIPTOR = _MULTIGETFILETESTFLOWARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:MultiGetFileTestFlowArgs)
  ))
_sym_db.RegisterMessage(MultiGetFileTestFlowArgs)

DataAgnosticConverterTestValue = _reflection.GeneratedProtocolMessageType('DataAgnosticConverterTestValue', (_message.Message,), dict(
  DESCRIPTOR = _DATAAGNOSTICCONVERTERTESTVALUE,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:DataAgnosticConverterTestValue)
  ))
_sym_db.RegisterMessage(DataAgnosticConverterTestValue)

DataAgnosticConverterTestValueWithMetadata = _reflection.GeneratedProtocolMessageType('DataAgnosticConverterTestValueWithMetadata', (_message.Message,), dict(
  DESCRIPTOR = _DATAAGNOSTICCONVERTERTESTVALUEWITHMETADATA,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:DataAgnosticConverterTestValueWithMetadata)
  ))
_sym_db.RegisterMessage(DataAgnosticConverterTestValueWithMetadata)

DefaultArgsTestFlowArgs = _reflection.GeneratedProtocolMessageType('DefaultArgsTestFlowArgs', (_message.Message,), dict(
  DESCRIPTOR = _DEFAULTARGSTESTFLOWARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:DefaultArgsTestFlowArgs)
  ))
_sym_db.RegisterMessage(DefaultArgsTestFlowArgs)

SampleGetHandlerArgs = _reflection.GeneratedProtocolMessageType('SampleGetHandlerArgs', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEGETHANDLERARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SampleGetHandlerArgs)
  ))
_sym_db.RegisterMessage(SampleGetHandlerArgs)

SampleGetHandlerResult = _reflection.GeneratedProtocolMessageType('SampleGetHandlerResult', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEGETHANDLERRESULT,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SampleGetHandlerResult)
  ))
_sym_db.RegisterMessage(SampleGetHandlerResult)

ApiRDFProtoStructRendererSample = _reflection.GeneratedProtocolMessageType('ApiRDFProtoStructRendererSample', (_message.Message,), dict(
  DESCRIPTOR = _APIRDFPROTOSTRUCTRENDERERSAMPLE,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:ApiRDFProtoStructRendererSample)
  ))
_sym_db.RegisterMessage(ApiRDFProtoStructRendererSample)

SampleDeleteHandlerArgs = _reflection.GeneratedProtocolMessageType('SampleDeleteHandlerArgs', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEDELETEHANDLERARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SampleDeleteHandlerArgs)
  ))
_sym_db.RegisterMessage(SampleDeleteHandlerArgs)

SampleDeleteHandlerResult = _reflection.GeneratedProtocolMessageType('SampleDeleteHandlerResult', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEDELETEHANDLERRESULT,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SampleDeleteHandlerResult)
  ))
_sym_db.RegisterMessage(SampleDeleteHandlerResult)

SamplePatchHandlerArgs = _reflection.GeneratedProtocolMessageType('SamplePatchHandlerArgs', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEPATCHHANDLERARGS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SamplePatchHandlerArgs)
  ))
_sym_db.RegisterMessage(SamplePatchHandlerArgs)

SamplePatchHandlerResult = _reflection.GeneratedProtocolMessageType('SamplePatchHandlerResult', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLEPATCHHANDLERRESULT,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:SamplePatchHandlerResult)
  ))
_sym_db.RegisterMessage(SamplePatchHandlerResult)

DummyAuthManagerTestConfigurableApiRouterParams = _reflection.GeneratedProtocolMessageType('DummyAuthManagerTestConfigurableApiRouterParams', (_message.Message,), dict(
  DESCRIPTOR = _DUMMYAUTHMANAGERTESTCONFIGURABLEAPIROUTERPARAMS,
  __module__ = 'grr_response_proto.tests_pb2'
  # @@protoc_insertion_point(class_scope:DummyAuthManagerTestConfigurableApiRouterParams)
  ))
_sym_db.RegisterMessage(DummyAuthManagerTestConfigurableApiRouterParams)


_CLIENTACTIONRUNNERARGS.fields_by_name['action']._options = None
_MULTIGETFILETESTFLOWARGS.fields_by_name['file_limit']._options = None
_DATAAGNOSTICCONVERTERTESTVALUE.fields_by_name['urn_value']._options = None
_DATAAGNOSTICCONVERTERTESTVALUE.fields_by_name['datetime_value']._options = None
_APIRDFPROTOSTRUCTRENDERERSAMPLE.fields_by_name['index']._options = None
_APIRDFPROTOSTRUCTRENDERERSAMPLE.fields_by_name['values']._options = None
# @@protoc_insertion_point(module_scope)
