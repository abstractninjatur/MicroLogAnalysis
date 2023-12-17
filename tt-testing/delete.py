

from api_client import APIClient

def delete(tickets: list, api_client: APIClient):
    count = 0
    for ticket in tickets:
        print(f"Ticket  { ticket['id'] } is deleted !")
        api_client.make_api_call(f"orderservice/order/{ticket['id']}",
                                 'DELETE', None, None)

        count = count+1
    print(f"Deleted ticket counts {count}")

