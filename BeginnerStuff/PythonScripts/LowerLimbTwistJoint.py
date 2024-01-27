import maya.cmds as cmds


def createShoulderTwistJoint(placeholderName, numJoints, firstJoint, secondJoint, sAxis, locatorOffset, zDirection,
                             endOfChain):
    isShoulder = True

    aimLoc = cmds.spaceLocator(n=placeholderName + '_Aim_Loc')[0]
    locGrp = cmds.group(aimLoc, n=placeholderName + '_Twist_Loc_Grp')
    cmds.matchTransform(locGrp, firstJoint)
    targetLoc = cmds.duplicate(aimLoc, n=placeholderName + '_Target_Loc')[0]
    cmds.matchTransform(targetLoc, secondJoint, pos=1)
    upTargetLoc = cmds.duplicate(targetLoc, n=placeholderName + '_Up_Target')[0]
    cmds.xform(upTargetLoc, r=1, t=getLocatorAxis(locatorOffset, sAxis, zDirection))
    cmds.parentConstraint(firstJoint, locGrp, mo=1)
    cmds.scaleConstraint(firstJoint, locGrp)
    cmds.pointConstraint(secondJoint, targetLoc, mo=0)
    cmds.aimConstraint(targetLoc, aimLoc, o=(0, 0, 0), aim=(zDirection, 0, 0), u=getUpAxis(sAxis, zDirection),
                       wut='object', wuo=upTargetLoc)
    # create the joints
    ikJointOne = cmds.joint(n=placeholderName + '_IK_Joint_1')
    ikJointTwo = cmds.duplicate(ikJointOne, n=placeholderName + '_IK_Joint_2')[0]
    cmds.parent(ikJointTwo, ikJointOne)
    cmds.matchTransform(ikJointOne, firstJoint)
    cmds.xform(ikJointOne, r=1, os=1, t=getLocatorAxis(locatorOffset, sAxis, zDirection))
    cmds.matchTransform(ikJointTwo, secondJoint, pos=1)
    cmds.joint(ikJointOne, e=1, oj='xyz', zso=1)
    cmds.joint(ikJointTwo, e=1, oj='none', zso=1)
    cmds.setAttr(ikJointTwo + '.translateX', cmds.getAttr(ikJointTwo + '.translateX') * .5)
    #   group the joints and flip them
    cmds.parent(ikJointOne, w=1)
    cmds.select(cl=1)
    ikJointGrp = cmds.group(w=1, em=1, n=placeholderName + '_IK_Joint_Grp')
    cmds.matchTransform(ikJointGrp, ikJointOne)
    cmds.parent(ikJointOne, ikJointGrp)
    cmds.setAttr(ikJointGrp + '.rotateX', cmds.getAttr(ikJointGrp + '.rotateX') + (90 * zDirection))
    # create and handle the IK Handle
    ikHandle = placeholderName + '_IK_Jnt_Handle'
    cmds.ikHandle(n=ikHandle, sol='ikRPsolver', sj=ikJointOne, ee=ikJointTwo)
    cmds.pointConstraint(secondJoint, ikHandle, mo=0)
    ikJntPVLoc = cmds.spaceLocator(n=placeholderName + '_IK_Handle_PV_Loc')
    cmds.matchTransform(ikJntPVLoc, ikJointOne)
    cmds.xform(ikJntPVLoc, os=1, r=1, t=(0, -locatorOffset, 0))
    cmds.poleVectorConstraint(ikJntPVLoc, ikHandle)
    # connect the systems
    cmds.pointConstraint(ikJointOne, upTargetLoc, mo=1)
    jointSystemGrp = cmds.group(ikJntPVLoc, ikJointGrp, ikHandle, n=placeholderName + '_IK_Jnt_System')
    metaGrp = cmds.group(locGrp, jointSystemGrp, n=placeholderName + '_Master_Grp')
    createMidTwists(placeholderName, numJoints, firstJoint, secondJoint, zDirection, endOfChain, isShoulder, aimLoc,
                    targetLoc)
    parentJointCheck = cmds.listRelatives(firstJoint, p=True)
    if not parentJointCheck:
        print('no parent')
    else:
        cmds.parentConstraint(parentJointCheck, metaGrp, mo=1)
        cmds.scaleConstraint(parentJointCheck, metaGrp)


