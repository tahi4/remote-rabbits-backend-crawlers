import scrapy
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
client = MongoClient("mongodb+srv://tahi:74391200@cluster0.ipj2m8y.mongodb.net/?retryWrites=true&w=majority")

db = client.remoterabbits
posts = db.posts

# posts.delete_many({})


class WeWorkRemotely(scrapy.Spider):

    we_work_remotely = requests.get('https://weworkremotely.com/remote-jobs.rss')

    soup = BeautifulSoup(we_work_remotely.text, 'xml' )
    items = soup.find_all('item')
    listings=[]
    for item in items:
        link = item.find('link').text
        listings.append(link)



    name = "wwr"
    # posts.delete_many({})
    start_urls = listings #didnt give a [] cus its already an array

 

    def parse(self, response):

        # card_button = response.css('div.company-card')
        # for button in card_button:
            

            tags = response.css('div.listing-header-container span.listing-tag::text').getall()
            type = tags[0]
            category = tags[1]
            region = tags[2]

            data = {

                'title': response.css('div.listing-header-container h1::text').get(),
                'company': response.css('div.company-card h2 a::text').get(),
                'jobtype': type,
                'category': category,
                'location': region,
                'link':  response.css('div.company-card a#job-cta-alt-2::attr(href)').get(),  
                'logo': response.css('div.listing-logo img::attr(src)').get(),
                's_link': response.request.url,
                'source': 'we work remotely'

            }
            yield posts.insert_one(data)



# REMEBER TO CHANGE COOKIES BEFORE YOU RUN !!
def Remotive():
    # name = 'remotive'
    
       
    header1={
            'Authority': 'remotive.com',
            'method': 'GET',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'cookie':'frontend_lang=en_US; _hjSessionUser_1264668=eyJpZCI6ImVhYjViOTY1LWFlYjYtNTBmMy05YzFlLTU1MzJhMTAyN2Y5ZiIsImNyZWF0ZWQiOjE2NzQzODYwOTIwNjUsImV4aXN0aW5nIjp0cnVlfQ==; crisp-client%2Fsession%2F52fbe69c-9517-4998-88a0-b10d4415b60e=session_53bb048d-1508-4d33-adc1-93e4c050793b; __stripe_mid=9a845626-21ba-4ce6-9e2d-45bc5ebabe4879ca8c; _ck_form=%7B%22166235%22%3A%7B%22shown%22%3A%222023-02-07T17%3A21%3A55.919Z%22%7D%7D; _ga_C4Z8MEF30D=GS1.1.1675790514.1.1.1675790734.0.0.0; session_id=f7470963d55d7c123703a0d60c488cd342d16d50; _gid=GA1.2.1291916473.1676205342; _hjShownFeedbackMessage=true; __atuvc=5%7C6%2C14%7C7; _ga_6LVX55VKHW=GS1.1.1676222750.10.1.1676223335.0.0.0; _ga=GA1.1.705195303.1675779810; cf_chl_2=e4f268421322cab; cf_clearance=hs6I7B4ZEEc6DpVMtapVG.AOXCfSCTjSQot1fI59rHg-1676225246-0-150'
                }
    # listings=[]

    remotive=requests.get('https://remotive.com/api/remote-jobs', headers=header1)
    print(remotive.status_code)
    # print(len(remotive.json()["jobs"]))
    response = remotive.json()
    for x in range(0, len(remotive.json()["jobs"])):
       posts.insert_one({
        'link':response['jobs'][x]['url'],
        'category':response['jobs'][x]['category'],
        'jobtype': response['jobs'][x]['job_type'],
        'location': response['jobs'][x]['candidate_required_location'],
        'company': response['jobs'][x]['company_name'],
        'title': response['jobs'][x]['title'],
        'logo': response['jobs'][x]['company_logo'],
        'source': 'remotive'
        })

    
    # return print(listings)

    
Remotive()


def RemoteOk():
        url= 'https://remoteok.com/api'
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" }
        remoteok = requests.get(url, headers=headers).json()
        # listings = []
        for x in range(1, len(remoteok)):
            posts.insert_one( { 
                'link':remoteok[x]['apply_url'],
                'logo':remoteok[x]['company_logo'],
                'company': remoteok[x]['company'],
                'location': remoteok[x]['location'],
                'title': remoteok[x]['position'],
                # 'jobtype': remoteok[x][''],
                'tags': remoteok[x]['tags'],
                'source': 'remoteok'
                

         })

RemoteOk()





