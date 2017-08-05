(define (domain zenotravel)
(:requirements :fluents :durative-actions :typing :action-costs)
(:types
transportable city - object
    passenger cargo - transportable
    hub spoke - city
agent - object
airplane - agent
    large_plane small_plane - airplane
)

(:predicates
    (transportable_at_city ?t - transportable ?c - city)
    (transportable_on_plane ?t - transportable ?p - airplane)
    (plane_at_city ?a - airplane ?c - city)
    (not_managing_passenger ?a - airplane)
    (not_managing_cargo ?a - airplane)
  )
(:functions
    (total-cost)
    (fuel ?a - airplane)
    (fuel_rate ?a - airplane)
    (max_fuel ?a - airplane)
    (speed ?a - airplane)
    (distance ?c_1 - city ?c_2 - city)
    (num_passengers ?a - airplane)
    (max_passengers ?a - airplane)
    (num_cargo ?a - airplane)
    (max_cargo ?a - airplane)
    (zoom_fuel_factor)
    (zoom_speed_factor)
  )
(:durative-action refuel
  :parameters (?p - airplane ?c - city)
:duration (= ?duration (/ (- (max_fuel ?p) (fuel ?p)) (fuel_rate ?p)))
    :condition
      (and
        (over all (plane_at_city ?p ?c))
      )
    :effect
      (and
        (at end (assign (fuel ?p) (max_fuel ?p)))
      )
)

(:durative-action fly_small_1
  :parameters (?p - small_plane ?c_1 - city ?c_2 - city)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (speed ?p)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_1))
        (at start (>= (fuel ?p) (distance ?c_1 ?c_2)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_1)))
        (at end (plane_at_city ?p ?c_2))
        (decrease (fuel ?p) (* #t (speed ?p)))
      )
)

(:durative-action zoom_small_1
  :parameters (?p - small_plane ?c_1 - city ?c_2 - city)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (* (speed ?p) zoom_speed_factor)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_1))
        (at start (>= (fuel ?p) (* (distance ?c_1 ?c_2) zoom_fuel_factor)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_1)))
        (at end (plane_at_city ?p ?c_2))
        (decrease (fuel ?p) (* #t (* zoom_fuel_factor (speed ?p))))
      )
)

(:durative-action fly_small_2
  :parameters (?p - small_plane ?c_2 - city ?c_1 - city)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (speed ?p)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_2))
        (at start (>= (fuel ?p) (distance ?c_1 ?c_2)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_2)))
        (at end (plane_at_city ?p ?c_1))
        (decrease (fuel ?p) (* #t (speed ?p)))
      )
)

(:durative-action zoom_small_2
  :parameters (?p - small_plane ?c_2 - city ?c_1 - city)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (* (speed ?p) zoom_speed_factor)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_2))
        (at start (>= (fuel ?p) (* (distance ?c_1 ?c_2) zoom_fuel_factor)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_2)))
        (at end (plane_at_city ?p ?c_1))
        (decrease (fuel ?p) (* #t (* zoom_fuel_factor (speed ?p))))
      )
)

(:durative-action fly_large_1
  :parameters (?p - large_plane ?c_1 - hub ?c_2 - hub)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (speed ?p)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_1))
        (at start (>= (fuel ?p) (distance ?c_1 ?c_2)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_1)))
        (at end (plane_at_city ?p ?c_2))
        (decrease (fuel ?p) (* #t (speed ?p)))
      )
)

(:durative-action zoom_large_1
  :parameters (?p - large_plane ?c_1 - hub ?c_2 - hub)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (* (speed ?p) zoom_speed_factor)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_1))
        (at start (>= (fuel ?p) (* (distance ?c_1 ?c_2) zoom_fuel_factor)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_1)))
        (at end (plane_at_city ?p ?c_2))
        (decrease (fuel ?p) (* #t (* zoom_fuel_factor (speed ?p))))
      )
)

(:durative-action fly_large_2
  :parameters (?p - large_plane ?c_2 - hub ?c_1 - hub)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (speed ?p)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_2))
        (at start (>= (fuel ?p) (distance ?c_1 ?c_2)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_2)))
        (at end (plane_at_city ?p ?c_1))
        (decrease (fuel ?p) (* #t (speed ?p)))
      )
)

(:durative-action zoom_large_2
  :parameters (?p - large_plane ?c_2 - hub ?c_1 - hub)
:duration (= ?duration (/ (distance ?c_1 ?c_2) (* (speed ?p) zoom_speed_factor)))
    :condition
      (and
        (at start (plane_at_city ?p ?c_2))
        (at start (>= (fuel ?p) (* (distance ?c_1 ?c_2) zoom_fuel_factor)))
      )
    :effect
      (and
        (at start (increase (total-cost) 1))
        (at start (not (plane_at_city ?p ?c_2)))
        (at end (plane_at_city ?p ?c_1))
        (decrease (fuel ?p) (* #t (* zoom_fuel_factor (speed ?p))))
      )
)

(:durative-action load_passenger
  :parameters (?a - airplane ?c - city ?t - passenger)
:duration (= ?duration 1)
    :condition
      (and
        (at start (transportable_at_city ?t ?c))
        (at start (< (num_passengers ?a) (max_passengers ?a)))
        (at start (not_managing_passenger ?a))
        (over all (plane_at_city ?a ?c))
      )
    :effect
      (and
        (at start (not (not_managing_passenger ?a)))
        (at start (not (transportable_at_city ?t ?c)))
        (at start (increase (num_passengers ?a) 1))
        (at end (transportable_on_plane ?t ?a))
        (at end (not_managing_passenger ?a))
      )
)

(:durative-action unload_passenger
  :parameters (?a - airplane ?c - city ?t - passenger)
:duration (= ?duration 1)
    :condition
      (and
        (at start (transportable_on_plane ?t ?a))
        (at start (not_managing_passenger ?a))
        (over all (plane_at_city ?a ?c))
      )
    :effect
      (and
        (at start (not (not_managing_passenger ?a)))
        (at start (not (transportable_on_plane ?t ?a)))
        (at end (decrease (num_passengers ?a) 1))
        (at end (transportable_at_city ?t ?c))
        (at end (not_managing_passenger ?a))
      )
)

(:durative-action load_cargo
  :parameters (?a - airplane ?c - city ?t - cargo)
:duration (= ?duration 1)
    :condition
      (and
        (at start (transportable_at_city ?t ?c))
        (at start (< (num_cargo ?a) (max_cargo ?a)))
        (at start (not_managing_cargo ?a))
        (over all (plane_at_city ?a ?c))
      )
    :effect
      (and
        (at start (not (not_managing_cargo ?a)))
        (at start (not (transportable_at_city ?t ?c)))
        (at start (increase (num_cargo ?a) 1))
        (at end (transportable_on_plane ?t ?a))
        (at end (not_managing_cargo ?a))
      )
)

(:durative-action unload_cargo
  :parameters (?a - airplane ?c - city ?t - cargo)
:duration (= ?duration 1)
    :condition
      (and
        (at start (transportable_on_plane ?t ?a))
        (at start (not_managing_cargo ?a))
        (over all (plane_at_city ?a ?c))
      )
    :effect
      (and
        (at start (not (not_managing_cargo ?a)))
        (at start (not (transportable_on_plane ?t ?a)))
        (at end (decrease (num_cargo ?a) 1))
        (at end (transportable_at_city ?t ?c))
        (at end (not_managing_cargo ?a))
      )
)

)
