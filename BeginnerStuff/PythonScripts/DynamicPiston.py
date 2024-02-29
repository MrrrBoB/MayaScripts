import maya.cmds as cmds


def CreatePiston(systemName, outVector, autoConstrainUpTarget, rotatingBase):
    sels = cmds.ls(sl=1)
    if len(sels) != 2:
        cmds.warning("please select the start and end attachment points")
        return
    housingLocator = sels[0]
    pistonLocator = sels[1]
    housingLocator = cmds.rename(housingLocator, systemName + '_Housing_Loc')
    pistonLocator = cmds.rename(pistonLocator, systemName + '_Piston_Loc')
    print(housingLocator + " pushes " + pistonLocator)

    # aim locators at eachother
    pistonUpLoc = cmds.duplicate(pistonLocator, n=pistonLocator + '_Up_Target')
    cmds.xform(pistonUpLoc, t=outVector, r=1, os=1)
    housingUpLoc = cmds.duplicate(housingLocator, n=housingLocator + '_Up_Target')
    cmds.xform(housingUpLoc, t=outVector, r=1, os=1)
    aimCon = cmds.aimConstraint(pistonLocator, housingLocator, wut='object', wuo=housingUpLoc[0], aim=(1, 0, 0),
                                u=outVector)
    cmds.delete(aimCon)
    aimCon = cmds.aimConstraint(housingLocator, pistonLocator, wut='object', wuo=pistonUpLoc[0], aim=(1, 0, 0),
                                u=outVector)
    cmds.delete(aimCon)
    cmds.select(cl=1)
    if (autoConstrainUpTarget):
        cmds.parentConstraint(pistonLocator, pistonUpLoc, mo=1)
        cmds.parentConstraint(housingLocator, housingUpLoc, mo=1)

    # piston Joints
    pistonJoint1 = cmds.joint(n=systemName + '_pistonJnt1')
    cmds.matchTransform(pistonJoint1, pistonLocator)
    pistonJoint2 = cmds.joint(n=systemName + '_pistonJnt2')
    pc = cmds.pointConstraint(pistonLocator, housingLocator, pistonJoint2, mo=0)
    cmds.delete(pc)
    cmds.setAttr(pistonJoint1 + '.rotateX', 180)
    cmds.makeIdentity(pistonJoint1, r=1, a=1)
    pistonIkHandle = \
    cmds.ikHandle(n=systemName + '_pistonIKHandle', sj=pistonJoint1, ee=pistonJoint2, sol='ikRPsolver')[0]
    cmds.select(cl=1)
    cmds.poleVectorConstraint(pistonUpLoc, pistonIkHandle)
    cmds.matchTransform(pistonIkHandle, housingLocator)
    cmds.parent(pistonIkHandle, housingLocator)
    cmds.pointConstraint(pistonLocator, pistonJoint1)

    # housing Joints
    cmds.select(cl=1)
    housingJoint1 = cmds.joint(n=systemName + '_housingJnt1')
    cmds.matchTransform(housingJoint1, housingLocator)
    housingJoint2 = cmds.joint(n=systemName + '_housingJnt2')
    pc = cmds.pointConstraint(housingLocator, pistonLocator, housingJoint2, mo=0)
    cmds.delete(pc)
    cmds.setAttr(housingJoint1 + '.rotateX', 180)
    cmds.makeIdentity(housingJoint1, r=1, a=1)
    housingIkHandle = \
        cmds.ikHandle(n=systemName + '_housingIKHandle', sj=housingJoint1, ee=housingJoint2, sol='ikRPsolver')[0]
    cmds.select(cl=1)
    cmds.poleVectorConstraint(housingUpLoc, housingIkHandle)
    cmds.matchTransform(housingIkHandle, pistonLocator)
    cmds.parent(housingIkHandle, pistonLocator)
    cmds.pointConstraint(housingLocator, housingJoint1)
    if rotatingBase:
        cmds.select(housingJoint1)
        baseJoint = cmds.joint(n=systemName + '_housingPivotJoint')
        cmds.aimConstraint(housingUpLoc, baseJoint, wut='object', wuo=pistonJoint1, aim=(0, -1, 0), u=(1, 0, 0))
        cmds.select(pistonJoint1)
        baseJoint = cmds.joint(n=systemName + '_pistonPivotJoint')
        cmds.aimConstraint(pistonUpLoc, baseJoint, wut='object', wuo=housingJoint1, aim=(0, -1, 0), u=(1, 0, 0))


CreatePiston("test2", (0, 1, 0), True, True)
