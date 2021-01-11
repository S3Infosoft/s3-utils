import unittest
from mmt import MMT
from booking import Bookingdotcom

booking_input_valid = {
    'hotel' : 'Mango Valley Resort Ganpatipule',
    'search' : 'Ratnagiri',
    'checkin': {
        'date' : '07',
        'month': '08',
        'year' : '2019',
    },
    'checkout': {
        'date': '08',
        'month': '08',
        'year': '2019',
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}


booking_output_valid = {
    'Standard Double Room': '₹2,700', 
    'Superior Double Room': '₹3,600', 
    'Deluxe Bungalow with Sea View': '₹7,500', 
    'Three-Bedroom Bungalow': '₹7,500', 
    'ota': 'Booking', 
    'listed_position': '0', 
    'check_in': '07/08/2019', 
    'check_out': '08/08/2019'
}


booking_input_invalid = {
    'hotel' : 'hotel not in list',
    'search' : 'some wrong thing',
    'checkin': {
        'date' : '07',
        'month': '08',
        'year' : '2019',
    },
    'checkout': {
        'date': '08',
        'month': '08',
        'year': '2019',
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}

booking_output_invalid = {
    'status': 'FAIL'
}

mmt_input_valid = {
    "search" : "Ganpatipule",
    "hotel" : 'Mango Valley Resort Ganpatipule',
    "checkin" : {
        "date" : "04",
        "month" : "08",
        "year" : "2019",
    },

    "checkout" : {
        "date" : "05",
        "month" : "08",
        "year" : "2019",
    },

    "room_code" : "2e2e1e3e"
    # Room Code 
    # e = _ skip (junk)
    # '3e2e1e3e' : 3 adults , 2 children of age 1 and 3
    # for another room repeat code with space
    # '3e2e1e3e4e3e1e3e5e' : 4 adults, 3 children of age 1 , 3 and 5

}

mmt_output_valid = {
    'check_in': '04/08/2019', 
    'check_out': '05/08/2019', 
    'Villa Oceanica Garden View': ['5,191', '5,710'], 
    'ota': 'MMT', 
    'Villa Oceanica Sea View': ['5,191', '6,229'], 
    'listed_position': 3, 
    'status': 'OK'
}

mmt_input_invalid = {
    "search" : "some wrong input",
    "hotel" : 'hotel thats not present',
    "checkin" : {
        "date" : "04",
        "month" : "08",
        "year" : "2019",
    },

    "checkout" : {
        "date" : "05",
        "month" : "08",
        "year" : "2019",
    },
    "room_code" : "2e2e1e3e"
}

mmt_output_invalid = {
    'status' : 'FAIL'
}

class resultTest(unittest.TestCase):
    def test_mmt_valid(self):
        m = MMT(mmt_input_valid)
        resp = m.get_response()
        resp.pop('runtime')
        self.assertEqual(resp,mmt_output_valid)
    
    def test_mmt_invalid(self):
        m = MMT(mmt_input_invalid)
        resp = m.get_response()
        resp.pop("reason")
        self.assertEqual(resp,mmt_output_invalid)

    def test_booking_valid(self):
        b = Bookingdotcom()
        resp = b.get_response(booking_input_valid)
        self.assertEqual(resp,mmt_output_valid)

    def test_booking_invalid(self):
        b = Bookingdotcom()
        resp = b.get_response(booking_input_invalid)
        self.assertEqual(resp,mmt_output_invalid)

if __name__ == '__main__':
    unittest.main()