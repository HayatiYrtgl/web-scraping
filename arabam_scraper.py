from bs4 import BeautifulSoup
import requests as req

# http header
header = {"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
"Accept-Language":"tr-TR,tr;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ar;q=0.5", }


# class for arabam scraper
class ArabamScraper:
    
     #  initialize
     def __init__(self):
         
          # const vars
          self.base_url = None
          
          # run the modifier
          self.brand = input("marka giriniz :")
          self.model = input("model giriniz:")
          self.min_pr = input("minumum fiyat giriniz:")
          self.max_pr = input("maximum fiyat giriniz:")
          self.min_year = input("minumum yıl giriniz:")
          self.max_year = input("maximum yıl giriniz:")
          
          # url list
          self.url_list = []
           
     # requester
     def requester(self, url):
         
          """ this function requests the given url and returns content of the web page """
          
          # get request
          my_request = req.get(url, headers=header)   
          
          # control the status code
          if my_request.status_code == 200:
              print("connected", url)
              return my_request.content
              
          else:
              print(my_request.status_code, "failed")
              return False
              
     # url modifier
     def url_modifier(self, page=1):
              
              # modify
              self.base_url = f"https://www.arabam.com/ikinci-el?searchText={self.brand}+{self.model}&take=50&currency=TL&minPrice={self.min_pr}&maxPrice={self.max_pr}&minYear={self.min_year}&maxYear={self.max_year}&page={page}"
              
     # scraper of content
     def scrap_the_content(self,  content):
              
              """ This function scrap the content of page and append url to the list of car urls """
              
              
              try:
                  # parse the page
                  page_content = BeautifulSoup(content, "lxml")
              
              
                  # div finder
                  divs = page_content.findAll("div", attrs={"class":"inner-container"})
              
                  # href finder
                  for i in divs:
                      try:
                          self.url_list.append("https://arabam.com"+i.find("a").get("href"))
                      except:
                          pass
              
              except:
                  pass
             
                                    
      # scarp between page numbers
     def scrap_pages(self, page_numbers):
          
          """this function scraps the given page numbers"""
          
          for number in range(1, page_numbers+1):
              self.url_modifier(page=number)
              
              content = self.requester(self.base_url)
              
              self.scrap_the_content(content)
              
              print(number, len(self.url_list))
      
     # scrap features from car urls list
     def feature_extractor(self):
          # for loop to travel on the car urls
          # requested and returned content
          # find the table content from parsed page
          
          for link in self.url_list:
              
              # request the page
              content = self.requester(link)
              
              # page parser
              div_finder = BeautifulSoup(content, "lxml")
              
              # table content
              div_list_header = div_finder.findAll("div", attrs={"class":"property-name"})
              
              div_list_value = div_finder.findAll("div", attrs={"class":"property-value"})
              
              
              # get some spesific features
              for header, value in zip(div_list_header, div_list_value):
                  
                  print(header.text.strip().replace("\n", ""), value.text.strip().replace("\n", ""))
              
              print("\n-------------")
              
          
          
c = ArabamScraper()
c.scrap_pages(4)
c.feature_extractor()