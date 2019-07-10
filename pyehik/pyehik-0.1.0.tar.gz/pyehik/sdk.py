from datetime import datetime

import ctypes

HC = None

try:
    from ctypes.wintypes import DWORD
except ValueError:
    DWORD = ctypes.c_uint32
    
LPDWORD = ctypes.POINTER(DWORD)
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

def REF(val):
    """usar cuando se necesite pasar valor a puntero
    este corresponde a & en C"""
    return ctypes.byref(val)

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

class NET_DVR_USER_LOGIN_INFO(ctypes.Structure):
    _fields_ = [
        ("sDeviceAddress", CHAR * NET_DVR_DEV_ADDRESS_MAX_LEN),
        ("byUseTransport", BYTE),
        ("wPort", WORD),
        ("sUserName", CHAR * NET_DVR_LOGIN_USERNAME_MAX_LEN),
        ("sPassword", CHAR * NET_DVR_LOGIN_PASSWD_MAX_LEN),
    ]
LPNET_DVR_USER_LOGIN_INFO = ctypes.POINTER(NET_DVR_USER_LOGIN_INFO)

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
    return _cfunc(ctypes.byref(pErrorNo))


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
