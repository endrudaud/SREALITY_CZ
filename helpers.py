from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import psycopg2
import time


def list_schemas_and_tables():
    conn = psycopg2.connect(
        dbname="docker",
        user="docker",
        password="docker",
        host="db-1"
    )
    cur = conn.cursor()

    # List all schemas
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    print("Schemas:")
    for schema in cur.fetchall():
        print(schema)

    # List all tables in the 'public' schema
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    print("\nTables in 'public' schema:")
    for table in cur.fetchall():
        print(table)

    cur.close()
    conn.close()
    
def crawl_data():
    options = Options()
    options.add_argument('-headless')  # Run Firefox in headless mode

    # Create a new Firefox profile
    profile = FirefoxProfile()

    # Add the profile to the options
    options.profile = profile

    # Configure Selenium to use the new profile
    driver = webdriver.Firefox(options=options)
    urls = ['https://www.sreality.cz/en/search/for-sale/apartments']  # Add the first URL directly
    urls += [f'https://www.sreality.cz/en/search/for-sale/apartments?strana={i}' for i in range(2, 5)]  # Add the rest of the URLs

    data = []
    count_urls = 0
    for url in urls:
        print(f"Processing URL: {url}")
        driver.get(url)
        count_urls += 1
        try:
            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.property.ng-scope span.name.ng-binding'))
            )
        except Exception as e:
            print(f"Error waiting for page to load: {url}")
            continue

        # Find the span elements
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'a:first-child img')
        span_elements = driver.find_elements(By.CSS_SELECTOR, 'div.property.ng-scope span.name.ng-binding')
        #print(span_elements)
        count = 0   
        for img_element,span_element in zip(img_elements,span_elements):
            time.sleep(2)
            count += 1
            try:    
                #print(element.get_attribute('src'))
                title = span_element.text
                url = img_element.get_attribute('src')
                #print(element.text)
                #title = element.text
                data.append({'url': title})
                # Create table if not exists
                create_table()
                # Insert the data into the PostgreSQL database
                insert_sql(title, url)
                #print(f"title: {title} url: {url}   count: {count}")
                print(f"processing url: {count_urls} element: {count}")
            except Exception as e:
                print(f"Error processing element: {count} on page: {url}")
                data.append({'url': "NULL"})

        time.sleep(20)
    # Close the driver
    driver.quit()
    # print total count from sql
    count_rows()

def insert_sql(title, url):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="docker",
        user="docker",
        password="docker",
        host="db-1"  # or the host where your db is running
    )

    # Create a new cursor
    cur = conn.cursor()

    # Insert the title and url into the sreality table
    cur.execute(
        "INSERT INTO sreality (title, url) VALUES (%s, %s)",
        (title, url)
    )

    # Commit the transaction
    conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()

def count_rows():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="docker",
        user="docker",
        password="docker",
        host="db-1"  # or the host where your db is running
    )

    # Create a new cursor
    cur = conn.cursor()

    # Get the number of rows in the sreality table
    cur.execute("SELECT COUNT(title) FROM sreality")
    row_count = cur.fetchone()[0]

    # Close the cursor and the connection
    cur.close()
    conn.close()

    print(f"The number of rows in the table is: {row_count}")

def create_table():
    conn = psycopg2.connect(
        dbname="docker",
        user="docker",
        password="docker",
        host="db-1"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sreality (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_sreality_data():
    conn = psycopg2.connect(
        dbname="docker",
        user="docker",
        password="docker",
        host="db-1"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM sreality;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data