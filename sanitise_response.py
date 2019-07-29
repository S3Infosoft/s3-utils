import datetime

class MealPlan(object):
    def __init__(self, ep, cp, map, ap):
        self.ep = ep
        self.cp = cp
        self.map = map
        self.ap = ap
    def get_json(self):
        returndata = {}
        returndata['ep'] = self.ep
        returndata['cp'] = self.cp
        returndata['map'] = self.map
        returndata['ap'] = self.ap
        return returndata

class Rates(object):
    def __init__(self):
        self.rates = {}
    def add_room(self, room_name, mealplan):
        self.rates[room_name] = mealplan
    def get_json(self):
        returndata = {}
        for k,v in self.rates.items():
            returndata[k] = v.get_json()
        return returndata


class OtaRunResponse(object):
    def __init__(self, ota, ts, cin, cout, status, comments):
        self.ota = ota
        self.timestamp = ts
        self.checkin = cin
        self.checkout = cout
        self.status = status
        self.comments = comments
        self.rates = {}
        self.run_start_time = datetime.datetime.now()
    def set_rates(self, rates):
        self.rates = rates
    def get_json(self):
        data = {
            'ota': self.ota,
            'timestamp': self.timestamp,
            'checkin': self.checkin,
            'checkout': self.checkout,
            'status': self.status,
            'run_start_time': self.run_start_time,
            'run_end_time': datetime.datetime.now()
        }
        if self.rates:
            data['rates'] = self.rates.get_json()
        if self.comments:
            data['comments'] = self.comments
        return data


def get_sample_mmt_response():
    return {"INR 1,969": "INR 2,326", "INR 2,819": "INR 3,045", "Status": "OK", "check_in": "28/07/2019",
     "check_out": "29/07/2019", "listed_position": "10", "ota": "MMT", "run_time": "2019-07-16 14:01:14"}

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

    mealplan1 = MealPlan(2000, 2500, 3000, 3500)
    mealplan2 = MealPlan(2500, 3000, 3500, 4000)

    rates = Rates()
    rates.add_room('Standard Room', mealplan1)
    rates.add_room('Superior Room', mealplan2)

    response = OtaRunResponse(r['ota'], r['run_time'], r['check_in'], r['check_out'], r['Status'], None)
    response.set_rates(rates)
    print(response.get_json())

if __name__ == '__main__':
    sanitize_response()
