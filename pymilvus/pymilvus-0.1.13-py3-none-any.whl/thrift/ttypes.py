#
# Autogenerated by Thrift Compiler (0.12.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class ErrorCode(object):
    SUCCESS = 0
    UNEXPECTED_ERROR = 1
    CONNECT_FAILED = 2
    PERMISSION_DENIED = 3
    TABLE_NOT_EXISTS = 4
    ILLEGAL_ARGUMENT = 5
    ILLEGAL_RANGE = 6
    ILLEGAL_DIMENSION = 7
    ILLEGAL_INDEX_TYPE = 8
    ILLEGAL_TABLE_NAME = 9
    ILLEGAL_TOPK = 10
    ILLEGAL_ROWRECORD = 11
    ILLEGAL_VECTOR_ID = 12
    ILLEGAL_SEARCH_RESULT = 13
    FILE_NOT_FOUND = 14
    META_FAILED = 15
    CACHE_FAILED = 16
    CANNOT_CREATE_FOLDER = 17
    CANNOT_CREATE_FILE = 18
    CANNOT_DELETE_FOLDER = 19
    CANNOT_DELETE_FILE = 20

    _VALUES_TO_NAMES = {
        0: "SUCCESS",
        1: "UNEXPECTED_ERROR",
        2: "CONNECT_FAILED",
        3: "PERMISSION_DENIED",
        4: "TABLE_NOT_EXISTS",
        5: "ILLEGAL_ARGUMENT",
        6: "ILLEGAL_RANGE",
        7: "ILLEGAL_DIMENSION",
        8: "ILLEGAL_INDEX_TYPE",
        9: "ILLEGAL_TABLE_NAME",
        10: "ILLEGAL_TOPK",
        11: "ILLEGAL_ROWRECORD",
        12: "ILLEGAL_VECTOR_ID",
        13: "ILLEGAL_SEARCH_RESULT",
        14: "FILE_NOT_FOUND",
        15: "META_FAILED",
        16: "CACHE_FAILED",
        17: "CANNOT_CREATE_FOLDER",
        18: "CANNOT_CREATE_FILE",
        19: "CANNOT_DELETE_FOLDER",
        20: "CANNOT_DELETE_FILE",
    }

    _NAMES_TO_VALUES = {
        "SUCCESS": 0,
        "UNEXPECTED_ERROR": 1,
        "CONNECT_FAILED": 2,
        "PERMISSION_DENIED": 3,
        "TABLE_NOT_EXISTS": 4,
        "ILLEGAL_ARGUMENT": 5,
        "ILLEGAL_RANGE": 6,
        "ILLEGAL_DIMENSION": 7,
        "ILLEGAL_INDEX_TYPE": 8,
        "ILLEGAL_TABLE_NAME": 9,
        "ILLEGAL_TOPK": 10,
        "ILLEGAL_ROWRECORD": 11,
        "ILLEGAL_VECTOR_ID": 12,
        "ILLEGAL_SEARCH_RESULT": 13,
        "FILE_NOT_FOUND": 14,
        "META_FAILED": 15,
        "CACHE_FAILED": 16,
        "CANNOT_CREATE_FOLDER": 17,
        "CANNOT_CREATE_FILE": 18,
        "CANNOT_DELETE_FOLDER": 19,
        "CANNOT_DELETE_FILE": 20,
    }


