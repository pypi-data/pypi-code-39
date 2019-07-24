#-------------------------------------------------------------------------#
# Forte DataGlove Python Module                                           #
# dataglove.py                                                            #
# © 2019 BeBop Sensors, Inc.                                              #
#                                                                         #
# Author: Jake Preston                                                    #
#                                                                         #
# Description: Python Wrapper for the DataGlove HID API                   #
#-------------------------------------------------------------------------#

import os
import sys
import ctypes
import pkgutil
from ctypes import cdll
from ctypes import c_int
from ctypes import c_char
from ctypes import c_byte
from ctypes import c_short
from ctypes import c_float
from ctypes import c_void_p
from ctypes import POINTER

#-------------------------------------------------------------------------#
# Private                                                                 #
#-------------------------------------------------------------------------#
__INFO    = 3
__QUAT    = 4
__FINGERS = 5
__SENSORS = 10

dir = os.path.dirname(sys.modules["dataglove"].__file__)
path = os.path.join(dir, "DataGloveHID.dll")

__lib = cdll.LoadLibrary(path)

def __func(lib_function, ret, args):
	function = lib_function
	if ret != None:
		function.restype = ret
	function.argtypes = args
	return function

def __createDeviceInfoString(arr):
	s = ""
	sep = "."
	for i, num in enumerate(arr):
		if i == len(arr)-1:
			sep = ""
		s += str(abs(num)) + sep
	return s

#-------------------------------------------------------------------------#
# Data Glove Core API                                                     #
#-------------------------------------------------------------------------#
def Forte_CreateDataGloveIO(handType):
	return __func(__lib.Forte_CreateDataGloveIO, c_void_p, [c_byte])(handType)

def Forte_DestroyDataGloveIO(dataGloveIO):
	return __func(__lib.Forte_DestroyDataGloveIO, c_byte, [c_void_p])(dataGloveIO)

def Forte_GetIMU(dataGloveIO):
	arr = __func(__lib.Forte_GetIMU, POINTER(c_short), [c_void_p])(dataGloveIO)
	return [int(arr[i]) for i in range(__QUAT)]

def Forte_GetSensors(dataGloveIO):
	arr = __func(__lib.Forte_GetSensors, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(__SENSORS)]

def Forte_GetBatteryLevel(dataGloveIO):
	return __func(__lib.Forte_GetBatteryLevel, c_float, [c_void_p])(dataGloveIO)

def Forte_GetConnectionState(dataGloveIO):
	return __func(__lib.Forte_GetConnectionState, c_byte, [c_void_p])(dataGloveIO)

def Forte_GetHandType(dataGloveIO):
	return __func(__lib.Forte_GetHandType, c_byte, [c_void_p])(dataGloveIO)

def Forte_UploadFile(dataGloveIO, filePath, slot):
	if not os.path.exists(filePath):
		return 1
	filePath = filePath.encode('utf-8')
	return __func(__lib.Forte_UploadFile, c_byte, [c_void_p, ctypes.c_char_p, c_byte])(dataGloveIO, filePath, slot)

def Forte_EnterBootloaderMode(dataGloveIO):
	return __func(__lib.Forte_EnterBootloaderMode, None, [c_void_p])(dataGloveIO)

def Forte_SetGloveDisplayID(dataGloveIO):
	return __func(__lib.Forte_SetGloveDisplayID, None, [c_byte, c_byte, c_byte, c_byte])(dataGloveIO)

def Forte_GetFullReport(dataGloveIO):
	arr = __func(__lib.Forte_GetFullReport, POINTER(c_byte), [c_void_p])(dataGloveIO)
	return [int(arr[i]) for i in range(__SENSORS)]

#-------------------------------------------------------------------------#
# Raw Sensors/Fingers                                                     #
#-------------------------------------------------------------------------#
def Forte_GetSensorRaw(dataGloveIO, index):
	return __func(__lib.Forte_GetSensorRaw, c_byte, [c_void_p, c_int])(dataGloveIO, index)

def Forte_GetSensorsRaw(dataGloveIO):
	arr = __func(__lib.Forte_GetSensorsRaw, POINTER(c_byte), [c_void_p])(dataGloveIO)
	return [int(arr[i]) for i in range(__SENSORS)]

