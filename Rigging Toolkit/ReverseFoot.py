import maya.cmds as cmds


def CreateLocators(name):
    cmds.spaceLocator(n=name + '_reverse_foot_heel_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_toe_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_outer_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_inner_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_ball_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_ankle_locator')


def CreateLocators(name, localScale):
    locatorList = [cmds.spaceLocator(n=name + '_reverse_foot_heel_locator')[0],
                   cmds.spaceLocator(n=name + '_reverse_foot_toe_locator')[0],
                   cmds.spaceLocator(n=name + '_reverse_foot_outer_locator')[0],
                   cmds.spaceLocator(n=name + '_reverse_foot_inner_locator')[0],
                   cmds.spaceLocator(n=name + '_reverse_foot_ball_locator')[0],
                   cmds.spaceLocator(n=name + '_reverse_foot_ankle_locator')[0]]
    for l in locatorList:
        cmds.setAttr(l + 'Shape.localScaleX', localScale)
        cmds.setAttr(l + 'Shape.localScaleY', localScale)
        cmds.setAttr(l + 'Shape.localScaleZ', localScale)


def CreateReverseFootSystem(systemName, controlSize):
    print('Creating ' + systemName + ' system')
    heelLocator = systemName + '_reverse_foot_heel_locator'
    toeLocator = systemName + '_reverse_foot_toe_locator'
    outerLocator = systemName + '_reverse_foot_outer_locator'
    innerLocator = systemName + '_reverse_foot_inner_locator'
    ballLocator = systemName + '_reverse_foot_ball_locator'
    ankleLocator = systemName + '_reverse_foot_ankle_locator'
    locatorList = [outerLocator, innerLocator, heelLocator, toeLocator, ballLocator, ankleLocator]
    controlList = []
    numItems = len(locatorList)
    for i in range(numItems):
        currentCtrl = cmds.circle(name=locatorList[i] + '_Ctrl', r=controlSize,
                                  nr=(0, 1, 0))[0]
        controlList.append(currentCtrl)
        currentCtrlGrp = cmds.group(currentCtrl, n=currentCtrl + '_Grp')
        cmds.matchTransform(currentCtrlGrp, locatorList[i], pos=1)
    for i in range(numItems - 1):
        childCtrl = controlList[i + 1]
        childCtrlGrp = cmds.listRelatives(childCtrl, parent=1)[0]
        cmds.parent(childCtrlGrp, controlList[i])
    for ctrl in controlList:
        controlShapeNode = cmds.listRelatives(ctrl, s=1)[0]
        cmds.setAttr(str(controlShapeNode) + ".overrideEnabled", 1)
        cmds.setAttr(str(controlShapeNode) + ".overrideColor", 13)