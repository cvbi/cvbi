import ImarisLib


def GetObjectId():

    """

    Get objectID for current iamris application (aImarisID)
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

def GetFileName():

    """

    Get file name of the current Imaris  dataset

    :return: File path

    """

    aImarisId = GetObjectId()
    vImarisLib = ImarisLib.ImarisLib()
    vImaris = vImarisLib.GetApplication(aImarisId)
    imaris_filepath = vImaris.GetCurrentFileName()

    return(imaris_filepath)