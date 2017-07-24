(define (domain blocksworld)
(:requirements :fluents :durative-actions :typing)
(:types
block effector - object
    single_block double_block - block
agent - object
arm - agent
)

(:predicates
    (has_effector ?a - arm ?e - effector)
    (empty ?a - arm)
    (not_moving ?a - arm)

    (requires ?b - block ?e - effector)

    (clear ?b - block)
    (on_block ?b_1 - block ?b_2 - block)
    (on_table ?b - block)
    (holding_single ?a - arm ?b - single_block)
    (holding_double ?a_1 - arm ?a_2 - arm ?b - double_block)
  )
(:functions
    (block_height ?b - block)
    (arm_height ?a - arm)
    (arm_id ?a - arm)
    (max_on_table)
    (num_on_table)
  )
(:durative-action move-up
  :parameters (?a - arm )
:duration (= ?duration 1)
    :condition
      (and
        (at start (not_moving ?a))
        (over all (empty ?a))
      )
    :effect
      (and
        (at start (not (not_moving ?a)))
        (at end (not_moving ?a))
        (at end (increase (arm_height ?a) 1))
      )
)

(:durative-action move-down
  :parameters (?a - arm )
:duration (= ?duration 1)
    :condition
      (and
        (at start (not_moving ?a))
        (over all (empty ?a))
        (at start (> (arm_height ?a) 0))
      )
    :effect
      (and
        (at start (not (not_moving ?a)))
        (at end (not_moving ?a))
        (at end (decrease (arm_height ?a) 1))
      )
)

(:durative-action move-up-with-single-block
  :parameters (?a - arm ?b - single_block)
:duration (= ?duration 1)
    :condition
      (and
        (over all (holding_single ?a ?b))
        (at start (not_moving ?a))
      )
    :effect
      (and
        (at start (not (not_moving ?a)))
        (at end (not_moving ?a))
        (at end (increase (arm_height ?a) 1))
        (at end (increase (block_height ?b) 1))
      )
)

(:durative-action move-down-with-single-block
  :parameters (?a - arm ?b - single_block)
:duration (= ?duration 1)
    :condition
      (and
        (over all (holding_single ?a ?b))
        (at start (not_moving ?a))
        (at start (> (arm_height ?a) 0))
      )
    :effect
      (and
        (at start (not (not_moving ?a)))
        (at end (not_moving ?a))
        (at end (decrease (arm_height ?a) 1))
        (at end (decrease (block_height ?b) 1))
      )
)

(:durative-action move-up-with-double-block
  :parameters (?a_1 - arm ?a_2 - arm ?b - double_block)
:duration (= ?duration 1)
    :condition
      (and
        (over all (holding_double ?a_1 ?a_2 ?b))
        (at start (not_moving ?a_1))
        (at start (not_moving ?a_2))
      )
    :effect
      (and
        (at start (not (not_moving ?a_1)))
        (at start (not (not_moving ?a_2)))
        (at end (not_moving ?a_1))
        (at end (not_moving ?a_2))
        (at end (increase (arm_height ?a_1) 1))
        (at end (increase (arm_height ?a_2) 1))
        (at end (increase (block_height ?b) 1))
      )
)

(:durative-action move-down-with-double-block
  :parameters (?a_1 - arm ?a_2 - arm ?b - double_block)
:duration (= ?duration 1)
    :condition
      (and
        (over all (holding_double ?a_1 ?a_2 ?b))
        (at start (not_moving ?a_1))
        (at start (not_moving ?a_2))
      )
    :effect
      (and
        (at start (not (not_moving ?a_1)))
        (at start (not (not_moving ?a_2)))
        (at end (not_moving ?a_1))
        (at end (not_moving ?a_2))
        (at end (decrease (arm_height ?a_1) 1))
        (at end (decrease (arm_height ?a_2) 1))
        (at end (decrease (block_height ?b) 1))
      )
)

(:durative-action pick-single-block-on-block
  :parameters (?a - arm ?b_1 - single_block ?b_2 - block ?e - effector)
:duration (= ?duration 1)
    :condition
      (and
        (at start (empty ?a))
        (at start (= (arm_height ?a) (block_height ?b_1)))
        (at start (clear ?b_1))
        (at start (on_block ?b_1 ?b_2))
        (at start (requires ?b_1 ?e))
        (at start (has_effector ?a ?e))
      )
    :effect
      (and
        (at start (not (empty ?a)))
        (at start (not (clear ?b_1)))
        (at start (not (on_block ?b_1 ?b_2)))
        (at end (clear ?b_2))
        (at end (holding_single ?a ?b_1))
      )
)

(:durative-action pick-single-block-on-table
  :parameters (?a - arm ?b - single_block ?e - effector)
:duration (= ?duration 1)
    :condition
      (and
        (at start (empty ?a))
        (at start (= (arm_height ?a) 0))
        (at start (clear ?b))
        (at start (on_table ?b))
        (at start (requires ?b ?e))
        (at start (has_effector ?a ?e))
      )
    :effect
      (and
        (at start (not (empty ?a)))
        (at start (not (clear ?b)))
        (at end (not (on_table ?b)))
        (at end (holding_single ?a ?b))
        (at end (decrease (num_on_table) 1))
      )
)

(:durative-action place-single-block-on-block
  :parameters (?a - arm ?b_1 - single_block ?b_2 - block)
:duration (= ?duration 1)
    :condition
      (and
        (at start (= (arm_height ?a) (+ (block_height ?b_2) 1)))
        (at start (clear ?b_2))
        (at start (holding_single ?a ?b_1))
      )
    :effect
      (and
        (at start (not (clear ?b_2)))
        (at end (clear ?b_1))
        (at end (on_block ?b_1 ?b_2))
        (at start (not (holding_single ?a ?b_1)))
        (at end (empty ?a))
      )
)

(:durative-action place-single-block-on-table
  :parameters (?a - arm ?b - single_block)
:duration (= ?duration 1)
    :condition
      (and
        (at start (= (arm_height ?a) 0))
        (at start (holding_single ?a ?b))
        (at start (< (num_on_table) (max_on_table)))
      )
    :effect
      (and
        (at end (clear ?b))
        (at start (not (holding_single ?a ?b)))
        (at end (empty ?a))
        (at end (on_table ?b))
        (at start (increase (num_on_table) 1))
      )
)

(:durative-action pick-double-block-on-block
  :parameters (?a_1 - arm ?a_2 - arm ?b_1 - double_block ?b_2 - block ?e - effector)
:duration (= ?duration 2)
    :condition
      (and
        (at start (empty ?a_1))
        (at start (empty ?a_2))
        (at start (= (arm_height ?a_1) (block_height ?b_1)))
        (at start (= (arm_height ?a_2) (block_height ?b_1)))
        (at start (clear ?b_1))
        (at start (on_block ?b_1 ?b_2))
        (at start (requires ?b_1 ?e))
        (at start (has_effector ?a_1 ?e))
        (at start (has_effector ?a_2 ?e))
        (at start (> (arm_id ?a_1) (arm_id ?a_2)))
      )
    :effect
      (and
        (at start (not (empty ?a_1)))
        (at start (not (empty ?a_2)))
        (at start (not (clear ?b_1)))
        (at start (not (on_block ?b_1 ?b_2)))
        (at end (clear ?b_2))
        (at end (holding_double ?a_1 ?a_2 ?b_1))
      )
)

(:durative-action pick-double-block-on-table
  :parameters (?a_1 - arm ?a_2 - arm ?b - double_block ?e - effector)
:duration (= ?duration 2)
    :condition
      (and
        (at start (empty ?a_1))
        (at start (empty ?a_2))
        (at start (= (arm_height ?a_1) 0))
        (at start (= (arm_height ?a_2) 0))
        (at start (clear ?b))
        (at start (on_table ?b))
        (at start (requires ?b ?e))
        (at start (has_effector ?a_1 ?e))
        (at start (has_effector ?a_2 ?e))
        (at start (> (arm_id ?a_1) (arm_id ?a_2)))
      )
    :effect
      (and
        (at start (not (empty ?a_1)))
        (at start (not (empty ?a_2)))
        (at start (not (clear ?b)))
        (at end (not (on_table ?b)))
        (at end (holding_double ?a_1 ?a_2 ?b))
        (at end (decrease (num_on_table) 1))
      )
)

(:durative-action place-double-block-on-block
  :parameters (?a_1 - arm ?a_2 - arm ?b_1 - double_block ?b_2 - block)
:duration (= ?duration 2)
    :condition
      (and
        (at start (= (arm_height ?a_1) (+ (block_height ?b_2) 1)))
        (at start (= (arm_height ?a_2) (+ (block_height ?b_2) 1)))
        (at start (clear ?b_2))
        (at start (holding_double ?a_1 ?a_2 ?b_1))
      )
    :effect
      (and
        (at start (not (clear ?b_2)))
        (at end (clear ?b_1))
        (at start (not (holding_double ?a_1 ?a_2 ?b_1)))
        (at end (on_block ?b_1 ?b_2))
        (at end (empty ?a_1))
        (at end (empty ?a_2))
      )
)

(:durative-action place-double-block-on-table
  :parameters (?a_1 - arm ?a_2 - arm ?b - double_block)
:duration (= ?duration 2)
    :condition
      (and
        (at start (= (arm_height ?a_1) 0))
        (at start (= (arm_height ?a_2) 0))
        (at start (holding_double ?a_1 ?a_2 ?b))
        (at start (< (num_on_table) (max_on_table)))
      )
    :effect
      (and
        (at end (clear ?b))
        (at start (not (holding_double ?a_1 ?a_2 ?b)))
        (at end (on_table ?b))
        (at end (empty ?a_1))
        (at end (empty ?a_2))
        (at start (increase (num_on_table) 1))
      )
)

)
