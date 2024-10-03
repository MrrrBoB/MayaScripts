import maya.cmds as cmds

# AUTO RIGGER V0.1
# ---------------------------------------------------------------
height = 0


def CreateHeightLocators():
    baseLocator = cmds.spaceLocator(p=(0, 0, 0), n="Base_Locator")
    topLocator = cmds.spaceLocator(p=(0, 0, 0), n='Top_Locator')
    cmds.select(cl=1)


def CreateHumanoidSkeletonTemplate():
    rigHeight = round(cmds.xform("Top_Locator", q=1, t=1)[1] - cmds.xform("Base_Locator", q=1, t=1)[1], 2)
    # create spine from hip to head
    cogJnt = cmds.joint(n='CoG_Jnt', p=(0, rigHeight * .575, 0), radius=10)
    spine01Jnt = cmds.joint(n="Spine_01_Jnt", p=cmds.xform(cogJnt, q=1, t=1), radius=5)
    spine02Jnt = cmds.joint(n="Spine_02_Jnt", p=(0, rigHeight * .065, rigHeight * .005), r=1, rad=5)
    spine03Jnt = cmds.joint(n="Spine_O3_Jnt", p=(0, rigHeight * .065, rigHeight * -.02), r=1, rad=5)
    neckJnt = cmds.joint(n="Neck_Jnt", p=(0, rigHeight * .125, rigHeight * -.03), r=1, rad=5)
    headJnt = cmds.joint(n="Head_Jnt", p=(0, rigHeight * .07, rigHeight * .01), r=1, rad=5)
    # create left arm
    cmds.select(spine03Jnt, r=1)
    leftClavJnt = cmds.joint(n="L_Clav_Jnt", p=(rigHeight * .025, rigHeight * .095, rigHeight * .005), r=1, rad=5)
    leftArm01Jnt = cmds.joint(n="L_Arm_01_Jnt", p=(rigHeight * .07, rigHeight * .01, rigHeight * -.03), r=1, rad=5)
    leftArm02Jnt = cmds.joint(n="L_Arm_02_Jnt", p=(rigHeight * .14, 0, rigHeight * .014), r=1, rad=5)
    leftArm03Jnt = cmds.joint(n="L_Arm_03_Jnt", p=(rigHeight * .125, 0, rigHeight * .06), r=1, rad=5)
    # create left leg
    cmds.select(cogJnt, r=1)
    pelvisJnt = cmds.joint(n="Pelvis_Jnt", p=cmds.xform(cogJnt, q=1, t=1), radius=5)
    leftLeg01Jnt = cmds.joint(n="L_Leg_01_Jnt", p=(rigHeight * .05, rigHeight * -.04, rigHeight * -.01), r=1, rad=5)
    leftLeg02Jnt = cmds.joint(n="L_Leg_02_Jnt", p=(0, rigHeight * -.25, 0), r=1, rad=5)
    leftLeg03Jnt = cmds.joint(n="L_Leg_03_Jnt", p=(0, rigHeight * -.25, rigHeight * -.005), r=1, rad=5)
    leftFoot01Jnt = cmds.joint(n="L_Foot_01_Jnt", p=cmds.xform(leftLeg03Jnt, q=1, t=1, ws=1), radius=7)
    leftFoot02Jnt = cmds.joint(n="L_Foot_02_Jnt", p=(0, rigHeight * -.025, rigHeight * .055), r=1, rad=5)
    leftFoot03Jnt = cmds.joint(n="L_Foot_03_Jnt", p=(0, 0, rigHeight * .055), r=1, rad=5)


def OrientSkeleton():
    print("Orient Skeleton Work In Progress")
    for currentJoint in ("L_Arm_01_Jnt", "L_Arm_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint("L_Arm_03_Jnt", e=1, oj='none', ch=0)


CreateHumanoidSkeletonTemplate()
OrientSkeleton()
