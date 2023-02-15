import maya.cmds as cmds


def rename_chain(format_ex):
    numDigits = format_ex.count("#")
    if numDigits <= 0:
        print("invalid")
        return
    search_string = (str("#" * numDigits))
    num_occurances = format_ex.count(search_string)
    if num_occurances <= 0:
        print("invalid")
        return
    format_tuple = format_ex.partition(search_string)
    print(format_tuple)
    selections = cmds.ls(sl=True)
    num = 0
    for obj in selections:
        num += 1
        current_name_string = (format_tuple[0] + str(num).zfill(numDigits) + format_tuple[2])
        cmds.rename(obj, current_name_string)


def button_command():
    inputString = cmds.textField(inputField, q=True, text=True)
    rename_chain(inputString)


def show_rename_window():
    if cmds.window("rcWindow", exists=True):
        cmds.deleteUI("rcWindow")

    cmds.showWindow(rcWindow)


rcWindow = cmds.window(title="Rename Chain", iconName='Short Name', widthHeight=(300, 70))
cmds.columnLayout(adjustableColumn=True)
cmds.text(label="Rename Format")
inputField = cmds.textField(placeholderText="use # for digit count, ex: Arm_##_Jnt")
cmds.button(label='Rename', command='button_command()')
cmds.setParent('..')

show_rename_window()

