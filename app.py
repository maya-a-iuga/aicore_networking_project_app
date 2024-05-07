from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

# Initialise Flask App
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ensuring all logs go to stderr
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

app.logger.error("test error")
# database connection parameters
username = 'postgres'
password = 'Pon3$5pone!'
host = 'np-demo-rds-database.clg9fn0gdgbo.eu-west-1.rds.amazonaws.com'
port = 5432  # Default port for PostgreSQL
database = 'inventory_app'

try:
    # Create the connection string for PostgreSQL
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

    # Create the engine to connect to the database
    engine = create_engine(connection_string)
    engine.connect()

    # Create the Session
    Session = sessionmaker(bind=engine)

    # Define the Order data model
    Base = declarative_base()
except Exception as e:
    app.logger.error(f' DB creation Error: {str(e)}')

class Order(Base):
    __tablename__ = 'orders'
    date_uuid = Column('date_uuid', String, primary_key=True)
    user_id = Column('user_id', String, primary_key=True)
    card_number = Column('card_number', String)
    store_code = Column('store_code', String)
    product_code = Column('product_code', String)
    product_quantity = Column('product_quantity', Integer)
    order_date = Column('order_date', DateTime)
    shipping_date = Column('shipping_date', DateTime)

# define routes
# route to display orders
@app.route('/')
def display_orders():
    try:
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
    except Exception as e:
        return f'diplay_orders Error: {str(e)}'

# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
