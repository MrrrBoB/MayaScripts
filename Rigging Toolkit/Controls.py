import maya.cmds as cmds


def createControl(target, controlName, radiusSize, ctrlColor, axis, constrainJoint):
    myControl = cmds.circle(radius=radiusSize, name=controlName + "_Ctrl")[0]
    controlShapeNode = cmds.listRelatives(myControl, shapes=True)[0]
    cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
    cmds.setAttr(str(controlShapeNode) + ".overrideColor", ctrlColor)
    controlGroup = cmds.group(myControl, name=controlName + "_Ctrl_Grp")
    if target == "world":
        constrainJoint = False
    else:
        cmds.matchTransform(controlGroup, target)
    if axis == 1:
        cmds.xform(myControl, ro=(90, 0, 0))
    elif axis == 0:
        cmds.xform(myControl, ro=(0, 90, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    if constrainJoint:
        cmds.parentConstraint(myControl, target)
        cmds.scaleConstraint(myControl, target)
    return myControl


def createWorldRotationControl(target, controlName, radiusSize, ctrlColor, axis, constrainJoint, worldRotation):
    myControl = cmds.circle(radius=radiusSize, name=controlName + "_Ctrl")[0]
    controlShapeNode = cmds.listRelatives(myControl, shapes=True)[0]
    cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
    cmds.setAttr(str(controlShapeNode) + ".overrideColor", ctrlColor)
    controlGroup = cmds.group(myControl, name=controlName + "_Ctrl_Grp")
    if target == "world":
        constrainJoint = False
    elif not worldRotation:
        cmds.matchTransform(controlGroup, target)
    else:
        cmds.matchTransform(controlGroup, target, pos=1)
    if axis == 1:
        cmds.xform(myControl, ro=(90, 0, 0))
    elif axis == 0:
        cmds.xform(myControl, ro=(0, 90, 0))
    cmds.makeIdentity(myControl, apply=True, rotate=True)
    if constrainJoint:
        cmds.parentConstraint(myControl, target, mo=1)
        cmds.scaleConstraint(myControl, target, mo=1)
    return myControl


def SquareControl(size, name):
    pnt = size * .5
    ctrl = cmds.curve(d=1, n=name, p=((pnt, 0, pnt),
                                      (pnt, 0, -pnt),
                                      (-pnt, 0, -pnt),
                                      (-pnt, 0, pnt),
                                      (pnt, 0, pnt)))


def MirrorControls():
    theControls = cmds.ls(sl=1)
    controlGrps = [cmds.listRelatives(control, parent=1)[0] for control in theControls]
    newControlGrp = cmds.duplicate(controlGrps, rr=1)
    mirrorGrp = cmds.group(newControlGrp, n='mirrorGrp', w=1)
    cmds.xform(mirrorGrp, piv=(0, 0, 0))
    cmds.xform(mirrorGrp, s=(-1, 1, 1))
    endCtrlGrp = []
    for grp in newControlGrp:
        cmds.parent(grp, w=1)
        newControlsFull = cmds.listRelatives(newControlGrp, c=1, f=1)
        newControlsShort = cmds.listRelatives(newControlGrp, c=1, f=0)
        endCtrlGrp.append(grp)
    print(endCtrlGrp)
    cmds.delete(mirrorGrp)