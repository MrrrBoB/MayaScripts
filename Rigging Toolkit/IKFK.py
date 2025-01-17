import maya.cmds as cmds


def autoLimbTool(startJoint, nameSet, numJointsSet, yesCreateHandle, transformControl, duplicateWholeJointChain):
    # SetupVariables from ui
    # is this front or rear
    isRearLeg = 1
    # how many joints?
    limbJoints = numJointsSet
    # checks selection is valid
    selectionCheck = cmds.ls(sl=True, type='joint')
    # no joints selected:
    if startJoint == '':
        if not selectionCheck:
            cmds.error("Please select a root joint")
        else:
            rootJoint = cmds.ls(sl=True, type='joint')[0]
            print(rootJoint)
    else:
        if not cmds.objExists(startJoint):
            cmds.error("The Specified joint %s could not be found when trying to implement IKFK")
        else:
            rootJoint = startJoint

    # check if root joint has parent


    # check transform control exists
    # check which side
    '''whichSide = rootJoint[0:2]
    if not 'L_' in whichSide:
        if not 'R_' in whichSide:
            cmds.error('Missing prefix L_ or R_')'''
    # build names
    #limbName = whichSide + limbType + '_limb'
    limbName = nameSet
    print(limbName)
    # with root joint selected, find and save the hierarchy
    originalJointHierarchy = cmds.listRelatives(rootJoint, ad=True)
    # list is backwards, add rootJoint to the end of the list
    originalJointHierarchy.append(rootJoint)
    # now reverse it
    originalJointHierarchy.reverse()
    cmds.select(cl=True)
    # duplicate the joint chain
    newJointTypeList = ['_IK', '_FK']
    '''if isRearLeg:
        newJointTypeList.append("_Driver")'''
    # build chains
    if not duplicateWholeJointChain:
        for newJoint in newJointTypeList:
            for i in range(limbJoints):
                newJointName = originalJointHierarchy[i] + newJoint
                cmds.joint(name=newJointName)
                cmds.matchTransform(newJointName, originalJointHierarchy[i])
                cmds.makeIdentity(newJointName, a=True, r=True)
            cmds.select(clear=True)
    else:
        for type in newJointTypeList:
            newRootJoint = cmds.duplicate(rootJoint, rc=True)[0]
            newJointHierarchy = cmds.listRelatives(newRootJoint, ad=True)
            newJointHierarchy.append(newRootJoint)
            newJointHierarchy.reverse()
            for i in range(len(originalJointHierarchy)):
                cmds.rename(newJointHierarchy[i], originalJointHierarchy[i] + type)
            print ('new '+ type)
            print(newJointHierarchy)

    # ---------------------------------------------------------------------------
    # Joint Chains have been created, now constrain IK and FK to the main so a switch can be created
    if not duplicateWholeJointChain:
        for i in range(limbJoints):
            cmds.parentConstraint((originalJointHierarchy[i] + '_IK'), (originalJointHierarchy[i] + '_FK'),
                                  originalJointHierarchy[i], w=1, mo=0)
            cmds.scaleConstraint((originalJointHierarchy[i] + '_IK'), (originalJointHierarchy[i] + '_FK'),
                                  originalJointHierarchy[i], w=1, mo=0)
    else:
        for i in range(len(originalJointHierarchy)):
            cmds.parentConstraint((originalJointHierarchy[i] + '_IK'), (originalJointHierarchy[i] + '_FK'),
                                  originalJointHierarchy[i], w=1, mo=0)
            cmds.scaleConstraint((originalJointHierarchy[i] + '_IK'), (originalJointHierarchy[i] + '_FK'),
                                  originalJointHierarchy[i], w=1, mo=0)
    # unlock drawing override for root chain
    cmds.setAttr(originalJointHierarchy[0] + ".overrideEnabled", 1)
    # unlock drawing overrides for each created chain
    for i in range(len(newJointTypeList)):
        cmds.setAttr(originalJointHierarchy[0] + newJointTypeList[i] + '.overrideEnabled', 1)
    # Set the color of each joint chain
    cmds.setAttr(originalJointHierarchy[0] + "_IK.overrideColor", 13)
    cmds.setAttr(originalJointHierarchy[0] + "_FK.overrideColor", 6)
    cmds.setAttr(originalJointHierarchy[0] + ".overrideColor", 14)
    # add IK handle to the IK chain
    if yesCreateHandle and not duplicateWholeJointChain:
        cmds.ikHandle(n=(limbName + "_IK_Handle"), sol="ikRPsolver", sj=originalJointHierarchy[0] + '_IK',
                      ee=(originalJointHierarchy[limbJoints - 1] + '_IK'))
    # create a switch attribute to the transform control
    cmds.addAttr(transformControl, longName=(limbName + '_IKFK'), attributeType='float', defaultValue=0, maxValue=1,
                 minValue=0, keyable=True)
    ikfkSwitchAttr = (transformControl + '.' + limbName + '_IKFK')
    # create reverse node for switch
    ikfkReverseNode = cmds.createNode('reverse', n=(limbName + '_IKFK_Reverse'))
    ikfkReverseOutPut = (ikfkReverseNode + '.outputX')
    # connect the switch to the reverse node
    cmds.connectAttr(ikfkSwitchAttr, (ikfkReverseNode + '.inputX'), f=True)
