import maya.cmds as cmds

# create a spline starting at a certain joint through ALL the joints down the chain
def CreateSplineFromJoints(firstJoint, name, degree):
    jointList = cmds.listRelatives(firstJoint, ad=True)
    jointList.append(firstJoint)
    jointList.reverse()
    jointPositions = [cmds.xform(joint, q=1, t=1, ws=1) for joint in jointList]
    newCurve = cmds.curve(n=name, ep=jointPositions, d=degree)
    splineHandle = cmds.ikHandle(n=firstJoint + "_Spline_IK_Handle",
                                 sol='ikSplineSolver',
                                 sj=firstJoint,
                                 ee=jointList[len(jointList) - 1],
                                 c=newCurve,
                                 ccv=0,
                                 roc=0,
                                 pcv=0)
    return newCurve

# create a spline starting at a certain joint through A CERTAIN NUMBER of joints down the chain
def CreateSplineFromJoint(firstJoint, name, numJoints, degree=3):
    jointList = cmds.listRelatives(firstJoint, ad=1)
    jointList.append(firstJoint)
    jointList.reverse()
    newJointList = [jointList[i] for i in range(numJoints)]
    jointPositions = [cmds.xform(joint, q=1, t=1, ws=1) for joint in newJointList]
    newCurve = cmds.curve(n=name+'_Curve', ep=jointPositions, d=degree)
    splineHandle = cmds.ikHandle(n=name + "_Spline_IK_Handle",
                                 sol='ikSplineSolver',
                                 sj=firstJoint,
                                 ee=newJointList[len(newJointList) - 1],
                                 c=newCurve,
                                 ccv=0,
                                 roc=0,
                                 pcv=0)
    return newCurve
