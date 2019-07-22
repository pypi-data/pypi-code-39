from datetime import datetime

import ctypes

HC = None

try:
    from ctypes.wintypes import DWORD
except ValueError:
    DWORD = ctypes.c_uint32
    
LPDWORD = ctypes.POINTER(DWORD)
DWORDP = ctypes.POINTER(DWORD)
CHAR = ctypes.c_char
WORD = ctypes.c_uint16
# TODO: no retorna negativo
#LONG = ctypes.c_long
INT = ctypes.c_int
LONG = ctypes.c_int32
LONGP = ctypes.POINTER(LONG)
BOOL = ctypes.c_bool
BYTE = ctypes.c_uint8
BYTEP = ctypes.POINTER(BYTE)
CHARP = ctypes.c_char_p
VOID = None
NULL = None
VOIDP = ctypes.c_void_p
LPVOID = VOIDP
HANDLE = ctypes.c_int

#Constants
SERIALNO_LEN = 48
NET_DVR_DEV_ADDRESS_MAX_LEN = 129
NET_DVR_LOGIN_USERNAME_MAX_LEN = 64
NET_DVR_LOGIN_PASSWD_MAX_LEN = 64
MAX_ETHERNET = 2
MAX_DOMAIN_NAME = 64
NAME_LEN = 32
PASSWD_LEN = 16
WIFI_MAX_AP_COUNT = 20
IW_ESSID_MAX_SIZE = 32
MACADDR_LEN = 6
LOG_INFO_LEN = 11840
MAX_NAMELEN = 16

def REF(val):
    """usar cuando se necesite pasar valor a puntero
    este corresponde a & en C"""
    return ctypes.byref(val)

def CAST(val, type_):
    return ctypes.cast(val, type_)

def POINTER(val):
    return ctypes.pointer(val)

def SIZEOF(val):
    return ctypes.sizeof(val)

def CREATE_STRING_BUFFER(size):
    return ctypes.create_string_buffer(size)

class _errors:
    _map_ = {
        'NET_DVR_NOERROR': 0,
        'NET_DVR_NOINIT': 3,
        'NET_DVR_VERSIONNOMATCH': 6,
        'NET_DVR_NETWORK_FAIL_CONNECT': 7,
        'NET_DVR_NETWORK_SEND_ERROR': 8,
        'NET_DVR_NETWORK_RECVERROR': 9,
        'NET_DVR_PARAMETER_ERROR': 17
    }

    @classmethod
    def get_type(code: int) -> str:
        for _type, _code  in self._map_.items():
            if _code == code:
                return _type
        raise ArgumentError('unknown code')

    def __getattr__(self, attr):
        return self._map_[attr]
errors = _errors()

# Structures
class NET_DVR_TIME(ctypes.Structure):
    _fields_ = [
        ("dwYear", DWORD),
        ("dwMonth", DWORD),
        ("dwDay", DWORD),
        ("dwHour", DWORD),
        ("dwMinute", DWORD),
        ("dwSecond", DWORD)
    ]

    @staticmethod
    def from_datetime(time: datetime):
        obj = NET_DVR_TIME()
        obj.dwYear = time.year
        obj.dwMonth = time.month
        obj.dwDay = time.day
        obj.dwHour = time.hour
        obj.dwMinute = time.minute
        obj.dwSecond = time.second
        return obj

    def to_datetime(self):
        return datetime(self.dwYear, self.dwMonth, self.dwDay,
                        self.dwHour, self.dwMinute, self.dwSecond)

LPNET_DVR_TIME = ctypes.POINTER(NET_DVR_TIME)

class NET_DVR_DEVICEINFO_V30(ctypes.Structure):
    _fields_ = [
        ("sSerialNumber", BYTE * SERIALNO_LEN),
        ("byAlarmInPortNum", BYTE),
        ("byAlarmOutPortNume", BYTE),
        ("byDiskNum", BYTE),
        ("byDVRType", BYTE),
        ("byChanNum", BYTE),
        ("byStartChan", BYTE),
        ("byAudioChanNum", BYTE),
        ("byIPChanNum", BYTE),
        ("byZeroChanNum", BYTE),
        ("byMainProto", BYTE),
        ("bySubProto", BYTE),
        ("bySupport", BYTE),
        ("bySupport1", BYTE),
        ("bySupport2", BYTE),
        ("wDevType", WORD),
        ("bySupport3", BYTE),
        ("byMultiStreamProto", BYTE),
        ("byStartDChan", BYTE),
        ("byStartDTalkChan", BYTE),
        ("byHighDChanNum", BYTE),
        ("bySupport4", BYTE),
        ("byLanguageType", BYTE),
        ("byVoiceInChanNum", BYTE),
        ("byStartVoiceInChanNo", BYTE),
        ("bySupport5", BYTE),
        ("bySupport6", BYTE),
        ("byMirrorChanNum", BYTE),
        ("wStartMirrorChanNo", WORD),
        ("bySupport7", BYTE),
        ("byRes2", BYTE)
    ]
