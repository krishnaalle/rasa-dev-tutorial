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

## ask_exercise
* ask_exercise
  - action_hello_world

## know_the_user_details path
* greet 
  - utter_greet
* customer_details_request
  - user_form
  - form{"name":"user_form"}
  - form{"name":null}
  - utter_form_values
* affirm
  - utter_goodbye 

# successful path
user : Hi
bot: hi how can I help
user: i want to know details of the customer 
bot: provide me the ID
user: 239y492384
bot: I have found the user name RAM with this ID please be specific on what you want know
user: how much he has to pay 
bot: pending amount Rs 12000
user: any offers on his card
bot: I have
user: ok
bot : thank you!

# wrong ID path
user : Hi
bot: hi how can I help
user: i want to know details of the customer 
bot: provide me the ID
user: 239y492384
bot: I haven't found any user

# out of scope path
user : Hi
bot: hi how can I help
user: what is the weather like 
bot: sorry I didn't understand that
bot: please ask questions from crm

# path continue
user : Hi
bot: hi how can I help
user: what is the weather like
bot: sorry I didn't understand that
bot: please ask questions from crm you want to continue 
user : yes 
bot: hi how can I help
user: i want to know details of the customer 
bot: provide me the ID
user: 239y492384
bot: I have found the user name RAM with this ID please be specific on what you want know
user: how much he has to pay 
bot: pending amount Rs 12000
user: any offers on his card
bot: I have found 3
user: ok
bot : thank you!



