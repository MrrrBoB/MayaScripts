import maya.cmds as cmds


def changeColor(colorIndex):
    theControls = cmds.ls(sl=1)
    for ctrl in theControls:
        ctrlShapeNode = cmds.listRelatives(ctrl, shapes=1, fullPath=1)
        for node in ctrlShapeNode:
            cmds.setAttr(node + ".overrideEnabled", 1)
            cmds.setAttr(node + ".overrideColor", colorIndex - 1)


def changeColorButtonCommand():
    chosenIndex = cmds.colorIndexSliderGrp(customColorSlider, q=1, value=1)
    changeColor(chosenIndex)


def createColorWindow():
    if cmds.window("cWindow", exists=True):
        cmds.deleteUI("cWindow")
    cmds.showWindow(cWindow)


cWindow = cmds.window(title="Change Override Color", widthHeight=(350, 60))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
customColorSlider = cmds.colorIndexSliderGrp(label="New Color", min=0, max=31, value=18)
applyButton = cmds.button(label='Change Color', command='changeColorButtonCommand()')

createColorWindow()