LPNET_DVR_DEVICEINFO_V30 = ctypes.POINTER(NET_DVR_DEVICEINFO_V30)

class NET_DVR_DEVICEINFO_V40(ctypes.Structure):
    _fields_ = [
        ("struDeviceV30", NET_DVR_DEVICEINFO_V30),
        ("bySupportLock", BYTE),
        ("byRetryLoginTime", BYTE),
        ("byPasswordLevel", BYTE),
        ("byProxyType", BYTE),
        ("dwSurplusLockTime", DWORD),
        ("byCharEncodeType", BYTE),
        ("bySupportDev5", BYTE),
        ("byLoginMode", BYTE),
        ("byRes2", BYTE * 253)
    ]
LPNET_DVR_DEVICEINFO_V40 = ctypes.POINTER(NET_DVR_DEVICEINFO_V40)

class NET_DVR_SDKSTATE(ctypes.Structure):
    _fields_ = [
        ("dwTotalLoginNum", DWORD),
        ("dwTotalRealPlayNum", DWORD),
        ("dwTotalPlayBackNum", DWORD),
        ("dwTotalAlarmChanNum", DWORD),
        ("dwTotalFormatNum", DWORD),
        ("dwTotalLogSearchNum", DWORD),
        ("dwTotalSerialNum", DWORD),
        ("dwTotalUpgradeNum", DWORD),
        ("dwTotalVoiceComNum", DWORD),
        ("dwRes", DWORD * 10)
    ]
LPNET_DVR_SDKSTATE = ctypes.POINTER(NET_DVR_SDKSTATE)

class NET_DVR_IPADDR(ctypes.Structure):
    _fields_ = [
        ("sIpV4", CHAR * 16),
        ("byIPv6", BYTE * 128)
    ]
LPNET_DVR_IPADDR = ctypes.POINTER(NET_DVR_IPADDR)

class NET_DVR_PPPOECFG(ctypes.Structure):
    _fields_ = [
        ("dwPPPOE", DWORD),
        ("sPPPoEUser", BYTE * NAME_LEN),
        ("sPPPoEPassword", CHAR * PASSWD_LEN),
        ("struPPPoEIP", NET_DVR_IPADDR)
    ]
LPNET_DVR_PPPOECFG = ctypes.POINTER(NET_DVR_PPPOECFG)

class NET_DVR_ETHERNET_V30(ctypes.Structure):
    _fields_ = [
        ("struDVRIP", NET_DVR_IPADDR),
        ("struDVRIPMask", NET_DVR_IPADDR),
        ("dwNetInterface", DWORD),
        ("wDVRPort", WORD),
        ("wMTU", WORD),
        ("byMACAddr", BYTE * MACADDR_LEN),
        ("byEthernetPortNo", BYTE)
    ]
LPNET_DVR_ETHERNET_V30 = ctypes.POINTER(NET_DVR_ETHERNET_V30)

class NET_DVR_WIFIETHERNET(ctypes.Structure):
    _fields_ = [
        ("sIpAddress", CHAR * 16),
        ("sIpMask", CHAR * 16),
        ("byMACAddr", BYTE * MACADDR_LEN),
        ("byCloseWifi", BYTE),
        ("byRes", BYTE),
        ("dwEnableDhcp", DWORD),
        ("dwAutoDns", DWORD),
        ("sFirstDns", CHAR * 16),
        ("sSecondDns", CHAR * 16),
        ("sGatewayIpAddr", CHAR * 16),
        ("bRes2", BYTE * 8)
    ]
LPNET_DVR_WIFIETHERNET = ctypes.POINTER(NET_DVR_WIFIETHERNET)

