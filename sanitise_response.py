


class OtaRunResponse(object):
    def __init__(self, ota, ts, cin, cout, status, rates, comments):
        self.ota = ota
        self.timestamp = ts
        self.checkin = cin
        self.checkout = cout
        self.status = status
        self.rates = rates
        self.comments = comments
    def get(self):
        data = {
            'ota': self.ota,
            'timestamp': self.timestamp,
            'checkin': self.checkin,
            'checkout': self.checkout,
            'status': self.status,
        }
        if self.rates:
            data['rates'] = self.rates
        if self.comments:
            data['comments'] = self.comments
        return data


def get_sample_mmt_response():
    return {"INR 1,969": "INR 2,326", "INR 2,819": "INR 3,045", "Status": "OK", "check_in": "28/07/2019",
     "check_out": "29/07/2019", "listed_position": "10", "ota": "Mmt", "run_time": "2019-07-16 14:01:14"}

def get_sample_booking_response():
    return {"Deluxe Bungalow with Sea View": "['\u20b9 7,500']", "Standard Double Room": "['\u20b9 2,700', '\u20b9 3,000']",
            "Status": "OK", "Superior Double Room": "['\u20b9 3,600', '\u20b9 4,000']",
            "Three-Bedroom Bungalow": "['\u20b9 7,500']", "check_in": "26/07/2019", "check_out": "27/07/2019",
            "listed_position": "3", "ota": "Booking", "run_time": "2019-07-16 14:07:37"}

def get_sample_goibibo_response():
    return {'run_time': '2019-07-16 20:48:42',
            'Villa Oceanica Garden View': "['4594', '5053']", 'Superior Double Room': "['2450', '2646']",
            'Status': 'OK', 'Standard Double Room': "['1694', '2022']",
            'Villa Oceanica Sea View': "['4594']", 'check_in': '26/07/2019',
            'check_out': '27/07/2019', 'ota': 'Goibibo', 'listed_position': '18'}

def sanitize_response():
    r = get_sample_mmt_response()
    # TODO: Goibibo and booking.com
    response = OtaRunResponse(r['ota'], r['run_time'], r['check_in'], r['check_out'], r['Status'], None, None).get()
    print(response)

if __name__ == '__main__':
    sanitize_response()
