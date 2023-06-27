import maya.cmds as cmds
import maya.mel as mel


def CreatePose(objectList, mainControl, poseName):
    print(objectList)
    print(mainControl)
    print(poseName)
    groupList = []
    for obj in objectList:
        groupList.append(CreateOffsetGroup(obj, poseName))
    print(groupList)
    cmds.addAttr(mainControl, longName=poseName, attributeType='float', minValue=0, maxValue=10, defaultValue=0, keyable=1)
    cmds.select(cl=1)
    for item in groupList:
        cmds.select(item, add=1)
    mel.eval('SetDrivenKey;')


def CreatePoseButtonCmd():
    theList = cmds.ls(sl=1)
    mainControl = theList[len(theList) - 1]
    theList.remove(mainControl)
    theName = cmds.textField(nameField, q=1, text=1)
    if not theName:
        cmds.error('Please give the pose a name')
    CreatePose(theList, mainControl, theName)


def CreateOffsetGroup(ctrl, grpName):
    pivot_position = cmds.xform(ctrl, query=True, worldSpace=True, pivots=True)[0:3]
    pivot_rotation = cmds.xform(ctrl, q=1, ws=1, rotation=1)[0:3]
    thisGroup = cmds.group(empty=1, n=ctrl + '_' + grpName + '_OFFSET')
    cmds.xform(thisGroup, translation=pivot_position, rotation=pivot_rotation, worldSpace=True)
    parent_object = cmds.listRelatives(ctrl, parent=True)
    if parent_object:
        cmds.parent(thisGroup, parent_object)
    cmds.parent(ctrl, thisGroup)
    return thisGroup


def createPoseWindow():
    if cmds.window("cPWindow", exists=True):
        cmds.deleteUI("cPWindow")
    cmds.showWindow(cPWindow)


cPWindow = cmds.window(title='Create Pose', widthHeight=(400, 75))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2)
cmds.text(label='Pose Name')
nameField = cmds.textField(placeholderText='ex:"Point"', w=200)
cmds.setParent('..')
cmds.text(label='NOTE: Please select involved controls and THEN the attribute control')
cmds.button(label='Begin Posing', command='CreatePoseButtonCmd()')

createPoseWindow()