class NET_DVR_NETCFG_V30(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("struEtherNet", NET_DVR_ETHERNET_V30 * MAX_ETHERNET),
        ("struRes1", NET_DVR_IPADDR * 2),
        ("struAlarmHostIpAddr", NET_DVR_IPADDR),
        ("wRes2", BYTE * 4),
        ("wAlarmHostIpPort", WORD),
        ("byUseDhcp", BYTE),
        ("byIPv6Mode", BYTE),
        ("struDnsServer1IpAddr", NET_DVR_IPADDR),
        ("struDnsServer2IpAddr", NET_DVR_IPADDR),
        ("byIpResolver", BYTE * MAX_DOMAIN_NAME),
        ("wIpResolverPort", WORD),
        ("wHttpPortNo", WORD),
        ("struMultiCastIpAddr", NET_DVR_IPADDR),
        ("struGatewayIpAddr", NET_DVR_IPADDR),
        ("struPPPoE", NET_DVR_PPPOECFG),
        ("byRes", BYTE * 64)
    ]
LPNET_DVR_NETCFG_V30 = ctypes.POINTER(NET_DVR_NETCFG_V30)


class NET_DVR_USER_LOGIN_INFO(ctypes.Structure):
    _fields_ = [
        ("sDeviceAddress", CHAR * NET_DVR_DEV_ADDRESS_MAX_LEN),
        ("byUseTransport", BYTE),
        ("wPort", WORD),
        ("sUserName", CHAR * NET_DVR_LOGIN_USERNAME_MAX_LEN),
        ("sPassword", CHAR * NET_DVR_LOGIN_PASSWD_MAX_LEN),
    ]
LPNET_DVR_USER_LOGIN_INFO = ctypes.POINTER(NET_DVR_USER_LOGIN_INFO)

class NET_DVR_AP_INFO(ctypes.Structure):
    _fields_ = [
        ("sSsid", CHAR * IW_ESSID_MAX_SIZE),
        ("dwMode", DWORD),
        ("dwSecurity", DWORD),
        ("dwChannel", DWORD),
        ("dwSignalStrength", DWORD),
        ("dwSpeed", DWORD)
    ]
LPNET_DVR_AP_INFO = ctypes.POINTER(NET_DVR_AP_INFO)
    
class NET_DVR_AP_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwCount", DWORD),
        ("struApInfo", NET_DVR_AP_INFO * WIFI_MAX_AP_COUNT)  
    ]
LPNET_DVR_AP_INFO_LIST = ctypes.POINTER(NET_DVR_AP_INFO_LIST)


class NET_DVR_WIFI_CFG_EX(ctypes.Structure):

    class _KEY(ctypes.Union):
        class _WEP(ctypes.Structure):
            WIFI_WEP_MAX_KEY_COUNT = 4
            WIFI_WEP_MAX_KEY_LENGTH = 33

            _fields_ = [
                ("dwAuthentication", DWORD),
                ("dwKeyLength", DWORD),
                ("dwKeyType", DWORD),
                ("dwActive", DWORD),
                ("sKeyInfo", (CHAR * WIFI_WEP_MAX_KEY_COUNT) * WIFI_WEP_MAX_KEY_LENGTH)
            ]
    
        class _WPA_PSK(ctypes.Structure):
            WIFI_WPA_PSK_MAX_KEY_LENGTH = 63
            _fields_ = [
                ("dwKeyLength", DWORD),
                ("sKeyInfo", CHAR * WIFI_WPA_PSK_MAX_KEY_LENGTH),
                ("byEncryptType", BYTE)
            ]

        class _WPA_WPA2(ctypes.Union):
            class AUTH_PARAMS(ctypes.Structure):
                class EAP_TTLS(ctypes.Structure):
                    _fields_ = [
                        ('byEapolVersion', BYTE),
                        ('byAuthType', BYTE),
                        ('byRes1', BYTE * 2),
                        ('byAnonyIdentity', BYTE * NAME_LEN),
                        ('byUserName', BYTE * NAME_LEN),
                        ('byPassword', BYTE * NAME_LEN),
                        ('byRes', BYTE * 44)
                    ]
                class EAP_PEAP(ctypes.Structure):
                    _fields_ = [
                        ('byEapolVersion', BYTE),
                        ('byAuthType', BYTE),
                        ('byPeapVersion', BYTE),
                        ('byPeapLabel', BYTE),
                        ('byAnonyIdentity', BYTE * NAME_LEN),
                        ('byUserName', BYTE * NAME_LEN),
                        ('byPassword', BYTE * NAME_LEN),
                        ('byRes', BYTE * 44)
                    ]
                    
                class EAP_TLS(ctypes.Structure):
                    _fields_ = [
                        ('byEapolVersion', BYTE),
                        ('byRes1', BYTE * 3),
                        ('byIdentity', BYTE * NAME_LEN),
                        ('byPrivateKeyPswd', BYTE * NAME_LEN),
                        ('byRes', BYTE * 76)
                    ]
                _fields_ = [
                    ("eap_ttls", EAP_TTLS),
                    ("eap_peap", EAP_PEAP),
                    ("eap_tls", EAP_TLS)
                ]

        _fields_ = [
            ("wep", _WEP),
            ("wpa_psk", _WPA_PSK),
            ("wpa_wpa2", _WPA_WPA2)
        ]

    _fields_ = [
        ("struEtherNet", NET_DVR_WIFIETHERNET),
        ("sEssid", CHAR * IW_ESSID_MAX_SIZE),
        ("dwMode", DWORD),
        ("dwSecurity", DWORD),
        ("key", _KEY)
    ]

