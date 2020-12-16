
from logging import raiseExceptions
from bs4 import BeautifulSoup
import nltk
import json
import requests
import webbrowser
import justext
from urllib.request import urlopen
import re
from urllib.parse import urlparse
import urllib.parse as urlparse
import re
def collect_item_JSON_data(query_item_id):
    item_json="http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="+query_item_id
    item_json_generate = urlopen(item_json)
    j_obj=json.load(item_json_generate)
    #print ("Printing price as " + str(j_obj['item']['current']['price'])+".")
    itemPrice_current=j_obj['item']['current']['price']
    item_name=j_obj['item']['name']
    #print("Item Name->",item_name)
    return item_name,itemPrice_current

def readify_queries(links):
    items=[]
    for x in links:
        #print("->",x)
        new_string=x
        new_string=new_string.replace('\n',"")
        new_string=new_string.replace('<td>',"")
        new_string=new_string.replace('</td>',"")
        new_string=new_string.replace('</a>',"")
        new_string=new_string.replace('<span>',"")
        new_string=new_string.replace('</span>',"")
        new_string=new_string.replace('"',"")
        new_string=new_string.split('title')
        str1=new_string[0]
        #print("->",str1)
        str2=str1.split('<a class=table-item-link href=https://secure.runescape.com/m=itemdb_rs/')
        #print("->",str2)
        str3=str2[1].split('/viewitem?obj=')
        #print(str3[1])
        query=str3[1].replace(" ","")
        #print(query)
        #print("--------------------------------------")
        items.append(query)
    return items
    

def start_finding_price(query):
    query_items=[]
    query=query.capitalize()
    base_link='http://services.runescape.com/m=itemdb_rs/results.ws?query='
    print("->",base_link+query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    r = requests.get(base_link+query, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = []

    for x in soup.findAll('td'):
        create_string=str(x)
        if (query in create_string ) and 'title' in create_string :
            links.append(create_string)
            #print("->",create_string)
            #print("--------------------------------")
    query_items=readify_queries(links)
    count=0
    items_to_send=[]
    for x in query_items:
        if(count>10):
            break
        item_info=collect_item_JSON_data(x)

        #print("--------------------------------")
        #print("Item ID->"+x+"<-")
        print("Item Price->",item_info)
        items_to_send.append(item_info)
        count+=1

    print("Done finding items. \n")
    print("All items: " , items_to_send)

    return items_to_send
#start_finding_price("Raw lobster")


