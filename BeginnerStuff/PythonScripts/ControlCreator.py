import maya.cmds as cmds


def createControl(controlName, radiusSize, ctrlColor, axis):
    theJoint = cmds.ls(sl=True)[0]
    myControl = cmds.circle(radius=radiusSize, name=controlName + "_Ctrl")[0]
    controlShapeNode = cmds.listRelatives(myControl, shapes=True)[0]
    cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
    cmds.setAttr(str(controlShapeNode) + ".overrideColor", ctrlColor)
    controlGroup = cmds.group(myControl, name=controlName + "_Ctrl_Grp")
    cmds.matchTransform(controlGroup, theJoint)
    if axis == 1:
        cmds.xform(myControl, ro=(0, 90, 0))
    elif axis == 2:
        cmds.xform(myControl, ro=(90, 0, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    cmds.parentConstraint(myControl, theJoint)
    cmds.scaleConstraint(myControl, theJoint)


def buttonCommand():
    if len(cmds.textField(chosenNameField, q=True, text=True)) == 0:
        cmds.warning("Please give the control a name")
        return
    else:
        chosenName = cmds.textField(chosenNameField, q=True, text=True)
    chosenRadius = cmds.floatSliderGrp(chosenRadiusField, q=True, value=True)
    selectedColor = 6
    selectedButton = cmds.radioButtonGrp(colorButtonGrp, q=True, select=True)
    if selectedButton == 1:
        selectedColor = 6
    elif selectedButton == 2:
        selectedColor = 4
    elif selectedButton == 3:
        selectedColor = cmds.colorIndexSliderGrp(customColorSlider, q=True, value=True) - 1
    selectedAxis = cmds.radioButtonGrp(axisSelection, q=True, select=True)
    createControl(chosenName, chosenRadius, selectedColor, selectedAxis)


def createControlWindow():
    if cmds.window("ccWindow", exists=True):
        cmds.deleteUI("ccWindow")
    cmds.showWindow(ccWindow)


ccWindow = cmds.window(title="Add Control", widthHeight=(450, 160))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, "right"))
cmds.text(label="Control name:")
chosenNameField = cmds.textField(placeholderText='ex:"Shoulder"')
cmds.setParent('..')
chosenRadiusField = cmds.floatSliderGrp(label="Radius Size:",
                                        min=.1,
                                        max=10,
                                        value=3,
                                        field=True)
axisSelection = cmds.radioButtonGrp(label='ControlAxis',
                                    labelArray3=['x', 'y', 'z'],
                                    numberOfRadioButtons=3, select=1)
colorButtonGrp = cmds.radioButtonGrp(label="Control Color:",
                                     labelArray3=["Blue(FK)", "Red(IK)", "Other"],
                                     numberOfRadioButtons=3, select=1)
customColorSlider = cmds.colorIndexSliderGrp(label="Other Color",
                                             min=0,
                                             max=31,
                                             value=18)
cmds.button(label="Create Control", command='buttonCommand()')

createControlWindow()
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
