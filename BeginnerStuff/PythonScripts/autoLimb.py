import maya.cmds as cmds


def autoLimbTool():
    # SetupVariables from ui
    # is this front or rear
    isRearLeg = 1
    # how many joints?
    limbJoints = 4
    if isRearLeg:
        limbType = "rear"
    else:
        limbType = "front"
    # checks selection is valid
    selectionCheck = cmds.ls(sl=True, type='joint')
    # no joints selected:
    if not selectionCheck:
        cmds.error("Please select a root joint")
    else:
        rootJoint = cmds.ls(sl=True, type='joint')[0]
        print(rootJoint)
    # check which side
    whichSide = rootJoint[0:2]
    if not 'L_' in whichSide:
        if not 'R_' in whichSide:
            cmds.error('Missing prefix L_ or R_')
    # build names
    limbName = whichSide + limbType + '_limb'
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
            print(newJointName)
            cmds.joint(name=newJointName)
            cmds.matchTransform(newJointName, originalJointHierarchy[i])
            cmds.makeIdentity(newJointName, a=True, r=True)
        cmds.select(clear=True)

    # ---------------------------------------------------------------------------
    # Joint Chains have been created, now constrain IK and FK to the main so a switch can be created
    for i in range(limbJoints):
        cmds.parentConstraint((originalJointHierarchy[i]+'_IK'), (originalJointHierarchy[i]+'_FK'), originalJointHierarchy[i], w=1, mo=0)
    # unlock drawing override for root chain
    cmds.setAttr(originalJointHierarchy[0]+".overrideEnabled", 1)
    # unlock drawing overrides for each created chain
    for i in range(len(newJointTypeList)):
        cmds.setAttr(originalJointHierarchy[0]+newJointTypeList[i]+'.overrideEnabled', 1)
    # Set the color of each joint chain
    cmds.setAttr(originalJointHierarchy[0]+"_IK.overrideColor", 13)
    cmds.setAttr(originalJointHierarchy[0] + "_FK.overrideColor", 6)
    cmds.setAttr(originalJointHierarchy[0] + ".overrideColor", 14)
    # add IK handle to the IK chain
    cmds.ikHandle(n=(limbName+"_IKHandle"), sol="ikRPsolver", sj=originalJointHierarchy[0]+'_IK', ee=(originalJointHierarchy[limbJoints-1]+'_IK'))
autoLimbTool()
# import autoLimb
# reload(autoLimb)
# autoLimb.autoLimbTool()
