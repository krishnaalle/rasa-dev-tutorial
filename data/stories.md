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
  - action_end_chat

## bot challenge
* bot_challenge
  - utter_iamabot

## know_the_user_details successful path
* greet 
  - utter_greet
* customer_details_request
  - action_customer_details_request
  - user_form
  - form{"name":"user_form"}
  - form{"name":null}
  - action_confirm_id
* affirm
  - action_send_api_request
* goodbye
  - action_end_chat
* affirm
  - utter_goodbye


## know_the_user_details reEnter path
* greet 
  - utter_greet
* customer_details_request
  - action_customer_details_request
  - user_form
  - form{"name":"user_form"}
  - form{"name":null}
  - action_confirm_id
* deny
  - action_customer_details_request
  - action_confirm_id

## know_the_user_details out_of_scope path
* greet 
  - utter_greet
* customer_details_request
  - action_customer_details_request
* out_of_scope
  - utter_out_scope

## know_the_user_details continue path
* greet 
  - utter_greet
* customer_details_request
  - action_customer_details_request
* out_of_scope
  - utter_out_scope
* customer_details_request
  - action_customer_details_request
  - user_form
  - form{"name":"user_form"}
  - form{"name":null}
  - action_confirm_id
* affirm
  - action_send_api_request

<!-- ## know_the_customer_details_with ID
* customer_details_request_with_id
  - action_customer_details_with_id -->

## get_the_disposition
* disposition_request
- action_get_disposition

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


## interactive_story_1
* greet
    - utter_greet
* out_of_scope
    - utter_out_scope
* out_of_scope
    - utter_out_scope
* greet
    - utter_greet
* customer_details_request
    - action_customer_details_request
    - user_form
    - action_confirm_id
* goodbye
    - action_end_chat

## interactive_story_1
* customer_details_request
    - action_customer_details_request
    - user_form
    - action_confirm_id
* affirm
    - action_send_api_request
* goodbye
    - action_end_chat

## interactive_story_1
* customer_details_request
    - action_customer_details_request
    - user_form
    - action_confirm_id
* deny
    - action_end_chat
