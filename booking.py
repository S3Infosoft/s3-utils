#!/usr/bin/env python3
import mechanize
import requests_html
import regex
from bs4 import BeautifulSoup
from datetime import datetime
Data = {
    'URL' : 'https://www.booking.com',
    'Hotel' : 'Mango Valley Resort Ganpatipule',
    'Search' : 'Ratnagiri',
    'CheckIn': {
        'Date' : '18',
        'Month': '07',
        'Year' : '2019',
    },
    'CheckOut': {
        'Date': '20',
        'Month': '07',
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

    def GetResponse(self,config):
        self.config = config
        self.br = Browser(self.config['URL'])
        self.br.__select_from_by_pos__(0)
        self.br.__select_control__('ss',self.config['Search'])
        response = self.br.browser.submit()
        url = response.geturl()
        url = self.__fill_option__(url,'checkin_year',self.config['CheckIn']['Year'])
        url = self.__fill_option__(url,'checkin_month',self.config['CheckIn']['Month'])
        url = self.__add_option__(url,'checkin_monthday=%s&'%(self.config['CheckIn']['Date']),'checkin_month',3)

        url = self.__fill_option__(url,'checkout_year',self.config['CheckOut']['Year'])
        url = self.__fill_option__(url,'checkout_month',self.config['CheckOut']['Month'])
        url = self.__add_option__(url,'checkout_monthday=%s&'%self.config['CheckOut']['Date'],'checkout_month',3)
        self.url = url
        r = session.get(self.url)
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
            if Name != config['Hotel'] and notfound:
                self.pos += 1
            else:
                notfound = False

            data = {
                'URL' : self.config['URL'] + URL,
                'Price' : Price_soup.text.strip().replace('₹\xa0',''),
            }
            self.hotel_list[Name] = data

        request = session.get(self.hotel_list[config['Hotel']]['URL'])
        soup = BeautifulSoup(request.text,'lxml')

        self.RoomsDetails = []

        for row in soup.find_all('tr'):
            Accommodation_Type = row.find('span',attrs={'hprt-roomtype-icon-link'})
            if Accommodation_Type is not None:
                Accommodation_Type = Accommodation_Type.text.strip()

                facilities = row.find_all('span',attrs={'hprt-facilities-facility'})
                ExtraCols = row.find_all('td',attrs={'hprt-table-cell'})
                ExtraColsData = [ col.text.strip().replace('\n','').replace('\xa0','') for col in ExtraCols[1:]]

                table_row_data = {
                    'Accommodation Type': Accommodation_Type,
                    'Facilities' : [fac.text.strip().replace('• ','') for fac in facilities],
                    'Max Person' : ExtraColsData[0].replace('Max persons: ',''),
                    'Price' : ExtraColsData[1].replace(' includes taxes and charges','')
                }
                self.RoomsDetails.append(table_row_data)
            
        now = datetime.now()
        return {
            'RoomDetails' : self.RoomsDetails,
            'ota' : 'Booking',
            'runtime' : now.strftime("%y-%m-%d %H:%M:%S"),
            'Position' : self.pos
        }


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

#hd = Bookingdotcom()
#print(hd.GetResponse(Data))