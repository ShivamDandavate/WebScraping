from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import dateparser
import logging


'''logger file configuration'''
logging.basicConfig(filename='logger.log',filemode="a",level=logging.INFO,format='%(asctime)s -- %(levelname)s : %(message)s')


''' class with scraping methods'''
class Scraper:

    
    def BingScraper(company: str,keywords: str, page_count: int):
        '''
        This method scrapes data based on the given search string from Bing search engine

        Parameters:
            company    : Company name.
            keywords   : List of keywords.
            page_count : Number of pages to scrap.
            
        Returns:
            df : DataFrame of scraped data from Bing search engine.
            
        '''
        titles=[]
        times=[]
        medias=[]
        links=[]
        i=1
        search_string=company+" "+keywords
           
        try:
            while(i <= page_count):
                response=requests.get(f"https://www.bing.com/news/infinitescrollajax?qs=n&form=QBNT&sp=-1&lq=0&pq=te&sc=10-2&sk=&cvid=1590B94F6A1A40E89C0451EE4930A31D&ghsh=0&ghacc=0&ghpl=&InfiniteScroll=1&q={search_string}&first={i}1&IG=0E2CB393962B4A62A88816B1959CC59C&IID=news.5199&SFX={i}&PCW=1116")
                soup=bs(response.text,'html.parser')
                for anchor in soup.find_all('div',class_='news-card newsitem cardcommon'):
                    links.append(anchor['url'])
                    titles.append(anchor['data-title'])
                    medias.append(anchor['data-author'])
                for time in soup.find_all('span',tabindex='0'):
                    times.append(dateparser.parse(time.text))
                i+=1
            data={"Link":links,"Title":titles,"Source":medias,"Time":times,"Search Engine" :'Bing',"search String":search_string}
            df=pd.DataFrame(data)
        except Exception as e:
            logging.error(f'An error occured: {e}',exec_info=True)
        return df


    def GoogleScraper(company: str,keywords: str, page_count: int):
        '''
        This method scrapes data based on the given search string from Google search engine

        Parameters:
            company    : Company name.
            keywords   : List of keywords.
            page_count : Number of pages to scrap.
            
        Returns:
            df : DataFrame of scraped data from Google search engine.
            
        '''
        titles=[]
        times=[]
        medias=[]
        links=[]
        j=1
        search_string=company+" "+keywords
        try:
            while(j<=page_count):
                    response=requests.get(f"https://www.google.com/search?q={search_string}&tbm=nws&page={j}/")
                    soup=bs(response.text,'html.parser')
                    for title in soup.find_all('div',class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
                            titles.append(title.h3.text)
                            for p in title.find_all('div',class_="BNeawe UPmit AP7Wnd lRVwie"):
                                medias.append(p.text)
                            links.append((title.a['href']).replace("/url?q=",""))
                            for p in title.find_all('span',class_="r0bn4c rQMQod"):
                                times.append(dateparser.parse(str(p.text)))
                    j+=1
            
        except Exception as e:
            logging.error(f'An error occured: {e}',exec_info=True)
            
        data={"Link":links,"Title":titles,"Source":medias,"Time":times,"Search Engine" :'google',"search String":search_string}
        df=pd.DataFrame(data)
        return df
    def YahooScraper(company: str,keywords: str, page_count: int):
        '''
        This method scrapes data based on the given search string from Yahoo search engine

        Parameters:
            company    : Company name.
            keywords   : List of keywords.
            page_count : Number of pages to scrap.
            
        Returns:
            df : DataFrame of scraped data from Yahoo search engine.
            
        '''
        links=[]
        titles=[]
        times=[]
        medias=[]
        search_string=company+" "+keywords
        j = 0
        try:
            while j <page_count:
                r = requests.get(f"https://news.search.yahoo.com/search?q={search_string}&page={j}/")
                soup = bs(r.text, 'html.parser')
                news = soup.find_all('div', class_='dd NewsArticle')
                for i in news:
                    tag = i.find('span', class_='fc-2nd s-time mr-8')
                    headline = i.find('h4' )
                    titles.append(headline.get_text())
                    links.append(i.a['href'])
                    medias.append(i.span.text)
                    times.append(dateparser.parse(tag.get_text()))
                j += 1   

            news_data ={"Link":links,"Title":titles,"Time":times,"Source":medias,"Search Engine" :'Yahoo',"search String":search_string}
            df = pd.DataFrame(news_data)
        except Exception as e:
              logging.error(f'An error occured: {e}',exec_info=True)  
        return df
