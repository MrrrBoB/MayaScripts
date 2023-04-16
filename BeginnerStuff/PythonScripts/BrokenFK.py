import maya.cmds as cmds

sels = cmds.ls(sl=True)
parentControl = sels[0]
childControl = sels[1]

childCtrlGrp = cmds.listRelatives(childControl, parent=True)[0]
pConstraint1 = cmds.parentConstraint(parentControl, childCtrlGrp, mo=True, skipRotate=['x', 'y', 'z'], weight=1)[0]#Translate Constraint
pConstraint2 = cmds.parentConstraint(parentControl, childCtrlGrp, mo=True, skipTranslate=['x', 'y', 'z'], weight=1)[0]#Rotate Constraint
sContstraint = cmds.scaleConstraint(parentControl, childCtrlGrp, weight=1)

cmds.addAttr(childControl, ln="FollowTranslate", at='double', min=0, max=1, dv=1, k=True)
cmds.addAttr(childControl, ln="FollowRotate", at='double', min=0, max=1, dv=1, k=True)

cmds.connectAttr('%s.FollowTranslate' % (childControl), '%s.w0' % (pConstraint1), f=True)
cmds.connectAttr('%s.FollowRotate' % (childControl), '%s.w0' % (pConstraint2), f=True)

