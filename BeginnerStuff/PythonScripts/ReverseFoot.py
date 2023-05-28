import maya.cmds as cmds


def CreateLocators(name):
    cmds.spaceLocator(n=name + '_reverse_foot_heel_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_toe_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_outer_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_inner_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_ball_locator')
    cmds.spaceLocator(n=name + '_reverse_foot_ankle_locator')


def CreateReverseFootSystem():
    systemName = cmds.textField(prefixField, q=1, text=1)
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
        currentCtrl = cmds.circle(name=locatorList[i] + '_Ctrl', r=cmds.xform(locatorList[i], q=1, s=1, r=1)[0],
                                  nr=(0, 1, 0))[0]
        controlList.append(currentCtrl)
        currentCtrlGrp = cmds.group(currentCtrl, n=currentCtrl+'_Grp')
        cmds.matchTransform(currentCtrlGrp, locatorList[i], pos=1)
    for i in range(numItems-1):
        childCtrl = controlList[i+1]
        childCtrlGrp = cmds.listRelatives(childCtrl, parent=1)[0]
        cmds.parent(childCtrlGrp, controlList[i])


def LocatorButtonCmd():
    prefix = cmds.textField(prefixField, q=1, text=1)
    CreateLocators(prefix)


def CreateReverseFootWindow():
    if cmds.window('rfWindow', exists=1):
        cmds.delete('rfWindow')
    cmds.showWindow(rfWindow)


rfWindow = cmds.window(title='Create Reverse Foot', widthHeight=(300, 75))
cmds.columnLayout(adjustableColumn=1, rowSpacing=5)
cmds.rowLayout(numberOfColumns=2)
prefixField = cmds.textField(placeholderText='System Prefix', width=150)
cmds.button(label='Create Locators', command='LocatorButtonCmd()', width=150)
cmds.setParent('..')
cmds.button(label="I've placed my locators, GO!", command='CreateReverseFootSystem()')

CreateReverseFootWindow()
