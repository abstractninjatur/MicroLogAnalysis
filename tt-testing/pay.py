

def pay(tickets, api_client):
    for ticket in tickets:
        print(f"Pay -->> Ticket id : {ticket['id']} - {ticket['status']}")
        payload = {"orderId": ticket['id'], "tripId": ticket['trainNumber']}
        api_client.make_api_call('inside_pay_service/inside_payment',
                                 'POST', None, payload)




