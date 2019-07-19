import requests_html

__URL__ = "https://www.goibibo.com/hotels/find-hotels-in-Ganpatipule/"


data = {
    "url" : {
        "header" : "https://www.goibibo.com/hotels",
        "place" : "Ganpatipule",
        "code" : "1878646129688888888",
        "end" : "?{}&sec=dom",
    },

    "checkin" : {
        "date" : "21",
        "month" : "07",
        "year" : "2019",
    },

    "checkout" : {
        "date" : "22",
        "month" : "07",
        "year" : "2019",
    },

    "rooms" : "1",
    "guests" : "2",
    "child" : "0",
}


class Goibibo:
    def __init__(self,data):

        self.url = self.__gen_url__(data)
        self.session = requests_html.HTMLSession()
        self.response = self.session.get(self.url)

    def __gen_url__(self,url_data):
        return '%s/find-hotels-in-%s/%s/%s/{"ci":"%s%s%s","co":"%s%s%s","r":"%s-%s-%s"}/%s' % (
            url_data["url"]["header"],
            url_data["url"]["place"],
            url_data["url"]["code"],url_data["url"]["code"],
            url_data["checkin"]["year"],url_data["checkin"]["month"],url_data["checkin"]["date"],
            url_data["checkout"]["year"],url_data["checkout"]["month"],url_data["checkout"]["date"],
            url_data["rooms"],
            url_data["guests"],
            url_data["child"],
            url_data["url"]["end"]
        )
