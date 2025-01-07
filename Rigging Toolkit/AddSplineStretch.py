import maya.cmds as cmds


def createStretchySplineWindow():
    if cmds.window("sIKWindow", exists=True):
        cmds.deleteUI("sIKWindow")
    cmds.showWindow(sSplineWindow)


sSplineWindow = cmds.window(title="Make IK Stretch", widthHeight=(450, 150))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Start Joint')
firstJointTextField = cmds.textField(placeholderText='ex:"Spline_01_Jnt"')
cmds.button(label='getSelection', command='getStartJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Curve')
curveTextField = cmds.textField(placeholderText='ex:"Tail_Curve"')
cmds.button(label='getSelection', command='getBaseControl()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Stretch Controller')
splineControlTextField = cmds.textField(placeholderText='ex:"Spline_Base_Ctrl"')
cmds.button(label='getSelection', command='getSplineControl()')
cmds.setParent('..')
reverseScalarCheckBox = cmds.checkBox(label='Negative Scalar Node (Use for mirrored joints)')
cmds.button(label='Add stretch', command='CreateStretchButtonCommand()')


def getStartJoint():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(firstJointTextField, e=True, text=selection)


def getBaseControl():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(curveTextField, e=True, text=selection)


def getSplineControl():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(splineControlTextField, e=True, text=selection)


def CreateStretchButtonCommand():
    chosenStartJoint = cmds.textField(firstJointTextField, q=1, text=1)
    chosenCurve = cmds.textField(curveTextField, q=1, text=True)
    chosenSplineControl = cmds.textField(splineControlTextField, q=1, text=True)
    needsReverseNode = cmds.checkBox(reverseScalarCheckBox, q=1, value=1)
    CreateIKStretch(chosenStartJoint, chosenCurve, chosenSplineControl, needsReverseNode)


def CreateIKStretch(startJoint, splineCurve, splineControl, needsReverseScalar):
    print('stretchingNEW')
    # add the stretch switch and max stretch attribute to the spline Control
    cmds.addAttr(splineControl, longName='Stretch', attributeType='float', minValue=0, maxValue=1, dv=1, keyable=True)
    placeholderName = splineControl.replace('_Ctrl', '')
    # get the shape node from the curve
    curveShapeNode = cmds.listRelatives(splineCurve, shapes=True)[0]
    curveInfoNode = cmds.createNode('curveInfo', n=placeholderName + '_CurveInfo')
    cmds.connectAttr(curveShapeNode + '.worldSpace', curveInfoNode + '.inputCurve')
    # create switch node
    stretchSwitchNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Switch_MD')
    cmds.connectAttr(splineControl + '.Stretch', stretchSwitchNode + '.input1X')
    cmds.connectAttr(curveInfoNode + '.arcLength', stretchSwitchNode + '.input2X')
    # get the list of joints under the start joint
    jointHierarchy = cmds.listRelatives(startJoint, type='joint', ad=True)
    jointHierarchy.append(startJoint)
    jointHierarchy.reverse()
    totalJoints = len(jointHierarchy)
    print('stretching %s joints' % totalJoints)

    # check to make sure the end joint is the last in the heirarchy
    print(jointHierarchy)
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
    #create master scalar node
    masterScaleOffsetNode = cmds.createNode('multiplyDivide', n= placeholderName+'MasterScale_Stretch_Offset')
    cmds.setAttr(masterScaleOffsetNode+'.input2X', 1)

    # create scalar node
    stretchsScalarNode = cmds.createNode('multiplyDivide', n=placeholderName + '_Stretch_Scalar_MD')
    cmds.setAttr(stretchsScalarNode + '.operation', 2)
    # sometimes the curve is longer than the total anatomical length, so here we subtract the difference
    curveBeginningOffsetPMA = cmds.createNode('plusMinusAverage', n=splineCurve+'StartOffsetPMA')
    cmds.connectAttr(stretchSwitchNode + '.outputX', curveBeginningOffsetPMA+'.input1D[0]')
    theDiff = cmds.getAttr(curveInfoNode + '.arcLength')-cmds.getAttr(totalAnatomicalLengthPMANode+'.output1D')
    cmds.setAttr(curveBeginningOffsetPMA+'.input1D[1]', theDiff)
    cmds.setAttr(curveBeginningOffsetPMA+'.operation', 2)
    cmds.connectAttr(curveBeginningOffsetPMA+'.output1D', stretchsScalarNode+'.input1X')
    # add a reverse scalar node if needed
    cmds.connectAttr(totalAnatomicalLengthPMANode+'.output1D', masterScaleOffsetNode+'.input1X')
    if needsReverseScalar:
        scalarReverseNode = cmds.createNode('multiplyDivide', n=placeholderName + '_negativeScalarMD')
        cmds.setAttr(scalarReverseNode + '.input2X', -1)
        cmds.connectAttr(masterScaleOffsetNode+'.outputX', scalarReverseNode + '.input1X')
        cmds.connectAttr(scalarReverseNode + '.outputX', stretchsScalarNode + '.input2X')
    else:
        cmds.connectAttr(masterScaleOffsetNode+'.outputX', stretchsScalarNode + '.input2X')
    # connect the scalar to each joint xtranslate with an MD for each joint
    splineTurnOffClampReverseNode = cmds.createNode('reverse', n=placeholderName+'Spline_Shrink_Clamp_ReverseNode')
    cmds.connectAttr(splineControl+'.Stretch', splineTurnOffClampReverseNode+'.inputX')
    for i in range(totalJoints - 1):
        currentMDNode = cmds.createNode('multiplyDivide', n=jointHierarchy[i + 1] + '_Stretch_Scalar_MD')
        scalarClampNode = cmds.createNode('clamp', n=jointHierarchy[i + 1] + '_ScalarClampNode')
        cmds.connectAttr(splineTurnOffClampReverseNode+'.outputX', scalarClampNode+'.minR')
        cmds.setAttr(scalarClampNode + '.maxR', 10)
        cmds.connectAttr(stretchsScalarNode + '.outputX', scalarClampNode + '.inputR')
        cmds.connectAttr(scalarClampNode+'.outputR', currentMDNode+'.input1X')
        cmds.connectAttr(jointHierarchy[i + 1] + '_Length_PMA.output1D', currentMDNode + '.input2X')
        cmds.connectAttr(currentMDNode + '.outputX', jointHierarchy[i+1]+'.translateX')
        # cmds.connectAttr(currentMDNode+'.outputX', jointHierarchy[i+1]+'.translateX')

