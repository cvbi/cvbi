#
# Methods to work with different objects as defined within Imaris
#


def GetSurpassObjects(vImaris, search="surfaces"):

    """
    Pass a imaris application generated for a specific applicationID and search for a object type

    Input  : vImaris = Imaris Applcation
             search = Object type from [frame, spots, surfaces, filaments]

    Output : A dictionary of all object connections of the specified type

    e.g. :

    vImarisLib = ImarisLib.ImarisLib()
    vImaris = vImarisLib.GetApplication(aImarisId)
    surfaces = GetSurpassObjects(vImaris=vImaris, search='surfaces')

    surfaces.keys()
    ['Th1']

    surfaces['Th1']
    cde839ab-bc29-47a5-8970-033983753001 -t -e 1.0:tcp -h 172.19.244.153 -p 50334 -t 60000

    """

    ret = {}

    vFactory = vImaris.GetFactory()
    vScene = vImaris.GetSurpassScene()

    if vScene is None:
        return(ret)

    nChildren = vScene.GetNumberOfChildren()

    for i in range(nChildren):
        vChild = vScene.GetChild(i)

        if search.lower() == "frame":
            if vFactory.IsFrame(vChild):
                vFrame = vFactory.ToFrame(vChild)
                vName = vChild.GetName()
                ret[vName] = vFrame

        elif search.lower() == "spots":
            if vFactory.IsSpots(vChild):
                vSpots = vFactory.ToSpots(vChild)
                vName = vChild.GetName()
                ret[vName] = vSpots

        elif search.lower() == "surfaces":
            if vFactory.IsSurfaces(vChild):
                vSurfaces = vFactory.ToSurfaces(vChild)
                vName = vChild.GetName()
                ret[vName] = vSurfaces

        elif search.lower() == "filaments":
            if vFactory.IsFilaments(vChild):
                vSurfaces = vFactory.ToFilaments(vChild)
                vName = vChild.GetName()
                ret[vName] = vSurfaces

        elif search.lower() == "cells":
            if vFactory.IsCells(vChild):
                vSurfaces = vFactory.ToCells(vChild)
                vName = vChild.GetName()
                ret[vName] = vSurfaces

    return(ret)