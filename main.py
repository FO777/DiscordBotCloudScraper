import cloudscraper
import helheim
from helheim.exceptions import (
    HelheimException,
    HelheimSolveError,
    HelheimRuntimeError,
    HelheimSaaSError,
    HelheimSaaSBalance,
    HelheimVersion,
    HelheimAuthError
)
import bs4 as bs
import lxml
import discord
import os
import requests
from replit import db
from keep_alive import keep_alive
import concurrent.futures
import random

my_helauth = os.environ['helauth']
helheim.auth(my_helauth)
my_token = os.environ['token']
db.clear()
UserSessions = []
UserScrapers = []

proxylist = []



def make_proxy():
  global proxylist
  get_proxy = cloudsession.get('https://free-proxy-list.net/')
  soup = bs.BeautifulSoup(get_proxy.content, "lxml")
  finding = soup.find_all(class_="table table-striped table-bordered")
  string_finding = str(finding[0].find('tbody'))
  separating = list(string_finding.split('</tr>'))
  proxylist = []
  for n in separating:
      try:
          helper = n.split('<td>')
          https = helper[4].split('<td')
          if 'yes' in https[2]:
              proxylist.append('http://'+helper[1][:-5]+':'+helper[2][:-5])
      except:
          pass
          
def extract(proxy):
  global working_proxy
  try:
      cloudsession.proxies = {
         'http':proxy,
         'https':proxy
      }
      url = 'https://httpbin.org/ip'
      cloudsession.get(url, timeout=30)
      print("working proxy : "+proxy)
      working_proxy.append(proxy)
      return proxy
  except:
      return False

def injection(session, response):
    if helheim.isChallenge(session, response):
        # solve(session, response, max_tries=5)
        return helheim.solve(session, response)
    else:
        return response

cloudsession = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome', # we want a chrome user-agent
                'mobile': False, # pretend to be a desktop by disabling mobile user-agents
                'platform': 'windows' # pretend to be 'windows' or 'darwin' by only giving this type of OS for user-agents
            },
            requestPostHook=injection,
            # Add a hCaptcha provider if you need to solve hCaptcha
             captcha={
                 'provider': 'vanaheim' # use 'vanaheim' for built in solver, dont need api key param
             })

def update_zip(zipcode, user):
  if zipcode.isnumeric() and len(zipcode) == 5: 
    if user+"zipcodes" in db.keys():
      zipcodes = db[user+"zipcodes"]
      if zipcode not in zipcodes and len(zipcodes) < 10:
        zipcodes.append(zipcode)
        db[user+"zipcodes"] = zipcodes
    else:
      db[user+"zipcodes"] = [zipcode]


def delete_zip(zipcode, user):
  if zipcode.isnumeric() and len(zipcode) == 5:
    if user+"zipcodes" in db.keys():
      zipcodes = db[user+"zipcodes"]
    else:
      zipcodes = []
    if zipcode in zipcodes:
      zipcodes.remove(zipcode)
    db[user+"zipcodes"] = zipcodes


def list_zip(zipcode, user):
  if user+"zipcodes" in db.keys():
    zipcodes = db[user+"zipcodes"]
  else:
    zipcodes = []
  if len(zipcode)+len(zipcodes) <= 10:
    for i in zipcode:
      if i.isnumeric() and len(i) == 5 and i not in zipcodes:
        zipcodes.append(i)
  db[user+"zipcodes"] = zipcodes  

def clear_zip(user):
  db[user+"zipcodes"] = []

def print_zip(user):
  if user+"zipcodes" not in db.keys():
    db[user+"zipcodes"] = []
  qoute = db[user+"zipcodes"]
  return qoute

def update_sku(sku, user):
  if sku.isnumeric():
    if user+"skus" in db.keys():
      skus = db[user+"skus"]
      if sku not in skus and len(skus) < 10:
        skus.append(sku)
        db[user+"skus"] = skus
    else:
      db[user+"skus"] = [sku]

def delete_sku(sku, user):
  if sku.isnumeric():
    if user+"skus" in db.keys():
      skus = db[user+"skus"]
    else:
      skus = []
    if sku in skus:
      skus.remove(sku)
    db[user+"skus"] = skus

def list_sku(sku, user):
  if user+"skus" in db.keys():
    skus = db[user+"skus"]
  else:
    skus = []
  if len(sku)+len(skus) <= 10:
    for i in sku:
      if i.isnumeric() and i not in skus:
        skus.append(i)
  db[user+"skus"] = skus

def clear_sku(user):
  db[user+"skus"] = []

def print_sku(user):
  if user+"skus" not in db.keys():
    db[user+"skus"] = []
  qoute = db[user+"skus"]
  return qoute


