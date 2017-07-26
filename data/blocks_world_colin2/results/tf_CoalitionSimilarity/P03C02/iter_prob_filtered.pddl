(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm0 arm1 arm2 arm3 arm4 arm5 arm6 arm7 - arm
block0 block1 block11 block9 - double_block
encompass friction magnetic suction - effector
block10 block12 block13 block14 block2 block3 block4 block5 block6 block7 block8 - single_block
)
(:init (empty arm1)
(not_moving arm1)
(not_moving arm4)
(clear block3)
(not_moving arm3)
(empty arm3)
(clear block2)
(requires block2 friction)
(has_effector arm3 friction)
(empty arm4)
(requires block4 magnetic)
(has_effector arm4 magnetic)
(not_moving arm0)
(clear block5)
(requires block5 encompass)
(has_effector arm0 encompass)
(requires block1 friction)
(has_effector arm4 friction)
(has_effector arm0 friction)
(empty arm7)
(has_effector arm7 encompass)
(clear block0)
(requires block0 suction)
(has_effector arm4 suction)
(has_effector arm1 suction)
(clear block11)
(requires block11 friction)
(clear block10)
(requires block10 encompass)
(empty arm6)
(not_moving arm6)
(has_effector arm6 encompass)
(on_block block2 block14)
(requires block14 suction)
(has_effector arm0 suction)
(requires block3 encompass)
(on_table block6)
(requires block6 friction)
(on_block block7 block6)
(requires block7 encompass)
(on_table block12)
(requires block13 friction)
(on_block block0 block9)
(has_effector arm7 suction)
(requires block9 magnetic)
(has_effector arm6 magnetic)
(not_moving arm7)
(requires block8 encompass)
(has_effector arm1 encompass)
(holding_single arm0 block13)
(has_effector arm6 suction)
(on_block block11 block1)
(on_table block3)
(requires block12 friction)
(has_effector arm1 magnetic)
(empty arm2)
(not_moving arm2)
(has_effector arm2 encompass)
(has_effector arm2 suction)
(has_effector arm3 suction)
(has_effector arm4 encompass)
(empty arm5)
(not_moving arm5)
(has_effector arm5 encompass)
(on_table block4)
(on_block block1 block8)
(on_block block14 block4)
(on_table block5)
(on_block block9 block12)
(on_block block10 block7)
(on_table block8)
(=(block_height block0) 2.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 2.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 0.0000)
(=(block_height block5) 0.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 0.0000)
(=(block_height block9) 1.0000)
(=(block_height block10) 2.0000)
(=(block_height block11) 2.0000)
(=(block_height block12) 0.0000)
(=(block_height block13) 2.0000)
(=(block_height block14) 1.0000)
(=(max_on_table) 6.0000)
(=(num_on_table) 6.0000)
(=(arm_height arm0) 2.0000)
(=(arm_id arm0) 0.0000)
(=(arm_height arm1) 0.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm2) 0.0000)
(=(arm_id arm2) 2.0000)
(=(arm_height arm3) 2.0000)
(=(arm_id arm3) 3.0000)
(=(arm_height arm4) 2.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 3.0000)
(=(arm_id arm5) 5.0000)
(=(arm_height arm6) 2.0000)
(=(arm_id arm6) 6.0000)
(=(arm_height arm7) 2.0000)
(=(arm_id arm7) 7.0000))
(:goal (and 
(on_block block0 block9)
(on_block block1 block8)
(on_block block10 block7)
(on_block block11 block1)
(on_block block14 block4)
(on_block block2 block14)
(on_block block3 block13)
(on_block block5 block3)
(on_block block7 block6)
(on_block block9 block12)
(on_table block12)
(on_table block13)
(on_table block4)
(on_table block6)
(on_table block8)
)
)
)