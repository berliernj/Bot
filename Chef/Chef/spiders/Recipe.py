import scrapy
import time
from twilio.rest import Client
from selenium import webdriver
from scrapy.http import Request
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# client = Client("ACCOUNT_SID", "AUTH_TOKEN")


class botSpider(scrapy.Spider):
   name = "bestbuy"
   USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/43.0.2357.130 Safari/537.36 "

   # Enter Your Product URL Here.
   start_urls = ["https://www.bestbuy.com/site/corsair-hs60-pro-surround-wired-stereo-gaming-headset-carbon/6360422.p?skuId=6360422", ]

   def parse(self, response):

       # Finding Product Status.
       try:
           product = response.xpath("//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
           if product:
               print(f"\nProduct is Currently: Available.\n")
           else:
               print("\nProduct is Out of Stock.\n")
       except NoSuchElementException:
           pass

       if product:
           print("\nFound 1 item to add to cart.\n")

           # Want to Receive text messages?
           # client.messages.create(to="+1YOURNUMBER", from_="+1TWILIONUMBER", body="Bot has made a Bestbuy purchase!")

           # Booting WebDriver.
           PATH = "/Users/berliernj/Documents/chromedriver"
           options = webdriver.ChromeOptions()
           options.add_argument(r'/Users/berliernj/Library/Application Support/Google/Chrome/')
           driver = webdriver.Chrome(PATH)

           # Starting Webpage.
           driver.get(response.url)
           time.sleep(5)

           # Click Add to Cart.
           print("\nClicking Add To Cart Button.\n")
           driver.find_element_by_xpath("//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']").click()
           time.sleep(5)

           # Click Cart.
           print("\nGoing to Shopping Cart.\n")
           driver.get("https://www.bestbuy.com/cart")
           time.sleep(5)

           # Click Check-out Button.
           print("\nClicking Checkout Button.\n")
           driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary']").click()

           # Giving Website Time To Login.
           print("\nGiving Website Time To Login. Program Sleeping for 10 Seconds.\n")
           time.sleep(10)

           # CVV Number Input.
           print("\nInputing CVV Number.\n")
           try:
               security_code = driver.find_element_by_id("credit-card-cvv")
               time.sleep(5)
               security_code.send_keys("016")  # You can enter your CVV number here.
           except NoSuchElementException:
               pass

           # ARE YOU READY TO BUY?
           #print("\nBuying Product.\n")
           #driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary button__fast-track']").click()

           #print("\nBot has Completed Checkout.\n")
           #time.sleep(10)

       else:
           print("\nRetrying Bot In 45 Seconds.\n")
           # Leave timer at 45 Seconds to avoid getting ip blocked.
           time.sleep(1)
           yield Request(response.url, callback=self.parse, dont_filter=True)
