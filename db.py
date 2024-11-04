import requests
from config import DATABASE_BASE_URL, API_KEY  # Import the database URL and API key

def test_database_connection():
    # Connection string for SQLite Cloud
    connection_string = f"{DATABASE_BASE_URL}?apikey={API_KEY}"
    
    # Base URL for the SQLite Cloud API
    base_url = "https://ccg8bpswnk.sqlite.cloud:8090/v2/weblite/sql"

    # SQL query to test the connection
    sql_query_version = "SELECT sqlite_version();"

    # SQL query to drop the markers table if it exists
    drop_table_query = "DROP TABLE IF EXISTS markers;"

    # SQL query to create the markers table with an additional column for images
    create_table_query = '''
    CREATE TABLE markers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        images TEXT  -- New column to store comma-separated image URLs
    );
    '''

    # SQL query to insert sample records including images
    insert_sample_records_query = '''
    INSERT INTO markers (location, latitude, longitude, images) VALUES
    ('Location A', 37.7749, -122.4194, 'https://i.ibb.co/R7dTbMk/algae1.jpg, https://i.ibb.co/someotherimage.jpg'),
    ('Location B', 34.0522, -118.2437, 'https://i.ibb.co/R7dTbMk/algae2.jpg'),
    ('Location C', 40.7128, -74.0060, 'https://i.ibb.co/R7dTbMk/algae3.jpg');
    '''

    # SQL query to select all records from markers table
    select_records_query = "SELECT * FROM markers;"

    # SQL query to delete all records from markers table
    flush_records_query = "DELETE FROM markers;"

    # Headers including the Authorization Bearer token
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {connection_string}"
    }

    try:
        # Make the POST request to execute the SQL query for SQLite version
        response = requests.post(base_url, headers=headers, json={"sql": sql_query_version})

        # Check if the request was successful for version query
        if response.status_code == 200:
            print("SQLite Version:", response.json())
        else:
            print("Failed to execute version query:", response.status_code, response.text)

        # Drop the markers table
        response = requests.post(base_url, headers=headers, json={"sql": drop_table_query})
        if response.status_code == 200:
            print("Markers table dropped (if it existed).")
        else:
            print("Failed to execute drop table query:", response.status_code, response.text)

        # Create the markers table
        response = requests.post(base_url, headers=headers, json={"sql": create_table_query})
        if response.status_code == 200:
            print("Markers table created.")
        else:
            print("Failed to execute create table query:", response.status_code, response.text)

        # Insert sample records
        response = requests.post(base_url, headers=headers, json={"sql": insert_sample_records_query})
        if response.status_code == 200:
            print("Sample records inserted into markers table.")
        else:
            print("Failed to execute insert sample records query:", response.status_code, response.text)

        # Flush all records from the markers table
        flush_records()

        # Select all records from the markers table
        response = requests.post(base_url, headers=headers, json={"sql": select_records_query})
        if response.status_code == 200:
            records = response.json()
            if 'data' in records:
                print("Records in markers table:")
                for record in records['data']:
                    print(record)
            else:
                print("No data found in response:", records)
        else:
            print("Failed to execute select records query:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)

def flush_records():
    # Base URL for the SQLite Cloud API
    base_url = "https://ccg8bpswnk.sqlite.cloud:8090/v2/weblite/sql"
    
    # SQL query to delete all records from markers table
    flush_records_query = "DELETE FROM markers;"

    # Headers including the Authorization Bearer token
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {DATABASE_BASE_URL}?apikey={API_KEY}"
    }

    # Send request to delete all records
    response = requests.post(base_url, headers=headers, json={"sql": flush_records_query})
    if response.status_code == 200:
        print("All records flushed from markers table.")
    else:
        print("Failed to execute flush records query:", response.status_code, response.text)

if __name__ == "__main__":
    test_database_connection()
