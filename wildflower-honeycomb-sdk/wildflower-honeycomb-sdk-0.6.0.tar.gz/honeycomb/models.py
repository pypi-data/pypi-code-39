# this file is generated, do not modify
from enum import Enum
from typing import List, NewType, TypeVar, Union

from gqlpycgen.api import QueryBase, ObjectBase, MutationBase


ID = NewType('ID', str)
Int = NewType('Int', int)
String = NewType('String', str)
Float = NewType('Float', float)
Boolean = NewType('Boolean', bool)
Upload = NewType('Upload', str)
DateTime = NewType('DateTime', str)


class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return str(self.value)


class SensorType(Enum):
    CAMERA = "CAMERA"
    RADIO = "RADIO"
    ACCELEROMETER = "ACCELEROMETER"
    GYROSCOPE = "GYROSCOPE"
    MAGNETOMETER = "MAGNETOMETER"
    INERTIAL = "INERTIAL"

    def __str__(self):
        return str(self.value)


class PropertyType(Enum):
    BOOL = "BOOL"
    STR = "STR"
    INT = "INT"
    FLOAT = "FLOAT"
    NULL = "NULL"

    def __str__(self):
        return str(self.value)


class AssignableTypeEnum(Enum):
    PERSON = "PERSON"
    DEVICE = "DEVICE"

    def __str__(self):
        return str(self.value)


class Operator(Enum):
    OR = "OR"
    AND = "AND"
    NOT = "NOT"
    EQ = "EQ"
    NE = "NE"
    LIKE = "LIKE"
    RE = "RE"
    IN = "IN"
    LT = "LT"
    GT = "GT"
    LTE = "LTE"
    GTE = "GTE"

    def __str__(self):
        return str(self.value)


class Status(Enum):
    ok = "ok"
    error = "error"

    def __str__(self):
        return str(self.value)


class DataFormat(Enum):
    BINARY = "BINARY"
    CSV = "CSV"
    IMAGE = "IMAGE"
    JSON = "JSON"
    TEXT = "TEXT"
    VIDEO = "VIDEO"

    def __str__(self):
        return str(self.value)


class Tuple(ObjectBase):
    FIELDS = ["x", "y", "z", ]
    TYPES = {"x": "Float", "y": "Float", "z": "Float"}

    def __init__(self, x: 'Float'=None, y: 'Float'=None, z: 'Float'=None):
        self.x = x
        self.y = y
        self.z = z


class DeviceList(ObjectBase):
    FIELDS = ["data", ]
    TYPES = {"data": "List[Device]"}

    def __init__(self, data: 'List[Device]'=None):
        self.data = data


class Device(ObjectBase):
    FIELDS = ["device_id", "part_number", "name", "tag_id", "description", "sensors", "configurations", "system", ]
    TYPES = {"device_id": "ID", "part_number": "String", "name": "String", "tag_id": "String", "description": "String", "sensors": "List[SensorInstallation]", "configurations": "List[DeviceConfiguration]", "system": "System"}

    def __init__(self, device_id: 'ID'=None, part_number: 'String'=None, name: 'String'=None, tag_id: 'String'=None, description: 'String'=None, sensors: 'List[SensorInstallation]'=None, configurations: 'List[DeviceConfiguration]'=None, system: 'System'=None):
        self.device_id = device_id
        self.part_number = part_number
        self.name = name
        self.tag_id = tag_id
        self.description = description
        self.sensors = sensors
        self.configurations = configurations
        self.system = system


class SensorInstallation(ObjectBase):
    FIELDS = ["sensor_install_id", "device", "description", "start", "end", "sensor", "tag_id", "config", "system", ]
    TYPES = {"sensor_install_id": "ID", "device": "Device", "description": "String", "start": "DateTime", "end": "DateTime", "sensor": "Sensor", "tag_id": "String", "config": "List[Property]", "system": "System"}

    def __init__(self, sensor_install_id: 'ID'=None, device: 'Device'=None, description: 'String'=None, start: 'DateTime'=None, end: 'DateTime'=None, sensor: 'Sensor'=None, tag_id: 'String'=None, config: 'List[Property]'=None, system: 'System'=None):
        self.sensor_install_id = sensor_install_id
        self.device = device
        self.description = description
        self.start = start
        self.end = end
        self.sensor = sensor
        self.tag_id = tag_id
        self.config = config
        self.system = system


class Sensor(ObjectBase):
    FIELDS = ["sensor_id", "part_number", "name", "description", "sensor_type", "version", "default_config", "system", ]
    TYPES = {"sensor_id": "ID", "part_number": "String", "name": "String", "description": "String", "sensor_type": "SensorType", "version": "Int", "default_config": "List[Property]", "system": "System"}

    def __init__(self, sensor_id: 'ID'=None, part_number: 'String'=None, name: 'String'=None, description: 'String'=None, sensor_type: 'SensorType'=None, version: 'Int'=None, default_config: 'List[Property]'=None, system: 'System'=None):
        self.sensor_id = sensor_id
        self.part_number = part_number
        self.name = name
        self.description = description
        self.sensor_type = sensor_type
        self.version = version
        self.default_config = default_config
        self.system = system


