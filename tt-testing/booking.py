
import random
from utils import random_boolean, random_str, random_phone
from api_client import APIClient
from common_queries import _query_high_speed_ticket
from common_queries import  _contact_details



def book(date_str: str, api_client: APIClient):
    place_pairs = [("Shang Hai", "Su Zhou")]

    place_choice = random.choice(place_pairs)

    payload = {
        "startPlace": place_choice[0],
        "endPlace": place_choice[1],
        "departureTime": date_str
    }
    start = ""
    end = ""
    trip_ids = []
    PRESERVE_URL = ""

    #
    # high_speed = random_boolean()
    # if high_speed:
    trip_ids = _query_high_speed_ticket(payload, api_client)
    PRESERVE_URL = "preserveservice/preserve"
    # else:
    #     trip_ids = _query_normal_speed_ticket(payload, api_client)
    #     PRESERVE_URL = "preserveotherservice/preserveOther"

    # assurance = api_client.make_api_call('assuranceservice/assurances/types',api_client)

    food_result = [{
        "foodName": "Soup",
        "foodPrice": 3.7,
        "foodType": 2,
        "stationName": "Su Zhou",
        "storeName": "Roman Holiday"
    }]
    contacts_result = _contact_details()

    base_preserve_payload = {

        "date": date_str,
        "from": place_choice[0],
        "to": place_choice[1],

    }

    base_preserve_payload['tripId'] = trip_ids[0]
    need_food = random_boolean()
    if need_food:
        base_preserve_payload.update(food_result[0])
    else:
        base_preserve_payload["foodType"] = "0"

    need_assurance = random_boolean()
    if need_assurance:
        base_preserve_payload["assurance"] = 1

    base_preserve_payload.update(contacts_result)

    # 高铁 2-3
    seat_type = random.choice(["2", "3"])
    base_preserve_payload["seatType"] = seat_type
    base_preserve_payload['isWithin'] = False

    need_consign = random_boolean()
    if need_consign:
        consign = {
            "consigneeName": random_str(),
            "consigneePhone": random_phone(),
            "consigneeWeight": random.randint(1, 10),
            "handleDate": date_str
        }
        base_preserve_payload.update(consign)

    print("payload:" + str(base_preserve_payload))

    api_client.make_api_call(PRESERVE_URL, "POST", None, base_preserve_payload)
