import importlib
import maya.cmds as cmds
import sys

sys.path.append('F:\SchoolMore\pythonProject\Rigging Toolkit')
import IKFK
import Controls
import SplineTools
import ColorChanger
import ReverseFoot

importlib.reload(IKFK)
importlib.reload(Controls)
importlib.reload(SplineTools)
importlib.reload(ColorChanger)
importlib.reload(ReverseFoot)
# AUTO RIGGER V0.1
# ---------------------------------------------------------------
height = 0


def InitializeHeirarchy():
    if cmds.objExists('TESTRIG'):
        cmds.error('Looks like you already have a rig started!')
    metaGroup = cmds.group(n='TESTRIG', w=1, em=1)
    geometryGroup = cmds.group(n='Geometry', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Geometry_Layer')
    skeletonGroup = cmds.group(n='Skeleton', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Skeleton_Layer')
    deformersGroup = cmds.group(n='Deformers', p=metaGroup, em=1)
    ControlGroup = cmds.group(n='Controls', p=metaGroup, em=1)
    cmds.createDisplayLayer(n='Controls_Layer')
    cmds.select(cl=1)


def CreateHeightLocators():
    baseLocator = cmds.spaceLocator(p=(0, 0, 0), n="Base_Locator")
    topLocator = cmds.spaceLocator(p=(0, 0, 0), n='Top_Locator')
    cmds.select(cl=1)


def CreateHumanoidSkeletonTemplate():
    global rigHeight
    global footLocators
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
    cmds.joint(n="L_Eye_Jnt", p=(rigHeight * .018, rigHeight * .0244, rigHeight * .05), r=1, rad=3)
    cmds.select(headJnt, r=1)
    cmds.joint(n='Jaw_Jnt', p=(0, rigHeight * .015, rigHeight * .01), r=1, rad=5)
    cmds.select(spine03Jnt, r=1)
    leftClavJnt = cmds.joint(n="L_Clav_Jnt", p=(rigHeight * .025, rigHeight * .095, rigHeight * .005), r=1, rad=5)
    leftArm01Jnt = cmds.joint(n="L_Arm_01_Jnt", p=(rigHeight * .07, rigHeight * .01, rigHeight * -.03), r=1, rad=5)
    leftArm02Jnt = cmds.joint(n="L_Arm_02_Jnt", p=(rigHeight * .14, 0, rigHeight * .014), r=1, rad=5)
    leftArm03Jnt = cmds.joint(n="L_Arm_03_Jnt", p=(rigHeight * .125, 0, rigHeight * .06), r=1, rad=5)
    # create left hand
    leftHandJoint = cmds.joint(n="L_Hand_Jnt", p=cmds.xform(leftArm03Jnt, q=1, t=1, ws=1), radius=7)
    thumbBaseJnt = cmds.joint(n="L_Thumb_Base_Jnt", p=(0, rigHeight * -.003, rigHeight * .0175), r=1, rad=3)
    thumb01Jnt = cmds.joint(n="L_Thumb_01_Jnt", p=(rigHeight * .005, rigHeight * -.004, rigHeight * .0175), r=1, rad=3)
    thumb02Jnt = cmds.joint(n="L_Thumb_02_Jnt", p=(rigHeight * .0075, rigHeight * -.004, rigHeight * .015), r=1, rad=3)
    # create and orient first finger
    cmds.select(leftHandJoint, r=1)
    leftPointerFinger01Jnt = cmds.joint(n="L_PointerFinger_01_Jnt", p=(rigHeight * .033,
                                                                       rigHeight * .005,
                                                                       rigHeight * .035), r=1, rad=3)
    leftPointerFinger03Jnt = cmds.joint(n="L_PointerFinger_03_Jnt", p=(rigHeight * .0245,
                                                                       rigHeight * -.003,
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
        newFingerJoint1 = cmds.duplicate(leftPointerFinger01Jnt, n="L_%s_01_Jnt" % fingerName, rc=1)
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
    footLocators = ReverseFoot.CreateLocators('L', rigHeight * .001)
    cmds.xform('L_Reverse_Foot_Heel_Locator', t=(rigHeight * .0455, 0, rigHeight * -.0445), ws=1)
    cmds.xform('L_Reverse_Foot_Toe_Locator', t=(rigHeight * .0455, 0, rigHeight * .1), ws=1)
    cmds.xform('L_Reverse_Foot_Outer_Locator', t=(rigHeight * .083, 0, rigHeight * .05), ws=1)
    cmds.xform('L_Reverse_Foot_Inner_Locator', t=(rigHeight * .035, 0, rigHeight * .05), ws=1)
    cmds.xform('L_Reverse_Foot_Ball_Locator', t=(cmds.xform(leftFoot02Jnt, q=1, t=1, ws=1)), ws=1)
    cmds.xform('L_Reverse_Foot_Ankle_Locator', t=(cmds.xform(leftFoot01Jnt, q=1, t=1, ws=1)), ws=1)
    cmds.parent(cogJnt, 'Skeleton')


def OrientSkeleton():
    # orient spine
    print("Orienting Skeleton...")
    for currentJoint in (cmds.ls(typ='joint')):
        cmds.makeIdentity(currentJoint, r=1, a=1)
    for currentJoint in ("Spine_01_Jnt", "Spine_02_Jnt", "Spine_03_Jnt", "Neck_Jnt"):
        cmds.joint(currentJoint, e=1, oj="xyz", sao="zdown", ch=0)
    # Orient Arm
    cmds.joint("L_Clav_Jnt", e=1, oj='xyz', sao='yup', ch=0)
    for currentJoint in ("L_Arm_01_Jnt", "L_Arm_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint("L_Arm_03_Jnt", e=1, oj='none', ch=0)
    cmds.joint("L_Hand_Jnt", e=1, oj='none', ch=0)
    # orient thumb joint
    thumbAngleX = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[0]
    thumbAngleY = cmds.xform("L_Thumb_02_Jnt", q=1, t=1)[1]
    rotation = 90 * (thumbAngleX / (abs(thumbAngleX) + abs(thumbAngleY)))
    cmds.joint('L_Thumb_01_Jnt', e=1, oj='xyz', sao='yup', ch=0)
    cmds.joint('L_Thumb_02_Jnt', e=1, oj='none')
    cmds.xform("L_Thumb_01_Jnt", ro=(rotation, 0, 0))
    cmds.makeIdentity("L_Thumb_01_Jnt", r=1, a=1)
    cmds.joint('L_Thumb_Base_Jnt', e=1, oj='none', ch=0)
    # SKIP FINGERS
    # Orient Leg
    for currentJoint in ("L_Leg_01_Jnt", "L_Leg_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='zdown', ch=0)
    cmds.joint("L_Leg_03_Jnt", e=1, oj='none', ch=0)
    for currentJoint in ("L_Foot_01_Jnt", "L_Foot_02_Jnt"):
        cmds.joint(currentJoint, e=1, oj='xyz', sao='yup')
    cmds.joint("L_Foot_03_Jnt", e=1, oj='none')


def MirrorJoints(alreadyOriented):
    if not alreadyOriented:
        OrientSkeleton()
    cmds.mirrorJoint("L_Clav_Jnt", myz=1, mirrorBehavior=1, sr=('L_', 'R_'))
    cmds.mirrorJoint("L_Leg_01_Jnt", myz=1, mirrorBehavior=1, sr=('L_', 'R_'))
    cmds.mirrorJoint("L_Eye_Jnt", myz=1, mirrorBehavior=0, sr=('L_', 'R_'))
    # Mirror the locators for reverse IK foot
    flipLocs = []
    flipGrp = cmds.group(n='LocFlipGrp', w=1, em=1)
    for locator in footLocators:
        newLoc = cmds.duplicate(locator, n=locator.replace('L_', 'R_'))[0]
        flipLocs.append(newLoc)
        cmds.parent(newLoc, flipGrp)
    cmds.xform(flipGrp, s=(-1, 1, 1))
    for x in cmds.listRelatives(flipGrp, c=1):
        cmds.parent(x, w=1)
        # cmds.makeIdentity(x, r=1, a=1)
    cmds.delete(flipGrp)


# Create controls and add IKFK systems to limbs and spine
def ImplementIKFK():
    print('Implementing IKFK systems...')
    # Left Arm
    LArmIKFKCtrl = Controls.createControl('world', 'L_Arm_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(LArmIKFKCtrl + '_Grp', t=(rigHeight * .2, rigHeight * .9, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('L_Arm_01_Jnt', 'L_Arm', 3, 1, 'L_Arm_IKFK_Switch_Ctrl', 0)
    # Right Arm
    RArmIKFKCtrl = Controls.createControl('world', 'R_Arm_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(RArmIKFKCtrl + '_Grp', t=(rigHeight * -.2, rigHeight * .9, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('R_Arm_01_Jnt', 'R_Arm', 3, 1, 'R_Arm_IKFK_Switch_Ctrl', 0)
    # Left Leg
    LLegIKFKCtrl = Controls.createControl('world', 'L_Leg_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(LLegIKFKCtrl + '_Grp', t=(rigHeight * .2, rigHeight * .27, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('L_Leg_01_Jnt', 'L_Leg', 6, 0, 'L_Leg_IKFK_Switch_Ctrl', 0)
    cmds.ikHandle(n='L_Leg_IK_Handle', sj='L_Leg_01_Jnt_IK', ee='L_Leg_03_Jnt_IK', sol='ikRPsolver')
    # Right Leg
    RLegIKFKCtrl = Controls.createControl('world', 'R_Leg_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(RLegIKFKCtrl + '_Grp', t=(rigHeight * -.2, rigHeight * .27, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('R_Leg_01_Jnt', 'R_Leg', 6, 0, 'R_Leg_IKFK_Switch_Ctrl', 0)
    cmds.ikHandle(n='R_Leg_IK_Handle', sj='R_Leg_01_Jnt_IK', ee='R_Leg_03_Jnt_IK', sol='ikRPsolver')
    # Spine
    SpineIKFKCtrl = Controls.createControl('world', 'Spine_IKFK_Switch', rigHeight * .025, 17, 2, 0)
    cmds.xform(SpineIKFKCtrl + '_Grp', t=(rigHeight * .15, rigHeight * .65, rigHeight * -.04), ws=1)
    IKFK.autoLimbTool('Spine_01_Jnt', 'Spine', 3, 0, 'Spine_IKFK_Switch_Ctrl', 0)
    SplineTools.CreateSplineFromJoint('Spine_01_Jnt_IK', 'Spine', 3)
    cmds.group(SpineIKFKCtrl + '_Grp',
               RArmIKFKCtrl + '_Grp',
               LArmIKFKCtrl + '_Grp',
               RLegIKFKCtrl + '_Grp',
               LLegIKFKCtrl + '_Grp',
               n='IKFK_Switches', w=1)


def IKControls():
    print('Creating IK Controls...')
    print('Creating Control Joints for spine')
    cmds.select(cl=1)
    CTRLJnt3 = cmds.joint(n='Spine_IK_Ctrl_Jnt_3', p=cmds.xform('Spine_03_Jnt', q=1, t=1, ws=1), radius=10)
    cmds.select(cl=1)
    CTRLJnt2 = cmds.joint(n='Spine_IK_Ctrl_Jnt_2', p=cmds.xform('Spine_02_Jnt', q=1, t=1, ws=1), radius=10)
    ColorChanger.changeColor([CTRLJnt2, CTRLJnt3], 18)
    cmds.group()
    cmds.select((CTRLJnt3, CTRLJnt2, 'CoG_Jnt'), r=1)
    cmds.select('Spine_Curve', add=1)
    cmds.skinCluster(('CoG_Jnt', CTRLJnt2, CTRLJnt3), 'Spine_Curve', tsb=1, bm=0, sm=0, nw=1)
    cmds.orientConstraint(CTRLJnt3, 'Spine_03_Jnt_IK', mo=1)
    Controls.createControl(CTRLJnt3, 'IK_Torso_Top', 1, 13, 1, 1)
    Controls.createControl(CTRLJnt2, 'IK_Torso_Mid', .85, 13, 1, 1)
    # Create Limb IK Controls
    for prefix in ('L_', 'R_'):
        # Create Arm Controls
        print('Creating ' + prefix + ' arm controls')
        Controls.createControl(prefix + 'Hand_Jnt', prefix + 'Hand_IK', .5, 13, 0, 0)
        cmds.parent(prefix + 'Arm_IK_Handle', prefix + 'Hand_IK_Ctrl')
        pvCtrl = Controls.createControl(prefix + 'Arm_02_Jnt_IK', prefix + 'Arm_IK_PV', .25, 13, 1, 0)
        offsetGrp = cmds.group(n=pvCtrl + '_OFFSET_Grp', w=1, em=1)
        cmds.matchTransform(offsetGrp, pvCtrl, pos=1)
        cmds.parent(offsetGrp, pvCtrl + '_Grp')
        cmds.parent(pvCtrl, offsetGrp)
        cmds.xform(offsetGrp, t=(0, 0, rigHeight * -.2), ws=1, r=1)
        cmds.poleVectorConstraint(pvCtrl, prefix + 'Arm_IK_Handle')
        # Legs
        print('Creating ' + prefix + ' leg controls')
        Controls.createControl('world', prefix + 'Leg_IK_Control', .5, 13, 1, 0)
        cmds.matchTransform(prefix + 'Leg_IK_Control_Ctrl_Grp', prefix + 'Leg_03_Jnt_IK', pos=1)
        pvCtrl = Controls.createControl('world', prefix + 'Leg_IK_PV', .25, 13, 0, 0)
        offsetGrp = cmds.group(n=pvCtrl + '_OFFSET_Grp', w=1, em=1)
        cmds.matchTransform(offsetGrp, pvCtrl, pos=1)
        cmds.parent(offsetGrp, pvCtrl + '_Grp')
        cmds.parent(pvCtrl, offsetGrp)
        cmds.matchTransform(prefix + 'Leg_IK_PV_Ctrl_Grp', prefix + 'Leg_02_Jnt_IK', pos=1)
        cmds.xform(offsetGrp, t=(0, 0, rigHeight * .2), ws=1, r=1)
        cmds.poleVectorConstraint(pvCtrl, prefix + 'Leg_IK_Handle')
        # Reverse Foot
        ReverseFoot.CreateReverseFootSystem(prefix.replace('_', ''), rigHeight * .02)
        cmds.ikHandle(sj=prefix + 'Foot_01_Jnt_IK',
                      ee=prefix + 'Foot_02_Jnt_IK',
                      n=prefix + 'Reverse_Foot_Ball_Handle',
                      sol='ikSCsolver')
        cmds.parent(prefix + 'Reverse_Foot_Ball_Handle', prefix + 'Reverse_Foot_Ball_Ctrl')
        cmds.parent(prefix+'Leg_IK_Handle', prefix+'Reverse_Foot_Ball_Ctrl')
        cmds.ikHandle(sj=prefix + 'Foot_02_Jnt_IK',
                      ee=prefix + 'Foot_03_Jnt_IK',
                      n=prefix + 'Reverse_Foot_Toe_Handle',
                      sol='ikSCsolver')
        cmds.parent(prefix + 'Reverse_Foot_Toe_Handle', prefix + 'Reverse_Foot_ToeTap_Ctrl')


InitializeHeirarchy()
CreateHumanoidSkeletonTemplate()
OrientSkeleton()
MirrorJoints(True)
ImplementIKFK()
IKControls()