class Property(ObjectBase):
    FIELDS = ["name", "value", "type", ]
    TYPES = {"name": "String", "value": "String", "type": "PropertyType"}

    def __init__(self, name: 'String'=None, value: 'String'=None, type: 'PropertyType'=None):
        self.name = name
        self.value = value
        self.type = type


class DeviceConfiguration(ObjectBase):
    FIELDS = ["device_configuration_id", "device", "start", "end", "properties", "system", ]
    TYPES = {"device_configuration_id": "ID", "device": "Device", "start": "DateTime", "end": "DateTime", "properties": "List[Property]", "system": "System"}

    def __init__(self, device_configuration_id: 'ID'=None, device: 'Device'=None, start: 'DateTime'=None, end: 'DateTime'=None, properties: 'List[Property]'=None, system: 'System'=None):
        self.device_configuration_id = device_configuration_id
        self.device = device
        self.start = start
        self.end = end
        self.properties = properties
        self.system = system


class SensorList(ObjectBase):
    FIELDS = ["data", ]
    TYPES = {"data": "List[Sensor]"}

    def __init__(self, data: 'List[Sensor]'=None):
        self.data = data


class SensorInstallationList(ObjectBase):
    FIELDS = ["data", ]
    TYPES = {"data": "List[SensorInstallation]"}

    def __init__(self, data: 'List[SensorInstallation]'=None):
        self.data = data


class EnvironmentList(ObjectBase):
    FIELDS = ["data", ]
    TYPES = {"data": "List[Environment]"}

    def __init__(self, data: 'List[Environment]'=None):
        self.data = data


class Environment(ObjectBase):
    FIELDS = ["environment_id", "name", "description", "location", "assignments", "layouts", "system", ]
    TYPES = {"environment_id": "ID", "name": "String", "description": "String", "location": "String", "assignments": "List[Assignment]", "layouts": "List[Layout]", "system": "System"}

    def __init__(self, environment_id: 'ID'=None, name: 'String'=None, description: 'String'=None, location: 'String'=None, assignments: 'List[Assignment]'=None, layouts: 'List[Layout]'=None, system: 'System'=None):
        self.environment_id = environment_id
        self.name = name
        self.description = description
        self.location = location
        self.assignments = assignments
        self.layouts = layouts
        self.system = system


class Assignment(ObjectBase):
    FIELDS = ["assignment_id", "environment", "assigned", "assigned_type", "start", "end", "data", "system", ]
    TYPES = {"assignment_id": "ID", "environment": "Environment", "assigned": "Assignable", "assigned_type": "AssignableTypeEnum", "start": "DateTime", "end": "DateTime", "data": "List[Datapoint]", "system": "System"}

    def __init__(self, assignment_id: 'ID'=None, environment: 'Environment'=None, assigned: 'Assignable'=None, assigned_type: 'AssignableTypeEnum'=None, start: 'DateTime'=None, end: 'DateTime'=None, data: 'List[Datapoint]'=None, system: 'System'=None):
        self.assignment_id = assignment_id
        self.environment = environment
        self.assigned = assigned
        self.assigned_type = assigned_type
        self.start = start
        self.end = end
        self.data = data
        self.system = system


class Person(ObjectBase):
    FIELDS = ["person_id", "name", ]
    TYPES = {"person_id": "ID", "name": "String"}

    def __init__(self, person_id: 'ID'=None, name: 'String'=None):
        self.person_id = person_id
        self.name = name


class Datapoint(ObjectBase):
    FIELDS = ["data_id", "parents", "format", "file", "url", "observed_time", "observer", "duration", "system", ]
    TYPES = {"data_id": "ID", "parents": "List[Datapoint]", "format": "String", "file": "S3File", "url": "String", "observed_time": "DateTime", "observer": "Observer", "duration": "Int", "system": "System"}

    def __init__(self, data_id: 'ID'=None, parents: 'List[Datapoint]'=None, format: 'String'=None, file: 'S3File'=None, url: 'String'=None, observed_time: 'DateTime'=None, observer: 'Observer'=None, duration: 'Int'=None, system: 'System'=None):
        self.data_id = data_id
        self.parents = parents
        self.format = format
        self.file = file
        self.url = url
        self.observed_time = observed_time
        self.observer = observer
        self.duration = duration
        self.system = system


