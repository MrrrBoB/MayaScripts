import maya.cmds as cmds


def CreateLocators(name):
    locatorList = [cmds.spaceLocator(n=name + '_Reverse_Foot_Heel_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Toe_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Outer_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Inner_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Ball_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Ankle_Locator')[0]]
    return locatorList


def CreateLocators(name, localScale):
    locatorList = [cmds.spaceLocator(n=name + '_Reverse_Foot_Heel_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Toe_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Outer_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Inner_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Ball_Locator')[0],
                   cmds.spaceLocator(n=name + '_Reverse_Foot_Ankle_Locator')[0]]
    for l in locatorList:
        cmds.setAttr(l + 'Shape.localScaleX', localScale)
        cmds.setAttr(l + 'Shape.localScaleY', localScale)
        cmds.setAttr(l + 'Shape.localScaleZ', localScale)
    return locatorList


def CreateReverseFootSystem(systemName, controlSize):
    print('Creating ' + systemName + ' reverse foot system')
    heelLocator = systemName + '_Reverse_Foot_Heel_Locator'
    toeLocator = systemName + '_Reverse_Foot_Toe_Locator'
    outerLocator = systemName + '_Reverse_Foot_Outer_Locator'
    innerLocator = systemName + '_Reverse_Foot_Inner_Locator'
    ballLocator = systemName + '_Reverse_Foot_Ball_Locator'
    ankleLocator = systemName + '_Reverse_Foot_Ankle_Locator'
    locatorList = [outerLocator, innerLocator, heelLocator, toeLocator, ballLocator, ankleLocator]
    controlList = []
    numItems = len(locatorList)
    for i in range(numItems):
        currentCtrl = cmds.circle(name=locatorList[i].replace('_Locator', '_Ctrl'), r=controlSize,
                                  nr=(0, 1, 0))[0]
        controlList.append(currentCtrl)
        currentCtrlGrp = cmds.group(currentCtrl, n=currentCtrl + '_Grp')
        cmds.matchTransform(currentCtrlGrp, locatorList[i])
    for i in range(numItems - 1):
        childCtrl = controlList[i + 1]
        childCtrlGrp = cmds.listRelatives(childCtrl, parent=1)[0]
        cmds.parent(childCtrlGrp, controlList[i])
    for ctrl in controlList:
        controlShapeNode = cmds.listRelatives(ctrl, s=1)[0]
        cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
        cmds.setAttr(str(controlShapeNode) + ".overrideColor", 13)
    for locator in locatorList:
        cmds.delete(locator)
    toeTapCtrl = cmds.duplicate(systemName + '_Reverse_Foot_Ball_Ctrl', n=systemName + '_Reverse_Foot_ToeTap_Ctrl')
    cmds.delete('%s_Reverse_Foot_ToeTap_Ctrl|%s_Reverse_Foot_Ankle_Ctrl_Grp' % (systemName, systemName))
    cmds.xform(toeTapCtrl, ro=(90, 0, 0))
    cmds.makeIdentity(toeTapCtrl, r=1, a=1)
    return controlList


def InsertOffsetGroup(target, offsetName):
    theGroup = cmds.group(target, n=target + '_' + offsetName, em=1, w=1)
    targetParent = cmds.listRelatives(target, p=1)[0]
    cmds.matchTransform(theGroup, targetParent, pos=1)
    cmds.parent(theGroup, targetParent)
    cmds.makeIdentity(t=1, r=1, s=1, a=1)
    cmds.parent(target, theGroup)
    return theGroup


def AddRollControls(mainControl, systemName):
    print('adding roll controls to ' + mainControl)
    cmds.addAttr(mainControl, at='enum', nn='____________', ln='FootRollDivider', en='IK_FOOT', k=1)
    # Outwards Tilt
    cmds.addAttr(mainControl, at='double', ln='Tilt', min=-10, max=10, dv=0, k=1)
    tiltOutOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Outer_Ctrl', 'TiltOutOFFSET')
    tiltInOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Inner_Ctrl', 'TiltInOFFSET')
    cmds.setDrivenKeyframe(tiltOutOffsetGrp, cd=mainControl + '.Tilt', dv=0, at='.rotateZ', v=0)
    cmds.setDrivenKeyframe(tiltInOffsetGrp, cd=mainControl + '.Tilt', dv=0, at='.rotateZ', v=0)
    cmds.setDrivenKeyframe(tiltOutOffsetGrp, cd=mainControl + '.Tilt', dv=10, at='.rotateZ', v=-90)
    cmds.setDrivenKeyframe(tiltInOffsetGrp, cd=mainControl + '.Tilt', dv=-10, at='.rotateZ', v=90)
    # Foot Pitch
    cmds.addAttr(mainControl, at='double', ln='Pitch', min=-10, max=10, dv=0, k=1)
    pitchForwardOutOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Toe_Ctrl', 'PitchForwardOFFSET')
    pitchBackwardOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Heel_Ctrl', 'PitchBackwardOFFSET')
    cmds.setDrivenKeyframe(pitchForwardOutOffsetGrp, cd=mainControl + '.Pitch', dv=0, at='.rx', v=0)
    cmds.setDrivenKeyframe(pitchBackwardOffsetGrp, cd=mainControl + '.Pitch', dv=0, at='.rx', v=0)
    cmds.setDrivenKeyframe(pitchForwardOutOffsetGrp, cd=mainControl + '.Pitch', dv=10, at='.rx', v=80)
    cmds.setDrivenKeyframe(pitchBackwardOffsetGrp, cd=mainControl + '.Pitch', dv=-10, at='.rx', v=-80)
    # Heel Pivot
    cmds.addAttr(mainControl, at='double', ln='Heel_Pivot', min=-10, max=10, dv=0, k=1)
    thisOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Heel_Ctrl', 'HeelPivotOFFSET')
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Heel_Pivot', dv=0, at='.ry', v=0)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Heel_Pivot', dv=-10, at='.ry', v=-170)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Heel_Pivot', dv=10, at='.ry', v=170)
    # Toe Pivot
    cmds.addAttr(mainControl, at='double', ln='Toe_Pivot', min=-10, max=10, dv=0, k=1)
    thisOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Toe_Ctrl', 'ToePivotOFFSET')
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Toe_Pivot', dv=0, at='.ry', v=0)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Toe_Pivot', dv=-10, at='.ry', v=100)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Toe_Pivot', dv=10, at='.ry', v=-100)
    # Toe tap
    cmds.addAttr(mainControl, at='double', ln='Toe_Tap', min=0, max=10, dv=0, k=1)
    thisOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_ToeTap_Ctrl', 'ToeTapOFFSET')
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Toe_Tap', dv=0, at='.rx', v=0)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Toe_Tap', dv=10, at='.rx', v=-90)
    # Toe Pivot
    cmds.addAttr(mainControl, at='double', ln='Ball_Tilt', min=0, max=10, dv=0, k=1)
    thisOffsetGrp = InsertOffsetGroup(systemName + '_Reverse_Foot_Ball_Ctrl', 'BallTiltOFFSET')
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Ball_Tilt', dv=0, at='.rx', v=0)
    cmds.setDrivenKeyframe(thisOffsetGrp, cd=mainControl + '.Ball_Tilt', dv=10, at='.rx', v=100)