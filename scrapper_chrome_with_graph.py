import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options
import time
import math
from os import system
from pyfiglet import Figlet
from playsound import playsound as ps
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

system('cls')
system('mode con: cols=90 lines=30')
# Create figure for plotting
fig = plt.figure()
fig.canvas.set_window_title('Gold Price Comparision Graph')
ax = fig.subplots(2)
plt.subplots_adjust(bottom=0.25, hspace=0)
xs = []
ys = []
ys2 = []

system("title "+ "Gold Tracker")

start_time = time.time()

        
custom_fig = Figlet(font='big')
print(custom_fig.renderText('GOLDTRACKER'))
print("With graph support")
print("Author: Akarsh Tripathi")
time.sleep(5)


#old requests method

#URL = 'https://paytm.com/digitalgold'

#headers = {
#    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
#
#page = requests.get(URL, headers=headers)


op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_argument('--log-level=3')
driver = webdriver.Chrome(options=op)


driver.get("https://paytm.com/digitalgold")
html = driver.execute_script("return document.documentElement.outerHTML")

soup = BeautifulSoup(html, 'html.parser')

#infinite loop
#i = -1

def main():
    while True:
        system('mode con: cols=40 lines=7')
        print("Refreshing...")
        system('cls')

        #get buy price
        buy_rate = soup.find("div", class_="_1cMg").get_text()
        buy_obj = re.findall("\d+\.\d+", buy_rate)
        buy_price = float(buy_obj[0])

        #add tax
        #add_tax_raw = ((buy_price * 3.0/100.0) + buy_price)/1000
        add_tax_raw = (buy_price * 3.0/100.0) + buy_price
        add_tax = round(add_tax_raw, 2)
        
        print(" ")
        buy_var = "  Buy Price including tax : " + "₹" + str(add_tax) + "/g"
        print(buy_var)
        print(" ")
        print("----------------------------------------")
        print(" ")


        #get sell price
        click_sell = driver.find_element_by_link_text('Sell')
        click_sell.click()

        sell_html = driver.execute_script("return document.documentElement.outerHTML")
        sell_soup = BeautifulSoup(sell_html, 'html.parser')

        sell_rate = sell_soup.find("div", class_="_1cMg").get_text()
        sell_obj = re.findall("\d+\.\d+", sell_rate)
        sell_price = float(sell_obj[0])
        #sell_price = round(((float(sell_obj[0]))/1000), 2)
        sell_var = "  Current Selling Price :" + " ₹" + str(sell_price) + "/g"
        print(sell_var)

        string_add_tax = str(add_tax)
        string_sell_price = str(sell_price)

        if add_tax <= 5039.00 :
            ps('alert.mp3')
        if sell_price >= 5029.00 :
            ps('alert.mp3')

        #dataset for ploting
        rate_list = open("y_axis_buy.txt", "a")
        
        #write to list
        L = [string_add_tax, "\n"]
        rate_list.writelines(L) 
        rate_list.close()

        sell_list = open("y_axis_sell.txt", "a")
        M = [string_sell_price, "\n"]
        sell_list.writelines(M)
        sell_list.close()

        return add_tax, sell_price
        #i = i + 1

        #num_gen.x_gen(i)

        #refresh
        driver.refresh()
        break

#########GRAPH DEF#################
def animate(i, xs, ys, ys2):

# Read temperature (Celsius) from TMP102
    #temp_c = round(tmp102.read_temp(), 2)

    price = main()

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append((price[0])/1000)
    ys2.append((price[1])/1000)
    # Limit x and y lists to 20 items
    xs = xs[-70:]
    ys = ys[-20:]
    ys2 = ys2[-20:]

    # Draw x and y lists
    ax[0].clear()
    ax[1].clear()   
    ax[0].plot(ys, label = 'Buy Price(inc. tax)', color='orange')
    ax[1].plot(xs, ys2, label = 'Sell Price', color='green')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    ax[0].set_title('Live Gold Buy Rate (inc. gst)')
    ax[1].set_title('Live Gold Sell Rate')
    plt.ylabel('-------Price per mg---------->')
    


ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, ys2), interval = 10000, repeat = False)
ani.event_source.stop()
plt.show()


#########GRAPH DEF#################
#print(rate)
driver.quit()

print()
print("--- Ran for: ")
print("--- %s seconds ---" % (time.time() - start_time))