class S3File(ObjectBase):
    FIELDS = ["name", "bucketName", "key", "data", "filename", "mime", "encoding", "contentType", "size", "created", ]
    TYPES = {"name": "String", "bucketName": "String", "key": "String", "data": "String", "filename": "String", "mime": "String", "encoding": "String", "contentType": "String", "size": "Int", "created": "String"}

    def __init__(self, name: 'String'=None, bucketName: 'String'=None, key: 'String'=None, data: 'String'=None, filename: 'String'=None, mime: 'String'=None, encoding: 'String'=None, contentType: 'String'=None, size: 'Int'=None, created: 'String'=None):
        self.name = name
        self.bucketName = bucketName
        self.key = key
        self.data = data
        self.filename = filename
        self.mime = mime
        self.encoding = encoding
        self.contentType = contentType
        self.size = size
        self.created = created


class Layout(ObjectBase):
    FIELDS = ["layout_id", "environment", "spaces", "objects", "start", "end", "system", ]
    TYPES = {"layout_id": "ID", "environment": "Environment", "spaces": "List[Rect]", "objects": "List[Rect]", "start": "DateTime", "end": "DateTime", "system": "System"}

    def __init__(self, layout_id: 'ID'=None, environment: 'Environment'=None, spaces: 'List[Rect]'=None, objects: 'List[Rect]'=None, start: 'DateTime'=None, end: 'DateTime'=None, system: 'System'=None):
        self.layout_id = layout_id
        self.environment = environment
        self.spaces = spaces
        self.objects = objects
        self.start = start
        self.end = end
        self.system = system


class Rect(ObjectBase):
    FIELDS = ["name", "x", "y", "width", "height", ]
    TYPES = {"name": "String", "x": "Int", "y": "Int", "width": "Int", "height": "Int"}

    def __init__(self, name: 'String'=None, x: 'Int'=None, y: 'Int'=None, width: 'Int'=None, height: 'Int'=None):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class DatapointList(ObjectBase):
    FIELDS = ["data", ]
    TYPES = {"data": "List[Datapoint]"}

    def __init__(self, data: 'List[Datapoint]'=None):
        self.data = data


class DeleteStatusResponse(ObjectBase):
    FIELDS = ["status", "error", ]
    TYPES = {"status": "Status", "error": "String"}

    def __init__(self, status: 'Status'=None, error: 'String'=None):
        self.status = status
        self.error = error


class Sort(ObjectBase):
    FIELDS = ["field", "direction", ]
    TYPES = {"field": "String", "direction": "SortDirection"}

    def __init__(self, field: 'String'=None, direction: 'SortDirection'=None):
        self.field = field
        self.direction = direction


class PageInfo(ObjectBase):
    FIELDS = ["total", "count", "max", "cursor", "sort", ]
    TYPES = {"total": "Int", "count": "Int", "max": "Int", "cursor": "String", "sort": "Sort"}

    def __init__(self, total: 'Int'=None, count: 'Int'=None, max: 'Int'=None, cursor: 'String'=None, sort: 'Sort'=None):
        self.total = total
        self.count = count
        self.max = max
        self.cursor = cursor
        self.sort = sort


class System(ObjectBase):
    FIELDS = ["type_name", "created", "last_modified", ]
    TYPES = {"type_name": "String", "created": "DateTime", "last_modified": "DateTime"}

    def __init__(self, type_name: 'String'=None, created: 'DateTime'=None, last_modified: 'DateTime'=None):
        self.type_name = type_name
        self.created = created
        self.last_modified = last_modified


class CoordinateSpace(ObjectBase):
    FIELDS = ["space_id", "name", "environment", "start", "end", "system", ]
    TYPES = {"space_id": "ID", "name": "String", "environment": "Environment", "start": "DateTime", "end": "DateTime", "system": "System"}

    def __init__(self, space_id: 'ID'=None, name: 'String'=None, environment: 'Environment'=None, start: 'DateTime'=None, end: 'DateTime'=None, system: 'System'=None):
        self.space_id = space_id
        self.name = name
        self.environment = environment
        self.start = start
        self.end = end
        self.system = system


class Vector(ObjectBase):
    FIELDS = ["x", "y", "z", ]
    TYPES = {"x": "Float", "y": "Float", "z": "Float"}

    def __init__(self, x: 'Float'=None, y: 'Float'=None, z: 'Float'=None):
        self.x = x
        self.y = y
        self.z = z


class Point(ObjectBase):
    FIELDS = ["x", "y", "z", ]
    TYPES = {"x": "Float", "y": "Float", "z": "Float"}

    def __init__(self, x: 'Float'=None, y: 'Float'=None, z: 'Float'=None):
        self.x = x
        self.y = y
        self.z = z


class Pair(ObjectBase):
    FIELDS = ["x", "y", ]
    TYPES = {"x": "Float", "y": "Float"}

    def __init__(self, x: 'Float'=None, y: 'Float'=None):
        self.x = x
        self.y = y


class CameraParameters(ObjectBase):
    FIELDS = ["camera_matrix", "distortion_coeffs", ]
    TYPES = {"camera_matrix": "List[Float]", "distortion_coeffs": "List[Float]"}

    def __init__(self, camera_matrix: 'List[Float]'=None, distortion_coeffs: 'List[Float]'=None):
        self.camera_matrix = camera_matrix
        self.distortion_coeffs = distortion_coeffs


