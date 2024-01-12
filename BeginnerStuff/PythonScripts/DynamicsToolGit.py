import maya.cmds as cmds


def MakeExistingCurveDynamic(existingCurve, attributeHandle):
    cmds.duplicate(existingCurve, n=existingCurve + " dynamicDuplicate")


def createDynamicsWindow():
    if cmds.window("dynamicsWindow", exists=True):
        cmds.deleteUI("dynamicsWindow")
    cmds.showWindow(dynamicsWindow)


dynamicsWindow = cmds.window(title="Dynamic Curves", widthHeight=(400, 225))
cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
cmds.rowLayout(numberOfColumns=1, columnAlign=(1, 'right'))
useExistingInputBox = cmds.checkBox(label='Use existing spline curve', v=1, ofc='existingCheckboxOn(0)', onc='existingCheckboxOn(1)')
cmds.setParent('..')
existingCurveRow = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Curve')
curveField = cmds.textField(placeholderText='eg. spline_Curve', w=200)
cmds.button(label='GetSelection', command='getCurve()')
cmds.setParent('..')
nonExistingCurveRow = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'), vis=0)
cmds.text(label='First joint in chain')
cmds.textField(placeholderText='eg. IK_Spline_01_Jnt')
cmds.button(label='Get Selection', command='getJoint()')
cmds.setParent('..')
cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
cmds.text(label='Attribute Control')
cmds.textField(placeholderText='eg. spline_IK_Handle')
cmds.button(label='Get Selection', command='getControl')
cmds.setParent('..')
cmds.button(label='create', command='makeDynamicButtonCmd')


createDynamicsWindow()


def getCurve():
    return 1


def getJoint():
    return 1


def getControl():
    return 1


def makeDynamicButtonCmd():
    return 1


def existingCheckboxOn(value):
    cmds.rowLayout(existingCurveRow, e=1, vis=value)
    cmds.rowLayout(nonExistingCurveRow, e=1, vis=not value)


