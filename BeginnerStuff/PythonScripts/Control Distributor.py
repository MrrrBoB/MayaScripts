import maya.cmds as cmds


# Select the control first!
def DistributeControls():
    theList = cmds.ls(sl=1)
    print(theList)
    theControlGrp = cmds.listRelatives(theList[0], parent=1)
    if not theControlGrp:
        cmds.error('The control does not have a parent group')
    jointList = []
    for item in theList:
        if cmds.objectType(item) == 'joint':
            jointList.append(item)
    for joint in jointList:
        currentControl = cmds.duplicate(theControlGrp, n=joint + '_Ctrl_Grp', rc=1)[0]
        cmds.rename(cmds.listRelatives(currentControl, c=1)[0], joint + '_Ctrl')
        cmds.matchTransform(currentControl, joint)


DistributeControls()
