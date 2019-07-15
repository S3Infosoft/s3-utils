#!/usr/bin/env python3
import mechanize
import requests
from bs4 import BeautifulSoup

class Browser:

    def __init__(self,config,url):
        self.browser = mechanize.Browser()
        self.__config_browser__()
        self.response = self.browser.open(url)
        self.config = config
    
    def load(self): 
        if self.__select_form__() == -1: return -1

        for i in self.config['controls']:
            ctrn = self.browser.form.find_control(i['name'])
            

    
    def __select_form_by_name__(self,name):
        self.browser.select_form(name)

    def __select_from_by_pos__(self,pos):
        self.browser.form = list(self.browser.forms())[pos]

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
    def __init__(self,page_data):
        self.page_data = page_data
        self.soup = BeautifulSoup(self.page_data,'html.parser')

    def list_hotels(self):
        hotels = self.soup.find_all('a',attrs={'class':'hotel_name_link'})
        hotel_list={}
        for i in hotels:
            hotel_list[i.find('span',attrs={'sr-hotel__name'}).text.strip()] =  i.get('href').replace('\n','')

        return hotel_list


Data = {
    'form': {
        'search_by': 'pos',
        'pos': 0
    },

    'controls' : {
        'control1': {
            'name': 'ss',
            'value': 'mangovalley',
        },

        'control2': {
            'name': 'checkin_year',
            'value': '2019',
        },

        'control3': {
            'name': 'checkin_month',
            'value': '5',
        },

        'control4': {
            'name': 'checkout_year',
            'value': '',
        },

        'control5': {
            'name': 'checkout_month',
            'type': 'hidden',
        },

        'control6': {
            'name': 'checkout_month',
            'type': 'select'
        },
    },
}

