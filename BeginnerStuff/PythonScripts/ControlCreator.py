import maya.cmds as cmds


def createControl(controlName, radiusSize, ctrlColor):
    theJoint = cmds.ls(sl=True)
    myControl = cmds.circle(radius=radiusSize, name=controlName + "_Ctrl")
    controlShape = myControl[0]
    cmds.setAttr(str(controlShape) + ".overrideEnabled", 1)
    cmds.setAttr(str(controlShape) + ".overrideColor", ctrlColor)
    controlGroup = cmds.group(myControl, name=controlName + "_Ctrl_Grp")
    cmds.matchTransform(controlGroup, theJoint)
    cmds.xform(myControl, ro=(0, 90, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    cmds.parentConstraint(myControl, theJoint)
    cmds.scaleConstraint(myControl, theJoint)


def buttonCommand():
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
    createControl(chosenName, chosenRadius, selectedColor)


def createControlWindow():
    cmds.showWindow(ccWindow)


ccWindow = cmds.window(title="Add Control", widthHeight=(450, 130))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, "right"))
cmds.text(label="Control name:")
chosenNameField = cmds.textField(placeholderText='ex:"Shoulder"')
cmds.setParent('..')
chosenRadiusField = cmds.floatSliderGrp(label="Radius Size:", min=.1, max=10, value=3, field=True)
colorButtonGrp = cmds.radioButtonGrp(label="Control Color:", labelArray3=["Blue(FK)", "Red(IK)", "Other"],
                                     numberOfRadioButtons=3, select=1)
customColorSlider = cmds.colorIndexSliderGrp(label="Other Color", min=0, max=31, value=18)
cmds.button(label="Create Control", command='buttonCommand()')

createControlWindow()