import sys
import cv2
import numpy as np
from PIL import Image
from pyspark import SparkContext
import io
import uuid
from azure.storage.blob import BlockBlobService, ContentSettings

class AccountKeyOrSas:
  """
  Access Type when contacting azure blob. Currently, we only support AccountKey and SAS.
  """
  SAS = "sas"
  ACCOUNTKEY = "accountkey"

def sparkHadoopConf(sc:SparkContext, accountName:str, containerName:str, keyOrSas:str, accessType:str):
  """
  Use accountKey or sas tokens to access azure blob storage directly.
  
  :param sc: SparkContext
  :type sc: SparkContext
  :param accountName: account name of azure blob storage
  :type accountName: str
  :param containerName: container name of azure blob storage. (Only needed when for SAS access type)
  :type containerName: str
  :param accountKeyOrSas: account key or sas tokens
  :type accountKeyOrSas: str
  """
  sc._jsc.hadoopConfiguration().set("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
  if AccountKeyOrSas.ACCOUNTKEY == accessType.lower():
    sc._jsc.hadoopConfiguration().set("fs.azure.account.key." + accountName + ".blob.core.windows.net", keyOrSas)
  elif AccountKeyOrSas.SAS == accessType.lower():
    sc._jsc.hadoopConfiguration().set("fs.azure.sas." + containerName + "." + accountName + ".blob.core.windows.net", keyOrSas)
  else:
    #Not in the right access type:
    raise Exception("configuration not in the right access type")
    
def CutLists(listToCut:list, pieces:int):
  """
  Cut a list into given pieces.
  
  :param listToCut: a list passed in
  :type listToCut: list
  :param pieces: the number of lists after cutting
  :type pieces: int
  :return: an iterator, each element is a sublist 
  :rtype: iterator
  """
  listLen = len(listToCut)
  batchSize = listLen//pieces if listLen%pieces==0 else listLen//pieces+1
  for i in range(0, len(listToCut), batchSize):
    yield listToCut[i:i+batchSize]

def GetImageInPartitions(elements):
  """
  Get a list of tuples, each tuple contains the image's full path in azure blob and image object.
  
  :param elements: each element of the collection contains relative path of image in azure blob, account name, account key and container name.
  :type elements: iterator
  :return: a list of tuples, each tuple contains image object and a list of boxes information
  :rtype: list
  """
  imgObjList = []
  num = 0
  accountName = ""
  accountKey = ""
  containerName = ""
  blobService = None
  for element in elements:
    if num==0: 
      #initialize blob service only at the first element
      accountName = element[1]
      accountKey = element[2]
      containerName = element[3]
      blobService = BlockBlobService(accountName, accountKey)
    if blobService is not None:
      filePathRelativeName = element[0]
      filePathFullName = "wasbs://" + containerName + "@" + accountName + ".blob.core.windows.net/" + element[0]
      blobContent = blobService.get_blob_to_bytes(containerName, filePathRelativeName).content
      imgObj = Image.open(io.BytesIO(blobContent))
      imgObjList.append((filePathFullName,imgObj))
    num += 1
  return imgObjList

def GetImageRdds(sc:SparkContext, accountName:str, accountKey:str, containerName:str, typeImage:str, partitionNumPerRdd:int, rddNum:int):
  """
  Read all the images in the "containerName/typeImage" folder of this account.
  Return a list of rdds, each element of rdd contains the image's full path in azure blob and image object
  
  :param sc: SparkContext
  :type sc: SparkContext
  :param accountName: account name of blob storage
  :type accountName: str
  :param accountKey: account key of blob storage
  :type accountKey: str
  :param containerName: container name of blob storage
  :type containerName: str
  :param typeImage: image type(train, test or validation)
  :type typeImage: str
  :param partitionNumPerRdd: partition number of each rdd
  :type partitionNumPerRdd: int
  :param rddNum: the number of rdds to store images
  :type rddNum: int
  :return: a list of RDDs
  :rtype: list
  """
  blobService = BlockBlobService(accountName, accountKey)
  blobNames = blobService.list_blob_names(containerName, prefix=typeImage+"/")
  blobNameList = list(blobNames)
  multipleLists = list(CutLists(blobNameList, rddNum))
  imageRddList = []
  for singleList in multipleLists:
    imageRdd = sc.parallelize(singleList, partitionNumPerRdd).map(lambda blobName: (blobName, accountName, accountKey, containerName)).mapPartitions(GetImageInPartitions, preservesPartitioning=True)
    imageRddList.append(imageRdd)
  return imageRddList

def GetImageAndBoxesInPartitions(elements):
  """
  Get an iterator of tuples. if there is no exception, 
  each tuple contains the image object and information of boxes.
  otherwise it contains None and information of boxes.
  
  :param elements: each element of the collection contains relative path of image in azure blob, account name, account key and container name.
  :type elements: iterator
  :return: an iterator contains information of image and boxes.
  :rtype: iterator
  """
  num = 0
  accountName = ""
  accountKey = ""
  containerName = ""
  blobService = None
  for element in elements:
    if num==0: 
      #initialize blob service only at the first element
      accountName = element[1]
      accountKey = element[2]
      containerName = element[3]
      blobService = BlockBlobService(accountName, accountKey)
    if blobService is not None:
      filePathRelativeName = element[0]
      filePathFullName = "wasbs://" + containerName + "@" + accountName + ".blob.core.windows.net/" + element[0]
      num += 1
      try:
        blobContent = blobService.get_blob_to_bytes(containerName, filePathRelativeName).content
        imgObj = Image.open(io.BytesIO(blobContent))
        yield (imgObj, element[4])
      except:
        yield (None, element[4])

def GetBoxesLightness(img:Image, dataList:list):
  """
  Get luminance of boxes within a image.
  
  :param img: image passed in
  :type img: Image object
  :param dataList: a list of tuple, each tuple contains boxId, xmin, xmax, ymin, ymax.
  :type dataList: list
  :return: a list of tuple, each tuple contains boxId, the average lightness and the standard deviation of lightness.
  :rtype: list
  """
  boxLightness = []
  imgArr = np.array(img)
  for data in dataList:
    try:
      boxId = data[0]
      xmin = int(data[1])
      xmax = int(data[2])
      ymin = int(data[3])
      ymax = int(data[4])
      lightnessMean = 0
      lightnessStd = 0
      if img.mode == 'RGB':
        hls = cv2.cvtColor(imgArr, cv2.COLOR_RGB2HLS)
        boxArea = hls[:,:,1][ymin:ymax, xmin:xmax]
        lightnessMean = np.mean(boxArea)
        lightnessStd = np.std(boxArea)
      elif img.mode == 'L':
        boxArea = imgArr[ymin:ymax, xmin:xmax]
        lightnessMean = np.mean(boxArea)
        lightnessStd = np.std(boxArea)
      lightnessMean = int(round(lightnessMean))
      lightnessStd = int(round(lightnessStd))
      boxLightness.append([boxId, str(lightnessMean),str(lightnessStd)])
    except:
      boxLightness.append([boxId, None, None])
  return boxLightness

def GetImageInfo(img:Image):
  """
  Get image infomation from image Object.
  
  :param img: image passed in
  :type img: Image object
  :return: image information with mode, width, height, lightness
  :rtype: str
  """
  if img.mode == 'RGB':
    hls = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HLS)
    lightnessMean = np.mean(hls[:,:,1])
    lightnessStd = np.std(hls[:,:,1])
  elif img.mode == 'L':
    lightnessMean = np.mean(np.array(img))
    lightnessStd = np.std(np.array(img))
  return img.mode + "," + str(img.width)+ "," + str(img.height)+ "," + str(lightnessMean)+ "," + str(lightnessStd)

def SaveImageInfo(imageRdds:list, saveDirectory:str):
  """
  Save image infomation of Rdd list according to a given path
  
  :param imgRdds: list of rdd contained image object
  :type imgRdds: list
  :param saveDirectory: a directory address to save image information
  :type saveDirectory: str
  """
  num = 0
  for imageRdd in imageRdds:
    imageRdd.map(lambda x : (x[0], GetImageInfo(x[1]))).saveAsTextFile(saveDirectory + str(num) + "/")
    num += 1
    
