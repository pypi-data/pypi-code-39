# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr_response_proto/checks.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grr_response_proto import anomaly_pb2 as grr__response__proto_dot_anomaly__pb2
from grr_response_proto import jobs_pb2 as grr__response__proto_dot_jobs__pb2
from grr_response_proto import knowledge_base_pb2 as grr__response__proto_dot_knowledge__base__pb2
from grr_response_proto import semantic_pb2 as grr__response__proto_dot_semantic__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr_response_proto/checks.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x1fgrr_response_proto/checks.proto\x1a grr_response_proto/anomaly.proto\x1a\x1dgrr_response_proto/jobs.proto\x1a\'grr_response_proto/knowledge_base.proto\x1a!grr_response_proto/semantic.proto\"\xbd\x03\n\x05\x43heck\x12\x46\n\x08\x63heck_id\x18\x01 \x01(\tB4\xe2\xfc\xe3\xc4\x01.\x12,A distinguishing identifier for an advisory.\x12;\n\x06method\x18\x02 \x03(\x0b\x32\x07.MethodB\"\xe2\xfc\xe3\xc4\x01\x1c\x12\x1a\x41 way to analyse the host.\x12\x90\x01\n\x05match\x18\x03 \x03(\x0e\x32\x06.MatchBy\xe2\xfc\xe3\xc4\x01s\x12qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.\x12\x46\n\x06target\x18\x04 \x01(\x0b\x32\x07.TargetB-\xe2\xfc\xe3\xc4\x01\'\x12%Limit this check to specific targets.\x12T\n\x04hint\x18\x05 \x01(\x0b\x32\x05.HintB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37Textual descriptions of a problem, fix and/or findings.\"\xcb\x03\n\x06Method\x12?\n\x05probe\x18\x01 \x03(\x0b\x32\x06.ProbeB(\xe2\xfc\xe3\xc4\x01\"\x12 A way to process some host data.\x12\x90\x01\n\x05match\x18\x02 \x03(\x0e\x32\x06.MatchBy\xe2\xfc\xe3\xc4\x01s\x12qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.\x12N\n\x08resource\x18\x03 \x03(\x0b\x32\x05.DictB5\xe2\xfc\xe3\xc4\x01/\x12-Extra data (e.g. hint text, comparison data).\x12G\n\x06target\x18\x04 \x01(\x0b\x32\x07.TargetB.\xe2\xfc\xe3\xc4\x01(\x12&Limit this method to specific targets.\x12T\n\x04hint\x18\x05 \x01(\x0b\x32\x05.HintB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37Textual descriptions of a problem, fix and/or findings.\"\xab\t\n\x05Probe\x12\x43\n\x08\x61rtifact\x18\x01 \x01(\tB1\xe2\xfc\xe3\xc4\x01+\x12)The artifact that provides the host data.\x12?\n\x06parser\x18\x02 \x03(\tB/\xe2\xfc\xe3\xc4\x01)\x12\'Which parsers should process host data.\x12\x9d\x01\n\x04mode\x18\x03 \x01(\x0e\x32\x0b.Probe.Mode:\x06SERIALBz\xe2\xfc\xe3\xc4\x01t\x12rHow to apply filters. Serial runs data through each filtersequentially. Parallel applies each filter individually.\x12\xd2\x01\n\x08\x62\x61seline\x18\x04 \x03(\x0b\x32\x07.FilterB\xb6\x01\xe2\xfc\xe3\xc4\x01\xaf\x01\x12\xac\x01One or more filters used to extract baseline data (e.g. all the apt repos on a system). If defined, baseline data is used to evaluate filter results, rather than host data.\x12O\n\x07\x66ilters\x18\x05 \x03(\x0b\x32\x07.FilterB5\xe2\xfc\xe3\xc4\x01/\x12-One or more filters applied to the host data.\x12\x90\x01\n\x05match\x18\x06 \x03(\x0e\x32\x06.MatchBy\xe2\xfc\xe3\xc4\x01s\x12qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.\x12\x46\n\x06target\x18\x07 \x01(\x0b\x32\x07.TargetB-\xe2\xfc\xe3\xc4\x01\'\x12%Limit this Probe to specific targets.\x12T\n\x04hint\x18\x08 \x01(\x0b\x32\x05.HintB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37Textual descriptions of a problem, fix and/or findings.\x12\xb3\x01\n\x0eresult_context\x18\t \x01(\x0e\x32\x14.Probe.ResultContext:\x06PARSERB}\xe2\xfc\xe3\xc4\x01w\x12uWhich stage of results in the artifact collection to use for the checks. Defaults to the registered artifact parsers.\" \n\x04Mode\x12\n\n\x06SERIAL\x10\x00\x12\x0c\n\x08PARALLEL\x10\x01\"M\n\rResultContext\x12\x1a\n\x16UNKNOWN_RESULT_CONTEXT\x10\x00\x12\n\n\x06PARSER\x10\x01\x12\x0b\n\x07\x41NOMALY\x10\x02\x12\x07\n\x03RAW\x10\x03\"\x83\x02\n\x06\x46ilter\x12\x39\n\x04type\x18\x01 \x01(\tB+\xe2\xfc\xe3\xc4\x01%\x12#The type of filter to hand data to.\x12h\n\nexpression\x18\x02 \x01(\tBT\xe2\xfc\xe3\xc4\x01N\x12LA rule definition or match term used to pass runtime parameters to a filter.\x12T\n\x04hint\x18\x05 \x01(\x0b\x32\x05.HintB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37Textual descriptions of a problem, fix and/or findings.\"\xb1\x01\n\x0b\x43heckResult\x12P\n\x08\x63heck_id\x18\x01 \x01(\tB>\xe2\xfc\xe3\xc4\x01\x38\x12\x36The check id, identifies what check is being reported.\x12P\n\x07\x61nomaly\x18\x02 \x03(\x0b\x32\x08.AnomalyB5\xe2\xfc\xe3\xc4\x01/\x12-Specific findings indicating an issue exists.\"\x8f\x01\n\x0c\x43heckResults\x12;\n\x02kb\x18\x01 \x01(\x0b\x32\x0e.KnowledgeBaseB\x1f\xe2\xfc\xe3\xc4\x01\x19\x12\x17\x44\x65tails about the host.\x12\x42\n\x06result\x18\x02 \x03(\x0b\x32\x0c.CheckResultB$\xe2\xfc\xe3\xc4\x01\x1e\x12\x1cThe check results for a host\"\xea\x02\n\x04Hint\x12\x34\n\x07problem\x18\x01 \x01(\tB#\xe2\xfc\xe3\xc4\x01\x1d\x12\x1b\x41 description of the issue.\x12;\n\x03\x66ix\x18\x02 \x01(\tB.\xe2\xfc\xe3\xc4\x01(\x12&A description of how to fix the issue.\x12M\n\x06\x66ormat\x18\x03 \x01(\tB=\xe2\xfc\xe3\xc4\x01\x37\x12\x35\x41 template expression to format finding for an issue.\x12P\n\x07summary\x18\x04 \x01(\tB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37\x41 short name or term used to describe the type of data.\x12N\n\x0bmax_results\x18\x05 \x01(\x04\x42\x39\xe2\xfc\xe3\xc4\x01\x33\x12\x31Maximum number of findings to include in results.\"\xf3\x01\n\x06Target\x12L\n\x03\x63pe\x18\x01 \x03(\tB?\xe2\xfc\xe3\xc4\x01\x39\x12\x37Restrict this check to hosts with any of these CPE ids.\x12L\n\x02os\x18\x02 \x03(\tB@\xe2\xfc\xe3\xc4\x01:\x12\x38Restrict this check to hosts with any of these OS types.\x12M\n\x05label\x18\x03 \x03(\tB>\xe2\xfc\xe3\xc4\x01\x38\x12\x36Restrict this check to hosts with any of these labels.*6\n\x05Match\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03ONE\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\x07\n\x03\x41LL\x10\x03\x12\x08\n\x04SOME\x10\x04')
  ,
  dependencies=[grr__response__proto_dot_anomaly__pb2.DESCRIPTOR,grr__response__proto_dot_jobs__pb2.DESCRIPTOR,grr__response__proto_dot_knowledge__base__pb2.DESCRIPTOR,grr__response__proto_dot_semantic__pb2.DESCRIPTOR,])

