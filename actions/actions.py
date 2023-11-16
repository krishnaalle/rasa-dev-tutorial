import psycopg2
import json
import requests
import re
from typing import Any, Text, Dict, List, Union
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
# from scripts.resume_analysis import calculate_overall_score, python_dev_word_list
# from scripts.answer_analysis import answer_score
# from scripts.video_analysis import download_answer_video
# from templates.quick_reply import add_quick_reply

# def send_api_request():
#     db_credentials = {
#     'host': '127.0.0.1',
#     'database': 'flexydial',
#     'user': 'flexydial',
#     'password': 'flexydial',
#     }

#     conn = psycopg2.connect(db_credentials)

#     cursor = conn.cursor()

#     query = "SELECT * FROM crm_contact"

#     cursor.execute(query)

#     rows = cursor.fetchall()

#     for row in rows:
#         print(row)
#         row

#     cursor.close()
#     conn.close()

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="action_hello_world")
        dispatcher.utter_message(text="Actions called.")

        return []
class ActionCustomerDetails(Action):

    def name(self) -> Text:
        return "action_customer_details_request"
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "phone_number": self.from_text(),
            "customer_id": self.from_text()  # Map the "customer_id" slot to a text input
        }

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="action_customer_details_request")
        text = "Sure ! I can help you with that."
        text1 = "Enter mobile number of the customer"
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text=text1)
        return []

class UserForm(FormAction):
    def name(self) -> Text:
        return "user_form"
    
    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["customer_id"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "customer_id": self.from_text()
        }

    def validate_customer_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> Dict[Text, Any]:

        print(f"Input value: {value}")  # Debug print to check the input value

        phone_num_pattern = re.compile(r"[+]?[0-9]{10}")
        is_valid_phone_num = phone_num_pattern.search(value)
        
        print(f"Regex match result: {is_valid_phone_num}")  # Debug print to check regex match result

        if is_valid_phone_num:
            return {"customer_id": value}
        else:
            enter_valid_customer_id = "Please enter a valid customer ID. (for example: 9987456432)"
            dispatcher.utter_message(text=enter_valid_customer_id)
            return {"customer_id": None}
        
    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        customer_id = tracker.get_slot("customer_id")
        self.saved_customer_id = customer_id
        # dispatcher.utter_message(f"Customer ID {customer_id} has been saved.")
        return []
    
class ActionConfirmId(Action):

    def name(self) -> Text:
        return "action_confirm_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        customer_id = tracker.get_slot("customer_id")
        data = [
            {
                "title": "✅ continue",
                "payload": "/affirm"
            },
            {
                "title": "❌ reEnter",
                "payload": "/deny"
            }
        ]
        message = {"payload": "quickReplies", "data": data}
        if tracker.latest_message['intent'].get('name') == 'deny':
            return [AllSlotsReset(), ActionCustomerDetails()]
        dispatcher.utter_message(text=f"check your entered id {customer_id}", buttons=data)

        return []

class SendApiRequest(Action):
    def name(self) -> Text:
        return "action_send_api_request"

    def run(self, dispatcher, tracker, domain):
        # Get database credentials from environment variables or a secure configuration
        
        db_params = {
			'dbname': 'crm',
			'user': 'flexydial',
			'password': 'flexydial',
			'host': '10.12.0.20',
			'port': '5432'
		}
        customer_id = tracker.get_slot("customer_id")

        print("called actions")

        # Initialize variables to None
        conn = None
        cur = None
        data = None

        try:
            # Establish a database connection
            # conn = psycopg2.connect(**db_credentials)
            conn = psycopg2.connect(**db_params)
            
            cur = conn.cursor()

            # Example query to select data from the 'crm_contact' table
            query = f"SELECT first_name, last_name FROM crm_contact WHERE numeric::bigint = {customer_id}::bigint;"
            cur.execute(query)

            # Fetch all the rows from the result set
            rows = cur.fetchall()
            
            for row in rows:
                print(row)
            # You can do something with the fetched data here
            data = rows
        except Exception as e:
            # asb
            # Handle database connection errors
            print(f"Error connecting to the database: {e}")
        finally:
            # Close the cursor and connection in a 'finally' block to ensure it happens even if an exception occurs
            if cur:
                cur.close()
            if conn:
                conn.close()
        if data:
            dispatcher.utter_message(f"I found the user named {data}")
            dispatcher.utter_message(f"What details would you like to know about {data}?")
        else:
            dispatcher.utter_message("No user found with that mobile number")

        # Set the fetched data as a slot for future reference
        return [SlotSet("fetched_data", data)]
    