class ExtrinsicCalibration(ObjectBase):
    FIELDS = ["start", "end", "translation", "rotation", "objects", ]
    TYPES = {"start": "DateTime", "end": "DateTime", "translation": "Tuple", "rotation": "Tuple", "objects": "List[GeometricObject]"}

    def __init__(self, start: 'DateTime'=None, end: 'DateTime'=None, translation: 'Tuple'=None, rotation: 'Tuple'=None, objects: 'List[GeometricObject]'=None):
        self.start = start
        self.end = end
        self.translation = translation
        self.rotation = rotation
        self.objects = objects


class PaginationInput(ObjectBase):
    FIELDS = ["max", "cursor", "sort", ]
    TYPES = {"max": "Int", "cursor": "String", "sort": "List[SortInput]"}

    def __init__(self, max: 'Int'=None, cursor: 'String'=None, sort: 'List[SortInput]'=None):
        self.max = max
        self.cursor = cursor
        self.sort = sort


class SortInput(ObjectBase):
    FIELDS = ["field", "direction", ]
    TYPES = {"field": "String", "direction": "SortDirection"}

    def __init__(self, field: 'String'=None, direction: 'SortDirection'=None):
        self.field = field
        self.direction = direction


class QueryExpression(ObjectBase):
    FIELDS = ["field", "operator", "value", "children", ]
    TYPES = {"field": "String", "operator": "Operator", "value": "String", "children": "List[QueryExpression]"}

    def __init__(self, field: 'String'=None, operator: 'Operator'=None, value: 'String'=None, children: 'List[QueryExpression]'=None):
        self.field = field
        self.operator = operator
        self.value = value
        self.children = children


class DeviceInput(ObjectBase):
    FIELDS = ["name", "description", "part_number", "tag_id", ]
    TYPES = {"name": "String", "description": "String", "part_number": "String", "tag_id": "String"}

    def __init__(self, name: 'String'=None, description: 'String'=None, part_number: 'String'=None, tag_id: 'String'=None):
        self.name = name
        self.description = description
        self.part_number = part_number
        self.tag_id = tag_id


class DeviceConfigurationInput(ObjectBase):
    FIELDS = ["device", "start", "end", "properties", ]
    TYPES = {"device": "ID", "start": "DateTime", "end": "DateTime", "properties": "List[PropertyInput]"}

    def __init__(self, device: 'ID'=None, start: 'DateTime'=None, end: 'DateTime'=None, properties: 'List[PropertyInput]'=None):
        self.device = device
        self.start = start
        self.end = end
        self.properties = properties


class PropertyInput(ObjectBase):
    FIELDS = ["name", "value", "type", ]
    TYPES = {"name": "String", "value": "String", "type": "PropertyType"}

    def __init__(self, name: 'String'=None, value: 'String'=None, type: 'PropertyType'=None):
        self.name = name
        self.value = value
        self.type = type


class SensorInput(ObjectBase):
    FIELDS = ["part_number", "name", "description", "sensor_type", "version", "default_config", ]
    TYPES = {"part_number": "String", "name": "String", "description": "String", "sensor_type": "SensorType", "version": "Int", "default_config": "List[PropertyInput]"}

    def __init__(self, part_number: 'String'=None, name: 'String'=None, description: 'String'=None, sensor_type: 'SensorType'=None, version: 'Int'=None, default_config: 'List[PropertyInput]'=None):
        self.part_number = part_number
        self.name = name
        self.description = description
        self.sensor_type = sensor_type
        self.version = version
        self.default_config = default_config


class SensorInstallationInput(ObjectBase):
    FIELDS = ["device", "sensor", "description", "start", "end", "tag_id", "config", ]
    TYPES = {"device": "ID", "sensor": "ID", "description": "String", "start": "DateTime", "end": "DateTime", "tag_id": "String", "config": "List[PropertyInput]"}

    def __init__(self, device: 'ID'=None, sensor: 'ID'=None, description: 'String'=None, start: 'DateTime'=None, end: 'DateTime'=None, tag_id: 'String'=None, config: 'List[PropertyInput]'=None):
        self.device = device
        self.sensor = sensor
        self.description = description
        self.start = start
        self.end = end
        self.tag_id = tag_id
        self.config = config


class SensorInstallationUpdateInput(ObjectBase):
    FIELDS = ["description", "start", "end", "tag_id", "config", ]
    TYPES = {"description": "String", "start": "DateTime", "end": "DateTime", "tag_id": "String", "config": "List[PropertyInput]"}

    def __init__(self, description: 'String'=None, start: 'DateTime'=None, end: 'DateTime'=None, tag_id: 'String'=None, config: 'List[PropertyInput]'=None):
        self.description = description
        self.start = start
        self.end = end
        self.tag_id = tag_id
        self.config = config


