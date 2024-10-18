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


def SquareControl(size, name):
    pnt = size * .5
    ctrl = cmds.curve(d=1, n=name, p=((pnt, 0, pnt),
                                      (pnt, 0, -pnt),
                                      (-pnt, 0, -pnt),
                                      (-pnt, 0, pnt),
                                      (pnt, 0, pnt)))

