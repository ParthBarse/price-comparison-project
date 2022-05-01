from cgitb import text
from distutils.log import debug
from operator import index
import os
from numpy import append
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request
import requests
import random


app = Flask(__name__)


# @app.route("/", methods=["GET", "POST"])
# def home():
#     return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def index():
    s = HTMLSession()

    def get_lnks_amz(soup):
        for dt1 in soup.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
            prodLnk = dt1['href']
            productLinks_amz.append(prodLnk)

    def get_info_amz(url):
        productName2 = ""
        price = ""
        imgLnk = ""
        starRating = ""

        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]
        proxies = {'https': random.choice(proxies_list)}

        r = requests.get(url, headers=headers).text
        soup = bs(r, "html.parser")

        try:
            productName2 = soup.find(
                'span', {'id': 'productTitle'}).text.strip()
        except Exception as e:
            print(e)
            print("Product Name not found !")

        try:
            price = soup.find('span', {'class': 'a-price-whole'}).text.strip()
            price = "₹" + price
        except Exception as e:
            print(e)
            print("Product Price not found !")

        try:
            imgLnk = soup.find('img', {'id': 'landingImage'})
            imgLnk = imgLnk['src']
        except Exception as e:
            print(e)
            print("Image Link not found !")

        tempV = {
            "Site": "Amazon",
            "Product Name": productName2,
            "Quantity": 1,
            "Price": price,
            "Image  Link": imgLnk,
            "Star Rating": starRating,
            "Product Link": url}

        finalData_amz.append(tempV)

    def get_lnks_flp(soup):
        for dt1 in soup.find_all('a', {'rel': 'noopener noreferrer'}):
            prodLnk = dt1['href']
            productLinks_flp.append(prodLnk)

    def get_info_flp(url):
        productName2 = ""
        price = ""
        imgLnk = ""
        starRating = ""

        s = HTMLSession()
        r = s.get(url).text
        soup = bs(r, "html.parser")

        try:
            productName2 = soup.find('span', {'class': 'B_NuCI'}).text.strip()
        except Exception as e:
            print(e)
            print("Product Name not found !")

        try:
            price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()
        except Exception as e:
            print(e)
            print("Product Price not found !")

        try:
            imgLnk = soup.find('div', {'class': 'CXW8mj _3nMexc'}).find('img')
            imgLnk = imgLnk['src']
        except Exception as e:
            print(e)
            print("Image Link not found !")

        tempV = {
            "Site": "Flipkart",
            "Product Name": productName2,
            "Quantity": 1,
            "Price": price,
            "Image  Link": imgLnk,
            "Star Rating": starRating,
            "Product Link": url}

        finalData_flp.append(tempV)

    # #Driver Code Amazon -

    def driverAmz(productName):
        surl = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + productName

        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]
        proxies = {'https': random.choice(proxies_list)}

        r = requests.get(surl, headers=headers).text

        soup1 = bs(r, "html.parser")
        print(soup1)

        try:
            get_lnks_amz(soup1)
        except Exception as e:
            print(e)
            print("Product Links not found !")

        try:
            for lnk1 in productLinks_amz[2:6]:
                nurl = "https://www.amazon.in" + lnk1
                get_info_amz(nurl)
        except Exception as e:
            print(e)
            print("Product info not found !")

    # Driver Code Flipkart -

    def driverFlp(productName):
        surl = "https://www.flipkart.com/search?q=" + productName

        s = HTMLSession()
        r = s.get(surl).text

        soup2 = bs(r, "html.parser")

        try:
            get_lnks_flp(soup2)
        except Exception as e:
            print(e)
            print("Product Links not found !")

        try:
            for lnk1 in productLinks_flp[0:5]:
                nurl = "https://www.flipkart.com" + lnk1
                get_info_flp(nurl)
        except Exception as e:
            print(e)
            print("Product info not found !")

    # Driver Code -

    finalData_amz = []
    productLinks_amz = []
    finalData_flp = []
    productLinks_flp = []

    productName1 = request.form.get("productName_inp", "")
    productName = productName1.replace(" ", "+")

    if productName == "":
        productName = "Iphone"

    driverAmz(productName)
    driverFlp(productName)

    finalData = finalData_amz + finalData_flp

    d1 = ""
    d2 = ""
    d3 = ""
    d4 = ""
    d5 = ""
    d6 = ""
    d7 = ""
    d8 = ""
    d9 = ""

    try:
        d_1 = finalData[0]
        keys1, values1 = zip(*d_1.items())
        d1 = values1
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_2 = finalData[1]
        keys2, values2 = zip(*d_2.items())
        d2 = values2
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_3 = finalData[2]
        keys3, values3 = zip(*d_3.items())
        d3 = values3
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_4 = finalData[3]
        keys4, values4 = zip(*d_4.items())
        d4 = values4
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_5 = finalData[4]
        keys5, values5 = zip(*d_5.items())
        d5 = values5
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_6 = finalData[5]
        keys6, values6 = zip(*d_6.items())
        d6 = values6
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_7 = finalData[6]
        keys7, values7 = zip(*d_7.items())
        d7 = values7
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_8 = finalData[7]
        keys8, values8 = zip(*d_8.items())
        d8 = values8
    except Exception as e:
        print(e)
        print("Data not found !")

    try:
        d_9 = finalData[7]
        keys9, values9 = zip(*d_9.items())
        d9 = values9
    except Exception as e:
        print(e)
        print("Data not found !")

    return render_template("index.html", data=finalData, productName_=productName1, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7, d8=d8, d9=d9)


if __name__ == "__main__":
    app.run(debug=True)

# -------------------------------------------------------------------------------------


# ........................................................................................

# Data Saving for Website - 1

# Saving the Data to Excel Sheet -

# df = pd.DataFrame.from_dict(finalData_amz)
# print(df)
# df.to_excel('dataWeb_1.xlsx', index=False)


# # To Save Data in JSON file -
# import json

# def save_data(title, data):
#   with open(title, 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)

# def load_data(title):
#   with open(title, encoding="utf-8") as f:
#     return json.load(f)


# save_data("dataWeb_1.json", finalData_amz)

# ........................................................................................
