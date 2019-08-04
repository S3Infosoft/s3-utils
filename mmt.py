from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sys
import re
from datetime import datetime

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
    
    def get_response(self):
        try:
            self.selected_url = self.AllHotels[self.data['hotel']]['url']
            pos = self.AllHotels[self.data['hotel']]['pos']
        except KeyError:
            return {
                'status' : 'FAIL',
                'reason' : 'No Hotel with name : "%s"' % self.data['hotel']
            }
        self.hotelpagecontent = self.browser.Load(self.selected_url)
        self.hotelsoup = BeautifulSoup(self.hotelpagecontent,'html.parser')
        self.content = self.hotelsoup.find_all('div',attrs={'roomWrap'})
        now = datetime.now()
        self.Response = {
            'status' : 'OK',
            'listed_position' : pos,
            'ota' : 'MMT',
            'runtime' : now.strftime("%y-%m-%d %H:%M:%S"),
            'check_in' : "%s/%s/%s" % (self.data['checkin']['date'],
                                         self.data['checkin']['month'],
                                         self.data['checkin']['year']),

            'check_out' : "%s/%s/%s" % (self.data['checkout']['date'],
                                          self.data['checkout']['month'],
                                          self.data['checkout']['year'])
        }
        for row in self.content:
            left = row.find('div',attrs={'roomLeft'})
            RoomType = left.find('h2').text.strip()
            right = row.find_all('span',attrs={'bxNegotiate'})
            r = [r.text.strip() for r in right]
            pc = []
            for p in r:
                st = p.find('Total PayableINR')
                price = (p[(st + len('Total PayableINR') + 1):])
                pc.append(price)

            self.Response[RoomType] = pc

        return self.Response




    def __gen_url__(self,url_data):
        return 'https://www.makemytrip.com/hotels/hotel-listing/?checkin=%s%s%s&checkout=%s%s%s&roomStayQualifier=%s&city=XGP&country=IN&type=CTY&searchText=%s' % (
            url_data['checkin']['month'],
            url_data['checkin']['date'],
            url_data['checkin']['year'],
            url_data['checkout']['month'],
            url_data['checkout']['date'],
            url_data['checkout']['year'],
            url_data['room_code'],
            url_data['search']
       

        )

class Browser:
    def __init__(self):
        self.opt = webdriver.FirefoxOptions()
        self.opt.headless = True
        self.opt.add_argument('--ignore-certificate-errors')
        self.opt.add_argument('--test-type')
    
    def Load(self,url):
        self.browser = webdriver.Firefox(executable_path="./driver/geckodriver", options=self.opt)
        self.browser.get(url)
        sleep(2)
        return self.browser.page_source
