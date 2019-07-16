import os

from plateNet.tools import message

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
import plateNet.color


def imageFolder2List(basePath, ignoreFolders=None, ignoreWords=None):
    # return the set of files that are valid
    return list(__list_files__(basePath, ignoreFolders=ignoreFolders, ignoreWords=ignoreWords))


def __list_files__(basePath, ignoreFolders, ignoreWords):
    # loop over the directory structure
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        # loop over the filenames in the current directory

        for filename in filenames:
            # print(rootDir.split("/")[-1])
            if ignoreFolders is not None and rootDir.split("/")[-1] in ignoreFolders:
                continue
            # if the contains string is not none and the filename does not contain
            # the supplied string, then ignore the file
            # if ignoreWords is not None and filename.find(ignoreWords) != -1:
            # if ignoreWords is not None and bool(re.search(r'{}'.format(ignoreWords), filename)):
            #     continue
            # [os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]

            # determine the file extension of the current file
            ext = filename[filename.rfind("."):].lower()

            # check to see if the file is an image and should be processed
            if image_types is None or ext.endswith(image_types):
                # construct the path to the image and yield it
                imagePath = os.path.join(rootDir, filename)
                yield imagePath


def generateFolder(path, foldername):
    mainPath = os.path.join(path, foldername)

    if not os.path.exists(mainPath):
        os.mkdir(mainPath)
        message("{} folder generated.".format(mainPath), color.CGREEN)

    return mainPath


def generateOutputFolder(path, foldername):
    head, root = os.path.split(path)

    filename = root.split('.')[0]
    mainPath = "{}/{}".format(head, foldername)

    if not os.path.exists(mainPath):
        os.mkdir(mainPath)

    # print("main path : " + mainPath)
    return mainPath, filename
