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
from scripts.g_sheet import add_candidate_data, fetch_gsheet_data 
# from templates.quick_reply import add_quick_reply

# def create_form(customer_id):
    

def save_candidate_data(tracker: Tracker):
    customer_id = tracker.get_slot("customer_id")

    candidate_data = [customer_id]
    if add_candidate_data(candidate_data = candidate_data):
        return "Data Added"

    return "Unable to add data" 

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

        text = "Sure ! I can help you with that."
        text1 = "Please provide me 10digits ID of the customer."
        text2 = tracker.get_slot("phone_number")
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text=text1)
        dispatcher.utter_message(text=text2)

        return []
    
class UserForm(FormAction):
    def name(self) -> Text:
        return "user_form"
    
    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["phone_number", "customer_id"]  # Add "customer_id" to the required slots
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "phone_number": self.from_text(),
            "customer_id": self.from_text()  # Map the "customer_id" slot to a text input
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the phone number and customer ID from the tracker
        phone_number = tracker.get_slot("phone_number")
        customer_id = tracker.get_slot("customer_id")
        
        # Construct the API URL
        api_url = f"CRM/phonebook/{customer_id}"
        
        # Send an API request
        response = requests.get(api_url)
        
        # Print the response content
        print("API Response:", response.content)
        
        # You can also handle the API response in other ways, such as extracting data or generating a response message
        
        # Respond to the user indicating that the phone number has been saved and the API response has been printed
        dispatcher.utter_message(f"Phone number {phone_number} has been saved. API response: {response.content}")
        
        # Returning an empty list will end the form action
        return []

    def name(self) -> Text:
        return "user_form"
    
    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["customer_id"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "customer_id": self.from_text()
        }
        
    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        customer_id = tracker.get_slot("customer_id")
        self.saved_customer_id = customer_id
        dispatcher.utter_message(f"Customer ID {customer_id} has been saved.")
        return []