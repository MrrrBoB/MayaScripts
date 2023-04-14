import maya.cmds as cmds


def autoLimbTool(nameSet, numJointsSet, yesCreateHandle):
    # SetupVariables from ui
    # is this front or rear
    isRearLeg = 1
    # how many joints?
    limbJoints = numJointsSet
    # checks selection is valid
    selectionCheck = cmds.ls(sl=True, type='joint')
    # no joints selected:
    if not selectionCheck:
        cmds.error("Please select a root joint")
    else:
        rootJoint = cmds.ls(sl=True, type='joint')[0]
        print(rootJoint)
    # check if root joint has parent
    parentJointCheck = cmds.listRelatives(rootJoint, p=True)
    if not parentJointCheck:
        hasParent = False
    else:
        hasParent = True
        hierarchyParent = parentJointCheck
        print (hierarchyParent)
    print(hasParent)

    # check transform control exists
    if not cmds.ls("Transform_Ctrl"):
        cmds.error('No "Transform_Ctrl" to assign switch to')
    else:
        transformControl = cmds.ls("Transform_Ctrl")[0]
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
    newJointTypeList = ['_IK', '_FK', '_Stretch']
    if isRearLeg:
        newJointTypeList.append("_Driver")
    # build chains
    for newJoint in newJointTypeList:
        for i in range(limbJoints):
            newJointName = originalJointHierarchy[i] + newJoint
            cmds.joint(name=newJointName)
            cmds.matchTransform(newJointName, originalJointHierarchy[i])
            cmds.makeIdentity(newJointName, a=True, r=True)
        cmds.select(clear=True)

    # ---------------------------------------------------------------------------
    # Joint Chains have been created, now constrain IK and FK to the main so a switch can be created
    for i in range(limbJoints):
        cmds.parentConstraint((originalJointHierarchy[i] + '_IK'), (originalJointHierarchy[i] + '_FK'),
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
    if yesCreateHandle:
        cmds.ikHandle(n=(limbName + "_IKHandle"), sol="ikRPsolver", sj=originalJointHierarchy[0] + '_IK',
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

    for i in range(limbJoints):
        getConstraint = cmds.listConnections(originalJointHierarchy[i], type='parentConstraint')[0]
        getWeights = cmds.parentConstraint(getConstraint, q=True, wal=1)
        cmds.connectAttr(ikfkSwitchAttr, (getConstraint + '.' + getWeights[1]), f=1)
        cmds.connectAttr(ikfkReverseOutPut, (getConstraint + '.' + getWeights[0]), f=1)
    if hasParent:
        for i in range(len(newJointTypeList)):
            print((originalJointHierarchy[0]+newJointTypeList[i]))
            cmds.parent((originalJointHierarchy[0]+newJointTypeList[i]), hierarchyParent)


def buttonCommand():
    chosenName = cmds.textField(chainNameField, q=True, text=True)
    chosenName = chosenName.replace(" ", "_")
    chosenNumJoints = cmds.intField(numJointsField, q=True, value=True)
    handleChoice = cmds.checkBox(ikHandleCheckbox, q=True, value=True)
    autoLimbTool(chosenName, chosenNumJoints, handleChoice)


def AutoLimbUI():
    if cmds.window("aLWindow", exists=True):
        cmds.deleteUI("aLWindow")
    cmds.showWindow(aLWindow)


aLWindow = cmds.window(title="Create RK System", widthHeight=(500, 200))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, "right"))
cmds.text(label='Limb/Chain name:')
chainNameField = cmds.textField(placeholderText='ex:RearLeftLeg')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=2)
cmds.text(label='Number of joints in limb/chain')
numJointsField = cmds.intField()
cmds.setParent('..')
ikHandleCheckbox = cmds.checkBox(label='Create IK Handle')
cmds.button(label='Create RK System', command='buttonCommand()')

AutoLimbUI()
# import autoLimb
# reload(autoLimb)
# autoLimb.autoLimbTool()
