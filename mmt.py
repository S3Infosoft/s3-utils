from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
data = {
    "place" : "Ganpatipule",

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
        self.Hotels = self.soup.find_all('div',attrs={'listingRow'})
        for hotel in self.Hotels:
            hotel_name = hotel.find('p',attrs={'appendBottom12'}).text.strip()
            print(hotel_name)


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
        #self.opt.headless = True
        self.opt.add_argument('--ignore-certificate-errors')
        self.opt.add_argument('--test-type')
        self.opt.binary = '/usr/bin/firefox'
    
    def Load(self,url):
        self.browser = webdriver.Firefox(firefox_options=self.opt)
        self.browser.get(url)
        sleep(2)
        return self.browser.page_source


m = MMT(data)