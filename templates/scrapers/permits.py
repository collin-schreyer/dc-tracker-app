import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from models import PermitRecord, DataCenterProject
from database import SessionLocal

class PermitScraper:
    def __init__(self):
        self.session = requests.Session()
        self.db = SessionLocal()
    
    def scrape_nd_deq_permits(self):
        """Scrape North Dakota DEQ air permits for data center projects"""
        base_url = "https://www.ndhealth.gov/aq/permits/"
        
        # Keywords to identify data center permits
        dc_keywords = [
            "emergency generator", "backup generator", "RICE", 
            "server farm", "data center", "computing center"
        ]
        
        try:
            response = self.session.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simplified example - actual implementation would need
            # to navigate the specific permit database structure
            permits = self._extract_permits_from_page(soup, dc_keywords)
            
            for permit_data in permits:
                self._save_permit(permit_data, 'ND')
                
        except Exception as e:
            print(f"Error scraping ND permits: {e}")
    
    def _extract_permits_from_page(self, soup, keywords):
        """Extract permit information from parsed HTML"""
        permits = []
        
        # This would need to be customized for each state's permit database
        # Example structure - actual implementation depends on site layout
        permit_rows = soup.find_all('tr', class_='permit-row')
        
        for row in permit_rows:
            description = row.find('td', class_='description')
            if description and any(keyword.lower() in description.text.lower() for keyword in keywords):
                permit = {
                    'permit_number': row.find('td', class_='permit-number').text.strip(),
                    'applicant': row.find('td', class_='applicant').text.strip(),
                    'description': description.text.strip(),
                    'issue_date': self._parse_date(row.find('td', class_='date').text.strip()),
                    'source_url': row.find('a')['href'] if row.find('a') else None
                }
                permits.append(permit)
        
        return permits
    
    def _parse_date(self, date_str):
        """Parse date string to datetime object"""
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')
        except:
            return None
    
    def _save_permit(self, permit_data, state):
        """Save permit to database"""
        permit = PermitRecord(
            permit_number=permit_data['permit_number'],
            permit_type='Air',
            state=state,
            agency='ND DEQ',
            applicant=permit_data['applicant'],
            description=permit_data['description'],
            issue_date=permit_data['issue_date'],
            source_url=permit_data['source_url']
        )
        
        self.db.add(permit)
        self.db.commit()
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    scraper = PermitScraper()
    scraper.scrape_nd_deq_permits()
    scraper.close()