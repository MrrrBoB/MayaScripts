import maya.cmds as cmds


def createARWindow():
    if cmds.window("AutoRiggerWindow", exists=True):
        cmds.deleteUI("AutoRiggerWindow")
    cmds.showWindow(AutoRiggerWindow)

# AUTO RIGGER TAB
AutoRiggerWindow = cmds.window(widthHeight=(600, 300))
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, nch=3)
cmds.formLayout(form, edit=True,
                attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

child1 = cmds.columnLayout(adjustableColumn=1, rowSpacing=10)
line1RowLayout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine1 = cmds.text(label='1. Create Height Locators.', al='left')
locatorButton = cmds.button(label='CreateLocators', command='AR.CreateHeightLocators()', al='right')
cmds.setParent('..')
instructionLine2 = cmds.text(l='2. Place the base locator at the base of the character, and the top locator on '
                               'top of the head',
                             al='left')
line3Layout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine3 = cmds.text(l='3. Create skeleton template', al='left')
createTemplateButton = cmds.button(l='Create Joint Template', command='LayoutCommand()')
cmds.setParent('..')
instructionLine4 = cmds.text(l='4. Move joints to match your character. Fingers must be oriented manually', al='left')
line5Layout = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
instructionLine5 = cmds.text(l='5. Orient and mirror skeleton')
orientButton = cmds.button(l='Orient', command='OrientButton()', w=100)
mirrorButton = cmds.button(l='Mirror', command='MirrorButton()', w=100)
cmds.setParent('..')
instructionLine6 = cmds.text(l='6. Check your skeleton. Make sure all joints are oriented correctly (double check '
                               'fingers)',
                             al='left')
line7Layout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine7 = cmds.text(l='7. Rig it!', al='left')
rigButton = cmds.button(l='RIG', command='RigSimpleButton()', w=100)
cmds.setParent(tabs)

# CONTROL TAB
child2 = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
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
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'left'))
constraintCheckBox = cmds.checkBox(label='Constrain Joint', onc='TurnOffCheckBox(worldControlCheckBox)')
worldControlCheckBox = cmds.checkBox(label='Create empty', onc='TurnOffCheckBox(constraintCheckBox)')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
cmds.button(label="Create Control", command='ControlButtonCommand()')
cmds.button(label='Mirror Selected Controls (X axis)', command='ControlMirrorCommand()')
cmds.setParent(tabs)

#IK SYSTEMS TAB
child3 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
#IK STRETCH SUBTAB
IKchild1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Start Joint')
firstJointTextField = cmds.textField(placeholderText='ex:"IK_01_Jnt"')
cmds.button(label='getSelection', command='getStartJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Base Control')
baseControlTextField = cmds.textField(placeholderText='ex:"IK_Shoulder_Ctrl"')
cmds.button(label='getSelection', command='getBaseControl()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='IK Control')
IKControlTextField = cmds.textField(placeholderText='ex:"IK_03_Jnt"')
cmds.button(label='getSelection', command='getIKControl()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(label='Maximum Stretch Multiplier')
maxStretchFloatSlider = cmds.floatSliderGrp(label="Radius Size:",
                                            min=2,
                                            max=10,
                                            value=3,
                                            field=True)
cmds.setParent('..')
reverseScalarCheckbox = cmds.checkBox(label='Negative Scalar Node')
cmds.button(label='Add stretch', command='CreateStretchButtonCommand()')
cmds.setParent('..')
#IK REVERSE FOOT SUBTAB
IKchild2 = cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2)
prefixField = cmds.textField(placeholderText='System Prefix', width=150)
cmds.button(label='Create Locators', command='LocatorButtonCmd()', width=150)
cmds.setParent('..')
cmds.button(label="I've placed my locators, GO!", command='CreateReverseFootSystem()')
cmds.setParent('..')
cmds.setParent('..')


#JOINTS TAB
child4 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
#TWIST JOINT SUBTAB
JointsChild1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(label='System Name')
nameField = cmds.textField(placeholderText='Left Forearm Twist', w=200)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(label='Number of Twist Joints')
numJField = cmds.intField(min=1, v=1)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=1, columnAlign=(1, 'right'))
axisSelection = cmds.radioButtonGrp(label='Locator Axis', labelArray3=['x', 'y', 'z'], numberOfRadioButtons=3, select=1)
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Start Joint')
firstJointTextField = cmds.textField(placeholderText='ex:"Elbow Jnt"', w=200)
cmds.button(label='getSelection', command='getStartJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='SecondJoint')
secondJointTextField = cmds.textField(placeholderText='ex:"Hand Jnt"', w=200)
cmds.button(label='getSelection', command='getSecondJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
shoulderBox = cmds.checkBox(label='Shoulder')
endOfChainBox = cmds.checkBox(label='End Of Chain')
mirroredJointBox = cmds.checkBox(label='Mirrored Joint')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(label='Locator Offset')
locatorOffsetFloatField = cmds.floatField(value=1)
cmds.setParent('..')
cmds.button(label='create', command='twistButtonCommand()')
cmds.setParent('..')
JointsChild2 = cmds.button(l='Disable Segment Scale Compensate', command='SSCDisableCommand()')
cmds.setParent('..')


child5 = cmds.rowColumnLayout(numberOfColumns=2)
cmds.button()
cmds.button()
cmds.button()
cmds.setParent( '..' )

cmds.tabLayout(tabs, e=1, tl=((child1, 'AutoRigger'),
                              (child2, 'Controls'),
                              (child3, 'IK Systems'),
                              (child4, 'Joints'),
                              (child5, 'Misc')))
cmds.tabLayout(child3, e=1, tl=((IKchild1, 'IK_Stretch'), (IKchild2, 'Reverse Foot')))
cmds.tabLayout(child4, e=1, tl=((JointsChild1, 'Twist Joints'), (JointsChild2, 'Segment Scale Compensate')))


cmds.showWindow()


def TurnOffCheckBox(checkbox):
    cmds.checkBox(checkbox, e=1, v=0)


def ControlButtonCommand():
    print('ControlCreatorButton has not been set up')


def ControlMirrorCommand():
    print('ControlCreatorButton has not been set up')
