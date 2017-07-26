(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm2 arm3 arm4 arm6 - arm
block2 block3 block6 - double_block
encompass friction magnetic suction - effector
block0 block1 block4 block5 block7 block8 - single_block
)
(:init (requires block5 friction)
(requires block8 encompass)
(requires block4 magnetic)
(requires block0 magnetic)
(on_block block1 block0)
(requires block1 encompass)
(empty arm6)
(not_moving arm6)
(clear block3)
(requires block3 friction)
(has_effector arm6 friction)
(on_table block0)
(clear block2)
(on_block block2 block1)
(requires block2 suction)
(on_table block6)
(requires block6 magnetic)
(on_block block7 block6)
(requires block7 encompass)
(empty arm0)
(not_moving arm0)
(has_effector arm0 friction)
(has_effector arm0 encompass)
(has_effector arm0 magnetic)
(has_effector arm0 suction)
(empty arm2)
(not_moving arm2)
(has_effector arm2 friction)
(has_effector arm2 encompass)
(has_effector arm2 magnetic)
(has_effector arm2 suction)
(empty arm3)
(not_moving arm3)
(has_effector arm3 friction)
(has_effector arm3 magnetic)
(empty arm4)
(not_moving arm4)
(has_effector arm4 encompass)
(has_effector arm4 magnetic)
(has_effector arm6 magnetic)
(has_effector arm6 suction)
(clear block7)
(on_table block8)
(on_block block5 block8)
(on_block block3 block5)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 2.0000)
(=(block_height block3) 2.0000)
(=(block_height block4) 2.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 0.0000)
(=(max_on_table) 4.0000)
(=(num_on_table) 3.0000)
(=(arm_height arm0) 2.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm2) 3.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 0.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 0.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm6) 2.0000)
(=(arm_id arm6) 6.0000))
(:goal (and 
(= (block_height block0) 0)
(= (block_height block1) 1)
(= (block_height block2) 0)
(= (block_height block3) 2)
(= (block_height block4) 2)
(= (block_height block5) 1)
(= (block_height block6) 1)
(= (block_height block7) 2)
(= (block_height block8) 0)
(on_block block1 block0)
(on_block block3 block5)
(on_block block4 block6)
(on_block block5 block8)
(on_block block6 block2)
(on_block block7 block1)
(on_table block0)
(on_table block2)
(on_table block8)
)
)
)