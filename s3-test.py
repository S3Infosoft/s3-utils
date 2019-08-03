
from mmt import MMT

booking_data = {
    'hotel' : 'Mango Valley Resort Ganpatipule',
    'search' : 'Ratnagiri',
    'checkin': {
        'date' : '31',
        'month': '07',
        'year' : '2019',
    },
    'checkout': {
        'date': '2',
        'month': '08',
        'year': '2019',
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}

mmt_data = {
    "search" : "Ganpatipule",
    "hotel" : 'Mango Valley Resort Ganpatipule',
    "checkin" : {
        "date" : "01",
        "month" : "08",
        "year" : "2019",
    },

    "checkout" : {
        "date" : "02",
        "month" : "08",
        "year" : "2019",
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}


m = MMT(mmt_data)
print(m.get_response())