class EnvironmentInput(ObjectBase):
    FIELDS = ["name", "description", "location", ]
    TYPES = {"name": "String", "description": "String", "location": "String"}

    def __init__(self, name: 'String'=None, description: 'String'=None, location: 'String'=None):
        self.name = name
        self.description = description
        self.location = location


class AssignmentInput(ObjectBase):
    FIELDS = ["environment", "assigned_type", "assigned", "start", "end", ]
    TYPES = {"environment": "ID", "assigned_type": "AssignableTypeEnum", "assigned": "ID", "start": "DateTime", "end": "DateTime"}

    def __init__(self, environment: 'ID'=None, assigned_type: 'AssignableTypeEnum'=None, assigned: 'ID'=None, start: 'DateTime'=None, end: 'DateTime'=None):
        self.environment = environment
        self.assigned_type = assigned_type
        self.assigned = assigned
        self.start = start
        self.end = end


class AssignmentUpdateInput(ObjectBase):
    FIELDS = ["end", ]
    TYPES = {"end": "DateTime"}

    def __init__(self, end: 'DateTime'=None):
        self.end = end


class LayoutInput(ObjectBase):
    FIELDS = ["environment", "spaces", "objects", "start", "end", ]
    TYPES = {"environment": "ID", "spaces": "List[RectInput]", "objects": "List[RectInput]", "start": "DateTime", "end": "DateTime"}

    def __init__(self, environment: 'ID'=None, spaces: 'List[RectInput]'=None, objects: 'List[RectInput]'=None, start: 'DateTime'=None, end: 'DateTime'=None):
        self.environment = environment
        self.spaces = spaces
        self.objects = objects
        self.start = start
        self.end = end


class RectInput(ObjectBase):
    FIELDS = ["name", "x", "y", "width", "height", ]
    TYPES = {"name": "String", "x": "Int", "y": "Int", "width": "Int", "height": "Int"}

    def __init__(self, name: 'String'=None, x: 'Int'=None, y: 'Int'=None, width: 'Int'=None, height: 'Int'=None):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class DatapointInput(ObjectBase):
    FIELDS = ["format", "file", "observed_time", "observer", "parents", "duration", ]
    TYPES = {"format": "String", "file": "S3FileInput", "observed_time": "DateTime", "observer": "ID", "parents": "List[ID]", "duration": "Int"}

    def __init__(self, format: 'String'=None, file: 'S3FileInput'=None, observed_time: 'DateTime'=None, observer: 'ID'=None, parents: 'List[ID]'=None, duration: 'Int'=None):
        self.format = format
        self.file = file
        self.observed_time = observed_time
        self.observer = observer
        self.parents = parents
        self.duration = duration


class S3FileInput(ObjectBase):
    FIELDS = ["name", "contentType", "data", ]
    TYPES = {"name": "String", "contentType": "String", "data": "Upload"}

    def __init__(self, name: 'String'=None, contentType: 'String'=None, data: 'Upload'=None):
        self.name = name
        self.contentType = contentType
        self.data = data


class CascadeLink(ObjectBase):
    FIELDS = ["target_type_name", "target_field_name", "isS3File", ]
    TYPES = {"target_type_name": "String", "target_field_name": "String", "isS3File": "Boolean"}

    def __init__(self, target_type_name: 'String'=None, target_field_name: 'String'=None, isS3File: 'Boolean'=None):
        self.target_type_name = target_type_name
        self.target_field_name = target_field_name
        self.isS3File = isS3File


class CoordinateSpaceInput(ObjectBase):
    FIELDS = ["name", "start", "end", ]
    TYPES = {"name": "String", "start": "DateTime", "end": "DateTime"}

    def __init__(self, name: 'String'=None, start: 'DateTime'=None, end: 'DateTime'=None):
        self.name = name
        self.start = start
        self.end = end


class TupleInput(ObjectBase):
    FIELDS = ["x", "y", "z", ]
    TYPES = {"x": "Float", "y": "Float", "z": "Float"}

    def __init__(self, x: 'Float'=None, y: 'Float'=None, z: 'Float'=None):
        self.x = x
        self.y = y
        self.z = z


class CalibrationInput(ObjectBase):
    FIELDS = ["translation", "rotation", ]
    TYPES = {"translation": "TupleInput", "rotation": "TupleInput"}

    def __init__(self, translation: 'TupleInput'=None, rotation: 'TupleInput'=None):
        self.translation = translation
        self.rotation = rotation


class PersonInput(ObjectBase):
    FIELDS = ["name", ]
    TYPES = {"name": "String"}

    def __init__(self, name: 'String'=None):
        self.name = name


Assignable = Union[Device, Person]
Observer = Union[Assignment, SensorInstallation]
GeometricObject = Union[SensorInstallation, CoordinateSpace]