class Session:
  def __init__(self, user, c_session):
    self.user = user
    self.searchurl = 'https://brickseek.com/walmart-inventory-checker?sku='
    self.url = 'https://brickseek.com/'
    self.c_session = c_session

  def NewSession(self, proxy):
    c_session = self.c_session
    c_session.proxies = {
           'http':proxy,
           'https':proxy
        }
    print("Getting Status...")                
    print(c_session.get('https://google.com/').status_code)
    gets = c_session.get(self.url)
    print(gets.status_code)
    
  def title(self, sku, proxy):
    c_session = self.c_session
    c_session.proxies = {
           'http':proxy,
           'https':proxy
        }
    get = c_session.get(self.searchurl+str(sku))
    title = bs.BeautifulSoup(get.content, "lxml")
    finding_title = title.find_all(class_="item-overview__title")
    some_of_title = str(finding_title[0])
    the_title = some_of_title[33:-5]
    sku_and_title = str(sku) + " : " + str(the_title)
    finding_image = title.find_all(class_="item-overview__image-wrap")
    string_image = str(finding_image[0])
    image_begin = string_image.find("src=")
    image_url = string_image[image_begin+5:-10]
    with open('image.png', 'wb') as f:
      f.write(requests.get(image_url).content)
    return sku_and_title
    

  def run(self, sku, proxy):
    user = self.user
    c_session = self.c_session
    c_session.proxies = {
           'http':proxy,
           'https':proxy
        }
    results = []
    price_final = []
    address_final = []
    stock_final = []
    zipcode = []
    state = []
    if str(user)+"zipcodes" in db.keys():
      print('yes')
      zips = db[self.user+"zipcodes"]
    else:
        print('no')
        zips = []
    for i in range(len(zips)):
      myobj = {'zip': zips[i], 'sku': sku}
      print('getting_status')
      post = c_session.post(self.searchurl, data=myobj)
      print(post.status_code)
      content = bs.BeautifulSoup(post.content, "lxml")
      price = content.find_all(class_="price-formatted__dollars")
      address = content.find_all(class_="address")
      stock = content.find_all(class_="availability-status-indicator__text")
      quantity = content.find_all(class_="table__cell-quantity")
      for x in range(len(price)):
        price_string = str(price[x])
        price_final.append(price_string[39:-7])
      for x in range(len(address)):
        address_string = str(address[x])
        end_of_address = address_string.find('<br')
        end_of_zip = address_string.find(" <div")
        address_final.append(address_string[26:end_of_address])
        state.append(address_string[end_of_address+5:end_of_zip-6])
        zipcode.append(address_string[end_of_zip-5:end_of_zip])
      for x in range(len(stock)):
        stock_string = str(stock[x])
        if stock_string[50:-7] == 'In Stock':
            quantity_string = str(quantity[0])
            stock_quantity = stock_string[50:-7] +": "+ quantity_string[45:-7]+","
            stock_final.append(stock_quantity)
            quantity.pop(0)
        else:
            stock_final.append(stock_string[50:-7])
      for x in range(len(address_final)):
        check = str(address_final[x])+", "+str(state[x])+"  "+str(zipcode[x])+", "+str(stock_final[x])+" price: "+str(price_final[x])
        if "Out of Stock" not in check:
          if check not in results:
            results.append(str(address_final[x])+", "+str(state[x])+", zip: "+str(zipcode[x])+", "+str(stock_final[x])+" price: "+str(price_final[x]))
    return results
      

