#!/usr/bin/env python3
import mechanize
import requests
from bs4 import BeautifulSoup

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

class ParseHotel:

    def load_page(self,config):
        self.br = Browser(config['URL'])
        self.br.__select_from_by_pos__(0)
        self.br.__select_control__('ss',config['Search'])
        response = self.br.browser.submit()
        url = response.geturl()
        url = self.__fill_option__(url,'checkin_year',config['CheckIn']['Year'])
        url = self.__fill_option__(url,'checkin_month',config['CheckIn']['Month'])
        url = self.__add_option__(url,'checkin_monthday=%s&'%(config['CheckIn']['Date']),'checkin_month',3)

        url = self.__fill_option__(url,'checkout_year',config['CheckOut']['Year'])
        url = self.__fill_option__(url,'checkout_month',config['CheckOut']['Month'])
        url = self.__add_option__(url,'checkout_monthday=%s&'%config['CheckOut']['Date'],'checkout_month',3)

        self.page_data = requests.get(url).text
        self.soup = BeautifulSoup(self.page_data,'html.parser')

    def list_hotels(self):
        hotels = self.soup.find_all('a',attrs={'class':'hotel_name_link'})
        hotel_list={}
        for i in hotels:
            hotel_list[i.find('span',attrs={'sr-hotel__name'}).text.strip()] =  i.get('href').replace('\n','')

        return hotel_list

    def __add_option__(self,url,option,after,space):
        loc = url.find(after) + len(after) + space + 1
        return url[:loc] + option + url[loc:]
    
    def __fill_option__(self,url,option,value):
        loc = url.find(option) + len(option) + 1
        return url[:loc] + value + url[loc:]

Data = {
    'URL' : 'https://www.booking.com/',
    'Search' : 'Ganputipule',
    'CheckIn': {
        'Date' : '16',
        'Month': '07',
        'Year' : '2019',
    },
    'CheckOut': {
        'Date': '18',
        'Month': '07',
        'Year': '2019',
    },
}


hd = ParseHotel()
hd.load_page(Data)
print(hd.list_hotels())