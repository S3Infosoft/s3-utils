import PyPDF2
import re

class MMT_PDF_Parser:
    def __init__(self,pdf_file_loc):
        self.pdf_object = open(pdf_file_loc,'rb')
        self.pdf_reader = PyPDF2.PdfFileReader(self.pdf_object)
        self.pdf_data = ""
        for page_num in range(self.__page_count__()):
            self.pdf_data += self.__page_data__(page_num)

    def Data(self):
        rooms, nights, price = self.hotel_sell_price()
    
        return {
            "Booking ID": 
                    self.__extract_data__("Booking ID - (.*?) .*"),

            "No of nights":
                    self.__extract_data__("INRBOOKING DETAILS(.*?) Night.*"),


            "Check In": self.checkin(),
            "Check Out": self.checkout(),

            "Room" : rooms,
            "Night" : nights,
            "Hotel Sell Price" : price,

            "Extra Adult / Child Charge":
                    self.__extract_data__("Adult / Child Charges(\d+)(A)*"),

            "Hotel Gross Price": 
                    self.__extract_data__("Hotel Gross Charges(\d+)"),

            "MMT Commission": 
                    self.__extract_data__("MMT Commission(\d+)"),
            
            "GST @ 18% (Including IGST or (SGST & CGST))": 
                    self.__extract_data__("\\(SGST & CGST\\)\\)(\d+)"),

            "MMT to Pay Hotel (A-B)" : 
                    self.__extract_data__("MMT to Pay Hotel \\(A-B\\)(\d+)"),
                
            "GST on hotel accommodation charges by Ecommerce Operator":
                    self.__extract_data__("GST on hotel accommodation charges by Ecommerce Operator: (\d+)"),

            "Primary Guest":
                    self.guest_name(),
            
            "E-mail":
                    self.email_id(),
        
            "Contact No":
                    self.contact_no(),
            
            "Room Category":
                    self.__extract_data__("Room Category : (.*?)Meal"),
            
            "Meal Plan":
                    self.__extract_data__("Meal Plan : (.*?)Inclusions"),
        }


    def checkin(self):
       datetime = self.__extract_data__("Check In(.*?)Check Out")
       obj = re.match("(\d{2}) (\w{3}) (\d{4})(\d{2}):(\d{2}) (\w{2})",datetime)
       return "%s:%s%s %s-%s-%s" % (obj.group(4),obj.group(5),obj.group(6),
                                    obj.group(1),obj.group(2),obj.group(3))

    def checkout(self):
       datetime = self.__extract_data__("Check Out(.*?)Room")
       obj = re.match("(\d{2}) (\w{3}) (\d{4})(\d{2}):(\d{2}) (\w{2})",datetime)
       return "%s:%s%s %s-%s-%s" % (obj.group(4),obj.group(5),obj.group(6),
                                    obj.group(1),obj.group(2),obj.group(3))

    def hotel_sell_price(self):
        obj = re.search("Hotel Sell Price(\d) Room x (\d) Night(.*?)Extra",self.pdf_data)
        return obj.group(1), obj.group(2), obj.group(3)
    
    def guest_name(self):
        return self.__extract_data__("Primary Guest : (.*?)E-mail")

    def email_id(self):
        return self.__extract_data__("%sE-mail : (.*?)Contact" % self.guest_name())

    def contact_no(self):
        all_no = self.__extract_data__("%sContact Number : (.*?)Room" % self.email_id())
        all_no = all_no.replace(',','')
        return all_no.split()

    def __extract_data__(self,pattern):
        obj = re.search(pattern,self.pdf_data)
        return obj.group(1)
    
    def __page_data__(self,page_number):
        page_obj = self.pdf_reader.getPage(page_number)
        return page_obj.extractText()

    def __page_count__(self):
        pages_count = self.pdf_reader.numPages
        return pages_count

# Sample Usage
if __name__ == '__main__':
    pdfobj = MMT_PDF_Parser("data.pdf")
    print(pdfobj.Data()) 