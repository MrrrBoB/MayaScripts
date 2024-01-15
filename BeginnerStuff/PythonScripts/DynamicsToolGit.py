import maya.cmds as cmds
import maya.mel as mel


def MakeExistingCurveDynamic(existingCurve, attributeHandle):
    systemName = 'placeholder'
    print('called successfully')
    duplicatedCurve = cmds.duplicate(existingCurve, n='%s_Dynamic Duplicate' % existingCurve)
    cmds.select(duplicatedCurve)
    mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')
    hairSystem = 'hairSystem1'
    nucleus = 'nucleus1'
    simulationCurve = 'curve1'
    follicle = 'follicle1'
    cmds.select(follicle, r=1)
    cmds.select(duplicatedCurve, add=1)
    cmds.select(simulationCurve, add=1)
    cmds.parent(w=1)
    follicle = cmds.rename(follicle, '%s_Follicle' % systemName)
    simulationCurve = cmds.rename(simulationCurve, '%s_Simulation_Curve' % systemName)
    hairSystem = cmds.rename(hairSystem, '%s_Hair_System' % systemName)
    follicleShape = cmds.listRelatives(follicle, s=1)
    hairShape = cmds.listRelatives(hairSystem, s=1)[0]
    cmds.setAttr('%s.pointLock' % follicleShape[0], 1)
    dynamicBSNode = cmds.blendShape(simulationCurve, existingCurve)[0]
    cmds.addAttr(attributeHandle, ln='Simulation', at='float', min=0, max=1, dv=0, k=1)
    cmds.addAttr(attributeHandle, ln = 'Drag', at='float', min=0, max=10, dv=0, k=1)
    cmds.addAttr(attributeHandle, ln='Pose_Attract', at='float', min=0, max=1, dv=0, k=1)
    cmds.addAttr(attributeHandle, ln='Turbulence', at='float', min=0, max=1, dv=0, k=1)
    cmds.connectAttr(attributeHandle+'.Simulation', dynamicBSNode+'.'+simulationCurve)
    cmds.connectAttr(attributeHandle+'.Drag', hairShape+".drag")
    cmds.connectAttr(attributeHandle+'.Pose_Attract', hairShape+'.startCurveAttract')
    cmds.connectAttr(attributeHandle+'.Turbulence', hairShape+'.turbulenceStrength')
    # create control joints
    # bind to existing curve and duplicate curve


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


def createDynamicsWindow():
    if cmds.window("dynamicsWindow", exists=True):
        cmds.deleteUI("dynamicsWindow")
    cmds.showWindow(dynamicsWindow)


dynamicsWindow = cmds.window(title="Dynamic Curves", widthHeight=(400, 225))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=1, columnAlign=(1, 'right'))
useExistingInputBox = cmds.checkBox(label='Use existing spline curve', v=0, ofc='existingCheckboxOn(0)',
                                    onc='existingCheckboxOn(1)')
cmds.setParent('..')
existingCurveRow = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'), vis=0)
cmds.text(label='Curve')
curveField = cmds.textField(placeholderText='eg. spline_Curve', w=200)
cmds.button(label='GetSelection', command='getCurve()')
cmds.setParent('..')
nonExistingCurveRow = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'), vis=1)
cmds.text(label='First joint in chain')
firstJointField = cmds.textField(placeholderText='eg. IK_Spline_01_Jnt')
cmds.button(label='Get Selection', command='getJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Attribute Control')
controlField = cmds.textField(placeholderText='eg. spline_IK_Handle_Ctrl')
cmds.button(label='Get Selection', command='getControl()')
cmds.setParent('..')
cmds.button(label='create', command='makeDynamicButtonCmd()')

createDynamicsWindow()


def getCurve():
    cmds.textField(curveField, e=1, tx=cmds.ls(sl=1)[0])


def getJoint():
    cmds.textField(firstJointField, e=1, tx=cmds.ls(sl=1)[0])


def getControl():
    cmds.textField(controlField, e=1, tx=cmds.ls(sl=1)[0])


def existingCheckboxOn(value):
    cmds.rowLayout(existingCurveRow, e=1, vis=value)
    cmds.rowLayout(nonExistingCurveRow, e=1, vis=not value)


def makeDynamicButtonCmd():
    print('using existing curve')
    if cmds.checkBox(useExistingInputBox, q=1, v=1):
        if cmds.textField(curveField, q=1, tx=1) == '' or cmds.textField(controlField, q=1, tx=1) == '':
            cmds.warning('Please fill empty fields')
        else:
            MakeExistingCurveDynamic(cmds.textField(curveField, q=1, tx=1), cmds.textField(controlField, q=1, tx=1))
    elif cmds.textField(firstJointField, q=1, tx=1) == '' or cmds.textField(controlField, q=1, tx=1) == '':
        cmds.warning('Please fill empty fields')
    else:
        MakeExistingCurveDynamic(CreateSplineFromJoints(cmds.textField(firstJointField, q=1, text=1)),
                                 cmds.textField(controlField, q=1, text=1))
