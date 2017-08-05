(define (domain first_response)
(:requirements :fluents :durative-actions :typing :duration-inequalities :negative-preconditions)
(:types
locatable wpt - object
		fixed movable - locatable
		fire_base police_base hospital battery_charger - fixed
		weapons drugs victim - movable
agent - object
human robot - agent
		ground quadrotor - robot
		policebot firebot emsbot - ground
		firefighter police ems - human
)

(:predicates
		(gas_clear ?wpt - wpt)
		(road ?wpt_a - wpt ?wpt_b - wpt)
		(clear ?wpt_a - wpt ?wpt_b - wpt)
		(located_at ?l - locatable ?wpt - wpt)
		(agent_at ?a - agent ?wpt - wpt)
		(idle ?a - agent)
		(empty ?r - ground)
		(victim_triaged ?v - victim)
		(carrying_weapons ?r - policebot ?w - weapons)
		(carrying_drugs ?r - emsbot ?d - drugs)
		(carrying_victim ?r - emsbot ?v - victim)
		(victim_at_hosp ?v - victim ?hosp - hospital)
		(drugs_stored ?d - drugs ?hosp - hospital)
		(weapons_stored ?w - weapons ?b - police_base)
	)
(:functions
		(power_max ?r - robot)
		(power ?r - robot)
		(victim_injury ?v - victim)
		(victim_state ?v - victim)
	)
(:durative-action change-battery
  :parameters (?r - robot ?b - battery_charger ?wpt - wpt)
:duration (= ?duration 2)
		:condition
		(and
			(over all (agent_at ?r ?wpt))
			(over all (located_at ?b ?wpt))
		)
		:effect
		(and
			(at start (assign (power ?r) 0))
			(at end (assign (power ?r) (power_max ?r)))
		)
)

(:durative-action quad-move
  :parameters (?r - quadrotor ?wpt_a - wpt ?wpt_b - wpt)
:duration (= ?duration 1.0)
		:condition
		(and
			(over all (>= (power ?r) 0))
			(at start (idle ?r))
			(over all (road ?wpt_a ?wpt_b))
			(at start (agent_at ?r ?wpt_a))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (idle ?r)))
			(at start (not (agent_at ?r ?wpt_a)))
			(at end (agent_at ?r ?wpt_b))
			(at end (idle ?r))
		)
)

(:durative-action ground-move
  :parameters (?r - ground ?wpt_a - wpt ?wpt_b - wpt)
:duration (= ?duration 1.0)
		:condition
		(and
			(over all (>= (power ?r) 0))
			(over all (road ?wpt_a ?wpt_b))
			(over all (clear ?wpt_a ?wpt_b))
			(at start (idle ?r))
			(at start (agent_at ?r ?wpt_a))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (idle ?r)))
			(at start (not (agent_at ?r ?wpt_a)))
			(at end (agent_at ?r ?wpt_b))
			(at end (idle ?r))
		)
)

(:durative-action human-move
  :parameters (?h - human ?wpt_a - wpt ?wpt_b - wpt)
:duration (= ?duration 1.0)
		:condition
		(and
			(over all (road ?wpt_a ?wpt_b))
			(over all (clear ?wpt_a ?wpt_b))
			(at start (idle ?h))
			(at start (agent_at ?h ?wpt_a))
		)
		:effect
		(and
			(at start (not (idle ?h)))
			(at start (not (agent_at ?h ?wpt_a)))
			(at end (agent_at ?h ?wpt_b))
			(at end (idle ?h))
		)
)

(:durative-action guide-victim
  :parameters (?r - quadrotor ?v - victim ?wpt_a - wpt ?wpt_b - wpt)
:duration (= ?duration 2.0)
		:condition
		(and
			(over all (>= (power ?r) 0))
			(over all (road ?wpt_a ?wpt_b))
			(over all (clear ?wpt_a ?wpt_b))
			(at start (idle ?r))
			(at start (located_at ?v ?wpt_a))
			(at start (agent_at ?r ?wpt_a))
			(over all (>= (victim_state ?v) 4))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (idle ?r)))
			(at start (not (agent_at ?r ?wpt_a)))
			(at start (not (located_at ?v ?wpt_a)))
			(at end (agent_at ?r ?wpt_b))
			(at end (located_at ?v ?wpt_b))
			(at end (idle ?r))
		)
)

(:durative-action guide-victim-to-hospital
  :parameters (?r - quadrotor ?v - victim ?h - hospital ?wpt - wpt)
:duration (= ?duration 0.5)
		:condition
		(and
			(at start (located_at ?v ?wpt))
			(over all (>= (power ?r) 0))
			(over all (located_at ?h ?wpt))
			(over all (agent_at ?r ?wpt))
			(over all (>= (victim_state ?v) 4))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (located_at ?v ?wpt)))
			(at end (victim_at_hosp ?v ?h))
		)
)

