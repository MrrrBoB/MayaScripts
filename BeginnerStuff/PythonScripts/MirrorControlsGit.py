import maya.cmds as cmds

theControls = cmds.ls(sl=1)
print(theControls)
controlGrps = [cmds.listRelatives(control, parent=1)[0] for control in theControls]
print(controlGrps)
newControlGrp = cmds.duplicate(controlGrps, rr=1)
mirrorGrp = cmds.group(newControlGrp, n='mirrorGrp', w=1)
cmds.xform(mirrorGrp, piv=(0, 0, 0))
cmds.xform(mirrorGrp, s=(-1, 1, 1))
#cmds.makeIdentity(mirrorGrp, a=1, s=1, jo=1)
for grp in newControlGrp:
    cmds.parent(grp, w=1)
cmds.delete(mirrorGrp)
fullControlGrp = cmds.listRelatives(newControlGrp, ad=1)