LPNET_DVR_WIFI_CFG_EX = ctypes.POINTER(NET_DVR_WIFI_CFG_EX)

class NET_DVR_WIFI_CFG(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("struWifiCfg", NET_DVR_WIFI_CFG_EX)
    ]
LPNET_DVR_WIFI_CFG = ctypes.POINTER(NET_DVR_WIFI_CFG)

class NET_DVR_WIFI_WORKMODE(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwNetworkInterfaceMode", DWORD)
    ]
LPNET_DVR_WIFI_WORKMODE = ctypes.POINTER(NET_DVR_WIFI_WORKMODE)

class NET_DVR_WIFI_CONNECT_STATUS(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("byCurStatus", BYTE),
        ("byRes1", BYTE * 3),
        ("dwErrorCode", DWORD),
        ("byRes", BYTE * 244)
    ]
LPNET_DVR_WIFI_CONNECT_STATUS = ctypes.POINTER(NET_DVR_WIFI_CONNECT_STATUS)

class NET_DVR_STORAGE_DETECTION(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("byHealthState", BYTE),
        ("bySDCardState", BYTE),
        ("wAbnormalPowerLoss", WORD),
        ("wBadBlocks", WORD),
        ("byRemainingLife", BYTE),
        ("byRes", BYTE * 125)
    ]
LPNET_DVR_STORAGE_DETECTION = ctypes.POINTER(NET_DVR_STORAGE_DETECTION)

class NET_DVR_STD_CONFIG(ctypes.Structure):
    _fields_ = [
        ("lpCondBuffer", VOIDP),
        ("dwCondSize", DWORD),
        ("lpInBuffer", VOIDP),
        ("dwInSize", DWORD),
        ("lpOutBuffer", VOIDP),
        ("dwOutSize", DWORD),
        ("lpStatusBuffer", VOIDP),
        ("dwStatusSize", DWORD),
        ("lpXmlBuffer", VOIDP),
        ("dwXmlSize", DWORD),
        ("byDataType", BYTE),
        ("byRes", BYTE * 23)
    ]
LPNET_DVR_STD_CONFIG = ctypes.POINTER(NET_DVR_STD_CONFIG)


class NET_DVR_LOG_V30(ctypes.Structure):
    _fields_ = [
        ("strLogTime", NET_DVR_TIME),
        ("dwMajorType", DWORD),
        ("dwMinorType", DWORD),
        ("sPanelUser", BYTE * MAX_NAMELEN),
        ("sNetUser", BYTE * MAX_NAMELEN),
        ("struRemoteHostAddr", NET_DVR_IPADDR),
        ("dwParaType", DWORD),
        ("dwChannel", DWORD),
        ("dwDiskNumber", DWORD),
        ("dwAlarmInPort", DWORD),
        ("dwAlarmOutPort", DWORD),
        ("dwInfoLen", DWORD),
        ("sInfo", CHAR * LOG_INFO_LEN)
    ]
LPNET_DVR_LOG_V30 = ctypes.POINTER(NET_DVR_LOG_V30)

# Callbacks

fLoginResultCallBack = ctypes.CFUNCTYPE(
    LONG, #lUserID
    DWORD, #dwResult
    LPNET_DVR_DEVICEINFO_V30, #lpDeviceInfo
    VOIDP #pUser
)

