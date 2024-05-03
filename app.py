from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import pyodbc
import os

# Initialise Flask App
app = Flask(__name__)

# database connection 
server = 'devops-project-server.database.windows.net'
database = 'orders-db'
username = 'maya'
password = 'AiCore1237'
driver= '{ODBC Driver 18 for SQL Server}'

# Create the connection string
connection_string=f'Driver={driver};\
    Server=tcp:{server},1433;\
    Database={database};\
    Uid={username};\
    Pwd={password};\
    Encrypt=yes;\
    TrustServerCertificate=no;\
    Connection Timeout=30;'

# Create the engine to connect to the database
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(connection_string))
engine.connect()

# Create the Session
Session = sessionmaker(bind=engine)

# Define the Order data model
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    date_uuid = Column('date_uuid', String, primary_key=True)
    user_id = Column('User ID', String, primary_key=True)
    card_number = Column('Card Number', String)
    store_code = Column('Store Code', String)
    product_code = Column('product_code', String)
    product_quantity = Column('Product Quantity', Integer)
    order_date = Column('Order Date', DateTime)
    shipping_date = Column('Shipping Date', DateTime)

# define routes
# route to display orders
@app.route('/')
def display_orders():

    page = int(request.args.get('page', 1))
    rows_per_page = 25

    # Calculate the start and end indices for the current page
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page

    # Create a session to interact with the database
    session = Session()

    # Fetch a subset of data for the current page
    current_page_orders = session.query(Order).order_by(Order.user_id, Order.date_uuid).slice(start_index, end_index).all()

    # Calculate the total number of pages
    total_rows = session.query(Order).count()
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page

    # Close the session
    session.close()

    return render_template('orders.html', orders=current_page_orders, page=page, total_pages=total_pages)


# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
