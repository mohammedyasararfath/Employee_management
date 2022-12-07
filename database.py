from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://root:Arfath@1997@127.0.0.1:3306/employee_management', echo=True)
conn = engine.connect()

metadata = db.MetaData()

Base = automap_base()
Base.prepare(engine, reflect=True)

Session = sessionmaker(bind=engine)
session = Session()