_MATCH = _descriptor.EnumDescriptor(
  name='Match',
  full_name='Match',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ONE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOME', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3483,
  serialized_end=3537,
)
_sym_db.RegisterEnumDescriptor(_MATCH)

Match = enum_type_wrapper.EnumTypeWrapper(_MATCH)
NONE = 0
ONE = 1
ANY = 2
ALL = 3
SOME = 4


_PROBE_MODE = _descriptor.EnumDescriptor(
  name='Mode',
  full_name='Probe.Mode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SERIAL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PARALLEL', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2171,
  serialized_end=2203,
)
_sym_db.RegisterEnumDescriptor(_PROBE_MODE)

_PROBE_RESULTCONTEXT = _descriptor.EnumDescriptor(
  name='ResultContext',
  full_name='Probe.ResultContext',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_RESULT_CONTEXT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PARSER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANOMALY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RAW', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2205,
  serialized_end=2282,
)
_sym_db.RegisterEnumDescriptor(_PROBE_RESULTCONTEXT)


_CHECK = _descriptor.Descriptor(
  name='Check',
  full_name='Check',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='check_id', full_name='Check.check_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001.\022,A distinguishing identifier for an advisory.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method', full_name='Check.method', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\034\022\032A way to analyse the host.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='match', full_name='Check.match', index=2,
      number=3, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001s\022qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='Check.target', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\'\022%Limit this check to specific targets.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hint', full_name='Check.hint', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227Textual descriptions of a problem, fix and/or findings.'), file=DESCRIPTOR),
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
  serialized_start=177,
  serialized_end=622,
)


