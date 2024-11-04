import requests
from config import DATABASE_BASE_URL, API_KEY  # Import the database URL and API key

# Base URL for the SQLite Cloud API
BASE_URL = "https://ccg8bpswnk.sqlite.cloud:8090/v2/weblite/sql"

def connect_db():
    """Return the authorization headers for connecting to the SQLite Cloud API."""
    connection_string = f"{DATABASE_BASE_URL}?apikey={API_KEY}"
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {connection_string}"
    }

def test_database_connection():
    """Test the connection to the database and manage the markers table."""
    check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='markers';"
    create_table_query = '''
    CREATE TABLE markers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        images TEXT  -- New field for storing image URLs
    );
    '''
    insert_sample_records_query = '''
    INSERT INTO markers (location, latitude, longitude, images) VALUES
    ('Poland', 51.1055, 17.0355, 'https://i.ibb.co/R7dTbMk/algae1.jpg'),
    ('Chennai', 13.0827, 80.2707, 'https://example.com/chennai.jpg'),
    ('London', 51.5074, -0.1278, 'https://example.com/london.jpg');
    '''

    headers = connect_db()

    try:
        # Check if the markers table exists
        response = requests.post(BASE_URL, headers=headers, json={"sql": check_table_query})
        if response.status_code == 200:
            table_check_result = response.json()
            if 'data' in table_check_result and table_check_result['data']:
                print("Markers table already exists.")
            else:
                response = requests.post(BASE_URL, headers=headers, json={"sql": create_table_query})
                if response.status_code == 200:
                    print("Markers table created.")
                else:
                    print("Failed to execute create table query:", response.status_code, response.text)

        # Insert sample records only if the table exists or has just been created
        response = requests.post(BASE_URL, headers=headers, json={"sql": insert_sample_records_query})
        if response.status_code == 200:
            print("Sample records inserted into markers table.")
        else:
            print("Failed to execute insert sample records query:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)

def insert_marker(location, latitude, longitude, images=None):
    """Insert a new marker into the markers table."""
    headers = connect_db()

    # Use default image if images is blank
    if not images:
        images = 'https://i.ibb.co/D465LSQ/algae3.png'  # Default image URL

    # SQL query to insert a new marker with an image
    insert_query = f"INSERT INTO markers (location, latitude, longitude, images) VALUES ('{location}', {latitude}, {longitude}, '{images}');"
    
    try:
        response = requests.post(BASE_URL, headers=headers, json={"sql": insert_query})

        if response.status_code == 200:
            print(f"Marker added: {location}, {latitude}, {longitude}, {images}")
        else:
            print("Failed to insert marker:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred while inserting the marker:", e)

def update_marker_images(marker_id, direct_urls):
    """Update the images for the specified marker by appending unique new image URLs."""
    headers = connect_db()

    # Retrieve existing images for the marker
    select_query = f"SELECT images FROM markers WHERE id = {marker_id};"
    try:
        response = requests.post(BASE_URL, headers=headers, json={"sql": select_query})
        if response.status_code == 200:
            result = response.json()
            existing_images = result['data'][0][0] if 'data' in result and result['data'] else ""
            
            # Split existing images into a list, if any
            current_images = set(existing_images.split(',')) if existing_images else set()
            
            # Add only unique new URLs
            new_images = set(direct_urls)
            updated_images = current_images.union(new_images)  # Union to keep only unique URLs
            
            # Join the updated set of images back into a comma-separated string
            updated_images_str = ','.join(updated_images)
            
            # SQL query to update the images column for the specified marker
            update_query = f"""
            UPDATE markers 
            SET images = '{updated_images_str}'
            WHERE id = {marker_id};
            """

            # Execute the update query
            update_response = requests.post(BASE_URL, headers=headers, json={"sql": update_query})
            if update_response.status_code == 200:
                print(f"Images updated for marker ID {marker_id}.")
            else:
                print("Failed to update images:", update_response.status_code, update_response.text)
        else:
            print("Failed to retrieve existing images:", response.status_code, response.text)
            
    except Exception as e:
        print("An error occurred while updating images:", e)

def get_all_markers():
    """Retrieve all markers from the database."""
    headers = connect_db()
    select_records_query = "SELECT id, location, latitude, longitude, images FROM markers;"

    try:
        response = requests.post(BASE_URL, headers=headers, json={"sql": select_records_query})
        if response.status_code == 200:
            records = response.json()
            if 'data' in records:
                return records['data']  # Return the list of markers
            else:
                print("No data found in response:", records)
                return []  # Return an empty list if no data
        else:
            print("Failed to execute select records query:", response.status_code, response.text)
            return []  # Return an empty list on failure

    except Exception as e:
        print("An error occurred while retrieving markers:", e)
        return []  # Return an empty list on exception

if __name__ == "__main__":
    test_database_connection()
