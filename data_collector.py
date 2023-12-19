from encrypt_decrypt_tools import write_encrypted_data, read_encrypted_data
import json

class ReportDataCollector:
    """
    Report Data Collector for Email (RDCE).
    This code assumes that the write_encrypted_data  function takes the data to be encrypted (as a string), the file path, and the key path as arguments, and handles the encryption and file writing
    """
    def __init__(self):
        self.data = {}

    def collect(self, key, value):
        if isinstance(value, str):
            # Remove leading and trailing whitespace when the value is a string
            cleaned_value = value.strip()
            # Remove extra spaces between words
            cleaned_value = ' '.join(cleaned_value.split())
            self.data[key] = cleaned_value
        else:
            self.data[key] = value

    def get_data(self):
        return self.data

    def write_to_file(self, file_path, key_path):
        # Convert the data to a JSON string
        data_json = json.dumps(self.data)
        
        # Encrypt and write the data using the provided function
        write_encrypted_data(data_json, file_path, key_path)
if __name__ == '__main__':
    # Usage
    collector = ReportDataCollector()
    collector.collect('client_name', 'AKZO')
    collector.collect('document_id', 'GG-009')
# ... collect other data ...

    # File paths
    file_path = "d:\\Data_Vault\\encrypted_CF_data_email.txt"
    key_path = "d:\\Data_Vault\\key_CF_data_email.key"

    # Write the collected data to an encrypted file
    collector.write_to_file(file_path, key_path)

    # Later in the code, you can read and decrypt the data using the corresponding functions from encrypt_decrypt_tools
    print(read_encrypted_data(file_path, key_path))

    print('Reminder: Run Expro_body (in folder Thunderbird), for sending this report by email')