(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 arm7 - arm
block13 block6 - double_block
encompass friction magnetic suction - effector
block0 block1 block10 block11 block12 block14 block2 block3 block4 block5 block7 block8 block9 - single_block
)
(:init (clear block2)
(requires block2 suction)
(has_effector arm5 suction)
(empty arm5)
(requires block5 encompass)
(has_effector arm5 encompass)
(not_moving arm5)
(clear block4)
(requires block4 magnetic)
(has_effector arm5 magnetic)
(requires block0 friction)
(requires block1 encompass)
(on_table block0)
(on_table block3)
(requires block3 suction)
(on_table block6)
(requires block6 friction)
(on_block block7 block6)
(requires block7 magnetic)
(clear block8)
(on_block block8 block7)
(requires block8 friction)
(on_table block9)
(requires block9 encompass)
(on_block block10 block9)
(requires block10 friction)
(clear block11)
(on_block block11 block10)
(requires block11 suction)
(on_table block12)
(requires block12 friction)
(on_block block13 block12)
(requires block13 suction)
(clear block14)
(on_block block14 block13)
(requires block14 friction)
(empty arm0)
(not_moving arm0)
(has_effector arm0 encompass)
(has_effector arm0 magnetic)
(empty arm1)
(not_moving arm1)
(has_effector arm1 encompass)
(has_effector arm1 magnetic)
(has_effector arm1 suction)
(empty arm2)
(not_moving arm2)
(has_effector arm2 friction)
(has_effector arm2 encompass)
(has_effector arm2 magnetic)
(has_effector arm2 suction)
(empty arm3)
(not_moving arm3)
(has_effector arm3 friction)
(has_effector arm3 encompass)
(empty arm4)
(not_moving arm4)
(has_effector arm4 encompass)
(has_effector arm4 magnetic)
(has_effector arm4 suction)
(has_effector arm5 friction)
(empty arm6)
(not_moving arm6)
(has_effector arm6 friction)
(has_effector arm6 encompass)
(has_effector arm6 suction)
(empty arm7)
(not_moving arm7)
(has_effector arm7 friction)
(has_effector arm7 encompass)
(has_effector arm7 suction)
(on_table block5)
(on_block block2 block5)
(clear block0)
(on_block block1 block3)
(on_block block4 block1)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 1.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 2.0000)
(=(block_height block5) 0.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 2.0000)
(=(block_height block9) 0.0000)
(=(block_height block10) 1.0000)
(=(block_height block11) 2.0000)
(=(block_height block12) 0.0000)
(=(block_height block13) 1.0000)
(=(block_height block14) 2.0000)
(=(max_on_table) 6.0000)
(=(num_on_table) 6.0000)
(=(arm_height arm0) 1.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 0.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 2.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 3.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 1.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 2.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 2.0000)
(=(arm_id arm6) 6.0000)
(=(arm_height arm7) 2.0000)
(=(arm_id arm7) 7.0000))
(:goal (and 
(on_block block1 block3)
(on_block block10 block13)
(on_block block13 block11)
(on_block block14 block9)
(on_block block4 block1)
(on_block block9 block0)
(on_table block0)
(on_table block11)
(on_table block3)
)
)
)