class ActionEndChat(Action):
    def name(self) -> Text:
        return "action_end_chat"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Ending the chat. If you have more questions, feel free to ask!")
        return [AllSlotsReset()]


# class SendApiRequestWithID(Action):
#     def name(self) -> Text:
#         return "action_customer_details_with_id"

#     def run(self, dispatcher, tracker, domain):
#         # Get database credentials from environment variables or a secure configuration
        
#         db_params = {
# 			'dbname': 'crm',
# 			'user': 'flexydial',
# 			'password': 'flexydial',
# 			'host': '10.12.0.20',
# 			'port': '5432'
# 		}
        
#         customer_id = tracker.latest_message.get("entities", {}).get("customer_id", None)
#         if customer_id:
#             dispatcher.utter_message(f"What details would you like to know about {customer_id}?")
#             return [SlotSet("customer_id", customer_id)]
            
#         else:
#             dispatcher.utter_message("No customer ID found in the user's message.")

#         # Initialize variables to None
#         conn = None
#         cur = None
#         data = None

#         try:
#             # Establish a database connection
#             conn = psycopg2.connect(**db_params)
#             cur = conn.cursor()

#             # Example query to select data from the 'crm_contact' table
#             query = f"SELECT first_name, last_name FROM crm_contact WHERE numeric::bigint = {customer_id}::bigint;"
#             cur.execute(query)

#             # Fetch all the rows from the result set
#             rows = cur.fetchall()
            
#             for row in rows:
#                 print(row)
#             # You can do something with the fetched data here
#             data = rows
#         except Exception as e:
#             # asb
#             # Handle database connection errors
#             print(f"Error connecting to the database: {e}")
#         finally:
#             # Close the cursor and connection in a 'finally' block to ensure it happens even if an exception occurs
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#         if data:
#             dispatcher.utter_message(f"I found the user named {data}")
#             dispatcher.utter_message(f"What details would you like to know about {data}?")
#         else:
#             dispatcher.utter_message("No user found with that mobile number")

#         # Set the fetched data as a slot for future reference
#         return [SlotSet("customer_name", data)]
    
class ActionGetDisposition(Action):
    def name(self) -> Text:
        return "action_get_disposition"

    def run(self, dispatcher, tracker, domain):
        # Get database credentials from environment variables or a secure configuration
        
        db_params = {
			'dbname': 'crm',
			'user': 'flexydial',
			'password': 'flexydial',
			'host': '10.12.0.20',
			'port': '5432'
		}
        customer_id = tracker.get_slot("customer_id")
        if customer_id is None:
            
#################################################################################################################################################################
            data = get_disposition()
        # Initialize variables to None
        conn = None
        cur = None
        data = None

        try:
            # Establish a database connection
            # conn = psycopg2.connect(**db_credentials)
            conn = psycopg2.connect(**db_params)
            
            cur = conn.cursor()

            # Example query to select data from the 'crm_contact' table
            query = f"SELECT disposition FROM crm_contact WHERE numeric::bigint = {customer_id}::bigint;"
            cur.execute(query)

            # Fetch all the rows from the result set
            rows = cur.fetchall()
            
            for row in rows:
                print(row)
            # You can do something with the fetched data here
            data = rows
        except Exception as e:
            # asb
            # Handle database connection errors
            print(f"Error connecting to the database: {e}")
        finally:
            # Close the cursor and connection in a 'finally' block to ensure it happens even if an exception occurs
            if cur:
                cur.close()
            if conn:
                conn.close()
        if data:
            dispatcher.utter_message(f"I found the previous disposition as {data}")
        else:
            dispatcher.utter_message("No user found with that mobile number")

        # Set the fetched data as a slot for future reference
        return [SlotSet("disposition", data)]
    