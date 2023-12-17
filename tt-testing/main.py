import datetime
import threading

from booking import book
from pay import pay
from collect import collect

from enter_station import enter_station
from api_client import APIClient

date_str = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
api_client = APIClient("http://3.94.54.180:32677" )


def ticket_booking_flow():
    threads = []
    for i in range(3):  # Creating 10 flows
        t = threading.Thread(target=book(date_str, api_client))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    payload = { "loginId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f", "state" : 0 }

    tickets = api_client.make_api_call('orderservice/order/query',
                                    'POST',None,payload)
    tickets = [ticket for ticket in tickets if ticket['status']==0]
    pay(tickets, api_client)
    collect(tickets, api_client)
    enter_station(tickets, api_client)



if __name__ == '__main__':
    for i in range(10):
        ticket_booking_flow()