from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sys
from datetime import datetime
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
                    'url' : 'https:' + hotel_url,
                    'pos' : i,
                }
            except AttributeError:
                pass
    
    def GetResponse(self):
        self.selected_url = self.AllHotels[data['hotel']]['url']
        pos = self.AllHotels[data['hotel']]['pos']
        self.hotelpagecontent = self.browser.Load(self.selected_url)
        self.hotelsoup = BeautifulSoup(self.hotelpagecontent,'html.parser')
        self.content = self.hotelsoup.find_all('div',attrs={'roomWrap'})
        now = datetime.now()
        self.Response = {
            'position' : pos,
            'ota' : 'mmt',
            'runtime' : now.strftime("%y-%m-%d %H:%M:%S"),
            'Data' : {

            },
        }
        for row in self.content:
            left = row.find('div',attrs={'roomLeft'})
            RoomType = left.find('h2').text.strip()
            FeatureSoup = left.find_all('li')
            RoomFeatures = [f.text.strip() for f in FeatureSoup]
            self.Response['Data'][RoomType] = {
                'features' : RoomFeatures,
            }
            right = row.find_all('div',attrs={'roomRight'})
            for r in right:
                optsSoup = r.find_all('div',attrs={'bdrBottom'})
                for j in optsSoup:
                    a = [x.text.strip() for x in j.find_all('span')]
                    options = a[1:]
                    options.remove('')
                    self.Response['Data'][RoomType][a[0]] = options

        return self.Response




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
        self.browser = webdriver.Firefox(executable_path="./driver/geckodriver", options=self.opt)
        self.browser.get(url)
        sleep(2)
        return self.browser.page_source

m = MMT(data)
response = m.GetResponse()