_METHOD = _descriptor.Descriptor(
  name='Method',
  full_name='Method',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='probe', full_name='Method.probe', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\"\022 A way to process some host data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='match', full_name='Method.match', index=1,
      number=2, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001s\022qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource', full_name='Method.resource', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001/\022-Extra data (e.g. hint text, comparison data).'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='Method.target', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001(\022&Limit this method to specific targets.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hint', full_name='Method.hint', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227Textual descriptions of a problem, fix and/or findings.'), file=DESCRIPTOR),
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
  serialized_start=625,
  serialized_end=1084,
)


_PROBE = _descriptor.Descriptor(
  name='Probe',
  full_name='Probe',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifact', full_name='Probe.artifact', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001+\022)The artifact that provides the host data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parser', full_name='Probe.parser', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001)\022\'Which parsers should process host data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mode', full_name='Probe.mode', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001t\022rHow to apply filters. Serial runs data through each filtersequentially. Parallel applies each filter individually.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='baseline', full_name='Probe.baseline', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\257\001\022\254\001One or more filters used to extract baseline data (e.g. all the apt repos on a system). If defined, baseline data is used to evaluate filter results, rather than host data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filters', full_name='Probe.filters', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001/\022-One or more filters applied to the host data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='match', full_name='Probe.match', index=5,
      number=6, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001s\022qThe condition is detected if the specified number of host results exist after processing. Set to ANY, by default.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='Probe.target', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\'\022%Limit this Probe to specific targets.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hint', full_name='Probe.hint', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227Textual descriptions of a problem, fix and/or findings.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_context', full_name='Probe.result_context', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001w\022uWhich stage of results in the artifact collection to use for the checks. Defaults to the registered artifact parsers.'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROBE_MODE,
    _PROBE_RESULTCONTEXT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1087,
  serialized_end=2282,
)


_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Filter.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001%\022#The type of filter to hand data to.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expression', full_name='Filter.expression', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001N\022LA rule definition or match term used to pass runtime parameters to a filter.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hint', full_name='Filter.hint', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227Textual descriptions of a problem, fix and/or findings.'), file=DESCRIPTOR),
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
  serialized_start=2285,
  serialized_end=2544,
)