class Query(QueryBase):

    def devices(self, envId: 'String'=None, page: 'PaginationInput'=None) -> DeviceList:
        args = ["envId: 'String'=None", "page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if envId is not None:
            var_types["envId"] = String
            if hasattr(envId, "to_json"):
                variables["envId"] = envId.to_json()
            else:
                variables["envId"] = envId

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(DeviceList, "devices", variables, var_types)
        results = self.query(query, variables)
        return DeviceList.from_json(results.get("devices"))

    def device(self, device_id: 'ID'=None) -> Device:
        args = ["device_id: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if device_id is not None:
            var_types["device_id"] = ID
            if hasattr(device_id, "to_json"):
                variables["device_id"] = device_id.to_json()
            else:
                variables["device_id"] = device_id

        query = self.prepare(Device, "device", variables, var_types)
        results = self.query(query, variables)
        return Device.from_json(results.get("device"))

    def findDevice(self, name: 'String'=None, part_number: 'String'=None) -> DeviceList:
        args = ["name: 'String'=None", "part_number: 'String'=None"]
        variables = dict()
        var_types = dict()

        if name is not None:
            var_types["name"] = String
            if hasattr(name, "to_json"):
                variables["name"] = name.to_json()
            else:
                variables["name"] = name

        if part_number is not None:
            var_types["part_number"] = String
            if hasattr(part_number, "to_json"):
                variables["part_number"] = part_number.to_json()
            else:
                variables["part_number"] = part_number

        query = self.prepare(DeviceList, "findDevice", variables, var_types)
        results = self.query(query, variables)
        return DeviceList.from_json(results.get("findDevice"))

    def sensors(self, page: 'PaginationInput'=None) -> SensorList:
        args = ["page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(SensorList, "sensors", variables, var_types)
        results = self.query(query, variables)
        return SensorList.from_json(results.get("sensors"))

    def sensor(self, sensor_id: 'ID'=None) -> Sensor:
        args = ["sensor_id: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if sensor_id is not None:
            var_types["sensor_id"] = ID
            if hasattr(sensor_id, "to_json"):
                variables["sensor_id"] = sensor_id.to_json()
            else:
                variables["sensor_id"] = sensor_id

        query = self.prepare(Sensor, "sensor", variables, var_types)
        results = self.query(query, variables)
        return Sensor.from_json(results.get("sensor"))

    def findSensor(self, name: 'String'=None, version: 'Int'=None) -> SensorList:
        args = ["name: 'String'=None", "version: 'Int'=None"]
        variables = dict()
        var_types = dict()

        if name is not None:
            var_types["name"] = String
            if hasattr(name, "to_json"):
                variables["name"] = name.to_json()
            else:
                variables["name"] = name

        if version is not None:
            var_types["version"] = Int
            if hasattr(version, "to_json"):
                variables["version"] = version.to_json()
            else:
                variables["version"] = version

        query = self.prepare(SensorList, "findSensor", variables, var_types)
        results = self.query(query, variables)
        return SensorList.from_json(results.get("findSensor"))

    def sensorInstallations(self, page: 'PaginationInput'=None) -> SensorInstallationList:
        args = ["page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(SensorInstallationList, "sensorInstallations", variables, var_types)
        results = self.query(query, variables)
        return SensorInstallationList.from_json(results.get("sensorInstallations"))

    def environments(self, page: 'PaginationInput'=None) -> EnvironmentList:
        args = ["page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(EnvironmentList, "environments", variables, var_types)
        results = self.query(query, variables)
        return EnvironmentList.from_json(results.get("environments"))

    def getEnvironment(self, environment_id: 'ID'=None) -> Environment:
        args = ["environment_id: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if environment_id is not None:
            var_types["environment_id"] = ID
            if hasattr(environment_id, "to_json"):
                variables["environment_id"] = environment_id.to_json()
            else:
                variables["environment_id"] = environment_id

        query = self.prepare(Environment, "getEnvironment", variables, var_types)
        results = self.query(query, variables)
        return Environment.from_json(results.get("getEnvironment"))

    def findEnvironment(self, name: 'String'=None, location: 'String'=None) -> EnvironmentList:
        args = ["name: 'String'=None", "location: 'String'=None"]
        variables = dict()
        var_types = dict()

        if name is not None:
            var_types["name"] = String
            if hasattr(name, "to_json"):
                variables["name"] = name.to_json()
            else:
                variables["name"] = name

        if location is not None:
            var_types["location"] = String
            if hasattr(location, "to_json"):
                variables["location"] = location.to_json()
            else:
                variables["location"] = location

        query = self.prepare(EnvironmentList, "findEnvironment", variables, var_types)
        results = self.query(query, variables)
        return EnvironmentList.from_json(results.get("findEnvironment"))

    def datapoints(self, page: 'PaginationInput'=None) -> DatapointList:
        args = ["page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(DatapointList, "datapoints", variables, var_types)
        results = self.query(query, variables)
        return DatapointList.from_json(results.get("datapoints"))

    def getDatapoint(self, data_id: 'ID'=None) -> Datapoint:
        args = ["data_id: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if data_id is not None:
            var_types["data_id"] = ID
            if hasattr(data_id, "to_json"):
                variables["data_id"] = data_id.to_json()
            else:
                variables["data_id"] = data_id

        query = self.prepare(Datapoint, "getDatapoint", variables, var_types)
        results = self.query(query, variables)
        return Datapoint.from_json(results.get("getDatapoint"))

    def findDatapointsForObserver(self, observer: 'ID'=None) -> DatapointList:
        args = ["observer: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if observer is not None:
            var_types["observer"] = ID
            if hasattr(observer, "to_json"):
                variables["observer"] = observer.to_json()
            else:
                variables["observer"] = observer

        query = self.prepare(DatapointList, "findDatapointsForObserver", variables, var_types)
        results = self.query(query, variables)
        return DatapointList.from_json(results.get("findDatapointsForObserver"))

    def findDatapoints(self, query: 'QueryExpression'=None, page: 'PaginationInput'=None) -> DatapointList:
        args = ["query: 'QueryExpression'=None", "page: 'PaginationInput'=None"]
        variables = dict()
        var_types = dict()

        if query is not None:
            var_types["query"] = QueryExpression
            if hasattr(query, "to_json"):
                variables["query"] = query.to_json()
            else:
                variables["query"] = query

        if page is not None:
            var_types["page"] = PaginationInput
            if hasattr(page, "to_json"):
                variables["page"] = page.to_json()
            else:
                variables["page"] = page

        query = self.prepare(DatapointList, "findDatapoints", variables, var_types)
        results = self.query(query, variables)
        return DatapointList.from_json(results.get("findDatapoints"))


class Mutation(MutationBase):

    def createDevice(self, device: 'DeviceInput'=None) -> Device:
        args = ["device: 'DeviceInput'=None"]
        variables = dict()
        var_types = dict()

        if device is not None:
            var_types["device"] = DeviceInput
            if hasattr(device, "to_json"):
                variables["device"] = device.to_json()
            else:
                variables["device"] = device

        query = self.prepare(Device, "createDevice", variables, var_types)
        results = self.query(query, variables)
        return Device.from_json(results.get("createDevice"))

    def setDeviceConfiguration(self, deviceConfiguration: 'DeviceConfigurationInput'=None) -> DeviceConfiguration:
        args = ["deviceConfiguration: 'DeviceConfigurationInput'=None"]
        variables = dict()
        var_types = dict()

        if deviceConfiguration is not None:
            var_types["deviceConfiguration"] = DeviceConfigurationInput
            if hasattr(deviceConfiguration, "to_json"):
                variables["deviceConfiguration"] = deviceConfiguration.to_json()
            else:
                variables["deviceConfiguration"] = deviceConfiguration

        query = self.prepare(DeviceConfiguration, "setDeviceConfiguration", variables, var_types)
        results = self.query(query, variables)
        return DeviceConfiguration.from_json(results.get("setDeviceConfiguration"))

    def createSensor(self, sensor: 'SensorInput'=None) -> Sensor:
        args = ["sensor: 'SensorInput'=None"]
        variables = dict()
        var_types = dict()

        if sensor is not None:
            var_types["sensor"] = SensorInput
            if hasattr(sensor, "to_json"):
                variables["sensor"] = sensor.to_json()
            else:
                variables["sensor"] = sensor

        query = self.prepare(Sensor, "createSensor", variables, var_types)
        results = self.query(query, variables)
        return Sensor.from_json(results.get("createSensor"))

    def addSensorToDevice(self, sensorInstallation: 'SensorInstallationInput'=None) -> SensorInstallation:
        args = ["sensorInstallation: 'SensorInstallationInput'=None"]
        variables = dict()
        var_types = dict()

        if sensorInstallation is not None:
            var_types["sensorInstallation"] = SensorInstallationInput
            if hasattr(sensorInstallation, "to_json"):
                variables["sensorInstallation"] = sensorInstallation.to_json()
            else:
                variables["sensorInstallation"] = sensorInstallation

        query = self.prepare(SensorInstallation, "addSensorToDevice", variables, var_types)
        results = self.query(query, variables)
        return SensorInstallation.from_json(results.get("addSensorToDevice"))

    def updateSensorInstall(self, sensor_install_id: 'ID'=None, sensorInstallation: 'SensorInstallationUpdateInput'=None) -> SensorInstallation:
        args = ["sensor_install_id: 'ID'=None", "sensorInstallation: 'SensorInstallationUpdateInput'=None"]
        variables = dict()
        var_types = dict()

        if sensor_install_id is not None:
            var_types["sensor_install_id"] = ID
            if hasattr(sensor_install_id, "to_json"):
                variables["sensor_install_id"] = sensor_install_id.to_json()
            else:
                variables["sensor_install_id"] = sensor_install_id

        if sensorInstallation is not None:
            var_types["sensorInstallation"] = SensorInstallationUpdateInput
            if hasattr(sensorInstallation, "to_json"):
                variables["sensorInstallation"] = sensorInstallation.to_json()
            else:
                variables["sensorInstallation"] = sensorInstallation

        query = self.prepare(SensorInstallation, "updateSensorInstall", variables, var_types)
        results = self.query(query, variables)
        return SensorInstallation.from_json(results.get("updateSensorInstall"))

    def createEnvironment(self, environment: 'EnvironmentInput'=None) -> Environment:
        args = ["environment: 'EnvironmentInput'=None"]
        variables = dict()
        var_types = dict()

        if environment is not None:
            var_types["environment"] = EnvironmentInput
            if hasattr(environment, "to_json"):
                variables["environment"] = environment.to_json()
            else:
                variables["environment"] = environment

        query = self.prepare(Environment, "createEnvironment", variables, var_types)
        results = self.query(query, variables)
        return Environment.from_json(results.get("createEnvironment"))

    def assignToEnvironment(self, assignment: 'AssignmentInput'=None) -> Assignment:
        args = ["assignment: 'AssignmentInput'=None"]
        variables = dict()
        var_types = dict()

        if assignment is not None:
            var_types["assignment"] = AssignmentInput
            if hasattr(assignment, "to_json"):
                variables["assignment"] = assignment.to_json()
            else:
                variables["assignment"] = assignment

        query = self.prepare(Assignment, "assignToEnvironment", variables, var_types)
        results = self.query(query, variables)
        return Assignment.from_json(results.get("assignToEnvironment"))

    def updateAssignment(self, assignment_id: 'ID'=None, assignment: 'AssignmentUpdateInput'=None) -> Assignment:
        args = ["assignment_id: 'ID'=None", "assignment: 'AssignmentUpdateInput'=None"]
        variables = dict()
        var_types = dict()

        if assignment_id is not None:
            var_types["assignment_id"] = ID
            if hasattr(assignment_id, "to_json"):
                variables["assignment_id"] = assignment_id.to_json()
            else:
                variables["assignment_id"] = assignment_id

        if assignment is not None:
            var_types["assignment"] = AssignmentUpdateInput
            if hasattr(assignment, "to_json"):
                variables["assignment"] = assignment.to_json()
            else:
                variables["assignment"] = assignment

        query = self.prepare(Assignment, "updateAssignment", variables, var_types)
        results = self.query(query, variables)
        return Assignment.from_json(results.get("updateAssignment"))

    def createLayout(self, layout: 'LayoutInput'=None) -> Layout:
        args = ["layout: 'LayoutInput'=None"]
        variables = dict()
        var_types = dict()

        if layout is not None:
            var_types["layout"] = LayoutInput
            if hasattr(layout, "to_json"):
                variables["layout"] = layout.to_json()
            else:
                variables["layout"] = layout

        query = self.prepare(Layout, "createLayout", variables, var_types)
        results = self.query(query, variables)
        return Layout.from_json(results.get("createLayout"))

    def updateLayout(self, layout_id: 'ID'=None, layout: 'AssignmentUpdateInput'=None) -> Layout:
        args = ["layout_id: 'ID'=None", "layout: 'AssignmentUpdateInput'=None"]
        variables = dict()
        var_types = dict()

        if layout_id is not None:
            var_types["layout_id"] = ID
            if hasattr(layout_id, "to_json"):
                variables["layout_id"] = layout_id.to_json()
            else:
                variables["layout_id"] = layout_id

        if layout is not None:
            var_types["layout"] = AssignmentUpdateInput
            if hasattr(layout, "to_json"):
                variables["layout"] = layout.to_json()
            else:
                variables["layout"] = layout

        query = self.prepare(Layout, "updateLayout", variables, var_types)
        results = self.query(query, variables)
        return Layout.from_json(results.get("updateLayout"))

    def createDatapoint(self, datapoint: 'DatapointInput'=None) -> Datapoint:
        args = ["datapoint: 'DatapointInput'=None"]
        variables = dict()
        var_types = dict()

        if datapoint is not None:
            var_types["datapoint"] = DatapointInput
            if hasattr(datapoint, "to_json"):
                variables["datapoint"] = datapoint.to_json()
            else:
                variables["datapoint"] = datapoint

        query = self.prepare(Datapoint, "createDatapoint", variables, var_types)
        results = self.query(query, variables)
        return Datapoint.from_json(results.get("createDatapoint"))

    def deleteDatapoint(self, data_id: 'ID'=None) -> DeleteStatusResponse:
        args = ["data_id: 'ID'=None"]
        variables = dict()
        var_types = dict()

        if data_id is not None:
            var_types["data_id"] = ID
            if hasattr(data_id, "to_json"):
                variables["data_id"] = data_id.to_json()
            else:
                variables["data_id"] = data_id

        query = self.prepare(DeleteStatusResponse, "deleteDatapoint", variables, var_types)
        results = self.query(query, variables)
        return DeleteStatusResponse.from_json(results.get("deleteDatapoint"))
