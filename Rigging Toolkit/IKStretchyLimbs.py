import maya.cmds as cmds


def CreateIKStretch(startJoint, baseControl, ikControl, maxStretchValue, needsReverseScalar, includeMasterScalar):
    # add the stretch switch and max stretch attribute to the ik Control
    cmds.addAttr(ikControl, longName='Stretch', attributeType='float', minValue=0, maxValue=1, dv=1, keyable=True)
    cmds.addAttr(ikControl, longName='Max_Stretch', attributeType='float', minValue=1, maxValue=maxStretchValue,
                 dv=maxStretchValue, keyable=True)
    # add the locators
    baseLoc = cmds.spaceLocator(n=(startJoint + '_baseStretch_Loc'))[0]
    cmds.matchTransform(baseLoc, startJoint)
    cmds.parentConstraint(baseControl, baseLoc, mo=1)
    endLoc = cmds.spaceLocator(n=(startJoint + '_endStretch_Loc'))[0]
    cmds.matchTransform(endLoc, ikControl)
    cmds.parentConstraint(ikControl, endLoc)
    # get the list of joints under the start joint
    jointHierarchy = cmds.listRelatives(startJoint, type='joint', ad=True)
    jointHierarchy.append(startJoint)
    jointHierarchy.reverse()
    totalJoints = len(jointHierarchy)
    placeholderName = ikControl.replace('_Ctrl', '')
    # check to make sure the end joint is the last in the heirarchy
    '''print(totalJointHierarchy[len(totalJointHierarchy)-1])
    print(endJoint)
    if totalJointHierarchy[len(totalJointHierarchy)-1] is not endJoint:
        cmds.error("end joint is not the end of the joint chain")
    print(totalJointHierarchy)'''
    # add the total anatomical length of joint chain
    totalAnatomicalLengthPMANode = cmds.createNode('plusMinusAverage',
                                                   n=placeholderName + '_Stretch_Total_Anatomical_Length_PMA')
    for i in range(totalJoints - 1):
        currentPMALengthNode = cmds.createNode('plusMinusAverage', n=jointHierarchy[i + 1] + '_Length_PMA')
        cmds.connectAttr((jointHierarchy[i + 1] + '.translateX'), currentPMALengthNode + '.input1D[0]')
        cmds.connectAttr(currentPMALengthNode + '.output1D',
                         (totalAnatomicalLengthPMANode + '.input1D[' + str(i) + ']'))
        cmds.disconnectAttr((jointHierarchy[i + 1] + '.translateX'), currentPMALengthNode + '.input1D[0]')
    # create a node that holds the distance between the locators
    distanceBetweenLocatorsNode = cmds.createNode('distanceBetween',
                                                  n=placeholderName + '_Stretch_Locator_DistanceBetween')
    cmds.connectAttr(baseLoc + '.worldMatrix', distanceBetweenLocatorsNode + '.inMatrix1')
    cmds.connectAttr(endLoc + '.worldMatrix', distanceBetweenLocatorsNode + '.inMatrix2')
    # create switch node
    stretchSwitchNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Switch_MD')
    if includeMasterScalar:
        masterScalarMDNode = cmds.createNode('multiplyDivide', n=placeholderName + 'Master_Scalar_MD')
        cmds.setAttr(masterScalarMDNode + '.operation', 2)
        cmds.connectAttr(distanceBetweenLocatorsNode + '.distance', masterScalarMDNode + '.input1X')
        cmds.setAttr(masterScalarMDNode + '.input2X', 1)
        cmds.connectAttr(masterScalarMDNode + '.outputX', stretchSwitchNode + '.input2X')
    else:
        cmds.connectAttr(distanceBetweenLocatorsNode + '.distance', stretchSwitchNode + '.input2X')
    cmds.connectAttr(ikControl + '.Stretch', stretchSwitchNode + '.input1X')
    # create scalar node
    stretchsScalarNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Scalar_MD')
    cmds.setAttr(stretchsScalarNode + '.operation', 2)
    if needsReverseScalar:
        scalarReverseNode = cmds.createNode('multiplyDivide', n=placeholderName + '_negativeScalarMD')
        cmds.setAttr(scalarReverseNode + '.input2X', -1)
        cmds.connectAttr(totalAnatomicalLengthPMANode + '.output1D', scalarReverseNode + '.input1X')
        cmds.connectAttr(scalarReverseNode + '.outputX', stretchsScalarNode + '.input2X')
    else:
        cmds.connectAttr(totalAnatomicalLengthPMANode + '.output1D', stretchsScalarNode + '.input2X')
    cmds.connectAttr(stretchSwitchNode + '.outputX', stretchsScalarNode + '.input1X')
    # create clamp node for stretch
    stretchClampNode = cmds.createNode('clamp', n=placeholderName + '_Stretch_Clamp')
    cmds.setAttr(stretchClampNode + '.minR', 1)
    cmds.connectAttr(ikControl + '.Max_Stretch', stretchClampNode + '.maxR')

    cmds.connectAttr(stretchsScalarNode + ".outputX", stretchClampNode + '.inputR')
    # connect the scalar to each joint xtranslate with an MD for each joint
    for i in range(totalJoints - 1):
        currentMDNode = cmds.createNode('multiplyDivide', n=jointHierarchy[i + 1] + '_Stretch_Scalar_MD')
        cmds.connectAttr(stretchClampNode + '.outputR', currentMDNode + '.input1X')
        cmds.connectAttr(jointHierarchy[i + 1] + '_Length_PMA.output1D', currentMDNode + '.input2X')
        cmds.connectAttr(currentMDNode + '.outputX', jointHierarchy[i + 1] + '.translateX')