_CHECKRESULT = _descriptor.Descriptor(
  name='CheckResult',
  full_name='CheckResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='check_id', full_name='CheckResult.check_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0018\0226The check id, identifies what check is being reported.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='anomaly', full_name='CheckResult.anomaly', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001/\022-Specific findings indicating an issue exists.'), file=DESCRIPTOR),
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
  serialized_start=2547,
  serialized_end=2724,
)


_CHECKRESULTS = _descriptor.Descriptor(
  name='CheckResults',
  full_name='CheckResults',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='kb', full_name='CheckResults.kb', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\031\022\027Details about the host.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='CheckResults.result', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\036\022\034The check results for a host'), file=DESCRIPTOR),
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
  serialized_start=2727,
  serialized_end=2870,
)


_HINT = _descriptor.Descriptor(
  name='Hint',
  full_name='Hint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='problem', full_name='Hint.problem', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001\035\022\033A description of the issue.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fix', full_name='Hint.fix', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001(\022&A description of how to fix the issue.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='format', full_name='Hint.format', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0017\0225A template expression to format finding for an issue.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='summary', full_name='Hint.summary', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227A short name or term used to describe the type of data.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_results', full_name='Hint.max_results', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0013\0221Maximum number of findings to include in results.'), file=DESCRIPTOR),
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
  serialized_start=2873,
  serialized_end=3235,
)


_TARGET = _descriptor.Descriptor(
  name='Target',
  full_name='Target',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpe', full_name='Target.cpe', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0019\0227Restrict this check to hosts with any of these CPE ids.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='os', full_name='Target.os', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\001:\0228Restrict this check to hosts with any of these OS types.'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='Target.label', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\342\374\343\304\0018\0226Restrict this check to hosts with any of these labels.'), file=DESCRIPTOR),
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
  serialized_start=3238,
  serialized_end=3481,
)

_CHECK.fields_by_name['method'].message_type = _METHOD
_CHECK.fields_by_name['match'].enum_type = _MATCH
_CHECK.fields_by_name['target'].message_type = _TARGET
_CHECK.fields_by_name['hint'].message_type = _HINT
_METHOD.fields_by_name['probe'].message_type = _PROBE
_METHOD.fields_by_name['match'].enum_type = _MATCH
_METHOD.fields_by_name['resource'].message_type = grr__response__proto_dot_jobs__pb2._DICT
_METHOD.fields_by_name['target'].message_type = _TARGET
_METHOD.fields_by_name['hint'].message_type = _HINT
_PROBE.fields_by_name['mode'].enum_type = _PROBE_MODE
_PROBE.fields_by_name['baseline'].message_type = _FILTER
_PROBE.fields_by_name['filters'].message_type = _FILTER
_PROBE.fields_by_name['match'].enum_type = _MATCH
_PROBE.fields_by_name['target'].message_type = _TARGET
_PROBE.fields_by_name['hint'].message_type = _HINT
_PROBE.fields_by_name['result_context'].enum_type = _PROBE_RESULTCONTEXT
_PROBE_MODE.containing_type = _PROBE
_PROBE_RESULTCONTEXT.containing_type = _PROBE
_FILTER.fields_by_name['hint'].message_type = _HINT
_CHECKRESULT.fields_by_name['anomaly'].message_type = grr__response__proto_dot_anomaly__pb2._ANOMALY
_CHECKRESULTS.fields_by_name['kb'].message_type = grr__response__proto_dot_knowledge__base__pb2._KNOWLEDGEBASE
_CHECKRESULTS.fields_by_name['result'].message_type = _CHECKRESULT
DESCRIPTOR.message_types_by_name['Check'] = _CHECK
DESCRIPTOR.message_types_by_name['Method'] = _METHOD
DESCRIPTOR.message_types_by_name['Probe'] = _PROBE
DESCRIPTOR.message_types_by_name['Filter'] = _FILTER
DESCRIPTOR.message_types_by_name['CheckResult'] = _CHECKRESULT
DESCRIPTOR.message_types_by_name['CheckResults'] = _CHECKRESULTS
DESCRIPTOR.message_types_by_name['Hint'] = _HINT
DESCRIPTOR.message_types_by_name['Target'] = _TARGET
DESCRIPTOR.enum_types_by_name['Match'] = _MATCH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Check = _reflection.GeneratedProtocolMessageType('Check', (_message.Message,), dict(
  DESCRIPTOR = _CHECK,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Check)
  ))
