(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 - arm
block0 block11 block12 block14 block2 block8 block9 - double_block
encompass friction magnetic suction - effector
block1 block10 block13 block3 block4 block5 block6 block7 - single_block
)
(:init (empty arm1)
(not_moving arm1)
(empty arm5)
(not_moving arm5)
(empty arm4)
(not_moving arm4)
(requires block5 encompass)
(has_effector arm5 encompass)
(requires block4 friction)
(has_effector arm4 friction)
(requires block11 encompass)
(has_effector arm4 encompass)
(has_effector arm1 friction)
(clear block8)
(requires block8 friction)
(clear block2)
(requires block2 suction)
(has_effector arm5 suction)
(has_effector arm1 suction)
(requires block0 magnetic)
(on_table block3)
(requires block3 suction)
(clear block1)
(requires block1 suction)
(requires block14 friction)
(on_block block1 block7)
(requires block7 magnetic)
(has_effector arm1 magnetic)
(on_table block0)
(on_table block6)
(requires block6 encompass)
(on_table block9)
(requires block9 suction)
(on_block block10 block9)
(requires block10 encompass)
(on_table block12)
(requires block12 magnetic)
(on_block block13 block12)
(requires block13 encompass)
(empty arm0)
(not_moving arm0)
(has_effector arm0 friction)
(has_effector arm0 suction)
(has_effector arm1 encompass)
(empty arm2)
(not_moving arm2)
(has_effector arm2 friction)
(has_effector arm2 magnetic)
(has_effector arm2 suction)
(empty arm3)
(not_moving arm3)
(has_effector arm3 encompass)
(has_effector arm3 suction)
(empty arm6)
(not_moving arm6)
(has_effector arm6 friction)
(on_block block5 block3)
(on_block block11 block5)
(on_block block4 block10)
(on_block block8 block11)
(on_block block2 block4)
(clear block0)
(clear block13)
(on_table block14)
(clear block6)
(on_block block7 block14)
(=(block_height block0) 0.0000)
(=(block_height block1) 2.0000)
(=(block_height block2) 3.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 2.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 3.0000)
(=(block_height block9) 0.0000)
(=(block_height block10) 1.0000)
(=(block_height block11) 2.0000)
(=(block_height block12) 0.0000)
(=(block_height block13) 1.0000)
(=(block_height block14) 0.0000)
(=(max_on_table) 6.0000)
(=(num_on_table) 6.0000)
(=(arm_height arm0) 0.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 1.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 0.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 2.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 0.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 2.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 3.0000)
(=(arm_id arm6) 6.0000))
(:goal (and 
(on_block block0 block13)
(on_block block1 block7)
(on_block block11 block5)
(on_block block12 block2)
(on_block block13 block8)
(on_block block5 block3)
(on_block block6 block12)
(on_block block7 block14)
(on_table block14)
(on_table block2)
(on_table block3)
(on_table block8)
)
)
)