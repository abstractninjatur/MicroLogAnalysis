
from api_client import APIClient


def collect(tickets: list, api_client: APIClient, ):
    for ticket in tickets:
        print(f"Collect -->> Ticket id : {ticket['id']} - {ticket['status']}")
        api_client.make_api_call(f"executeservice/execute/collected/{ticket['id']}",
                                 'GET', None, None)
