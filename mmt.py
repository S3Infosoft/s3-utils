from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sys
data = {
    "place" : "Ganpatipule",
    "hotel" : 'Mango Valley Resort Ganpatipule',
    "checkin" : {
        "date" : "28",
        "month" : "07",
        "year" : "2019",
    },

    "checkout" : {
        "date" : "31",
        "month" : "07",
        "year" : "2019",
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}


class MMT:
    def __init__(self,data):
        self.data = data
        self.url = self.__gen_url__(data)
        self.browser = Browser()
        self.pagecontent = self.browser.Load(self.url)
        self.soup = BeautifulSoup(self.pagecontent,'html.parser')
        self.Hotels = self.soup.find_all('a',attrs={'class':''})
        i = 0
        self.AllHotels = {}
        for hotel in self.Hotels:
            try:
                hotel_name = hotel.find('p',attrs={'appendBottom12'}).text.strip()
                hotel_url  = hotel.get('href')
                i += 1
                self.AllHotels[hotel_name] = {
                    'url' : hotel_url,
                    'pos' : i,
                }
            except AttributeError:
                pass
    
    def GetResponse(self):
        selected_url = self.AllHotels[self.data['hotel']]['url']
        self.hotelpagecontent = self.browser.Load('https://www.makemytrip.com/' + selected_url)
        self.hotelsoup = BeautifulSoup(self.hotelpagecontent,'lxml')



    def __gen_url__(self,url_data):
        return 'https://www.makemytrip.com/hotels/hotel-listing/?checkin=%s%s%s&checkout=%s%s%s&roomStayQualifier=2e0e&city=XGP&country=IN&type=CTY&searchText=%s' % (
            url_data['checkin']['month'],
            url_data['checkin']['date'],
            url_data['checkin']['year'],
            url_data['checkout']['month'],
            url_data['checkout']['date'],
            url_data['checkout']['year'],
            url_data['place']
       

        )

class Browser:
    def __init__(self):
        self.opt = webdriver.FirefoxOptions()
        self.opt.headless = True
        self.opt.add_argument('--ignore-certificate-errors')
        self.opt.add_argument('--test-type')
        self.opt.binary = '/usr/bin/firefox'
    
    def Load(self,url):
        self.browser = webdriver.Firefox(options=self.opt)
        self.browser.get(url)
        sleep(2)
        return self.browser.page_source


m = MMT(data)
if data['hotel'] in m.AllHotels:
    print("Found %s at pos : %d" % ( data['hotel'],m.AllHotels[data['hotel']]['pos']))
else:
    print('Unable to find %s on page 1'%data['hotel'])
    sys.exit(1)
m.GetResponse()
