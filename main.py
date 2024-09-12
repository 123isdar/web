import ftplib
import io
import time

keep_alive()

# Replace these with your FTP server details
ftp_host = 'ftpupload.net'
ftp_username = 'ezyro_37108065'
ftp_password = '8c68592c9e997'

# Function to perform the FTP operation
def upload_file():
    # Connect to the FTP server
    ftp = ftplib.FTP(ftp_host)
    ftp.login(user=ftp_username, passwd=ftp_password)

    # File details
    file_name = 'htdocs/host.txt'
    new_content = "666"

    # Buffer to store existing content
    existing_content = ""

    # Attempt to download the existing file content
    try:
        # Use an in-memory bytes buffer to read the existing file content
        file_buffer = io.BytesIO()
        ftp.retrbinary(f'RETR {file_name}', file_buffer.write)
        existing_content = file_buffer.getvalue().decode('utf-8')
        print("Existing content retrieved successfully:")
        print(existing_content)
    except ftplib.error_perm as e:
        # If the file does not exist, print an error and continue
        if str(e).startswith('550'):
            print(f"File '{file_name}' does not exist on the server. A new file will be created.")
            existing_content = "0"  # Initialize to zero if the file doesn't exist
        else:
            raise

    # Combine the existing content with the new content, converting to integers first
    combined_content = int(existing_content) + int(new_content)

    # Convert the combined content back to a string before encoding to bytes
    combined_content_str = str(combined_content)

    # Use an in-memory bytes buffer to avoid local file system dependencies
    upload_buffer = io.BytesIO(combined_content_str.encode('utf-8'))

    # Upload the file back to the FTP server
    ftp.storbinary(f'STOR {file_name}', upload_buffer)

    # Close the FTP connection
    ftp.quit()

    print(f"File '{file_name}' uploaded successfully with the modified content.")

# Repeat the process every 30 seconds
while True:
    upload_file()
    time.sleep(30)  # Wait for 30 seconds before repeating
