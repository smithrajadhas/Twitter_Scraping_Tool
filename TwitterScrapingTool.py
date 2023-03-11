# Twitter Scraping Tool

# Importing of Required Libraries:

import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import numpy as np
import pymongo
from PIL import Image
import json
import base64


#Specifying the Header and Short Description of the App

image = Image.open("twitterheader.jpg")
st.image(image)
st.subheader("Search with a **Keyword or #** & Get Your Tweets in Seconds!!!")

# Defining the User Inputs Using Streamlit Library:

keyword = st.text_input("**Enter the Keyword**","")
limit = st.number_input("**Enter the Tweet Count**", min_value = 1, max_value = 1000, step = 1 )
st.write("**Note:** The Maximum Count is upto **1000** Tweets.")
start_date = st.date_input("**Select the Start Date**")
end_date = st.date_input("**Select the End Date**")


# Defining a Function "process" to Scrape Tweets & Return as Dataframe using Pandas & Numpy Library:

def process():
    scraper = sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}")

    list_of_tweets = []

    for i,tweet in enumerate(scraper.get_items()):
        if i > limit-1:
            break
        list_of_tweets.append ([tweet.date,tweet.id,tweet.url,tweet.content,tweet.user,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount]) 

        df = pd.DataFrame(list_of_tweets, columns = ["Date","Id","Url","Tweet Content","User","Reply Count","Retweets","Language","Source","Likes"])
        df.index = np.arange(1, len(df) + 1)
    return df


# To View the Tweets Extracted as Dataframe using "process" Function in Streamlit App:

if st.button("Extract Tweets"):
    df = process()
    st.dataframe(df)
        

# Uploading the Scraped Tweets Data to MongoDB Database Using PyMongo Library:

if st.button("Upload to MongoDB"):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Projects"]
    collection = db["Twitter_Scraper"]
    data_dict = json.loads(process().to_json(orient="records"))
    collection.insert_many(data_dict)
    st.success("Uploaded Sucessfully to MongoDB")
    
    
# To Download the Scraped Tweets Data in .csv Format Using Base64 Library:
    
if st.button("Download as CSV"): 
    st.write("**Click Below** to Download as **CSV**")
    csv = process().to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="scrapedtweet_data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)


# To Download the Scraped Tweets Data in .json Format Using Json & Base64 Library:
    
if st.button("Download as JSON"):
    st.write("**Click Below** to Download as **JSON**")
    json_string = process().to_json(indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="scrapedtweet_data.json">Download JSON File</a>'
    st.markdown(href, unsafe_allow_html=True)
    