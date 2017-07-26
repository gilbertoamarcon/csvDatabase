(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 - arm
block6 block8 - double_block
encompass friction magnetic suction - effector
block0 block1 block2 block3 block4 block5 block7 - single_block
)
(:init (empty arm3)
(not_moving arm3)
(empty arm1)
(not_moving arm4)
(empty arm5)
(not_moving arm5)
(empty arm6)
(requires block8 encompass)
(has_effector arm6 encompass)
(has_effector arm5 encompass)
(not_moving arm1)
(empty arm2)
(clear block7)
(requires block7 suction)
(has_effector arm2 suction)
(requires block5 suction)
(has_effector arm1 suction)
(not_moving arm6)
(not_moving arm2)
(empty arm0)
(not_moving arm0)
(requires block4 friction)
(has_effector arm4 friction)
(requires block0 encompass)
(on_block block1 block0)
(requires block1 suction)
(has_effector arm0 friction)
(has_effector arm0 encompass)
(clear block3)
(requires block3 friction)
(has_effector arm1 friction)
(requires block2 encompass)
(requires block6 suction)
(has_effector arm0 suction)
(on_table block0)
(has_effector arm0 magnetic)
(has_effector arm1 magnetic)
(has_effector arm3 friction)
(has_effector arm3 magnetic)
(has_effector arm3 suction)
(has_effector arm4 encompass)
(has_effector arm4 magnetic)
(has_effector arm4 suction)
(has_effector arm5 friction)
(has_effector arm5 magnetic)
(has_effector arm6 friction)
(has_effector arm6 magnetic)
(has_effector arm6 suction)
(clear block1)
(on_table block8)
(on_block block5 block8)
(on_block block3 block6)
(on_block block6 block2)
(holding_single arm4 block4)
(on_block block7 block5)
(on_table block2)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 0.0000)
(=(block_height block3) 2.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 1.0000)
(=(block_height block7) 2.0000)
(=(block_height block8) 0.0000)
(=(max_on_table) 4.0000)
(=(num_on_table) 3.0000)
(=(arm_height arm0) 1.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 2.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 1.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 2.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 1.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 1.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 1.0000)
(=(arm_id arm6) 6.0000))
(:goal (and 
(on_block block0 block1)
(on_block block3 block6)
(on_block block4 block0)
(on_block block5 block8)
(on_block block6 block2)
(on_block block7 block5)
(on_table block1)
(on_table block2)
(on_table block8)
)
)
)