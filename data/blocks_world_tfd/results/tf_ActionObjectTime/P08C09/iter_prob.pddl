(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 - arm
block0 block11 block12 block14 block2 block8 block9 - double_block
encompass friction magnetic suction - effector
block1 block10 block13 block3 block4 block5 block6 block7 - single_block
)
(:init (not_moving arm0)
(empty arm6)
(requires block14 friction)
(has_effector arm6 friction)
(has_effector arm4 friction)
(not_moving arm6)
(requires block8 friction)
(has_effector arm1 friction)
(has_effector arm0 friction)
(empty arm1)
(not_moving arm1)
(empty arm4)
(not_moving arm4)
(requires block7 magnetic)
(has_effector arm6 magnetic)
(clear block6)
(requires block6 encompass)
(has_effector arm4 encompass)
(requires block5 encompass)
(has_effector arm6 encompass)
(requires block13 encompass)
(has_effector arm0 encompass)
(requires block2 suction)
(has_effector arm1 suction)
(has_effector arm0 suction)
(clear block1)
(requires block1 suction)
(has_effector arm4 suction)
(requires block3 suction)
(on_table block12)
(requires block12 magnetic)
(has_effector arm0 magnetic)
(clear block0)
(requires block0 magnetic)
(has_effector arm4 magnetic)
(clear block11)
(requires block11 encompass)
(not_moving arm3)
(empty arm2)
(not_moving arm2)
(empty arm5)
(requires block10 encompass)
(has_effector arm5 encompass)
(has_effector arm3 suction)
(not_moving arm5)
(requires block4 friction)
(clear block9)
(holding_double arm3 arm0 block2)
(requires block9 suction)
(has_effector arm2 suction)
(on_block block11 block5)
(on_table block3)
(has_effector arm1 magnetic)
(has_effector arm3 friction)
(has_effector arm3 magnetic)
(has_effector arm5 friction)
(has_effector arm5 magnetic)
(has_effector arm6 suction)
(on_block block9 block4)
(on_table block14)
(on_block block7 block14)
(on_table block8)
(on_block block13 block8)
(on_block block6 block12)
(on_block block1 block7)
(on_block block0 block13)
(on_table block10)
(on_block block4 block10)
(on_block block5 block3)
(=(block_height block0) 2.0000)
(=(block_height block1) 2.0000)
(=(block_height block2) 3.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 1.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 0.0000)
(=(block_height block9) 2.0000)
(=(block_height block10) 0.0000)
(=(block_height block11) 2.0000)
(=(block_height block12) 0.0000)
(=(block_height block13) 1.0000)
(=(block_height block14) 0.0000)
(=(max_on_table) 6.0000)
(=(num_on_table) 5.0000)
(=(arm_height arm0) 3.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 2.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 2.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 3.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 2.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 1.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 2.0000)
(=(arm_id arm6) 6.0000))
(:goal (and 
(on_block block0 block13)
(on_block block1 block7)
(on_block block11 block5)
(on_block block12 block2)
(on_block block13 block8)
(on_block block4 block10)
(on_block block5 block3)
(on_block block6 block12)
(on_block block7 block14)
(on_block block9 block4)
(on_table block10)
(on_table block14)
(on_table block2)
(on_table block3)
(on_table block8)
)
)
)