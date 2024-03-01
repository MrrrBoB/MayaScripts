import maya.cmds as cmds


def createControl(chosenName, radiusSize, ctrlColor, axis, constrainJoint, theJoint):
    myControl = cmds.circle(radius=radiusSize, name=chosenName+"_Ctrl")[0]
    controlShapeNode = cmds.listRelatives(myControl, shapes=True)[0]
    cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
    cmds.setAttr(str(controlShapeNode) + ".overrideColor", ctrlColor)
    controlGroup = cmds.group(myControl, name=chosenName+"_Ctrl_Grp")
    cmds.matchTransform(controlGroup, theJoint)
    if axis == 1:
        cmds.xform(myControl, ro=(0, 90, 0))#NateMadeThis
    elif axis == 2:
        cmds.xform(myControl, ro=(90, 0, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    if constrainJoint:
        cmds.parentConstraint(myControl, theJoint)
        cmds.scaleConstraint(myControl, theJoint)


def buttonCommand():
    if len(cmds.textField(chosenNameField, q=True, text=True)) != 0:
        chosenName = cmds.textField(chosenNameField, q=True, text=True)
        noName = False
        hName = chosenName;
    else:
        noName = True
    chosenRadius = cmds.floatSliderGrp(chosenRadiusField, q=True, value=True)
    selectedColor = 6
    selectedButton = cmds.radioButtonGrp(colorButtonGrp, q=True, select=True)
    if selectedButton == 1:
        selectedColor = 6
    elif selectedButton == 2:
        selectedColor = 4#NateMadeThis
    elif selectedButton == 3:
        selectedColor = cmds.colorIndexSliderGrp(customColorSlider, q=True, value=True) - 1
    selectedAxis = cmds.radioButtonGrp(axisSelection, q=True, select=True)
    selectedConstrainOption = cmds.checkBox(constraintCheckBox, q=True, value=True)
    sels = cmds.ls(sl=1)
    if len(sels) <= 0:
        cmds.warning('Please select something to add the control to')
    elif len(sels) == 1:
        theJoint = sels[0]
        if noName:
            chosenName =theJoint
        createControl(chosenName, chosenRadius, selectedColor, selectedAxis, selectedConstrainOption, theJoint)
    else:
        i = 1
        for object in sels:
            if noName:
                chosenName = object
            else:
                chosenName = hName+str(i)
            i += 1
            createControl(chosenName, chosenRadius, selectedColor, selectedAxis, selectedConstrainOption, object)


def mirrorCommand():
    theControls = cmds.ls(sl=1)
    print(theControls)
    controlGrps = [cmds.listRelatives(control, parent=1)[0] for control in theControls]
    print(controlGrps)
    newControlGrp = cmds.duplicate(controlGrps, rr=1)
    mirrorGrp = cmds.group(newControlGrp, n='mirrorGrp', w=1)
    cmds.xform(mirrorGrp, piv=(0, 0, 0))
    cmds.xform(mirrorGrp, s=(-1, 1, 1))
    # cmds.makeIdentity(mirrorGrp, a=1, s=1, jo=1)
    for grp in newControlGrp:
        cmds.parent(grp, w=1)
    cmds.delete(mirrorGrp)
    fullControlGrp = cmds.listRelatives(newControlGrp, ad=1)


#NateMadeThis
def createControlWindow():
    if cmds.window("ccWindow", exists=True):
        cmds.deleteUI("ccWindow")
    cmds.showWindow(ccWindow)

#NateMadeThis
ccWindow = cmds.window(title="Add Control", widthHeight=(450, 205))#NateMadeThis
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, "right"))
cmds.text(label="Control name:")#NateMadeThis
chosenNameField = cmds.textField(placeholderText='ex:"Shoulder"')
cmds.setParent('..')
chosenRadiusField = cmds.floatSliderGrp(label="Radius Size:",
                                        min=.1,
                                        max=10,
                                        value=3,#NateMadeThis
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
                                             value=18)#NateMadeThis
constraintCheckBox = cmds.checkBox(label='Constrain Joint')
cmds.button(label="Create Control", command='buttonCommand()')
cmds.button(label='Mirror Selected Controls (X axis)', command='mirrorCommand()')

createControlWindow()

#constraintList = cmds.ls(type = 'parentConstraint')
#cmds.select(constraintList, r=True)