import maya.cmds as cmds


def createControl(control_name, radius_size):
    theJoint = cmds.ls(sl=True)
    myControl = cmds.circle(radius=radius_size, name=control_name + "_Ctrl")
    controlGroup = cmds.group(myControl, name=control_name + "_Ctrl_Grp")
    cmds.matchTransform(controlGroup, theJoint)
    cmds.xform(myControl, ro=(0, 90, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    cmds.parentConstraint(myControl, theJoint)
    cmds.scaleConstraint(myControl, theJoint)


def buttonCommand():
    chosenName = cmds.textField(chosenNameField, q=True, text=True)
    chosenRadius = cmds.floatSliderGrp(chosenRadiusField, q=True, value=True)
    createControl(chosenName, chosenRadius)


def createControlWindow():
    cmds.showWindow(ccWindow)


ccWindow = cmds.window(title="Add Control", widthHeight=(300, 100))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5,)
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, "right"))
cmds.text(label="Control name:")
chosenNameField = cmds.textField(placeholderText='ex:"Shoulder"')
cmds.setParent('..')
chosenRadiusField = cmds.floatSliderGrp(label="Radius Size", min=.1, max=10, field=True)

cmds.button(label="Create Control", command='buttonCommand()')