# assign the IKFK Switch to the transform control and assign values
    if not duplicateWholeJointChain:
        for i in range(limbJoints):
            getParentConstraint = cmds.listConnections(originalJointHierarchy[i], type='parentConstraint')[0]
            getScaleConstraint = cmds.listConnections(originalJointHierarchy[i], type='scaleConstraint')[0]
            getParentWeights = cmds.parentConstraint(getParentConstraint, q=True, wal=1)
            getScaleWeights = cmds.scaleConstraint(getScaleConstraint, q=1, wal=2)
            cmds.connectAttr(ikfkSwitchAttr, (getParentConstraint + '.' + getParentWeights[1]), f=1)
            cmds.connectAttr(ikfkReverseOutPut, (getParentConstraint + '.' + getParentWeights[0]), f=1)
            cmds.connectAttr(ikfkSwitchAttr, (getScaleConstraint + '.' + getScaleWeights[1]), f=1)
            cmds.connectAttr(ikfkReverseOutPut, (getScaleConstraint + '.' + getScaleWeights[0]), f=1)
    else:
        for i in range(len(originalJointHierarchy)):
            getParentConstraint = cmds.listConnections(originalJointHierarchy[i], type='parentConstraint')[0]
            getScaleConstraint = cmds.listConnections(originalJointHierarchy[i], type='scaleConstraint')[0]
            getParentWeights = cmds.parentConstraint(getParentConstraint, q=True, wal=1)
            getScaleWeights = cmds.scaleConstraint(getScaleConstraint, q=1, wal=2)
            cmds.connectAttr(ikfkSwitchAttr, (getParentConstraint + '.' + getParentWeights[1]), f=1)
            cmds.connectAttr(ikfkReverseOutPut, (getParentConstraint + '.' + getParentWeights[0]), f=1)
            cmds.connectAttr(ikfkSwitchAttr, (getScaleConstraint + '.' + getScaleWeights[1]), f=1)
            cmds.connectAttr(ikfkReverseOutPut, (getScaleConstraint + '.' + getScaleWeights[0]), f=1)
# checks if the root joint has a parent, and if so, parents the created chains to the parent
    parentJointCheck = cmds.listRelatives(rootJoint, p=True)
    if (not parentJointCheck) or duplicateWholeJointChain:
        hasParent = False
    else:
        hasParent = True
        hierarchyParent = parentJointCheck
        for i in range(len(newJointTypeList)):
            cmds.parent((originalJointHierarchy[0]+newJointTypeList[i]), hierarchyParent)


# Make stretchy





