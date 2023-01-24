import maya.cmds as cmds
import sys

sys.path.append("F:\SchoolMore\MayaScripts\BeginnerStuff\PythonScripts")
import ControlCreator
import RenameChain




def show_library_window():
    if cmds.window("lWindow", exists=True):
        cmds.deleteUI("lWindow")
    lWindow = cmds.window(title="Rigging Library", iconName='Short Name', widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Control Creator', command='show_control_creator()')
    cmds.button(label='Rename Joint Chain', command='show_rename_chain()')
    cmds.button(label='Close Library', command=('cmds.deleteUI(\"' + lWindow + '\", window=True)'))
    cmds.setParent('..')
    cmds.showWindow(lWindow)


def show_control_creator():
    ControlCreator.createControlWindow()


def show_rename_chain():
    RenameChain.show_rename_window()


show_library_window()
