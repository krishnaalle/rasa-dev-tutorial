## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot


## ask diet questions
* ask_eat_healthy
  - utter_diet_info

## ask_stress_questions
* ask_lower_stress
  - utter_stress_info
<!-- 
## ask_exercise
* ask_exercise
  - action_hello_world -->
  
## ticket booking path 1
* greet
  - action_fallback
  
* ticket_booking
  - utter_ticket_booking
  - utter_collect_from_and_to

* collect_from_and_to
  - utter_know_timings

* know_timings
  - utter_check_availability
  - utter_your_name

* phone_number
  - utter_phone_number

* email_id
  - utter_email_id
  - utter_travel_details

* details_agreed
  - utter_say_thankyou


## interactive_story_1
* greet
    - utter_greet
* ticket_booking
    - utter_ticket_booking
* affirm
    - utter_collect_from_and_to
* collect_from_and_to{"from": "Mumbai", "to": "Hyderabad"}
    - slot{"from": "Mumbai"}
    - slot{"to": "Hyderabad"}
    - utter_know_timings
* know_timings{"time": "11:45AM"}
    - slot{"time": "11:45AM"}
    - utter_check_availability
    - utter_your_name
* collect_name:
    - utter_phone_number
* phone_number:{"phone_number": "2491834124"}
    - slot{"phone_number": "2491834124"}
    - utter_phone_number
* phone_number:{"phone_number": "234121423"}
    - slot{"phone_number": "234121423"}
    - utter_email_id
    - utter_travel_details
* affirm
    - utter_say_thankyou

## interactive_story_1
* greet
    - utter_greet
* ticket_booking
    - utter_ticket_booking
    - utter_collect_from_and_to
* collect_from_and_to{"to": "hyderabad", "from": "mumbai"}
    - slot{"from": "mumbai"}
    - slot{"to": "hyderabad"}
    - utter_know_timings
* know_timings{"time": "11:45AM"}
    - slot{"time": "11:45AM"}
    - utter_check_availability
    - utter_your_name
* collect_name:
    - utter_phone_number
* phone_number:{"phone_number": "314124325435"}
    - slot{"phone_number": "314124325435"}
    - utter_email_id
    - utter_email_id
    - utter_travel_details
* affirm
    - utter_say_thankyou

## interactive_story_1
* greet
    - utter_greet
* ticket_booking
    - utter_ticket_booking
    - utter_collect_from_and_to
* collect_from_and_to{"to": "hyderabad", "from": "mumbai"}
    - slot{"from": "mumbai"}
    - slot{"to": "hyderabad"}
    - utter_know_timings
* know_timings{"time": "11:45AM"}
    - slot{"time": "11:45AM"}
    - utter_check_availability
    - utter_your_name
* collect_name:
    - utter_phone_number
* phone_number:{"phone_number": "234132413414"}
    - slot{"phone_number": "234132413414"}
    - utter_email_id
    - utter_email_id
* email_id:{"email_id": "krishna@gmail.com"}
    - slot{"email_id": "krishna@gmail.com"}
    - utter_email_id
    - utter_travel_details
* affirm
    - utter_say_thankyou