client = discord.Client()

  
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global working_proxy
  
    if message.author == client.user:
      return

    # ---- use to make only dm worthy to one person
    #elif str(message.author) != "alexander gallo#0790":
    #  return
  
    elif str(message.channel.type) == "private":
      return

    elif message.content.startswith('$hi'):
      await message.channel.send(message.author)

  
    elif message.content.startswith('$hello'):
      await message.channel.send("Hello!")

    elif message.content.startswith('$refresh'):
      make_proxy()
      proxers = list(set(proxylist))
      with concurrent.futures.ThreadPoolExecutor() as execu:
          working_proxy = []
          execu.map(extract, proxers)
      await message.channel.send(str(message.author)+" - ip's refreshed!")
      
    elif message.content.startswith('$addzip'):
      zipcode = message.content.split("$addzip ",1)[1]
      update_zip(zipcode, str(message.author))
      qoute = print_zip(str(message.author))
      await message.channel.send(str(message.author)+' - ZIP Added! ZIP List: '+ str(qoute))
    elif message.content.startswith('$delzip'):
      zipcode = message.content.split("$delzip ",1)[1]
      delete_zip(zipcode, str(message.author))
      qoute = print_zip(str(message.author))
      await message.channel.send(str(message.author)+' - ZIP Deleted! ZIP List: '+ str(qoute))
    elif message.content.startswith('$listzip'):
      ziplong = message.content.split("$listzip ",1)[1]
      zipcode = list(ziplong.split(" "))
      list_zip(zipcode, str(message.author))
      qoute = print_zip(str(message.author))
      await message.channel.send(str(message.author)+" - ZIP List added! ZIP List: "+str(qoute))
    elif message.content.startswith('$clearzip'):
      clear_zip(str(message.author))
      await message.channel.send(str(message.author)+": ZIP List cleared!")
    elif message.content.startswith('$zip'):
      qoute = print_zip(str(message.author))
      await message.channel.send(str(message.author)+" - ZIP List: "+ str(qoute))
      
    elif message.content.startswith('$addsku'):
      sku = message.content.split("$addsku ",1)[1]
      update_sku(sku, str(message.author))
      qoute = print_sku(str(message.author))
      await message.channel.send(str(message.author)+' - SKU Added! SKU List: '+ str(qoute))
    elif message.content.startswith('$delsku'):
      sku = message.content.split("$delsku ",1)[1]
      delete_sku(sku, str(message.author))
      qoute = print_sku(str(message.author))
      await message.channel.send(str(message.author)+' - SKU Deleted! SKU List: '+ str(qoute))
    elif message.content.startswith('$listsku'):
      skulong = message.content.split("$listsku ",1)[1]
      sku = list(skulong.split(" "))
      list_sku(sku, str(message.author))
      qoute = print_sku(str(message.author))
      await message.channel.send(str(message.author)+" - SKU list added! SKU List: "+str(qoute))
    elif message.content.startswith('$clearsku'):
      clear_sku(str(message.author))
      await message.channel.send(str(message.author)+': SKU List cleared!')
    elif message.content.startswith('$sku'):
      qoute = print_sku(str(message.author))
      await message.channel.send(str(message.author)+" - SKU List: "+ str(qoute))
      
    elif message.content.startswith('$create'):
      if "scrapers" in db.keys():
        scrapers = db["scrapers"]
      else:
        scrapers = []
      if str(message.author) not in scrapers:
        scrapers.append(str(message.author))
        db["scrapers"] = scrapers
        if "users" in db.keys():
          users = db["users"]
        else:
          db["users"] = []
          users = db["users"]
        if str(message.author) in users:
          author_index = users.index(str(message.author))
          UserScrapers.append([Session(str(message.author), UserSessions[author_index]), False])
        else:
          users.append(str(message.author))
          db["users"] = users
          UserSessions.append(cloudscraper.create_scraper(
            browser={
                'browser': 'chrome', # we want a chrome user-agent
                'mobile': False, # pretend to be a desktop by disabling mobile user-agents
                'platform': 'windows' # pretend to be 'windows' or 'darwin' by only giving this type of OS for user-agents
            },
            requestPostHook=injection,
            # Add a hCaptcha provider if you need to solve hCaptcha
             captcha={
                 'provider': 'vanaheim' # use 'vanaheim' for built in solver, dont need api key param
             }
        ))
          UserScrapers.append([Session(str(message.author), UserSessions[-1]), False])
      await message.channel.send(str(message.author)+': Session initiated!')
      
    elif message.content.startswith('$ready'):
      if "scrapers" not in db.keys():
        await message.channel.send(str(message.author)+': Use $create command first')
      elif "scrapers" in db.keys():
        scrapers = db["scrapers"]
        if str(message.author) not in scrapers:
          await message.channel.send(str(message.author)+': Use $create command first')
        else:
          scrapers = db["scrapers"]
          author_index = scrapers.index(str(message.author))
          for n in working_proxy:
            try:
              UserScrapers[author_index][0].NewSession(n)
              working = True
              UserScrapers[author_index][1] = True
              print('done')
              await message.channel.send(str(message.author)+': Session ready!')
              break
            except:
              working = False
          if working == False:
            await message.channel.send(str(message.author)+': use $refresh command')
      
    elif message.content.startswith('$run'):
      if "scrapers" not in db.keys():
        await message.channel.send(str(message.author)+': Use $create command first and then $ready command second')
      else:
        scrapers = db["scrapers"]
        if str(message.author) not in scrapers:
          await message.channel.send(str(message.author)+': Use $create command first and then $ready command second')
          return
        author_index = scrapers.index(str(message.author))
        if str(message.author) in scrapers and UserScrapers[author_index][1] == False:
          await message.channel.send(str(message.author)+': Use $ready command first')
          return
        else:
          await message.channel.send(str(message.author)+': Session running!')
      if str(message.author)+"skus" in db.keys():
        skus = db[str(message.author)+"skus"]
      else:
        skus = []
      for x in range(len(skus)):
        for n in working_proxy:
          try:
            qoute = UserScrapers[author_index][0].title(skus[x], n)
            await message.channel.send(str(message.author)+" - "+str(qoute), file=discord.File('image.png'))
            result = UserScrapers[author_index][0].run(skus[x], n)
            await message.channel.send(str(message.author)+":")
            for res in result:
              await message.channel.send(str(res))
            working = True
            break
          except:
            working = False
            pass  
      if working == False:
        await message.channel.send(str(message.author)+": use $refresh command") #could automate for them but eh, testing still



keep_alive()
#creates url that we will ping
#uptimerobot.com
# free account
# https
client.run(my_token)
