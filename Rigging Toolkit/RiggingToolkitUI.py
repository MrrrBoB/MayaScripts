import maya.cmds as cmds
# noinspection PyUnresolvedReferences
from Rigging_Toolkit import AutoRigger as AR
# noinspection PyUnresolvedReferences
from Rigging_Toolkit import BlendShapeController as BSC
# noinspection PyUnresolvedReferences
from Rigging_Toolkit import Controls as CC


def CreateRTWindow():
    if cmds.window("RiggingToolkitWindow", exists=True):
        cmds.deleteUI("RiggingToolkitWindow")
    cmds.showWindow(RiggingToolkitWindow)


# AUTO RIGGER TAB
RiggingToolkitWindow = cmds.window(widthHeight=(600, 300))
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

child2 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

# CONTROL CREATOR SUB-TAB

controlsChild1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=5, )
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
cmds.button(label="Create Control", command='ControlButtonCommand()')
cmds.setParent(child2)

# MIRROR CONTROLS SUB-TAB

controlsChild2 = cmds.button(label='Mirror Selected Controls (X axis)', command='ControlMirrorCommand()')

# BROKEN FK SUB-TAB

controlsChild3 = cmds.button(label='Create Broken FK Connection', command='CreateBrokenFKCommand()')

cmds.setParent(tabs)

# IK SYSTEMS TAB
child3 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
# IK STRETCH SUB-TAB
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
# IK REVERSE FOOT SUB-TAB
IKchild2 = cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2)
prefixField = cmds.textField(placeholderText='System Prefix', width=150)
cmds.button(label='Create Locators', command='LocatorButtonCmd()', width=150)
cmds.setParent('..')
cmds.button(label="I've placed my locators, GO!", command='CreateReverseFootSystem()')
cmds.setParent('..')
cmds.setParent('..')

# JOINTS TAB
child4 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
# TWIST JOINT SUB-TAB
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

# MISC TAB

child5 = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

# COLOR CHANGER SUB-TAB

miscChild1 = cmds.columnLayout(adjustableColumn=True, rowSpacing=25, )
cmds.text(l='Change the color of controls or joints')
customColorSlider = cmds.colorIndexSliderGrp(label="New Color", min=0, max=31, value=18, h=30)
applyButton = cmds.button(label='Change Color', command='changeColorButtonCommand()')
cmds.setParent('..')

# RENAME SEQUENCE SUB-TAB

miscChild2 = cmds.columnLayout(adjustableColumn=True, rowSpacing=15)
cmds.text(label="Rename Format")
inputField = cmds.textField(placeholderText="use # for digit count, ex: Arm_##_Jnt")
cmds.button(label='Rename', command='button_command()')
cmds.setParent('..')

# CONTROL TO BLENDSHAPE SUB-TAB

miscChild3 = cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
linearRadioGrp = cmds.radioButtonGrp(l='Blendshape Connection', nrb=2, la2=['Linear', 'Positive/Negative'],
                                     changeCommand='BSCRadioChangeCommand()', sl=0)
cmds.rowLayout(nc=2)
transformTypeMenu = cmds.optionMenu()
cmds.menuItem(l='translate')
cmds.menuItem(l='rotate')
cmds.menuItem(l='scale')
transformAxisMenu = cmds.optionMenu()
cmds.menuItem(l='X')
cmds.menuItem(l='Y')
cmds.menuItem(l='Z')
cmds.setParent('..')
twoColumnParent = cmds.rowLayout(nc=2)
leftColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
leftColumnLabel = cmds.text(l='lcolumn')
blendShapeList = cmds.ls(type='blendShape')
BSNodeMenuP = cmds.optionMenu(label='Blend shape Nodes', changeCommand='BSCUpdateTargetListP()')
cmds.menuItem(l="Select")
for item in blendShapeList:
    cmds.menuItem(l=item)
TargetMenuP = cmds.optionMenu(label='Target')
cmds.menuItem(l='N/A')
cmds.rowLayout(nc=2)
cmds.text(l='Multiplier')
multiplierField = cmds.floatField(v=1)
cmds.setParent(twoColumnParent)
# Break for right column
rightColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=5, vis=0)
cmds.text(l='Negative Value')
BSNodeMenuN = cmds.optionMenu(label='Blend shape Nodes', changeCommand='BSCUpdateTargetListN()')
cmds.menuItem(l="Select")
for item in blendShapeList:
    cmds.menuItem(l=item)
TargetMenuN = cmds.optionMenu(label='Target')
cmds.menuItem(l='N/A')
cmds.rowLayout(nc=2)
cmds.text(l='Multiplier')
multiplierFieldNegative = cmds.floatField(v=1)
cmds.setParent(twoColumnParent)
cmds.setParent('..')
cmds.button(l='CONNECT', command='BSCBUttonCommand()')
cmds.setParent(tabs)

# TAB NAMES TAB NAMES TAB NAMES

cmds.tabLayout(tabs, e=1, tl=((child1, 'AutoRigger'),
                              (child2, 'Controls'),
                              (child3, 'IK Systems'),
                              (child4, 'Joints'),
                              (child5, 'Misc')))