def Forte_GetFingerRaw(dataGloveIO, index):
	return __func(__lib.Forte_GetFingerRaw, c_byte, [c_void_p, c_int])(dataGloveIO, index)

def Forte_GetFingersRaw(dataGloveIO):
	arr = __func(__lib.Forte_GetFingersRaw, POINTER(c_byte), [c_void_p])(dataGloveIO)
	return [int(arr[i]) for i in range(__FINGERS)]

#-------------------------------------------------------------------------#
# Normalized Sensors/Fingers                                              #
#-------------------------------------------------------------------------#
def Forte_GetSensorNormalized(dataGloveIO, index):
	return __func(__lib.Forte_GetSensorNormalized, c_float, [c_void_p, c_int])(dataGloveIO, index)

def Forte_GetSensorsNormalized(dataGloveIO):
	arr = __func(__lib.Forte_GetSensorsNormalized, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(__SENSORS)]

def Forte_GetFingerNormalized(dataGloveIO, index):
	return __func(__lib.Forte_GetFingerNormalized, c_float, [c_void_p, c_int])(dataGloveIO, index)

def Forte_GetFingersNormalized(dataGloveIO):
	arr = __func(__lib.Forte_GetFingersNormalized, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(__SENSORS)]

#-------------------------------------------------------------------------#
# Raw/Normalized Finger Sum                                               #
#-------------------------------------------------------------------------#
def Forte_GetFingersSumRaw(dataGloveIO):
	return __func(__lib.Forte_GetFingersSumRaw, c_int, [c_void_p])(dataGloveIO)

def Forte_GetFingersSumNormalized(dataGloveIO):
	return __func(__lib.Forte_GetFingersSumNormalized, c_float, [c_void_p])(dataGloveIO)

#-------------------------------------------------------------------------#
# Haptics                                                                 #
#-------------------------------------------------------------------------#
def Forte_SendHaptic(dataGloveIO, actuatorID, note, amplitude):
	return __func(__lib.Forte_SendHaptic, None, [c_void_p, c_byte, c_byte, c_float])(dataGloveIO, actuatorID, note, amplitude)

def Forte_SendOneShotHaptic(dataGloveIO, actuatorID, note, amplitude):
	return __func(__lib.Forte_SendOneShotHaptic, None, [c_void_p, c_byte, c_byte, c_float])(dataGloveIO, actuatorID, note, amplitude)

def Forte_SendLoopHaptic(dataGloveIO, actuatorID, note, amplitude):
	return __funct(__lib.Forte_SendLoopHaptic, None, [c_void_p, c_byte, c_byte, c_float])(dataGloveIO, actuatorID, note, amplitude)

def Forte_ToggleOneShot(dataGloveIO, actuatorID, makeOneShot):
	return __func(__lib.Forte_ToggleOneShot, None, actuatorID, makeOneShot)(dataGloveIO, actuatorID, makeOneShot)

def Forte_SelectHapticWave(dataGloveIO, actuatorID, waveform):
	return __func(__lib.Forte_SelectHapticWave, None, [c_void_p, c_byte, c_byte])(dataGloveIO, actuatorID, waveform)

def Forte_SetGrainLocation(dataGloveIO, actuatorID, location):
	return __func(__lib.Forte_SetGrainLocation, None, [c_void_p, c_byte, c_float])(dataGloveIO, actuatorID, location)

def Forte_SetAmplitude(dataGloveIO, actuatorID, amplitude):
	return __func(__lib.Forte_SetAmplitude, None, [c_void_p, c_byte, c_float])(dataGloveIO, actuatorID, amplitude)

def Forte_SetPitchBend(dataGloveIO, actuatorID, pitch):
	return __func(__lib.Forte_SetPitchBend, None, [c_void_p, c_byte, c_byte])(dataGloveIO, actuatorID, pitch)

def Forte_SetGrainSize(dataGloveIO, actuatorID, size):
	return __func(__lib.Forte_SetGrainSize, None, [c_void_p, c_byte, c_float])(dataGloveIO, actuatorID, size)

def Forte_SetGrainFade(dataGloveIO, actuatorID, fade):
	return __func(__lib.Forte_SetGrainFade, None, [c_void_p, c_byte, c_float])(dataGloveIO, c_byte, c_float)

