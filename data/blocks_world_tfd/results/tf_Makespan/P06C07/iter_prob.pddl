(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 - arm
block0 block11 block7 - double_block
encompass friction magnetic suction - effector
block1 block10 block2 block3 block4 block5 block6 block8 block9 - single_block
)
(:init (not_moving arm1)
(empty arm2)
(not_moving arm2)
(not_moving arm6)
(requires block5 friction)
(has_effector arm2 friction)
(empty arm3)
(not_moving arm3)
(requires block4 suction)
(has_effector arm6 suction)
(empty arm5)
(not_moving arm5)
(clear block2)
(requires block2 encompass)
(has_effector arm0 encompass)
(requires block11 magnetic)
(has_effector arm1 magnetic)
(has_effector arm0 magnetic)
(requires block8 encompass)
(has_effector arm5 encompass)
(clear block3)
(has_effector arm3 friction)
(clear block10)
(requires block10 friction)
(holding_double arm1 arm0 block11)
(not_moving arm0)
(requires block3 encompass)
(has_effector arm2 encompass)
(requires block0 friction)
(on_table block6)
(requires block6 friction)
(on_block block7 block6)
(requires block7 encompass)
(clear block9)
(requires block9 magnetic)
(has_effector arm5 magnetic)
(requires block1 suction)
(holding_single arm6 block1)
(on_block block3 block4)
(has_effector arm2 suction)
(on_table block0)
(has_effector arm0 friction)
(has_effector arm0 suction)
(has_effector arm1 friction)
(has_effector arm2 magnetic)
(has_effector arm3 magnetic)
(empty arm4)
(not_moving arm4)
(has_effector arm4 encompass)
(has_effector arm4 magnetic)
(has_effector arm6 friction)
(has_effector arm6 magnetic)
(on_table block10)
(on_table block8)
(on_block block2 block7)
(on_block block5 block0)
(on_block block9 block5)
(on_block block4 block8)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 2.0000)
(=(block_height block3) 2.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 0.0000)
(=(block_height block9) 2.0000)
(=(block_height block10) 0.0000)
(=(block_height block11) 2.0000)
(=(max_on_table) 5.0000)
(=(num_on_table) 4.0000)
(=(arm_height arm0) 2.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 2.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 1.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 1.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 0.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 2.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 1.0000)
(=(arm_id arm6) 6.0000))
(:goal (and 
(= (block_height block0) 0)
(= (block_height block1) 0)
(= (block_height block11) 1)
(= (block_height block3) 2)
(= (block_height block4) 1)
(= (block_height block5) 1)
(= (block_height block6) 2)
(= (block_height block8) 0)
(= (block_height block9) 2)
(on_block block11 block1)
(on_block block3 block4)
(on_block block4 block8)
(on_block block5 block0)
(on_block block6 block11)
(on_block block9 block5)
(on_table block0)
(on_table block1)
(on_table block8)
)
)
)