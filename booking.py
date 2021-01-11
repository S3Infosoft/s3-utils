#!/usr/bin/env python3
import mechanize
import requests_html
from bs4 import BeautifulSoup
from datetime import datetime
Data = {
    'URL' : 'https://www.booking.com',
    'Hotel' : 'Mango Valley Resort Ganpatipule',
    'Search' : 'Ratnagiri',
    'CheckIn': {
        'Date' : '18',
        'Month': '08',
        'Year' : '2019',
    },
    'CheckOut': {
        'Date': '20',
        'Month': '08',
        'Year': '2019',
    },
}

session = requests_html.HTMLSession()

class Browser:

    def __init__(self,url):
        self.browser = mechanize.Browser()
        self.__config_browser__()
        self.response = self.browser.open(url)
         
    
    def __select_form_by_name__(self,name):
        self.browser.select_form(name)
        self.browser.form.set_all_readonly(False)

    def __select_from_by_pos__(self,pos):
        self.browser.form = list(self.browser.forms())[pos]
        self.browser.form.set_all_readonly(False)

    def __select_control__(self,control,value):
        self.browser[control] = value

    def __list_forms__(self):
        for frm in self.browser.forms():
            print("Form Name:",frm.name)
            print(frm)

    def __list_control__(self):
        for cntrl in self.browser.form.controls:
            print(cntrl)
            print("Type=",cntrl.type,
                  "name=",cntrl.name)

    def __config_browser__(self):
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
        self.browser.addheaders = [('User-agent','Firefox')]

class Bookingdotcom:

    def get_response(self,config):
        self.config = config
        self.br = Browser('https://www.booking.com/')
        self.br.__select_from_by_pos__(0)
        self.br.__select_control__('ss',self.config['search'])
        response = self.br.browser.submit()
        url = response.geturl()
        url = self.__fill_option__(url,'checkin_year',self.config['checkin']['year'])
        url = self.__fill_option__(url,'checkin_month',self.config['checkin']['month'])
        url = self.__add_option__(url,'checkin_monthday=%s&'%(self.config['checkin']['date']),'checkin_month',3)

        url = self.__fill_option__(url,'checkout_year',self.config['checkout']['year'])
        url = self.__fill_option__(url,'checkout_month',self.config['checkout']['month'])
        url = self.__add_option__(url,'checkout_monthday=%s&'%self.config['checkout']['date'],'checkout_month',3)
        self.url = url
        s = requests_html.HTMLSession()
        r = s.get(self.url)
        r.html.render()
        self.page_data = r.text
        self.soup = BeautifulSoup(self.page_data,'html.parser')

        containers = self.soup.find_all('div',attrs={'sr_item_new'})
        self.hotel_list = {}
        self.pos = 0
        notfound = True
        for content in containers:
            content_soup = BeautifulSoup(str(content),'html.parser')
            Price_obj = content_soup.find('div',attrs={'bui-price-display__value'})
            i = content_soup.find('a',attrs={'hotel_name_link'})
            
            Name = content_soup.find('span',attrs={'sr-hotel__name'}).text.strip()
            URL = i.get('href').strip()
            
            Price_soup = BeautifulSoup(str(Price_obj),'html.parser')
            if Name != config['hotel'] and notfound:
                self.pos += 1
            else:
                notfound = False

            data = {
                'url' : 'https://www.booking.com/' + URL,
                'price' : Price_soup.text.strip().replace('₹\xa0',''),
            }
            self.hotel_list[Name] = data
        try:    
            request = session.get(self.hotel_list[config['hotel']]['url'])

        except KeyError:
            return {
                'status' : 'FAIL'
            }
        soup = BeautifulSoup(request.text,'lxml')
        resp = {}
        for row in soup.find_all('tr'):
            Accommodation_Type = row.find('span',attrs={'hprt-roomtype-icon-link'})
            if Accommodation_Type is not None:
                Accommodation_Type = Accommodation_Type.text.strip()

#                facilities = row.find_all('span',attrs={'hprt-facilities-facility'})
                ExtraCols = row.find_all('td',attrs={'hprt-table-cell'})
                ExtraColsData = [ col.text.strip().replace('\n','').replace('\xa0','') for col in ExtraCols[1:]]
                resp[Accommodation_Type] = ExtraColsData[1].replace(' includes taxes and charges','')
            
        now = datetime.now()       
        resp['ota'] = 'Booking'
        resp['run_time'] = now.strftime("%y-%m-%d %H:%M:%S")
        resp['listed_position'] = str(self.pos)
        resp['check_in'] = "%s/%s/%s" % (self.config['checkin']['date'],
                                         self.config['checkin']['month'],
                                         self.config['checkin']['year'])

        resp['check_out'] = "%s/%s/%s" % (self.config['checkout']['date'],
                                          self.config['checkout']['month'],
                                          self.config['checkout']['year'])
        return resp
    def __add_option__(self,url,option,after,space):
        loc = url.find(after) + len(after) + space + 1
        return url[:loc] + option + url[loc:]
    
    def __fill_option__(self,url,option,value):
        loc = url.find(option) + len(option) + 1
        return url[:loc] + value + url[loc:]

class Hotel:
    def __init__(self,url):
        response = session.get(url)
        response.html.render()
        self.page_data = response.text
        self.soup = BeautifulSoup(self.page_data, 'html.parser')
<<<<<<< HEAD

hd = Bookingdotcom()
print(hd.GetResponse(Data))
=======
>>>>>>> 273c7e12c29c130a01ca3d220804566eef364252
