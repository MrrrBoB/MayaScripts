import maya.cmds as cmds

# AUTO RIGGER V0.1
# ---------------------------------------------------------------
height = 0


def CreateHeightLocators():
    baseLocator = cmds.spaceLocator(p=(0, 0, 0), n="Base_Locator")
    topLocator = cmds.spaceLocator(p=(0, 0, 0), n='Top_Locator')
    cmds.select(cl=1)


def CreateHumanoidSkeletonTemplate():
    print("Laying out joint template")
    rigHeight = round(cmds.xform("Top_Locator", q=1, t=1)[1] - cmds.xform("Base_Locator", q=1, t=1)[1], 2)
# create spine from hip to head
    cogJnt = cmds.joint(n='CoG_Jnt', p=(0, rigHeight * .575, 0), radius=10)
    spine01Jnt = cmds.joint(n="Spine_01_Jnt", p=cmds.xform(cogJnt, q=1, t=1), radius=5)
    spine02Jnt = cmds.joint(n="Spine_02_Jnt", p=(0, rigHeight * .065, rigHeight * .005), r=1, rad=5)
    spine03Jnt = cmds.joint(n="Spine_03_Jnt", p=(0, rigHeight * .065, rigHeight * -.02), r=1, rad=5)
    neckJnt = cmds.joint(n="Neck_Jnt", p=(0, rigHeight * .125, rigHeight * -.03), r=1, rad=5)
    headJnt = cmds.joint(n="Head_Jnt", p=(0, rigHeight * .08, rigHeight * .02), r=1, rad=5)
# create eyes and jaw
    cmds.joint(n="L_Eye_Jnt", p=(rigHeight*.018, rigHeight * .0244, rigHeight * .05), r=1, rad=3)
    cmds.select(headJnt, r=1)
    cmds.joint(n='Jaw_Jnt', p=(0, rigHeight * .015, rigHeight * .01), r=1, rad=5)
    cmds.select(spine03Jnt, r=1)
    leftClavJnt = cmds.joint(n="L_Clav_Jnt", p=(rigHeight * .025, rigHeight * .095, rigHeight * .005), r=1, rad=5)
    leftArm01Jnt = cmds.joint(n="L_Arm_01_Jnt", p=(rigHeight * .07, rigHeight * .01, rigHeight * -.03), r=1, rad=5)
    leftArm02Jnt = cmds.joint(n="L_Arm_02_Jnt", p=(rigHeight * .14, 0, rigHeight * .014), r=1, rad=5)
    leftArm03Jnt = cmds.joint(n="L_Arm_03_Jnt", p=(rigHeight * .125, 0, rigHeight * .06), r=1, rad=5)
# create left hand
    leftHandJoint = cmds.joint(n="L_Hand_Jnt", p=cmds.xform(leftArm03Jnt, q=1, t=1, ws=1), radius=7)
    thumbBaseJnt = cmds.joint(n="L_Thumb_Base_Jnt", p=(0, rigHeight*-.003, rigHeight*.0175), r=1, rad=3)
    thumb01Jnt = cmds.joint(n="L_Thumb_01_Jnt", p=(rigHeight*.005, rigHeight * -.004, rigHeight * .0175), r=1, rad=3)
    thumb02Jnt = cmds.joint(n="L_Thumb_02_Jnt", p=(rigHeight * .0075, rigHeight * -.004, rigHeight * .015), r=1, rad=3)
# create and orient first finger
    cmds.select(leftHandJoint, r=1)
    leftPointerFinger01Jnt = cmds.joint(n="L_PointerFinger_01_Jnt", p=(rigHeight * .033,
                                                                      rigHeight * .005,
                                                                      rigHeight * .035), r=1, rad=3)
    leftPointerFinger03Jnt = cmds.joint(n="L_PointerFinger_03_Jnt", p=(rigHeight * .0245,
                                                                       rigHeight*-.003,
                                                                       rigHeight * .0175), r=1, rad=3)
    cmds.select(leftPointerFinger01Jnt)
    leftPointerFinger02Jnt = cmds.joint(n="L_PointerFinger_02_Jnt", rad=3)
    tempFingerPointConstraint = cmds.pointConstraint(leftPointerFinger01Jnt,
                                                     leftPointerFinger03Jnt,
                                                     leftPointerFinger02Jnt,
                                                     mo=0)
    cmds.delete(tempFingerPointConstraint)
    cmds.parent(leftPointerFinger03Jnt, leftPointerFinger02Jnt)
    cmds.joint(leftPointerFinger01Jnt, e=1, oj='xyz', sao='yup', ch=1)
    cmds.joint(leftPointerFinger03Jnt, e=1, oj='none')
# duplicate rest of fingers
    for fingerName in ("MiddleFinger", "RingFinger", "Pinky"):
        newFingerJoint1 = cmds.duplicate(leftPointerFinger01Jnt, n="L_%s_01_Jnt" %fingerName, rc=1)
        childList = cmds.listRelatives(newFingerJoint1, ad=1)
        for child in childList:
            child = cmds.rename(child, child.replace("PointerFinger", fingerName))
            child = cmds.rename(child, child.replace("Jnt1", "Jnt"))
# move fingers
    cmds.xform("L_MiddleFinger_01_Jnt", t=(rigHeight * .04, rigHeight * .005, rigHeight * .025), ro=(0, 8, 0))
    cmds.xform("L_RingFinger_01_Jnt", t=(rigHeight * .045, rigHeight * .005, rigHeight * .0135), ro=(0, 12, 0))
    cmds.xform("L_Pinky_01_Jnt", t=(rigHeight * .045, rigHeight * .005, rigHeight * .003), ro=(0, 16, 0))
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
    # orient spine
    print("Orient Skeleton Work In Progress")
    for currentJoint in (cmds.ls(typ='joint')):
        cmds.makeIdentity(currentJoint, r=1, a=1)
    for currentJoint in ("Spine_01_Jnt","Spine_02_Jnt","Spine_03_Jnt", "Neck_Jnt"):
        cmds.joint(currentJoint, e=1, oj="xyz", sao="zdown", ch=0)
    # Orient Arm
    cmds.joint("L_Clav_Jnt", e=1, oj='xyz', sao='yup', ch=0)
    for currentJoint in ("L_Arm_01_Jnt", "L_Arm_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint("L_Arm_03_Jnt", e=1, oj='none', ch=0)
    cmds.joint("L_Hand_Jnt", e=1, oj='none', ch=0)
    # orient thumb joint MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE MOVE
    thumbAngleX = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[0]
    thumbAngleY = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[1]
    rotation = 90 * (thumbAngleX / (abs(thumbAngleX) + abs(thumbAngleY)))
    cmds.joint('L_Thumb_01_Jnt', e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint('L_Thumb_02_Jnt', e=1, oj='none')
    cmds.xform("L_Thumb_01_Jnt", ro=(rotation, 0, 0))
    # SKIP FINGERS
    # Orient Leg
    for currentJoint in ("L_Leg_01_Jnt", "L_Leg_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='zdown', ch=0)
    cmds.joint("L_Leg_03_Jnt", e=1, oj='none', ch=0)
    for currentJoint in ("L_Foot_01_Jnt", "L_Foot_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup')
    cmds.joint("L_Foot_03_Jnt", e=1, oj='none')




CreateHumanoidSkeletonTemplate()
OrientSkeleton()