(:durative-action clear-road
  :parameters (?r - firebot ?wpt_a - wpt ?wpt_b - wpt)
:duration (= ?duration 2.0)
		:condition
		(and
			(over all (>= (power ?r) 0))
			(over all (agent_at ?r ?wpt_a))
			(over all (road ?wpt_a ?wpt_b))(over all (road ?wpt_b ?wpt_a))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at end (clear ?wpt_a ?wpt_b))(at end (clear ?wpt_b ?wpt_a))
		)
)

(:durative-action seal-leak
  :parameters (?h - firefighter ?wpt - wpt)
:duration (= ?duration 3.0)
		:condition
		(and
			(over all (agent_at ?h ?wpt))
			(at start (not (gas_clear ?wpt)))
		)
		:effect
		(and
			(at end (gas_clear ?wpt))
		)
)

(:durative-action triage
  :parameters (?h - ems ?v - victim ?wpt - wpt)
:duration (= ?duration 2.0)
		:condition
		(and
			(at start (= (victim_state ?v) 0))
			(over all (agent_at ?h ?wpt))
			(over all (located_at ?v ?wpt))
			(over all (<= (victim_injury ?v) 4))
		)
		:effect
		(and
			(at end (assign (victim_state ?v) (victim_injury ?v)))
		)
)

(:durative-action load-victim
  :parameters (?h - ems ?r - emsbot ?v - victim ?wpt - wpt)
:duration (= ?duration 2.0)
		:condition
		(and
			(at start (located_at ?v ?wpt))
			(at start (empty ?r))
			(over all (>= (power ?r) 0))
			(over all (agent_at ?h ?wpt))
			(over all (agent_at ?r ?wpt))
			(over all (> (victim_state ?v) 0))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (located_at ?v ?wpt)))
			(at start (not (empty ?r)))
			(at end (carrying_victim ?r ?v))
		)
)

(:durative-action unload-victim-at-hospital
  :parameters (?r - emsbot ?v - victim ?wpt - wpt ?hosp - hospital)
:duration (= ?duration 2.0)
		:condition
		(and
			(at start (carrying_victim ?r ?v))
			(over all (>= (power ?r) 0))
			(over all (agent_at ?r ?wpt))
			(over all (located_at ?hosp ?wpt))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (carrying_victim ?r ?v)))
			(at end (victim_at_hosp ?v ?hosp))
			(at end (empty ?r))
		)
)

(:durative-action clear-pawn
  :parameters (?p - police ?r - policebot ?w - weapons ?wpt - wpt)
:duration (= ?duration 5.0)
		:condition
		(and
			(at start (empty ?r))
			(over all (>= (power ?r) 0))
			(over all (agent_at ?p ?wpt))
			(over all (agent_at ?r ?wpt))
			(over all (located_at ?w ?wpt))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (empty ?r)))
			(at end (carrying_weapons ?r ?w))
		)
)

(:durative-action clear-pharmacy
  :parameters (?h - ems ?r - emsbot ?p - drugs ?wpt - wpt)
:duration (= ?duration 5.0)
		:condition
		(and
			(at start (empty ?r))
			(over all (>= (power ?r) 0))
			(over all (agent_at ?h ?wpt))
			(over all (agent_at ?r ?wpt))
			(over all (located_at ?p ?wpt))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (empty ?r)))
			(at end (carrying_drugs ?r ?p))
		)
)

(:durative-action drop-weapons
  :parameters (?r - policebot ?w - weapons ?b - police_base ?wpt - wpt)
:duration (= ?duration 1.0)
		:condition
		(and
			(at start (carrying_weapons ?r ?w))
			(over all (>= (power ?r) 0))
			(over all (located_at ?b ?wpt))
			(over all (agent_at ?r ?wpt))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (carrying_weapons ?r ?w)))
			(at end (empty ?r))
			(at end (weapons_stored ?w ?b))
		)
)

(:durative-action drop-drugs
  :parameters (?r - emsbot ?p - drugs ?hosp - hospital ?wpt - wpt)
:duration (= ?duration 1.0)
		:condition
		(and
			(at start (carrying_drugs ?r ?p))
			(over all (>= (power ?r) 0))
			(over all (located_at ?hosp ?wpt))
			(over all (agent_at ?r ?wpt))
		)
		:effect
		(and
			(decrease (power ?r) #t)
			(at start (not (carrying_drugs ?r ?p)))
			(at end (empty ?r))
			(at end (drugs_stored ?p ?hosp))
		)
)

)
