import psycopg2
import b2sdk.v2
import io

# PostgreSQL Configuration
DB_HOST = 'localhost'
DB_NAME = 'pii_database'
DB_USER = 'soham'
DB_PASS = 'idfy_fraud'

# Backblaze B2 Configuration
B2_ACCOUNT_ID = '1af48fed9f34'
B2_APPLICATION_KEY = '003c91cec02d3184e64d26f87ce30797042bd05c6c'
B2_BUCKET_NAME = 'idfy-fraud-buster'


# PostgreSQL Connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Fetch data from PostgreSQL database
def fetch_database_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM pii_data;')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching database data: {e}")
        return None

# Backblaze B2 Connection
def setup_b2_connection():
    info = b2sdk.v2.InMemoryAccountInfo()
    b2_api = b2sdk.v2.B2Api(info)
    b2_api.authorize_account("production", B2_ACCOUNT_ID, B2_APPLICATION_KEY)
    bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)
    return bucket

# Fetch data from Backblaze B2 cloud
def fetch_cloud_data():
    try:
        bucket = setup_b2_connection()
        
        # List files in the bucket
        files = bucket.ls()

        # List to store data from all files
        all_data = []

        for file_version, file_info in files:
            file_name = None  # Initialize file_name to avoid referencing before assignment
            try:
                # Fetch file info
                # file_id = file_version.file_id
                file_id = file_version.id_
                file_name = file_version.file_name
                print(f"Attempting to download file: {file_name} (ID: {file_id})")
                
                # # Download the file content
                # file_content = bucket.download_file_by_id(file_id).read().decode('utf-8')

                # Download the file content into memory
                downloaded_file = bucket.download_file_by_id(file_id)
                content = io.BytesIO()
                downloaded_file.save(content)  # Save the downloaded file to the in-memory buffer
                content.seek(0)  
                
                # Log successful download
                print(f"Successfully downloaded file: {file_name}")
                
            except Exception as download_error:
                # Ensure file_name is not referenced before assignment, log more details for debugging
                error_message = f"Error downloading file {file_name if file_name else 'unknown'} (ID: {file_id if 'file_id' in locals() else 'unknown'}): {str(download_error)}"
                print(error_message)
                return None

            # Decode the file content and split into lines
            file_content_str = content.read().decode('utf-8')
            lines = file_content_str.strip().split('\n')
            lines = [line.strip().strip('"') for line in lines]
            
            # Append the lines to all_data list
            all_data.extend(lines)
        
        return all_data
    
    except Exception as e:
        print(f"Error fetching cloud data: {str(e)}")
        return None

# Main function to handle data fetching based on input
def fetch_data(source):
    if source == 'database':
        dat = fetch_database_data()
        formatted_dat = [f'"{entry[1]}",' for entry in dat]
        return formatted_dat
    elif source == 'cloud':
        dat = fetch_cloud_data()
        return dat
    else:
        print('Invalid source')
        return None

# Example usage
if __name__ == '__main__':
    source_input = input("Enter data source (database/cloud): ").strip().lower()
    data = fetch_data(source_input)

    if data:
        print("Fetched Data:")
        for entry in data:
            print(entry)
    else:
        print("Failed to fetch data.")