def CreateIKStretchNumJoints(startJoint, numJoints, baseControl, ikControl, maxStretchValue, needsReverseScalar,
                             includeMasterScalar):
    # add the stretch switch and max stretch attribute to the ik Control
    cmds.addAttr(ikControl, at='enum', nn='____________', ln='StretchDivider', en='STRETCH', k=1)
    cmds.addAttr(ikControl, longName='Stretch', attributeType='float', minValue=0, maxValue=1, dv=1, keyable=True)
    cmds.addAttr(ikControl, longName='Max_Stretch', attributeType='float', minValue=1, maxValue=maxStretchValue,
                 dv=maxStretchValue, keyable=True)
    # add the locators
    baseLoc = cmds.spaceLocator(n=(startJoint + '_baseStretch_Loc'))[0]
    cmds.matchTransform(baseLoc, startJoint)
    cmds.parentConstraint(baseControl, baseLoc, mo=1)
    endLoc = cmds.spaceLocator(n=(startJoint + '_endStretch_Loc'))[0]
    cmds.matchTransform(endLoc, ikControl)
    cmds.parentConstraint(ikControl, endLoc)
    # get the list of joints under the start joint
    jointHierarchy = cmds.listRelatives(startJoint, type='joint', ad=True)
    jointHierarchy.append(startJoint)
    jointHierarchy.reverse()
    totalJoints = numJoints
    placeholderName = ikControl.replace('_Ctrl', '')
    # check to make sure the end joint is the last in the heirarchy
    '''print(totalJointHierarchy[len(totalJointHierarchy)-1])
    print(endJoint)
    if totalJointHierarchy[len(totalJointHierarchy)-1] is not endJoint:
        cmds.error("end joint is not the end of the joint chain")
    print(totalJointHierarchy)'''
    # add the total anatomical length of joint chain
    totalAnatomicalLengthPMANode = cmds.createNode('plusMinusAverage',
                                                   n=placeholderName + '_Stretch_Total_Anatomical_Length_PMA')
    for i in range(totalJoints - 1):
        currentPMALengthNode = cmds.createNode('plusMinusAverage', n=jointHierarchy[i + 1] + '_Length_PMA')
        cmds.connectAttr((jointHierarchy[i + 1] + '.translateX'), currentPMALengthNode + '.input1D[0]')
        cmds.connectAttr(currentPMALengthNode + '.output1D',
                         (totalAnatomicalLengthPMANode + '.input1D[' + str(i) + ']'))
        cmds.disconnectAttr((jointHierarchy[i + 1] + '.translateX'), currentPMALengthNode + '.input1D[0]')
    # create a node that holds the distance between the locators
    distanceBetweenLocatorsNode = cmds.createNode('distanceBetween',
                                                  n=placeholderName + '_Stretch_Locator_DistanceBetween')
    cmds.connectAttr(baseLoc + '.worldMatrix', distanceBetweenLocatorsNode + '.inMatrix1')
    cmds.connectAttr(endLoc + '.worldMatrix', distanceBetweenLocatorsNode + '.inMatrix2')
    # create switch node
    stretchSwitchNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Switch_MD')
    if includeMasterScalar:
        masterScalarMDNode = cmds.createNode('multiplyDivide', n=placeholderName + 'Master_Scalar_MD')
        cmds.setAttr(masterScalarMDNode + '.operation', 2)
        cmds.connectAttr(distanceBetweenLocatorsNode + '.distance', masterScalarMDNode + '.input1X')
        cmds.setAttr(masterScalarMDNode + '.input2X', 1)
        cmds.connectAttr(masterScalarMDNode + '.outputX', stretchSwitchNode + '.input2X')
    else:
        cmds.connectAttr(distanceBetweenLocatorsNode + '.distance', stretchSwitchNode + '.input2X')
    cmds.connectAttr(ikControl + '.Stretch', stretchSwitchNode + '.input1X')
    # create scalar node
    stretchsScalarNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Scalar_MD')
    cmds.setAttr(stretchsScalarNode + '.operation', 2)
    if needsReverseScalar:
        scalarReverseNode = cmds.createNode('multiplyDivide', n=placeholderName + '_negativeScalarMD')
        cmds.setAttr(scalarReverseNode + '.input2X', -1)
        cmds.connectAttr(totalAnatomicalLengthPMANode + '.output1D', scalarReverseNode + '.input1X')
        cmds.connectAttr(scalarReverseNode + '.outputX', stretchsScalarNode + '.input2X')
    else:
        cmds.connectAttr(totalAnatomicalLengthPMANode + '.output1D', stretchsScalarNode + '.input2X')
    cmds.connectAttr(stretchSwitchNode + '.outputX', stretchsScalarNode + '.input1X')
    # create clamp node for stretch
    stretchClampNode = cmds.createNode('clamp', n=placeholderName + '_Stretch_Clamp')
    cmds.setAttr(stretchClampNode + '.minR', 1)
    cmds.connectAttr(ikControl + '.Max_Stretch', stretchClampNode + '.maxR')

    cmds.connectAttr(stretchsScalarNode + ".outputX", stretchClampNode + '.inputR')
    # connect the scalar to each joint xtranslate with an MD for each joint
    for i in range(totalJoints - 1):
        currentMDNode = cmds.createNode('multiplyDivide', n=jointHierarchy[i + 1] + '_Stretch_Scalar_MD')
        cmds.connectAttr(stretchClampNode + '.outputR', currentMDNode + '.input1X')
        cmds.connectAttr(jointHierarchy[i + 1] + '_Length_PMA.output1D', currentMDNode + '.input2X')
        cmds.connectAttr(currentMDNode + '.outputX', jointHierarchy[i + 1] + '.translateX')