def Forte_ToggleHapticsOn(dataGloveIO, turnOn):
	return __func(__lib.Forte_ToggleHapticsOn, None, [c_void_p, c_byte])(dataGloveIO, turnOn)

def Forte_SilenceHaptics(dataGloveIO):
	return __func(__lib.Forte_SilenceHaptics, None, [c_void_p])(dataGloveIO)

#-------------------------------------------------------------------------#
# Calibration                                                             #
#-------------------------------------------------------------------------#
def Forte_CalibrateFlat(dataGloveIO):
	return __func(__lib.Forte_CalibrateFlat, None, [c_void_p])(dataGloveIO)

def Forte_CalibrateFingersIn(dataGloveIO):
	return __func(__lib.Forte_CalibrateFingersIn, None, [c_void_p])(dataGloveIO)

def Forte_CalibrateThumbIn(dataGloveIO):
	return __func(__lib.Forte_CalibrateThumbIn, None, [c_void_p])(dataGloveIO)

def Forte_LoadCalibration(dataGloveIO, slot):
	return __func(__lib.Forte_LoadCalibration, None, [c_void_p, c_byte])(dataGloveIO, slot)

def Forte_SaveCalibration(dataGloveIO, slot):
	return __func(__lib.Forte_SaveCalibration, None, [c_void_p, c_byte])(dataGloveIO, slot)

def Forte_ResetCalibration(dataGloveIO):
	return __func(__lib.Forte_ResetCalibration, None, [c_void_p])(dataGloveIO)

#-------------------------------------------------------------------------#
# Device Info                                                             #
#-------------------------------------------------------------------------#
def Forte_GetHardwareRev(dataGloveIO):
	arr = __func(__lib.Forte_GetHardwareRev, POINTER(c_byte), [c_void_p])(dataGloveIO)
	return chr(arr[0])

def Forte_GetHardwareVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetHardwareVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

def Forte_GetSAMDBootloaderVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetSAMDBootloaderVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

def Forte_GetSAMDAppletVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetSAMDAppletVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

def Forte_GetBLESoftDeviceVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetBLESoftDeviceVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

def Forte_GetBLEBootloaderVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetBLEBootloaderVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

def Forte_GetBLEAppletVersion(dataGloveIO):
	arr = __func(__lib.Forte_GetBLEAppletVersion, POINTER(c_byte), [c_void_p])(dataGloveIO)
	arr =  [int(arr[i]) for i in range(__INFO)]
	return __createDeviceInfoString(arr)

#-------------------------------------------------------------------------#
# Conversions and Rotations                                               #
#-------------------------------------------------------------------------#
def Forte_HomeIMU(dataGloveIO):
	# !! not implemented in firmware yet
	#return __func(__lib.Forte_HomeIMU, None, [c_void_p])(dataGloveIO)
	pass

def Forte_GetQuaternionRaw(dataGloveIO):
	arr = __func(__lib.Forte_GetQuaternionRaw, POINTER(c_short), [c_void_p])(dataGloveIO)
	return [int(arr[i]) for i in range(__QUAT)]

def Forte_GetQuaternionNormalized(dataGloveIO):
	arr = __func(__lib.Forte_GetQuaternionNormalized, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(__QUAT)]

def Forte_GetEulerAngles(dataGloveIO):
	arr = __func(__lib.Forte_GetEulerAngles, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(3)]

def Forte_GetAxisAngle(dataGloveIO):
	arr = __func(__lib.Forte_GetAxisAngle, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(4)]

def Forte_GetRotationMatrix(dataGloveIO):
	arr = __func(__lib.Forte_GetRotationMatrix, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(9)]

def Forte_GetSphericalCoordinates(dataGloveIO):
	arr = __func(__lib.Forte_GetSphericalCoordinates, POINTER(c_float), [c_void_p])(dataGloveIO)
	return [float(arr[i]) for i in range(3)]

#-------------------------------------------------------------------------#
# Debugging                                                               #
#-------------------------------------------------------------------------#
def Forte_GetDebugVar(dataGloveIO):
	return __func(__lib.Forte_GetDebugVar, c_byte, [c_void_p, c_byte])(dataGloveIO)