class Exception(TException):
    """
    Attributes:
     - code
     - reason

    """


    def __init__(self, code=None, reason=None,):
        self.code = code
        self.reason = reason

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.code = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.reason = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Exception')
        if self.code is not None:
            oprot.writeFieldBegin('code', TType.I32, 1)
            oprot.writeI32(self.code)
            oprot.writeFieldEnd()
        if self.reason is not None:
            oprot.writeFieldBegin('reason', TType.STRING, 2)
            oprot.writeString(self.reason.encode('utf-8') if sys.version_info[0] == 2 else self.reason)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TableSchema(object):
    """
    @brief Table Schema

    Attributes:
     - table_name
     - index_type
     - dimension
     - store_raw_vector

    """


    def __init__(self, table_name=None, index_type=0, dimension=0, store_raw_vector=False,):
        self.table_name = table_name
        self.index_type = index_type
        self.dimension = dimension
        self.store_raw_vector = store_raw_vector

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.table_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.index_type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.dimension = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.BOOL:
                    self.store_raw_vector = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TableSchema')
        if self.table_name is not None:
            oprot.writeFieldBegin('table_name', TType.STRING, 1)
            oprot.writeString(self.table_name.encode('utf-8') if sys.version_info[0] == 2 else self.table_name)
            oprot.writeFieldEnd()
        if self.index_type is not None:
            oprot.writeFieldBegin('index_type', TType.I32, 2)
            oprot.writeI32(self.index_type)
            oprot.writeFieldEnd()
        if self.dimension is not None:
            oprot.writeFieldBegin('dimension', TType.I64, 3)
            oprot.writeI64(self.dimension)
            oprot.writeFieldEnd()
        if self.store_raw_vector is not None:
            oprot.writeFieldBegin('store_raw_vector', TType.BOOL, 4)
            oprot.writeBool(self.store_raw_vector)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.table_name is None:
            raise TProtocolException(message='Required field table_name is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Range(object):
    """
    @brief Range Schema

    Attributes:
     - start_value
     - end_value

    """


    def __init__(self, start_value=None, end_value=None,):
        self.start_value = start_value
        self.end_value = end_value

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.start_value = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.end_value = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Range')
        if self.start_value is not None:
            oprot.writeFieldBegin('start_value', TType.STRING, 1)
            oprot.writeString(self.start_value.encode('utf-8') if sys.version_info[0] == 2 else self.start_value)
            oprot.writeFieldEnd()
        if self.end_value is not None:
            oprot.writeFieldBegin('end_value', TType.STRING, 2)
            oprot.writeString(self.end_value.encode('utf-8') if sys.version_info[0] == 2 else self.end_value)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class RowRecord(object):
    """
    @brief Record inserted

    Attributes:
     - vector_data

    """


    def __init__(self, vector_data=None,):
        self.vector_data = vector_data

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.vector_data = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('RowRecord')
        if self.vector_data is not None:
            oprot.writeFieldBegin('vector_data', TType.STRING, 1)
            oprot.writeBinary(self.vector_data)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.vector_data is None:
            raise TProtocolException(message='Required field vector_data is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class QueryResult(object):
    """
    @brief Query result

    Attributes:
     - id
     - score

    """


    def __init__(self, id=None, score=None,):
        self.id = id
        self.score = score

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.id = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.DOUBLE:
                    self.score = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('QueryResult')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I64, 1)
            oprot.writeI64(self.id)
            oprot.writeFieldEnd()
        if self.score is not None:
            oprot.writeFieldBegin('score', TType.DOUBLE, 2)
            oprot.writeDouble(self.score)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TopKQueryResult(object):
    """
    @brief TopK query result

    Attributes:
     - query_result_arrays

    """


    def __init__(self, query_result_arrays=None,):
        self.query_result_arrays = query_result_arrays

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.query_result_arrays = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = QueryResult()
                        _elem5.read(iprot)
                        self.query_result_arrays.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TopKQueryResult')
        if self.query_result_arrays is not None:
            oprot.writeFieldBegin('query_result_arrays', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.query_result_arrays))
            for iter6 in self.query_result_arrays:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(Exception)
Exception.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'code', None, None, ),  # 1
    (2, TType.STRING, 'reason', 'UTF8', None, ),  # 2
)
all_structs.append(TableSchema)
TableSchema.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'table_name', 'UTF8', None, ),  # 1
    (2, TType.I32, 'index_type', None, 0, ),  # 2
    (3, TType.I64, 'dimension', None, 0, ),  # 3
    (4, TType.BOOL, 'store_raw_vector', None, False, ),  # 4
)
all_structs.append(Range)
Range.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'start_value', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'end_value', 'UTF8', None, ),  # 2
)
all_structs.append(RowRecord)
RowRecord.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'vector_data', 'BINARY', None, ),  # 1
)
all_structs.append(QueryResult)
QueryResult.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'id', None, None, ),  # 1
    (2, TType.DOUBLE, 'score', None, None, ),  # 2
)
all_structs.append(TopKQueryResult)
TopKQueryResult.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'query_result_arrays', (TType.STRUCT, [QueryResult, None], False), None, ),  # 1
)
fix_spec(all_structs)
del all_structs