fPlayDataCallBack = ctypes.CFUNCTYPE(
    VOID, #RETURN
    LONG, #lPlayHandle
    DWORD, #dwDataType
    BYTEP, #pBuffer
    DWORD, #dwBufSize
    DWORD #dwUser
)

# SDK Initialization

def NET_DVR_Init() -> bool:
    _cfunc = HC.NET_DVR_Init
    _cfunc.restype = BOOL
    return _cfunc()

def NET_DVR_Cleanup() -> bool:
    _cfunc = HC.NET_DVR_Cleanup
    _cfunc.restype = BOOL
    return  _cfunc()

# Getting Error Message

def NET_DVR_GetLastError() -> int:
    _cfunc = HC.NET_DVR_GetLastError
    _cfunc.restype = DWORD
    return _cfunc()

def NET_DVR_GetErrorMsg(pErrorNo: LONGP) -> CHARP:
    _cfunc = HC.NET_DVR_GetErrorMsg
    _cfunc.argtypes = [LONGP]
    _cfunc.restype = CHARP
    return _cfunc(pErrorNo)


# SDKL Local Function / SDK Version, Status and Capability

def NET_DVR_GetSDKVersion() -> DWORD:
    _cfunc = HC.NET_DVR_GetSDKVersion
    _cfunc.restype = DWORD
    return _cfunc()

def NET_DVR_GetSDKBuildVersion() -> DWORD:
    _cfunc = HC.NET_DVR_GetSDKBuildVersion
    _cfunc.restype = DWORD
    return _cfunc()

def NET_DVR_GetSDKState(pSDKState: LPNET_DVR_SDKSTATE) -> BOOL:
    _cfunc = HC.NET_DVR_GetSDKState
    _cfunc.argtypes = [LPNET_DVR_SDKSTATE]
    _cfunc.restype = BOOL
    return _cfunc(pSDKState)

# User Registration

def NET_DVR_Login_V40(pLoginInfo: LPNET_DVR_USER_LOGIN_INFO,
                      lpDeviceInfo: LPNET_DVR_DEVICEINFO_V40):
    _cfunc = HC.NET_DVR_Login_V40
    _cfunc.argtypes = [LPNET_DVR_USER_LOGIN_INFO,
                       LPNET_DVR_DEVICEINFO_V40]
    _cfunc.restype = LONG
    return _cfunc(pLoginInfo, lpDeviceInfo)

def NET_DVR_Login_V30(sDVRIP: CHARP,
                      wDVRPort: INT,
                      sUsername: CHARP,
                      sPassword: CHARP,
                      lpDeviceInfo: LPNET_DVR_DEVICEINFO_V30) -> LONG:
    _cfunc = HC.NET_DVR_Login_V30
    _cfunc.argtypes = [CHARP, WORD, CHARP, CHARP,
                       LPNET_DVR_DEVICEINFO_V30]
    _cfunc.restype = LONG
    return _cfunc(str.encode(sDVRIP),
                  wDVRPort,
                  str.encode(sUsername),
                  str.encode(sPassword),
                  lpDeviceInfo)

def NET_DVR_Logout(lUserID: LONG) -> BOOL:
    _cfunc = HC.NET_DVR_Logout
    _cfunc.argtypes = [LONG]
    _cfunc.restype = BOOL
    return _cfunc(lUserID)

# System Parameter Configuration
NET_DVR_GET_DEVICECFG = 100
NET_DVR_GET_NETCFG = 102
NET_DVR_GET_TIMECFG = 118
NET_DVR_GET_AP_INFO_LIST = 305
NET_DVR_GET_WIFI_CFG = 307
NET_DVR_GET_WIFI_WORKMODE = 308 #309
NET_DVR_GET_WIFI_STATUS = 310

def NET_DVR_GetDVRConfig(lUserID: LONG,
                         dwCommand: DWORD,
                         lChannel: LONG,
                         lpOutBuffer: LPVOID,
                         dwOutBufferSize: DWORD,
                         lpBytesReturned: LPDWORD) -> BOOL:
    _cfunc = HC.NET_DVR_GetDVRConfig
    _cfunc.argtypes = [LONG, DWORD, LONG, LPVOID, DWORD, LPDWORD]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, dwCommand, lChannel,
                  lpOutBuffer, dwOutBufferSize, lpBytesReturned)

