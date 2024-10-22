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
