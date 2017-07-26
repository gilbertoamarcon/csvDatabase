(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 - arm
block2 block3 block6 - double_block
encompass friction magnetic suction - effector
block0 block1 block4 block5 block7 block8 - single_block
)
(:init (not_moving arm6)
(clear block4)
(not_moving arm0)
(empty arm5)
(not_moving arm5)
(empty arm1)
(requires block5 friction)
(has_effector arm1 friction)
(requires block8 encompass)
(has_effector arm5 encompass)
(not_moving arm1)
(requires block4 magnetic)
(has_effector arm0 magnetic)
(requires block0 magnetic)
(on_block block1 block0)
(requires block1 encompass)
(on_table block6)
(clear block7)
(requires block7 encompass)
(clear block3)
(requires block3 friction)
(has_effector arm6 friction)
(requires block2 suction)
(has_effector arm6 suction)
(has_effector arm0 suction)
(on_table block0)
(requires block6 magnetic)
(has_effector arm0 friction)
(has_effector arm0 encompass)
(has_effector arm1 magnetic)
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
(has_effector arm5 magnetic)
(on_block block5 block8)
(has_effector arm6 magnetic)
(on_table block8)
(on_block block4 block6)
(on_block block3 block5)
(holding_double arm6 arm0 block2)
(on_block block7 block1)
(=(block_height block0) 0.0000)
(=(block_height block2) 2.0000)
(=(block_height block1) 1.0000)
(=(block_height block3) 2.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 2.0000)
(=(block_height block8) 0.0000)
(=(max_on_table) 4.0000)
(=(num_on_table) 3.0000)
(=(arm_height arm0) 2.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 2.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 3.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 0.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 0.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 2.0000)
(=(arm_id arm5) 5.0000)
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