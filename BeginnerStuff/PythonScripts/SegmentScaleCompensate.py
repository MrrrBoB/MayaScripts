import maya.cmds as cmds


jointList = cmds.ls(type='joint')
for joint in jointList:
    cmds.setAttr('%s.segmentScaleCompensate' % joint, 0)