import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


def load_data():
    try:
        with open("university_data.json", encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("Error: university_data.json not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in university_data.json")
        return []


class ActionFindMajor(Action):
    def name(self) -> Text:
        return "action_find_major"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        major = tracker.get_slot("major")
        if not major:
            dispatcher.utter_message(text="Vui lòng cung cấp ngành học.")
            return []

        try:
            data = load_data()
            if not data:
                dispatcher.utter_message(text="Không thể tải dữ liệu trường học.")
                return []

            matched = [uni["name"] for uni in data if major.lower() in [m.lower() for m in uni.get("majors", [])]]
            if matched:
                dispatcher.utter_message(text=f"Ngành {major} có ở các trường: {', '.join(matched)}.")
            else:
                dispatcher.utter_message(text=f"Không tìm thấy trường có ngành {major}.")
        except Exception as e:
            print(f"Error in ActionFindMajor: {str(e)}")
            dispatcher.utter_message(text="Có lỗi xảy ra khi tìm ngành học.")
        return []


class ActionFindTuition(Action):
    def name(self) -> Text:
        return "action_find_tuition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        uni = tracker.get_slot("university")
        if not uni:
            dispatcher.utter_message(text="Vui lòng cung cấp tên trường.")
            return []

        try:
            data = load_data()
            if not data:
                dispatcher.utter_message(text="Không thể tải dữ liệu trường học.")
                return []

            for item in data:
                if uni.lower() in item.get("name", "").lower():
                    dispatcher.utter_message(text=f"Học phí của {item['name']} là {item.get('tuition', 'không rõ')}")
                    return []
            dispatcher.utter_message(text=f"Không tìm thấy thông tin học phí cho {uni}.")
        except Exception as e:
            print(f"Error in ActionFindTuition: {str(e)}")
            dispatcher.utter_message(text="Có lỗi xảy ra khi tìm thông tin học phí.")
        return []


class ActionFindByCity(Action):
    def name(self) -> Text:
        return "action_find_by_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city = tracker.get_slot("city")
        if not city:
            dispatcher.utter_message(text="Vui lòng cung cấp tên thành phố.")
            return []

        try:
            data = load_data()
            if not data:
                dispatcher.utter_message(text="Không thể tải dữ liệu trường học.")
                return []

            matched = [uni["name"] for uni in data if city.lower() in uni.get("city", "").lower()]
            if matched:
                dispatcher.utter_message(text=f"Các trường ở {city}: {', '.join(matched)}")
            else:
                dispatcher.utter_message(text=f"Không tìm thấy trường nào ở {city}")
        except Exception as e:
            print(f"Error in ActionFindByCity: {str(e)}")
            dispatcher.utter_message(text="Có lỗi xảy ra khi tìm trường theo thành phố.")
        return []