import PyPDF2
import re

class readPDF:
    def __init__(self,pdf_file_loc):
        self.pdf_object = open(pdf_file_loc,'rb')
        self.pdf_reader = PyPDF2.PdfFileReader(self.pdf_object)
        self.pdf_data = ""
        for page_num in range(self.__page_count__()):
            self.pdf_data += self.__page_data__(page_num)

    def Data(self):
        return {
            "Booking ID": self.BookingID(),
            "No of nights": self.NoOfNights(),
            "Check In": self.checkin(),
            "Check Out": self.checkout(),
        }

    def BookingID(self):
        return self.__extract_data__("Booking ID - (.*?) .*")

    def NoOfNights(self):
        return self.__extract_data__("INRBOOKING DETAILS(.*?) Night.*")

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

    def __extract_data__(self,pattern):
        obj = re.search(pattern,self.pdf_data)
        return obj.group(1)
    
    def __page_data__(self,page_number):
        page_obj = self.pdf_reader.getPage(page_number)
        return page_obj.extractText()

    def __page_count__(self):
        pages_count = self.pdf_reader.numPages
        return pages_count

## Sample Usage
#
# if __name__ == '__main__':
#     pdfobj = readPDF("PDF_LOCATION")
#     print(pdfobj.Data()) 