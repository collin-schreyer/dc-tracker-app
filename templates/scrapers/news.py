import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from models import NewsArticle, DataCenterProject
from database import SessionLocal

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.db = SessionLocal()
        
        # RSS feeds for data center news
        self.feeds = {
            'DataCenterDynamics': 'https://www.datacenterdynamics.com/en/rss/',
            'DataCenterKnowledge': 'https://www.datacenterknowledge.com/feed'
        }
    
    def scrape_all_feeds(self):
        """Scrape all configured news feeds"""
        for source, feed_url in self.feeds.items():
            try:
                self.scrape_rss_feed(source, feed_url)
            except Exception as e:
                print(f"Error scraping {source}: {e}")
    
    def scrape_rss_feed(self, source, feed_url):
        """Scrape RSS feed for data center articles"""
        response = self.session.get(feed_url)
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')
        
        for item in items:
            title = item.find('title').text if item.find('title') else ''
            link = item.find('link').text if item.find('link') else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') else ''
            description = item.find('description').text if item.find('description') else ''
            
            # Filter for data center construction/development articles
            if self._is_datacenter_article(title, description):
                article_data = {
                    'title': title,
                    'url': link,
                    'source': source,
                    'published_date': self._parse_rss_date(pub_date),
                    'content': description
                }
                
                self._save_article(article_data)
    
    def _is_datacenter_article(self, title, description):
        """Check if article is about data center development"""
        keywords = [
            'data center', 'datacenter', 'hyperscale', 'campus',
            'construction', 'development', 'groundbreaking',
            'permits', 'approved', 'announced', 'pipeline'
        ]
        
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in keywords)
    
    def _parse_rss_date(self, date_str):
        """Parse RSS date to datetime"""
        try:
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except:
            return None
    
    def _save_article(self, article_data):
        """Save article to database"""
        # Check if article already exists
        existing = self.db.query(NewsArticle).filter_by(url=article_data['url']).first()
        if existing:
            return
        
        article = NewsArticle(
            title=article_data['title'],
            url=article_data['url'],
            source=article_data['source'],
            published_date=article_data['published_date'],
            content=article_data['content']
        )
        
        self.db.add(article)
        self.db.commit()
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_all_feeds()
    scraper.close()