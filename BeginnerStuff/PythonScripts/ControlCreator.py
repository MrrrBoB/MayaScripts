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
    else:
        chosenName = None
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
        if chosenName is None:
            chosenName = theJoint
        createControl(chosenName, chosenRadius, selectedColor, selectedAxis, selectedConstrainOption, theJoint)
    else:
        i=1
        for object in sels:
            i+=1
            if chosenName is None:
                chosenName = object
            else:
                chosenName = chosenName+str(i)
            createControl(chosenName, chosenRadius, selectedColor, selectedAxis, selectedConstrainOption, object)




#NateMadeThis
def createControlWindow():
    if cmds.window("ccWindow", exists=True):
        cmds.deleteUI("ccWindow")
    cmds.showWindow(ccWindow)

#NateMadeThis
ccWindow = cmds.window(title="Add Control", widthHeight=(450, 175))#NateMadeThis
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

createControlWindow()

#constraintList = cmds.ls(type = 'parentConstraint')
#cmds.select(constraintList, r=True)