import json
import pandas as pd
from ScrapingFunction import Scraper as sp
import tqdm
import logging
import streamlit as st

logging.basicConfig(filename='logger.log',filemode="w",level=logging.INFO,format='%(asctime)s -- %(levelname)s : %(message)s')

def main():
    with open("config.json") as f:
        data = json.load(f)

    company_names = data['company_name']
    keywords = data['keywords']
    page_count = data['page_count']

    final_df = pd.DataFrame()
    for company_name in tqdm.tqdm(company_names):
        for keyword in tqdm.tqdm(keywords):

            logging.info(f"Scraping data of company {company_name} with keywords {','.join(keyword)} using Google")
            df1 = sp.GoogleScraper(company_name,','.join(keyword), page_count)

            logging.info(f"Scraping data of company {company_name} with keywords {','.join(keyword)} using Yahoo")
            df2 = sp.YahooScraper(company_name, ','.join(keyword), page_count)

            logging.info(f"Scraping data of company {company_name} with keywords {','.join(keyword)} using Bing")  
            df3 = sp.BingScraper(company_name, ','.join(keyword), page_count)
            final_df = pd.concat([final_df,df1,df2,df3], ignore_index=True)
    final_df.to_csv('news.csv',index=False)
    
    st.dataframe(final_df)
if __name__ == '__main__':
    main()