def createMidTwists(placeholderName, numJoints, firstJoint, secondJoint, zDirection, endOfChain, isShoulder, aimLoc,
                    targetLoc):
    smallRadius = cmds.joint(firstJoint, q=1, radius=1)[0] * -.5
    for i in range(numJoints):
        # get weight values
        jointNum = i + 1
        secondJointWeight = jointNum * (1 / (numJoints + 1))
        firstJointWeight = 1 - secondJointWeight
        # create the locators
        midTwistLoc = cmds.duplicate(targetLoc, n=placeholderName + '_Mid_Loc' + str(i + 1))[0]
        cmds.pointConstraint(targetLoc, aimLoc, midTwistLoc, mo=0)
        # set the constraint to balance based on which locator it is
        thisPointConstraint = cmds.listConnections(midTwistLoc, type='pointConstraint')[0]
        weightList = cmds.pointConstraint(thisPointConstraint, q=1, wal=1)
        cmds.setAttr(thisPointConstraint + '.' + weightList[0], firstJointWeight)
        cmds.setAttr(thisPointConstraint + '.' + weightList[1], secondJointWeight)
        # set up the nodes
        thisRotateMDNode = cmds.createNode('multiplyDivide',
                                           n=placeholderName + '_MidLoc ' + str(jointNum) + '_Rotate_MD')
        if isShoulder:
            cmds.connectAttr(firstJoint + '.rotateX', thisRotateMDNode + '.input1X')
            cmds.setAttr(thisRotateMDNode + '.input2X', secondJointWeight * -1)
        else:
            cmds.connectAttr(aimLoc + '.rotateX', thisRotateMDNode + '.input1X')
            cmds.setAttr(thisRotateMDNode + '.input2X', secondJointWeight)
        cmds.connectAttr(thisRotateMDNode + '.outputX', midTwistLoc + '.rotateX')
        # create and place the joint
        thisJoint = cmds.duplicate(firstJoint, po=1, n=placeholderName + '_Mid_Twist_Jnt_' + str(i + 1))[0]
        cmds.parent(thisJoint, firstJoint)
        cmds.parentConstraint(midTwistLoc, thisJoint, mo=0)
        # set the color and size of the joint
        cmds.setAttr(thisJoint + ".overrideEnabled", 1)
        cmds.setAttr(thisJoint + ".overrideColor", 16)
        cmds.setAttr(thisJoint + '.radius', smallRadius)
    if endOfChain or isShoulder:
        endTwistJoint = cmds.duplicate(firstJoint, po=1, n=placeholderName + '_End_Twist_Jnt')[0]
        cmds.parent(endTwistJoint, firstJoint)
        cmds.parentConstraint(aimLoc, endTwistJoint, mo=0)
        cmds.setAttr(endTwistJoint + ".overrideEnabled", 1)
        cmds.setAttr(endTwistJoint + ".overrideColor", 16)
        cmds.setAttr(endTwistJoint + '.radius', smallRadius)


def createTwistJoint(placeholderName, numJoints, firstJoint, secondJoint, sAxis, locatorOffset, zDirection, endOfChain):
    isShoulder = False
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
    cmds.xform(upTargetLoc, r=1, t=getLocatorAxis(locatorOffset, sAxis, zDirection))
    cmds.parentConstraint(secondJoint, upTargetLoc, mo=1)
    cmds.pointConstraint(secondJoint, aimLoc)
    # create the aim constraint
    print(upTargetLoc)
    # if addConstraint:
    cmds.aimConstraint(targetLoc, aimLoc, o=(0, 0, 0), aim=(-zDirection, 0, 0), u=getUpAxis(sAxis, zDirection), wut='object',
                       wuo=upTargetLoc)
    createMidTwists(placeholderName, numJoints, firstJoint, secondJoint, zDirection, endOfChain, isShoulder, aimLoc,
                    targetLoc)

def getUpAxis(axis, zDirection):
    if axis == 1:
        return (-zDirection, 0, 0)
    elif axis == 2:
        return (0, -zDirection, 0)
    elif axis == 3:
        return (0, 0, -zDirection)


def getLocatorAxis(locatorOffset, axis, zDirection):
    if axis == 1:
        return (-locatorOffset * zDirection, 0, 0)
    elif axis == 2:
        return (0, -locatorOffset * zDirection, 0)
    elif axis == 3:
        return (0, 0, -locatorOffset * zDirection)


def createLowerTwistJointWindow():
    if cmds.window("ltWindow", exists=True):
        cmds.deleteUI("ltWindow")
    cmds.showWindow(ltWindow)


ltWindow = cmds.window(title="Add Roll Joint", widthHeight=(400, 225))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
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
locatorOffsetFloatField = cmds.floatField(min=.01, value=1)
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
    numJ = cmds.intField(numJField, q=1, v=1)
    chosenFirst = cmds.textField(firstJointTextField, q=1, text=1)
    chosenSecond = cmds.textField(secondJointTextField, q=1, text=1)
    if cmds.checkBox(mirroredJointBox, q=1, v=1):
        zDir = -1
    else:
        zDir = 1
    nameF = cmds.textField(nameField, q=1, text=1)
    nameF = nameF.replace(' ', '_')
    offsetDistance = cmds.floatField(locatorOffsetFloatField, q=1, value=1)
    endChain = cmds.checkBox(endOfChainBox, q=1, v=1)
    sAxis = cmds.radioButtonGrp(axisSelection, q=True, select=True)
    if cmds.checkBox(shoulderBox, q=1, v=1):
        createShoulderTwistJoint(nameF, numJ, chosenFirst, chosenSecond, sAxis, offsetDistance, zDir, endChain)
    else:
        createTwistJoint(nameF, numJ, chosenFirst, chosenSecond, sAxis, offsetDistance, zDir, endChain)
    # negative z is mirrored
