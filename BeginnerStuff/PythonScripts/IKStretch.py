import maya.cmds as cmds


def createStretchyIKWindow():
    if cmds.window("sIKWindow", exists=True):
        cmds.deleteUI("sIKWindow")
    cmds.showWindow(sIKWindow)


sIKWindow = cmds.window(title="Make IK Stretch", widthHeight=(450, 150))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
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
cmds.button(label='Add stretch', command='CreateStretchButtonCommand()')
createStretchyIKWindow()


def getStartJoint():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(firstJointTextField, e=True, text=selection)


def getBaseControl():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(baseControlTextField, e=True, text=selection)


def getIKControl():
    selection = cmds.ls(sl=1)[0]
    cmds.textField(IKControlTextField, e=True, text=selection)


def CreateStretchButtonCommand():
    chosenStartJoint = cmds.textField(firstJointTextField, q=1, text=1)
    chosenBaseControl = cmds.textField(baseControlTextField, q=1, text=True)
    chosenIKControl = cmds.textField(IKControlTextField, q=1, text=True)
    chosenMaxStretch = cmds.floatSliderGrp(maxStretchFloatSlider, q=True, v=True)
    CreateIKStretch(chosenStartJoint, chosenBaseControl, chosenIKControl, chosenMaxStretch)


def CreateIKStretch(startJoint, baseControl, ikControl, maxStretchValue):

# add the stretch switch and max stretch attribute to the ik Control
    cmds.addAttr(ikControl, longName='Stretch', attributeType='float', minValue=0, maxValue=1, dv=1, keyable=True)
    cmds.addAttr(ikControl, longName='Max_Stretch', attributeType='float', minValue=1, maxValue=maxStretchValue, dv=maxStretchValue, keyable=True)
# add the locators
    baseLoc = cmds.spaceLocator(n=(startJoint+'_baseStretch_Loc'))[0]
    cmds.matchTransform(baseLoc, startJoint)
    cmds.parentConstraint(baseControl, baseLoc)
    endLoc = cmds.spaceLocator(n=(startJoint+'_endStretch_Loc'))[0]
    cmds.matchTransform(endLoc, ikControl)
    cmds.parentConstraint(ikControl, endLoc)
#get the list of joints under the start joint
    jointHierarchy = cmds.listRelatives(startJoint, type='joint', ad=True)
    jointHierarchy.append(startJoint)
    jointHierarchy.reverse()
    totalJoints = len(jointHierarchy)
    print('stretching %s joints' %(totalJoints))
    placeholderName = ikControl.replace('_Ctrl', '')
#check to make sure the end joint is the last in the heirarchy
    print(jointHierarchy)
    '''print(totalJointHierarchy[len(totalJointHierarchy)-1])
    print(endJoint)
    if totalJointHierarchy[len(totalJointHierarchy)-1] is not endJoint:
        cmds.error("end joint is not the end of the joint chain")
    print(totalJointHierarchy)'''
# add the total anatomical length of joint chain
    totalAnatomicalLengthPMANode = cmds.createNode('plusMinusAverage', n=placeholderName+'_Stretch_Total_Anatomical_Length_PMA')
    for i in range(totalJoints-1):
        currentPMALengthNode = cmds.createNode('plusMinusAverage', n=jointHierarchy[i+1]+'_Length_PMA')
        cmds.connectAttr((jointHierarchy[i+1] + '.translateX'), currentPMALengthNode+'.input1D[0]')
        cmds.connectAttr(currentPMALengthNode+'.output1D', (totalAnatomicalLengthPMANode + '.input1D['+str(i)+']') )
        cmds.disconnectAttr((jointHierarchy[i+1] + '.translateX'), currentPMALengthNode+'.input1D[0]')
# create a node that holds the distance between the locators
    distanceBetweenLocatorsNode = cmds.createNode('distanceBetween', n=placeholderName+'_Stretch_Locator_DistanceBetween')
    cmds.connectAttr(baseLoc+'.worldMatrix', distanceBetweenLocatorsNode+'.inMatrix1')
    cmds.connectAttr(endLoc+'.worldMatrix', distanceBetweenLocatorsNode+'.inMatrix2')
#create switch node
    stretchSwitchNode = cmds.createNode('multiplyDivide', n=placeholderName+'_Stretch_Switch_MD')
    cmds.connectAttr(ikControl+'.Stretch', stretchSwitchNode+'.input1X')
    cmds.connectAttr(distanceBetweenLocatorsNode+'.distance', stretchSwitchNode+'.input2X')
# create scalar node
    stretchsScalarNode = cmds.createNode('multiplyDivide', n=placeholderName+'_Stretch_Scalar_MD')
    cmds.setAttr(stretchsScalarNode+'.operation', 2)
    cmds.connectAttr(stretchSwitchNode+'.outputX', stretchsScalarNode+'.input1X')
    cmds.connectAttr(totalAnatomicalLengthPMANode+'.output1D', stretchsScalarNode+'.input2X')
# create clamp node for stretch
    stretchClampNode = cmds.createNode('clamp', n=placeholderName+'_Stretch_Clamp')
    cmds.setAttr(stretchClampNode+'.minR', 1)
    cmds.connectAttr(ikControl+'.Max_Stretch', stretchClampNode+'.maxR')
    cmds.connectAttr(stretchsScalarNode+".outputX", stretchClampNode+'.inputR')
# connect the scalar to each joint xtranslate with an MD for each joint
    for i in range(totalJoints - 1):
        currentMDNode = cmds.createNode('multiplyDivide', n=jointHierarchy[i+1]+'_Stretch_Scalar_MD')
        cmds.connectAttr(stretchClampNode+'.outputR', currentMDNode+'.input1X')
        cmds.connectAttr(jointHierarchy[i+1]+'_Length_PMA.output1D', currentMDNode+'.input2X')
        cmds.connectAttr(currentMDNode+'.outputX', jointHierarchy[i+1]+'.translateX')