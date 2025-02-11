import maya.cmds as cmds
import sys
sys.path.append('F:\SchoolMore\pythonProject\Rigging Toolkit')
import AutoRigger as AR


alreadyOriented = False


def createARWindow():
    if cmds.window("AutoRiggerWindow", exists=True):
        cmds.deleteUI("AutoRiggerWindow")
    cmds.showWindow(AutoRiggerWindow)


AutoRiggerWindow = cmds.window(title="Rigging Toolkit", widthHeight=(600, 300))
parentColumn = cmds.columnLayout(adjustableColumn=1, rowSpacing=10)
line1RowLayout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine1 = cmds.text(label='1. Create Height Locators.', al='left')
locatorButton = cmds.button(label='CreateLocators', command='AR.CreateHeightLocators()', al='right')
cmds.setParent('..')
instructionLine2 = cmds.text(l='2. Place the base locator at the base of the character, and the top locator on '
                               'top of the head',
                             al='left')
cmds.setParent('..')
line3Layout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine3 = cmds.text(l='3. Create skeleton template', al='left')
createTemplateButton = cmds.button(l='Create Joint Template', command='LayoutCommand()')
cmds.setParent('..')
instructionLine4 = cmds.text(l='4. Move joints to match your character. Fingers must be oriented manually', al='left')
line5Layout = cmds.rowLayout(numberOfColumns=3, columnAlign=(1, 'right'))
instructionLine5 = cmds.text(l='5. Orient and mirror skeleton')
orientButton = cmds.button(l='Orient', command='OrientButton()', w=100)
mirrorButton = cmds.button(l='Mirror', command='MirrorButton()', w=100)
cmds.setParent('..')
instructionLine6 = cmds.text(l='6. Check your skeleton. Make sure all joints are oriented correctly (double check '
                               'fingers)',
                             al='left')
line7Layout = cmds.rowLayout(numberOfColumns=2, columnAlign=(1, 'right'))
instructionLine7 = cmds.text(l='7. Rig it!', al='left')
rigButton = cmds.button(l='RIG', command='RigSimpleButton()', w=100)


def LayoutCommand():
    AR.InitializeHeirarchy()
    AR.CreateHumanoidSkeletonTemplate()


def OrientButton():
    AR.OrientSkeleton()


def RigSimpleButton():
    AR.ImplementIKFK()
    AR.IKControls()
    AR.FKControls()
    AR.HeadCtrls()
    AR.HybridHands()
    AR.MetaControls()
    AR.SpaceSwapIK()
    AR.IKLimbStretch()
    AR.TwistJoints()
    AR.FixSegmentScaleCompensate()
    AR.RibbonJoints()


def MirrorButton():
    AR.MirrorJoints(0)

createARWindow()