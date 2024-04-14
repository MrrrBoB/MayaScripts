import maya.cmds as cmds


def createJoints(numJoints, createIk):
    print("creating joints")
    theCurve = cmds.ls(sl=1)[0]
    cmds.select(cl=1)
    jointList =[]
    for i in range(numJoints):
        currentDistanceAlongCurve = i/(numJoints-1)
        currentLocation = cmds.pointOnCurve(theCurve, pr=currentDistanceAlongCurve)
        print(currentLocation)
        jointList.append(cmds.joint(p=currentLocation, n=theCurve+'_joint'+str(i+1)))
    cmds.joint(jointList[0], e=1, zso=1, oj='xyz', sao='yup', ch=1)
    cmds.joint(jointList[len(jointList)-1], e=1, oj='none')
    print(jointList)
    if createIk:
        splineHandle = cmds.ikHandle(
            sol='ikSplineSolver',
            ccv=0,
            roc=0,
            pcv=0,
            c=theCurve,
            sj=jointList[0],
            ee=jointList[len(jointList)-1],
            n=theCurve+'_IkSplineHandle'
            )[0]
        cmds.setAttr(splineHandle+'.visibility', 0)






def createCurveJointChainWindow():
    if cmds.window("ltWindow", exists=True):
        cmds.deleteUI("ltWindow")
    cmds.showWindow(cjcWindow)


cjcWindow = cmds.window(title="Add Joints To Curve", widthHeight=(200, 75))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5, cal='center')
cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
cmds.text(l="Number of joints")
numJointsField = cmds.intField(min=3, dv=3)
cmds.setParent('..')
ikCheckBox = cmds.checkBox(l='Create IK Spline')
cmds.button(l="Create Joints",
            c='ButtonCommand()')


def ButtonCommand():
    createJoints(cmds.intField(numJointsField, q=1, v=1),cmds.checkBox(ikCheckBox, q=1, v=1))


createCurveJointChainWindow()