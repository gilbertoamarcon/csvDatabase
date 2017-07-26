(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 - arm
block10 block11 block3 block8 - double_block
encompass friction magnetic suction - effector
block0 block1 block2 block4 block5 block6 block7 block9 - single_block
)
(:init (not_moving arm3)
(clear block5)
(on_block block5 block4)
(requires block5 encompass)
(has_effector arm1 encompass)
(not_moving arm2)
(empty arm1)
(not_moving arm1)
(empty arm0)
(not_moving arm0)
(clear block2)
(requires block2 magnetic)
(has_effector arm2 magnetic)
(clear block1)
(requires block1 encompass)
(has_effector arm3 encompass)
(requires block0 suction)
(empty arm4)
(has_effector arm4 encompass)
(requires block4 magnetic)
(requires block11 magnetic)
(has_effector arm3 magnetic)
(on_table block0)
(on_table block3)
(requires block3 encompass)
(on_table block6)
(requires block6 magnetic)
(on_block block7 block6)
(requires block7 magnetic)
(on_block block8 block7)
(requires block8 encompass)
(on_table block9)
(requires block9 suction)
(on_block block10 block9)
(requires block10 magnetic)
(has_effector arm0 friction)
(has_effector arm0 encompass)
(has_effector arm1 friction)
(has_effector arm1 suction)
(has_effector arm3 friction)
(not_moving arm4)
(has_effector arm4 friction)
(has_effector arm4 suction)
(on_block block2 block8)
(clear block3)
(on_block block4 block0)
(holding_double arm3 arm2 block11)
(on_block block1 block10)
(=(block_height block1) 2.0000)
(=(block_height block0) 0.0000)
(=(block_height block2) 3.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 2.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 2.0000)
(=(block_height block9) 0.0000)
(=(block_height block10) 1.0000)
(=(block_height block11) 2.0000)
(=(max_on_table) 5.0000)
(=(num_on_table) 4.0000)
(=(arm_height arm0) 2.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 2.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 2.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 2.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 2.0000)
(=(arm_id arm4) 4.0000))
(:goal (and 
(= (block_height block0) 0)
(= (block_height block1) 2)
(= (block_height block10) 1)
(= (block_height block4) 1)
(= (block_height block5) 2)
(= (block_height block6) 2)
(= (block_height block7) 1)
(= (block_height block8) 0)
(= (block_height block9) 0)
(on_block block1 block10)
(on_block block10 block9)
(on_block block4 block0)
(on_block block5 block4)
(on_block block6 block7)
(on_block block7 block8)
(on_table block0)
(on_table block8)
(on_table block9)
)
)
)