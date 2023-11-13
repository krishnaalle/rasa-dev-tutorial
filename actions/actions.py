# import psycopg2
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
#     'host': 'your_host',
#     'database': 'your_database',
#     'user': 'your_user',
#     'password': 'your_password',
#     }

# conn = psycopg2.connect(db_credentials)

# cursor = conn.cursor()

# query = "SELECT * FROM crm_contact"

# cursor.execute(query)

# rows = cursor.fetchall()

# for row in rows:
#     print(row)
#     row

# cursor.close()
# conn.close()

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
        text1 = "Enter 10digits ID of the customer."
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

        phone_num_pattern = re.compile(r"[+]?[0-9]{12}")
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
        dispatcher.utter_message(f"Customer ID {customer_id} has been saved.")
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
        dispatcher.utter_message(text=f"check your entered id {customer_id}", buttons=data)

        return []
    
# class SendApiRequest(Action):
#     def name(self) -> Text:
#         return "action_send_api_request"
    
#     def run(self, dispatcher, tracker, domain):
#         print("Send API request")
#         customer_id = tracker.get_slot("customer_id")
#         # Establish a database connection
        
        

#         if data:
#             dispatcher.utter_message(f"Fetched data: {data}")
#         else:
#             dispatcher.utter_message("No data found.")

#         return [SlotSet("fetched_data", data)]

#     # def run(self, dispatcher: CollectingDispatcher,
#     #         tracker: Tracker,
#     #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#     #     customer_id = tracker.get_slot("customer_id")
        
        
#     #     print("Send API request")
        
#     #     response = requests.get(url)
#     #     print("Send API request")

#     #     if response.status_code == 200:
#     #         data = response.json()
#     #         existing_keywords = data.get('keywords', [])
#     #         if existing_keywords:
#     #             words = json.loads(existing_keywords[0])
#     #             print(words)
#     #         else:
#     #             print("No keywords found.")
#     #     else:
#     #         print(f"Failed to retrieve data. Status code: {response.status_code}")
        
#     print("Send API request")



class SendApiRequest(Action):
    def name(self) -> Text:
        return "action_send_api_request"

    def run(self, dispatcher, tracker, domain):
        # Get database credentials from environment variables or a secure configuration
        db_credentials = {
            'host': 'your_host',
            'database': 'your_database',
            'user': 'your_user',
            'password': 'your_password',
        }

        # Establish a database connection
        try:
            conn = psycopg2.connect(**db_credentials)
            cursor = conn.cursor()

            # Example query to select data from the 'crm_contact' table
            query = "SELECT * FROM crm_contact"
            cursor.execute(query)

            # Fetch all the rows from the result set
            rows = cursor.fetchall()

            # You can do something with the fetched data here
            data = rows

        except Exception as e:
            # Handle database connection errors
            print(f"Error connecting to the database: {e}")
            data = None

        finally:
            # Close the cursor and connection in a 'finally' block to ensure it happens even if an exception occurs
            cursor.close()
            conn.close()

        if data:
            dispatcher.utter_message(f"Fetched data: {data}")
        else:
            dispatcher.utter_message("No data found.")

        # Set the fetched data as a slot for future reference
        return [SlotSet("fetched_data", data)]
