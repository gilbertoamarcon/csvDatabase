(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm1 arm4 - arm
block0 block1 block11 block9 - double_block
encompass friction magnetic suction - effector
block10 block12 block13 block14 block2 block3 block4 block5 block6 block7 block8 - single_block
)
(:init (empty arm4)
(clear block2)
(requires block2 friction)
(has_effector arm4 friction)
(clear block5)
(requires block5 encompass)
(empty arm1)
(clear block1)
(on_block block1 block0)
(requires block1 friction)
(has_effector arm1 friction)
(not_moving arm1)
(not_moving arm4)
(requires block4 magnetic)
(requires block14 suction)
(has_effector arm1 suction)
(requires block13 friction)
(on_block block5 block3)
(requires block0 suction)
(on_table block6)
(requires block6 friction)
(requires block3 encompass)
(on_block block2 block14)
(requires block8 encompass)
(on_block block14 block4)
(clear block7)
(requires block7 encompass)
(on_table block0)
(on_table block9)
(requires block9 magnetic)
(on_block block10 block9)
(requires block10 encompass)
(clear block11)
(on_block block11 block10)
(requires block11 friction)
(on_table block12)
(requires block12 friction)
(has_effector arm1 encompass)
(has_effector arm4 encompass)
(has_effector arm4 suction)
(on_table block13)
(on_block block3 block13)
(on_table block4)
(clear block6)
(on_block block7 block12)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 2.0000)
(=(block_height block3) 1.0000)
(=(block_height block4) 0.0000)
(=(block_height block5) 2.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 2.0000)
(=(block_height block9) 0.0000)
(=(block_height block10) 1.0000)
(=(block_height block11) 2.0000)
(=(block_height block12) 0.0000)
(=(block_height block13) 0.0000)
(=(block_height block14) 1.0000)
(=(max_on_table) 6.0000)
(=(num_on_table) 6.0000)
(=(arm_height arm1) 1.0000)
(=(arm_id arm1) 1.0000)
(=(arm_height arm4) 2.0000)
(=(arm_id arm4) 4.0000))
(:goal (and 
(on_block block1 block8)
(on_block block10 block7)
(on_block block11 block1)
(on_block block14 block4)
(on_block block2 block14)
(on_block block3 block13)
(on_block block5 block3)
(on_block block7 block6)
(on_table block13)
(on_table block4)
(on_table block6)
(on_table block8)
)
)
)