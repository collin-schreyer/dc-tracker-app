from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

project_companies = Table('project_companies', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('company_id', Integer, ForeignKey('companies.id'))
)

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(100), unique=True)
    name = Column(String(255))
    address = Column(String(500))
    city = Column(String(100))
    county = Column(String(100))
    state = Column(String(2))
    lat = Column(Float)
    lon = Column(Float)
    
    status = Column(String(50))  # Rumored, Permitting, Approved, Under Construction, Live
    est_mw = Column(Float)
    phases = Column(Integer)
    go_live_est = Column(String(50))
    
    owner = Column(String(255))
    developer = Column(String(255))
    customer = Column(String(255))
    utility = Column(String(255))
    substation = Column(String(255))
    kv_class = Column(String(50))
    epc = Column(String(255))
    electrical_contractor = Column(String(255))
    line_builder = Column(String(255))
    
    sources = Column(Text)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    companies = relationship('Company', secondary=project_companies, back_populates='projects')

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    role = Column(String(100))  # Owner, Developer, EPC, Utility, etc.
    parent_company = Column(String(255))
    website = Column(String(500))
    contact = Column(String(255))
    
    projects = relationship('Project', secondary=project_companies, back_populates='companies')

class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    source_type = Column(String(50))  # permit, news, report
    url = Column(String(1000))
    title = Column(String(500))
    date = Column(DateTime)
    content = Column(Text)

def init_db():
    engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///dc_tracker.db'))
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///dc_tracker.db'))
    Session = sessionmaker(bind=engine)
    return Session()
