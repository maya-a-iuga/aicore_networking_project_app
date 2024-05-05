from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialise Flask App
app = Flask(__name__)

# database connection parameters
username = 'your_postgres_user'
password = 'your_postgres_password'
host = 'your-rds-instance-endpoint.rds.amazonaws.com'
port = 5432  # Default port for PostgreSQL
database = 'your_database_name'

# Create the connection string for PostgreSQL
connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

# Create the engine to connect to the database
engine = create_engine(connection_string)
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
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    session = Session()
    current_page_orders = session.query(Order).order_by(Order.user_id, Order.date_uuid).slice(start_index, end_index).all()
    total_rows = session.query(Order).count()
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page
    session.close()
    return render_template('orders.html', orders=current_page_orders, page=page, total_pages=total_pages)

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
