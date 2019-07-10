#!/usr/bin/env python3


class CsvData:
    samples = 'samples'
    timestamp = 'timestamp'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'


class DataTypeId:
    metropme = 'metropme'
    roads = 'roads'
    tomtomfcd = 'tomtomfcd'
    zones = 'zones'

    datapoints = 'datapoints'
    mappingroadsdatapoints = 'mappingroadsdatapoints'


class AttId:
    att = 'att'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roads = 'roads'
    tono = 'tono'
    webatt = 'webatt'

    datapointeid = 'datapointeid'
    roadeid = 'roadeid'
    validfrom = 'validfrom'
    validto = 'validto'
    zoneeid = 'zoneeid'


class NetworkObjId:
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    newdpmappings = 'newdpmappings'
    newzonemappings = 'newzonemappings'
    omiteddatapoints = 'omiteddatapoints'
    roadsdatamap = 'roadsdatamap'
    roadsffspeedmap = 'roadsffspeedmap'
    roadszonesmap = 'roadszonesmap'
    zonesdatamap = 'zonesdatamap'
