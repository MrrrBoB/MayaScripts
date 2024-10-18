import maya.cmds as cmds


def changeColor(theControls, colorIndex):
    for ctrl in theControls:
        ctrlShapeNode = cmds.listRelatives(ctrl, shapes=1, fullPath=1)
        if ctrlShapeNode is None:
            cmds.setAttr(ctrl + ".overrideEnabled", 1)
            cmds.setAttr(ctrl + ".overrideColor", colorIndex - 1)
        else:
            for node in ctrlShapeNode:
                cmds.setAttr(node + ".overrideEnabled", 1)
                cmds.setAttr(node + ".overrideColor", colorIndex - 1)


