#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|

import subprocess
import datetime
import sys



def screenShot(type, saveDir):
    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d_%H-%M-%S")
    saveName = saveDir + currentTime + ".png"
    if type == "selection":
        subprocess.call(["escrotum", "-s", saveName])
        return(saveName)
    else:
        type = "full"
        subprocess.call(["escrotum", saveName])
        return(saveName)

#arg = sys.argv[1:]
#screenShot(conversions.convertListString(arg))