_sym_db.RegisterMessage(Check)

Method = _reflection.GeneratedProtocolMessageType('Method', (_message.Message,), dict(
  DESCRIPTOR = _METHOD,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Method)
  ))
_sym_db.RegisterMessage(Method)

Probe = _reflection.GeneratedProtocolMessageType('Probe', (_message.Message,), dict(
  DESCRIPTOR = _PROBE,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Probe)
  ))
_sym_db.RegisterMessage(Probe)

Filter = _reflection.GeneratedProtocolMessageType('Filter', (_message.Message,), dict(
  DESCRIPTOR = _FILTER,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Filter)
  ))
_sym_db.RegisterMessage(Filter)

CheckResult = _reflection.GeneratedProtocolMessageType('CheckResult', (_message.Message,), dict(
  DESCRIPTOR = _CHECKRESULT,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:CheckResult)
  ))
_sym_db.RegisterMessage(CheckResult)

CheckResults = _reflection.GeneratedProtocolMessageType('CheckResults', (_message.Message,), dict(
  DESCRIPTOR = _CHECKRESULTS,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:CheckResults)
  ))
_sym_db.RegisterMessage(CheckResults)

Hint = _reflection.GeneratedProtocolMessageType('Hint', (_message.Message,), dict(
  DESCRIPTOR = _HINT,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Hint)
  ))
_sym_db.RegisterMessage(Hint)

Target = _reflection.GeneratedProtocolMessageType('Target', (_message.Message,), dict(
  DESCRIPTOR = _TARGET,
  __module__ = 'grr_response_proto.checks_pb2'
  # @@protoc_insertion_point(class_scope:Target)
  ))
_sym_db.RegisterMessage(Target)


_CHECK.fields_by_name['check_id']._options = None
_CHECK.fields_by_name['method']._options = None
_CHECK.fields_by_name['match']._options = None
_CHECK.fields_by_name['target']._options = None
_CHECK.fields_by_name['hint']._options = None
_METHOD.fields_by_name['probe']._options = None
_METHOD.fields_by_name['match']._options = None
_METHOD.fields_by_name['resource']._options = None
_METHOD.fields_by_name['target']._options = None
_METHOD.fields_by_name['hint']._options = None
_PROBE.fields_by_name['artifact']._options = None
_PROBE.fields_by_name['parser']._options = None
_PROBE.fields_by_name['mode']._options = None
_PROBE.fields_by_name['baseline']._options = None
_PROBE.fields_by_name['filters']._options = None
_PROBE.fields_by_name['match']._options = None
_PROBE.fields_by_name['target']._options = None
_PROBE.fields_by_name['hint']._options = None
_PROBE.fields_by_name['result_context']._options = None
_FILTER.fields_by_name['type']._options = None
_FILTER.fields_by_name['expression']._options = None
_FILTER.fields_by_name['hint']._options = None
_CHECKRESULT.fields_by_name['check_id']._options = None
_CHECKRESULT.fields_by_name['anomaly']._options = None
_CHECKRESULTS.fields_by_name['kb']._options = None
_CHECKRESULTS.fields_by_name['result']._options = None
_HINT.fields_by_name['problem']._options = None
_HINT.fields_by_name['fix']._options = None
_HINT.fields_by_name['format']._options = None
_HINT.fields_by_name['summary']._options = None
_HINT.fields_by_name['max_results']._options = None
_TARGET.fields_by_name['cpe']._options = None
_TARGET.fields_by_name['os']._options = None
_TARGET.fields_by_name['label']._options = None
# @@protoc_insertion_point(module_scope)