NET_DVR_SET_WIFI_CFG = 307 #306
NET_DVR_SET_NETCFG = 103
def NET_DVR_SetDVRConfig(lUserID: LONG,
                         dwCommand: DWORD,
                         lChannel: LONG,
                         lpInBuffer: LPVOID,
                         dwInBufferSize: DWORD) -> BOOL:
    _cfunc = HC.NET_DVR_SetDVRConfig
    _cfunc.argtypes = [LONG, DWORD, LONG, LPVOID, DWORD]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, dwCommand, lChannel,
                  lpInBuffer, dwInBufferSize)

# Enable Logs

def NET_DVR_SetLogToFile(nLogLevel: DWORD,
                         strLogDir: CHARP,
                         bAutoDel: BOOL) -> BOOL:
    _cfunc = HC.NET_DVR_SetLogToFile
    _cfunc.argtypes = [DWORD, CHARP, BOOL]
    _cfunc.restype = BOOL
    return _cfunc(nLogLevel, str.encode(strLogDir), bAutoDel)


# Downloading Video Files
def NET_DVR_GetFileByName(lUserID: LONG,
                          sDVRFileName: CHARP,
                          sSavedFileName: CHARP) -> LONG:
    _cfunc = HC.NET_DVR_GetFileByName
    _cfunc.argtypes = [LONG, CHARP, CHARP]
    _cfunc.restype = LONG
    return _cfunc(lUserID, str.encode(sDVRFileName), str.encode(sSavedFileName))

def NET_DVR_GetFileByTime(lUserID: LONG,
                          lChannel: LONG,
                          lpStartTime: LPNET_DVR_TIME,
                          lpStopTime: LPNET_DVR_TIME,
                          sSavedFileName: CHARP) -> LONG:
    _cfunc = HC.NET_DVR_GetFileByTime
    _cfunc.argtypes = [LONG, LONG, LPNET_DVR_TIME, LPNET_DVR_TIME, CHARP]
    _cfunc.restype = LONG
    return _cfunc(lUserID,
                  lChannel,
                  lpStartTime,
                  lpStopTime,
                  str.encode(sSavedFileName))

def NET_DVR_StopGetFile(lFileHandle: LONG) -> BOOL:
    _cfunc = HC.NET_DVR_StopGetFile
    _cfunc.argtypes = [LONG]
    _cfunc.restype = BOOL
    return _cfunc(lFileHandle)
    
def NET_DVR_GetDownloadPos(lFileHandle: LONG) -> INT:
    _cfunc = HC.NET_DVR_GetDownloadPos
    _cfunc.argtypes = [LONG]
    _cfunc.restype = INT
    return _cfunc(lFileHandle)

NET_DVR_PLAYSTART = 1
NET_DVR_PLAYSTOP = 2
NET_DVR_PLAYPAUSE = 3
NET_DVR_PLAYRESTART = 4
NET_DVR_PLAYFAST = 5
NET_DVR_PLAYSLOW = 6
NET_DVR_PLAYNORMAL = 7
NET_DVR_PLAYFRAME = 8
# TODO: faltan

def NET_DVR_PlayBackControl(lPlayHandle: LONG,
                            dwControlCode: DWORD,
                            dwInValue: DWORD,
                            lpOutValue: LPDWORD) -> BOOL:
    _cfunc = HC.NET_DVR_PlayBackControl
    _cfunc.argtypes = [LONG, DWORD, DWORD, LPDWORD]
    _cfunc.restype = BOOL
    return _cfunc(lPlayHandle, dwControlCode, dwInValue, lpOutValue)

def NET_DVR_SetPlayDataCallBack(lPlayHandle: LONG,
                                cbPlayDataCallBack: fPlayDataCallBack,
                                dwUser: DWORD) -> BOOL:
    _cfunc = HC.NET_DVR_SetPlayDataCallBack
    _cfunc.argtypes = [LONG, fPlayDataCallBack, DWORD]
    _cfunc.restype = BOOL
    return _cfunc(lPlayHandle, cbPlayDataCallBack, dwUser)

# Picture Playback and downloading

def NET_DVR_GetPicture(lUserID: LONG,
                       sDVRFileName: CHARP,
                       sSavedFileName: CHARP) -> BOOL:
    _cfunc = HC.NET_DVR_GetPicture
    _cfunc.argtypes = [LONG, CHARP, CHARP]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, sDVRFileName, sSavedFileName)

# Healt Monitor Disk

NET_DVR_GET_STORAGEDETECTION_STATE = 6640

