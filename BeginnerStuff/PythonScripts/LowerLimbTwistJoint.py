import maya.cmds as cmds


def createTwistJoint(placeholderName, firstJoint, secondJoint, zDirection, endOfChain):
    # create the aim loc
    aimLoc = cmds.spaceLocator(n=placeholderName + '_Aim_Loc')[0]
    locGrp = cmds.group(aimLoc, n=placeholderName + '_Twist_Loc_Grp')
    cmds.matchTransform(locGrp, firstJoint)
    cmds.matchTransform(locGrp, secondJoint, pos=1)
    # create the loc group
    cmds.parentConstraint(firstJoint, locGrp, mo=1)
    cmds.scaleConstraint(firstJoint, locGrp)
    # Create the target loc
    targetLoc = cmds.duplicate(aimLoc, n=placeholderName + '_Twist_Target_Loc')[0]
    cmds.matchTransform(targetLoc, firstJoint)
    # create the up locator
    upTargetLoc = cmds.duplicate(aimLoc, n=placeholderName + '_Up_Target')[0]
    cmds.xform(upTargetLoc, r=1, t=(0, 0, -3 * zDirection))
    cmds.parentConstraint(secondJoint, upTargetLoc, mo=1)
    cmds.pointConstraint(secondJoint, aimLoc)
    # create the aim constraint
    print(upTargetLoc)
    # if addConstraint:
    cmds.aimConstraint(targetLoc, aimLoc, o=(0, 0, 0), aim=(1, 0, 0), u=(0, 0, zDirection), wut='object', wuo=upTargetLoc)
    # creat mid loc
    midTwistLoc = cmds.duplicate(targetLoc, n=placeholderName + '_Mid_Loc')[0]
    cmds.pointConstraint(targetLoc, aimLoc, midTwistLoc)
    # hookup the twist joints
    scalarMDNode = cmds.createNode('multiplyDivide', n=placeholderName + '_MidLoc_Scale_MD')
    cmds.connectAttr(aimLoc + '.rotateX', scalarMDNode + '.input1X')
    cmds.setAttr(scalarMDNode + '.input2X', -0.5*zDirection)
    cmds.connectAttr(scalarMDNode + '.outputX', midTwistLoc + '.rotateX')
    # create and constrain the middle joint
    middleTwistJoint = cmds.duplicate(firstJoint, po=1, n=placeholderName+'_Mid_Twist_Jnt')[0]
    cmds.parent(middleTwistJoint, firstJoint)
    cmds.parentConstraint(midTwistLoc, middleTwistJoint, mo=0)
    cmds.setAttr(middleTwistJoint + ".overrideEnabled", 1)
    cmds.setAttr(middleTwistJoint + ".overrideColor", 16)
    smallRadius = (cmds.joint(firstJoint, q=1, radius=1)[0])*.5
    cmds.setAttr(middleTwistJoint+'.radius', smallRadius)
    if endOfChain:
        endTwistJoint = cmds.duplicate(firstJoint, po=1, n=placeholderName+'_End_Twist_Jnt')[0]
        cmds.parent(endTwistJoint, firstJoint)
        cmds.parentConstraint(aimLoc, endTwistJoint, mo=0)
        cmds.setAttr(endTwistJoint + ".overrideEnabled", 1)
        cmds.setAttr(endTwistJoint + ".overrideColor", 16)
        cmds.setAttr(endTwistJoint + '.radius', smallRadius)


def createLowerTwistJointWindow():
    if cmds.window("ltWindow", exists=True):
        cmds.deleteUI("ltWindow")
    cmds.showWindow(ltWindow)


ltWindow = cmds.window(title="Add Roll Joint", widthHeight=(400, 140))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(label='System Name')
nameField = cmds.textField(placeholderText='Left Forearm Twist', w=200)
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
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
endOfChainBox = cmds.checkBox(label='End Of Chain')
mirroredJointBox = cmds.checkBox(label='Mirrored Joint')
cmds.setParent('..')
cmds.button(label='create', command='twistButtonCommand()')
createLowerTwistJointWindow()


def getStartJoint():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(firstJointTextField, e=True, text=selection)


def getSecondJoint():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(secondJointTextField, e=True, text=selection)


def twistButtonCommand():
    chosenFirst = cmds.textField(firstJointTextField, q=1, text=1)
    chosenSecond = cmds.textField(secondJointTextField, q=1, text=1)
    if cmds.checkBox(mirroredJointBox, q=1, v=1):
        zDir = -1
    else:
        zDir = 1
    nameF = cmds.textField(nameField, q=1, text=1)
    endChain = cmds.checkBox(endOfChainBox, q=1, v=1)
    createTwistJoint(nameF, chosenFirst, chosenSecond, zDir, endChain)
    # negative z is mirrored
