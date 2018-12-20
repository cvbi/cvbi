import ImarisLib
import time

def get_objectID():

    """

    Get objectID for current Imaris application (aImarisID)
    :return: aImarisID value to be used within the XTension

    """

    vImarisLib = ImarisLib.ImarisLib()
    vServer = vImarisLib.GetServer()
    vNumberOfObjects = vServer.GetNumberOfObjects()

    try:
        for vIndex in range(vNumberOfObjects):
            vObjectId = vServer.GetObjectID(vIndex)
            # work with the ID (return first one)
            return(vObjectId)
    except:
        # If the process fails return an invalid id
        print('No ID Found')
        time.sleep(5)
        return(-1)

def get_all_objectIDs():

    """

    Get objectIDs for active Imaris applications (aImarisID)
    :return: Dictionary of ImarisIDs and corresponding data files

    """

    vImarisLib = ImarisLib.ImarisLib()
    vServer = vImarisLib.GetServer()
    vNumberOfObjects = vServer.GetNumberOfObjects()

    objectIDs = {}

    try:
        for vIndex in range(vNumberOfObjects):
            aImarisId = vServer.GetObjectID(vIndex)
            vImarisLib = ImarisLib.ImarisLib()
            vImaris = vImarisLib.GetApplication(aImarisId)
            imaris_file = vImaris.GetCurrentFileName()
            objectIDs[aImarisId] = imaris_file
    except:
        # If the process fails return an invalid id
        print('No ID Found')
        time.sleep(5)
        return(-1)

    return(objectIDs)

def GetFileName():

    """

    Get file name of the current Imaris  dataset

    :return: File path

    """

    aImarisId = get_objectID()
    vImarisLib = ImarisLib.ImarisLib()
    vImaris = vImarisLib.GetApplication(aImarisId)
    imaris_filepath = vImaris.GetCurrentFileName()

    return(imaris_filepath)

