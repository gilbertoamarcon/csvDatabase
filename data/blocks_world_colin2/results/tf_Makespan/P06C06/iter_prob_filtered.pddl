(define (problem blocksworldprob)
(:domain blocksworld)
(:objects arm4 arm5 - arm
block0 block11 block7 - double_block
encompass friction magnetic suction - effector
block1 block10 block2 block3 block4 block5 block6 block8 block9 - single_block
)
(:init (requires block1 suction)
(has_effector arm4 suction)
(clear block2)
(requires block2 encompass)
(clear block8)
(requires block8 encompass)
(has_effector arm5 encompass)
(requires block5 friction)
(requires block11 magnetic)
(has_effector arm5 magnetic)
(requires block0 friction)
(on_table block3)
(on_block block8 block4)
(requires block10 friction)
(on_block block2 block7)
(requires block7 encompass)
(clear block9)
(requires block9 magnetic)
(on_table block0)
(requires block3 encompass)
(on_block block4 block3)
(requires block4 suction)
(on_table block6)
(requires block6 friction)
(not_moving arm4)
(has_effector arm4 encompass)
(has_effector arm4 magnetic)
(not_moving arm5)
(has_effector arm5 friction)
(has_effector arm5 suction)
(holding_single arm4 block1)
(on_block block5 block0)
(on_table block10)
(clear block6)
(on_block block7 block10)
(on_block block9 block5)
(=(block_height block0) 0.0000)
(=(block_height block1) 1.0000)
(=(block_height block2) 2.0000)
(=(block_height block3) 0.0000)
(=(block_height block4) 1.0000)
(=(block_height block5) 1.0000)
(=(block_height block6) 0.0000)
(=(block_height block7) 1.0000)
(=(block_height block8) 2.0000)
(=(block_height block9) 2.0000)
(=(block_height block10) 0.0000)
(=(block_height block11) 2.0000)
(=(max_on_table) 5.0000)
(=(num_on_table) 4.0000)
(=(arm_height arm4) 1.0000)
(=(arm_id arm4) 4.0000)
(=(arm_height arm5) 2.0000)
(=(arm_id arm5) 5.0000))
(:goal (and 
(= (block_height block0) 0)
(= (block_height block1) 0)
(= (block_height block10) 0)
(= (block_height block11) 1)
(= (block_height block2) 2)
(= (block_height block5) 1)
(= (block_height block6) 2)
(= (block_height block7) 1)
(= (block_height block9) 2)
(on_block block11 block1)
(on_block block2 block7)
(on_block block5 block0)
(on_block block6 block11)
(on_block block7 block10)
(on_block block9 block5)
(on_table block0)
(on_table block1)
(on_table block10)
)
)
)