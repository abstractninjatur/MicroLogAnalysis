import logging

from datetime import datetime, timedelta
import random


logger = logging.getLogger("common_queries")

contact_details = [
    {
        "id": "24b85ce5-bbe7-4962-a5de-693f7c6eb9c9",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "",
        "documentType": 1,
        "documentNumber": "",
        "phoneNumber": ""
    },
    {
        "id": "81338a53-847c-43d2-b057-40bb9d53b3da",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "",
        "documentType": 2,
        "documentNumber": "",
        "phoneNumber": ""
    },
    {
        "id": "97a1eb44-1962-4708-9349-9f7774bd34f6",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "",
        "documentType": 3,
        "documentNumber": "",
        "phoneNumber": ""
    },
    {
        "id": "f8dea0d9-5365-4450-9907-5aa8c1e822d5",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "Contacts_One",
        "documentType": 1,
        "documentNumber": "DocumentNumber_One",
        "phoneNumber": "ContactsPhoneNum_One"
    },
    {
        "id": "a5591cc4-2db5-46cd-9454-e06cb5e6df85",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "Contacts_Two",
        "documentType": 1,
        "documentNumber": "DocumentNumber_Two",
        "phoneNumber": "ContactsPhoneNum_Two"
    },
    {
        "id": "60af9e49-e9d7-4546-a3bb-9b72e9371e16",
        "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
        "name": "contact_3",
        "documentType": 1,
        "documentNumber": "Document_2",
        "phoneNumber": "22222"
    }

]

date_str = (datetime.now() +  timedelta(days=1)).strftime("%Y-%m-%d")

def _query_high_speed_ticket(payload, client):


    url = "travelservice/trips/left"
    data = client.make_api_call(url, "POST", data=payload)

    trip_ids = ['D1345']
    if data:
        for d in data:
            trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
            trip_ids.append(trip_id)
    return trip_ids

def _query_normal_speed_ticket(payload,client):
    url = "travel2service/trips/left"
    data = client.make_api_call(url, "POST", data=payload)

    trip_ids = []
    for d in data:
        trip_id = d.get("tripId").get("type") + d.get("tripId").get("number")
        trip_ids.append(trip_id)
    return trip_ids


def _contact_details():
    contact_info = random.choice(contact_details)

    return {
        "contactsId": contact_info['id'],
        "accountId": contact_info['accountId']
    }