def NET_DVR_GetSTDConfig(lUserID: LONG,
                         dwCommand: DWORD,
                         lpConfigParam: LPNET_DVR_STD_CONFIG) -> BOOL:
    _cfunc = HC.NET_DVR_GetSTDConfig
    _cfunc.argtypes = [LONG, DWORD, LPNET_DVR_STD_CONFIG]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, dwCommand, lpConfigParam)

# importing and exporting configuration file

def NET_DVR_GetConfigFile(lUserID: LONG,
                          sFileName: CHARP) -> BOOL:
    _cfunc = HC.NET_DVR_GetConfigFile
    _cfunc.argtypes = [LONG, CHARP]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, str.encode(sFileName))

def NET_DVR_SetConfigFile(lUserID: LONG,
                          sFileName: CHARP) -> BOOL:
    _cfunc = HC.NET_DVR_SetConfigFile
    _cfunc.argtypes = [LONG, CHARP]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, sFileName)

def NET_DVR_GetConfigFile_V30(lUserID: LONG,
                              sOutBuffer: CHARP,
                              dwOutSize: DWORD,
                              pReturnSize: DWORDP) -> BOOL:
    _cfunc =HC.NET_DVR_GetConfigFile_V30
    _cfunc.argtypes = [LONG, CHARP, DWORD, DWORDP]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, sOutBuffer, dwOutSize, pReturnSize)

#device capabilities

DEVICE_SOFTHARDWARE_ABILITY = 0x001
DEVICE_NETWORK_ABILITY = 0x002
DEVICE_ALARM_ABILITY = 0x00a

def NET_DVR_GetDeviceAbility(lUserID: LONG,
                             dwAbilityType: DWORD,
                             pInBuf: CHARP,
                             dwInLength: DWORD,
                             pOutBuf: CHARP,
                             dwOutLength: DWORD) -> BOOL:
    _cfunc = HC.NET_DVR_GetDeviceAbility
    _cfunc.argtypes = [LONG, DWORD, CHARP, DWORD, CHARP, DWORD]
    _cfunc.restype = BOOL
    return _cfunc(lUserID, dwAbilityType, pInBuf, dwInLength,
                  pOutBuf, dwOutLength)


# Log Search
MAJOR_ALARM = 0x1
MINOR_ALARM_IN = 0x1
MINOR_ALARM_OUT = 0x2

MAJOR_EXCEPTION = 0x2
MINOR_IP_CONFLICT = 0x26
MINOR_NET_BROKEN = 0x27

MAJOR_OPERATION = 0x3
MINOR_LOCAL_LOGIN = 0x50
MINOR_LOCAL_LOGOUT = 0x51

MAJOR_INFORMATION = 0x4
# TODO: IMPLEMENTAR

MAJOR_EVENT = 0x5


def NET_DVR_FindDVRLog_V30(lUserID: LONG,
                           lSelectMode: LONG,
                           dwMajorType: DWORD,
                           dwMinorType: DWORD,
                           lpStartTime: LPNET_DVR_TIME,
                           lpStopTime: LPNET_DVR_TIME,
                           bOnlySmart: BOOL) -> LONG:
    _cfunc = HC.NET_DVR_FindDVRLog_V30
    _cfunc.argtypes = [LONG, LONG, DWORD, DWORD,
                       LPNET_DVR_TIME, LPNET_DVR_TIME, BOOL]
    _cfunc.restype = LONG
    return _cfunc(lUserID, lSelectMode, dwMajorType, dwMinorType,
                  lpStartTime, lpStopTime, bOnlySmart)

NET_DVR_FILE_SUCCESS = 1000
NET_DVR_FILE_NOFIND = 1001
NET_DVR_ISFINDING = 1002
NET_DVR_NOMOREFILE = 1003
NET_DVR_FILE_EXCEPTION = 1004

def NET_DVR_FindNextLog_V30(lLogHandle: LONG,
                            lpLogData: LPNET_DVR_LOG_V30) -> LONG:
    _cfunc = HC.NET_DVR_FindNextLog_V30
    _cfunc.argtypes = [LONG, LPNET_DVR_LOG_V30]
    _cfunc.restype = BOOL
    return _cfunc(lLogHandle, lpLogData)

def NET_DVR_FindLogClose_V30(lLogHandle: LONG) -> BOOL:
    _cfunc = HC.NET_DVR_FindLogClose_V30
    _cfunc.argtypes = [LONG]
    _cfunc.restype = BOOL
    return _cfunc(lLogHandle)
