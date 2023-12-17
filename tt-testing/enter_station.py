

from api_client import APIClient



def enter_station(tickets: list(), api_client: APIClient):
    for ticket in tickets:
        print(f"Enter Station -->> Ticket id : {ticket['id']} - {ticket['status']}")
        api_client.make_api_call(f"executeservice/execute/execute/{ticket['id']}",
                                 'GET', None, None)



