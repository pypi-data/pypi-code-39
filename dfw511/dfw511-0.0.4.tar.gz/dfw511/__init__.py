def auth(username, password):
    import requests
    import xml.etree.ElementTree as ET
    endpoint = "http://webservices.511dfw.org/DFW511/PublicWebServices/DFW511_WebServices.asmx/getAuthenticationToken"
    r = requests.post(url = endpoint, data = {'username': username, 'password': password})
    tree = ET.fromstring(r.text)
    for child in tree:
        if child.tag == 'Status':
            status = child.text
        if child.tag == 'Token':
            token = child.text
    return token

def getcctv(token):
    import requests
    import xml.etree.ElementTree as ET
    endpoint = "http://webservices.511dfw.org/DFW511/PublicWebServices/DFW511_WebServices.asmx/getCCTVs"
    r = requests.post(url = endpoint, data = {'Token': token})
    tree = ET.fromstring(r.text)
    result_list = []
    for camera in tree:
        camera_dict = {}
        for info in camera:
            if info.tag == 'CCTV_ID':
                camera_dict['id'] = info.text
            elif info.tag == 'CCTV_NAME':
                camera_dict['name'] = info.text
            elif info.tag == 'NATIVE_CCTV_ID':
                camera_dict['native_id'] = info.text
            elif info.tag == 'OWNER_NAME':
                camera_dict['owner_name'] = info.text
            elif info.tag == 'DESCRIPTION':
                camera_dict['description'] = info.text
            elif info.tag == 'DIRECTION':
                if info.text == '1':
                    camera_dict['direction'] = 'North'
                elif info.text == '2':
                    camera_dict['direction'] = 'South'
                elif info.text == '3':
                    camera_dict['direction'] = 'East'
                elif info.text == '4':
                    camera_dict['direction'] = 'West'
                elif info.text == '5':
                    camera_dict['direction'] = 'Both'
                elif info.text == '6':
                    camera_dict['direction'] = 'North_South'
                elif info.text == '7':
                    camera_dict['direction'] = 'East_West'
                else:
                    camera_dict['direction'] = 'Unknown'
            elif info.tag == 'LOCATION':
                camera_dict['location'] = info.text
            elif info.tag == 'STATE':
                camera_dict['state'] = info.text
            elif info.tag == 'LATITUDE':
                camera_dict['latitude'] = info.text
            elif info.tag == 'LONGITUDE':
                camera_dict['longitude'] = info.text
            elif info.tag == 'STATUS':
                if info.text == '3':
                    camera_dict['status'] = 'Device_Online'
                elif info.text == '4':
                    camera_dict['status'] = 'Device_Offline'
                else:
                    camera_dict['status'] = 'Unknown'
                camera_dict['status'] = info.text
            elif info.tag == 'URL':
                camera_dict['url'] = info.text
            elif info.tag == 'LASTUPDATED':
                camera_dict['last_update'] = info.text
        result_list.append(camera_dict)
    return(result_list)

def getdms(token):
    import requests
    import xml.etree.ElementTree as ET
    endpoint = "http://webservices.511dfw.org/DFW511/PublicWebServices/DFW511_WebServices.asmx/getDMSs"
    r = requests.post(url = endpoint, data = {'Token': token})
    tree = ET.fromstring(r.text)
    result_list = []
    for dms in tree:
        dms_dict = {}
        dms_dict['id'] = dms.attrib['id']
        dms_dict['name'] = dms.attrib['name']
        dms_dict['location'] = dms.attrib['location']
        dms_dict['owner_name'] = dms.attrib['owner_name']
        dms_dict['latitude'] = dms.attrib['lat']
        dms_dict['longitude'] = dms.attrib['lon']
        for info in dms:
            if info.tag == 'last_updtae':
                dms_dict['last_update'] = info.text
            elif info.tag == 'status':
                dms_dict['status'] = info.text
            elif info.tag == 'message':
                dms_dict['message'] = info.text
            elif info.attrib == 'id':
                dms_dict['id'] = info.text
            elif info.attrib == 'name':
                dms_dict['name'] = info.text
            elif info.attrib == 'location':
                dms_dict['location'] = info.text
            elif info.attrib == 'owner_name':
                dms_dict['owner_name'] = info.text
            elif info.attrib == 'lat':
                dms_dict['latitude'] = info.text
            elif info.attrib == 'lon':
                dms_dict['longitude'] = info.text
        result_list.append(dms_dict)
    return(result_list)

def getevent(token):
    import requests
    import xml.etree.ElementTree as ET
    endpoint = "http://webservices.511dfw.org/DFW511/PublicWebServices/DFW511_WebServices.asmx/getEvents"
    r = requests.post(url = endpoint, data = {'Token': token})
    tree = ET.fromstring(r.text)
    result_list = []
    for event in tree:
        event_dict = {}
        for info in event:
            if info.tag == 'EVENT_ID':
                event_dict['id'] = info.text
            elif info.tag == 'EVENT_STATE':
                event_dict['event_state'] = info.text
            elif info.tag == 'EVENT_CLASS':
                event_dict['event_class'] = info.text
            elif info.tag == 'EVENT_TYPE':
                event_dict['event_type'] = info.text
            elif info.tag == 'REPORT_ORG_ID':
                event_dict['report_org_id'] = info.text
            elif info.tag == 'FACILITY_ID':
                event_dict['facility_id'] = info.text
            elif info.tag == 'FACILITY_NAME':
                event_dict['facility_name'] = info.text
            elif info.tag == 'DIRECTION':
                event_dict['direction'] = info.text
            elif info.tag == 'ARTICLE_CODE':
                event_dict['qualifier'] = info.text
            elif info.tag == 'FROM_LOC_POINT':
                event_dict['from_location'] = info.text
            elif info.tag == 'TO_LOC_POINT':
                event_dict['to_location'] = info.text
            elif info.tag == 'CREATE_TIME':
                event_dict['time_created'] = info.text
            elif info.tag == 'LAST_UPDATE':
                event_dict['last_update'] = info.text
            elif info.tag == 'EVENT_DESCRIPTION':
                event_dict['description'] = info.text
            elif info.tag == 'CITY':
                event_dict['city'] = info.text
            elif info.tag == 'COUNTY':
                event_dict['county'] = info.text
            elif info.tag == 'STATE':
                event_dict['state'] = info.text
            elif info.tag == 'EST_DURATION':
                event_dict['duration'] = info.text
            elif info.tag == 'LAT':
                event_dict['latitude'] = info.text
            elif info.tag == 'LON':
                event_dict['longitude'] = info.text
            elif info.tag == 'TO_LAT':
                event_dict['latitude_to'] = info.text
            elif info.tag == 'TO_LON':
                event_dict['longitude_to'] = info.text
            elif info.tag == 'LANES_AFFECTED':
                event_dict['lanes_affected'] = info.text
            elif info.tag == 'LANE_STATUS':
                event_dict['lanes_status'] = info.text
            elif info.tag == 'TOTAL_LANES':
                event_dict['lanes_total'] = info.text
            elif info.tag == 'LANE_DESCRIPTION':
                event_dict['lanes_description'] = info.text
            elif info.tag == 'UPDATE_NUMBER':
                event_dict['update_number'] = info.text
            elif info.tag == 'RESPOND_ORG_NAME':
                event_dict['respond_org_name'] = info.text
            elif info.tag == 'START_DATE':
                event_dict['start_date'] = info.text
            elif info.tag == 'END_DATE':
                event_dict['end_date'] = info.text
        result_list.append(event_dict)
    return(result_list)
