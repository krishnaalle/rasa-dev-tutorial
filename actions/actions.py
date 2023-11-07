# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/core/actions/#custom-actions/


# # This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="action_hello_world")
        dispatcher.utter_message(text="Actions called.")

        return []


class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "😕 Oops!I am sorry. I didn't understand you."
        text2 = "I am incredibly bad with conversation because I was only designed for one purpose - " \
                "taking in job applications for TechCodeMonk"
        data = [
            {
                "title": "✅ Yes",
                "payload": "/affirm"
            },
            {
                "title": "❌ No",
                "payload": "/deny"
            }
        ]
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text=text2)
        dispatcher.utter_message(text="Are you looking for a job?", buttons=message)

        return [AllSlotsReset()]
    