cmds.tabLayout(child2, e=1, tl=((controlsChild1, 'Create Control'),  # Controls
                                (controlsChild2, 'Mirror Controls'),
                                (controlsChild3, 'Broken FK')))
cmds.tabLayout(child3, e=1, tl=((IKchild1, 'IK_Stretch'),  # IK Systems
                                (IKchild2, 'Reverse Foot')))
cmds.tabLayout(child4, e=1, tl=((JointsChild1, 'Twist Joints'),  # Joints
                                (JointsChild2, 'Segment Scale Compensate')))
cmds.tabLayout(child5, e=1, tl=((miscChild1, 'Change Color'),  # Misc
                                (miscChild2, 'Rename Chain'),
                                (miscChild3, 'BlendShape Controller')))

cmds.showWindow()


def TurnOffCheckBox(checkbox):
    cmds.checkBox(checkbox, e=1, v=0)


def ControlButtonCommand():
    print('ControlCreatorButton has not been set up')


def ControlMirrorCommand():
    print('ControlCreatorButton has not been set up')


def ShowBSCMenu():
    BSC.CreateBSControlWindow()


def LayoutCommand():
    AR.InitializeHeirarchy()
    AR.CreateHumanoidSkeletonTemplate()


def OrientButton():
    AR.OrientSkeleton()


def RigSimpleButton():
    AR.ImplementIKFK()
    AR.IKControls()
    AR.FKControls()
    AR.HeadCtrls()
    AR.HybridHands()
    AR.MetaControls()
    AR.SpaceSwapIK()
    AR.IKLimbStretch()
    AR.TwistJoints()
    AR.FixSegmentScaleCompensate()


def MirrorButton():
    AR.MirrorJoints(0)


def BSCUpdateTargetListP():
    blendShapeNode = cmds.optionMenu(BSNodeMenuP, q=1, v=1)
    print(blendShapeNode)
    # Get blend shape weight names!!!
    targetListCount = cmds.blendShape(blendShapeNode, q=1, wc=1)
    targetListAlias = cmds.aliasAttr(blendShapeNode, q=1)
    targetList = []
    for i in range(targetListCount):
        targetList.append(targetListAlias[i * 2])
    # End of copy
    cmds.optionMenu(TargetMenuP, e=1, dai=1)
    for target in targetList:
        cmds.menuItem(target, p=TargetMenuP)


def BSCUpdateTargetListN():
    blendShapeNode = cmds.optionMenu(BSNodeMenuN, q=1, v=1)
    print(blendShapeNode)
    # Get blend shape weight names!!!
    targetListCount = cmds.blendShape(blendShapeNode, q=1, wc=1)
    targetListAlias = cmds.aliasAttr(blendShapeNode, q=1)
    targetList = []
    for i in range(targetListCount):
        targetList.append(targetListAlias[i * 2])
    # End of copy
    cmds.optionMenu(TargetMenuN, e=1, dai=1)
    for target in targetList:
        cmds.menuItem(target, p=TargetMenuN)


def updateTargetLists():
    BSCUpdateTargetListN()
    BSCUpdateTargetListP()


def BSCRadioChangeCommand():
    linear = cmds.radioButtonGrp(linearRadioGrp, q=1, sl=1)
    if linear == 1:
        cmds.columnLayout(rightColumn, e=1, vis=0)
        cmds.text(leftColumnLabel, e=1, l='Value')
    else:
        cmds.columnLayout(rightColumn, e=1, vis=1)
        cmds.text(leftColumnLabel, e=1, l='Positive Value')


def BSCButtonCommand():
    if cmds.optionMenu(BSNodeMenuP, q=1, v=1) == 'Select':
        cmds.warning('Please Select a blendshape target')
        return
    BSNodeNameP = cmds.optionMenu(BSNodeMenuP, q=1, v=1)
    TargetNameP = cmds.optionMenu(TargetMenuP, q=1, v=1)
    transformMode = cmds.optionMenu(transformTypeMenu, q=1, v=1)
    axis = cmds.optionMenu(transformAxisMenu, q=1, v=1)
    multiplierP = cmds.floatField(multiplierField, q=1, v=1)
    isLinear = cmds.radioButtonGrp(linearRadioGrp, q=1, sl=1)
    if isLinear == 1:
        BSC.ConnectBSLinear(BSNodeNameP + '.' + TargetNameP, transformMode + axis, multiplierP)
    else:
        if cmds.optionMenu(BSNodeMenuN, q=1, v=1) == 'Select':
            cmds.warning('Please Select a blendshape target for the negative values')
            return
        BSNodeNameNegative = cmds.optionMenu(BSNodeMenuN, q=1, v=1)
        TargetNameNegative = cmds.optionMenu(TargetMenuN, q=1, v=1)
        multiplierNegative = cmds.floatField(multiplierFieldNegative, q=1, v=1)
        BSC.ConnectBSNonLinear(BSNodeNameP + '.' + TargetNameP,
                               BSNodeNameNegative + '.' + TargetNameNegative,
                               transformMode + axis,
                               multiplierP,
                               multiplierNegative)
