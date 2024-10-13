import maya.cmds as cmds


def CreateSplineFromJoints(firstJoint):
    jointList = cmds.listRelatives(firstJoint, ad=True)
    jointList.append(firstJoint)
    jointList.reverse()
    jointPositions = [cmds.xform(joint, q=1, t=1, ws=1) for joint in jointList]
    newCurve = cmds.curve(n=firstJoint + "_Curve", ep=jointPositions, d=3)
    splineHandle = cmds.ikHandle(n=firstJoint + "_Spline_IK_Handle",
                                 sol='ikSplineSolver',
                                 sj=firstJoint,
                                 ee=jointList[len(jointList) - 1],
                                 c=newCurve,
                                 ccv=0,
                                 roc=0,
                                 pcv=0)
    return newCurve