from collections import defaultdict
import logging
import os
import csv

# Set filepaths and directories
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data_cleanup.tsv")
log_dir = os.path.join(base_dir, "log")
log_file_path = os.path.join(log_dir, "data_cleanup.log")

# Create folders if they don't exist
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s: %(lineno)d  - Message: %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def load_data_from_tsv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Soubor '{file_path}' neexistuje. Ujistěte se, že je v kořenovém adresáři úkol1.")
    
    data = []
    with open(file_path, mode='r', newline='', encoding='windows-1250') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            data.append(row)    
    
    return data

# Main function which finds indexes to remove
def find_rows_indexes(data):
    rows_by_objectid_emptyName = defaultdict(list)

    for index, row in enumerate(data):
        if row['Name'] == '':            
            rows_by_objectid_emptyName[row['ObjectID']].append((index, row))

    rows_to_remove = []

    for objectid, rows in rows_by_objectid_emptyName.items():

        # Check for the first condition
        has_non_empty_name = any(row['Name'] != '' for row in data if row['ObjectID'] == objectid)
        if has_non_empty_name:            
            for index, row in rows:                
                rows_to_remove.append(index)
        
        # Process the second condition
        else:            
            rows_to_remove.extend(find_rows_to_remove(rows))

    return rows_to_remove

# Sub-function - If all NAME fields for ObjectID are empty, find rows to remove after the first row
def find_rows_to_remove(rows):
    first_empty_name_found = False
    rows_to_remove = []

    for index, row in rows:
        if row['Name'] == '':
            if not first_empty_name_found:
                first_empty_name_found = True
            else:
                rows_to_remove.append(index)

    return rows_to_remove

if __name__ == "__main__":    
    try:
        print("Získávání indexů řádků k odstranění...")
        data = load_data_from_tsv(file_path)
        rows_to_remove = find_rows_indexes(data)
        print("Indexy řádků k odstranění: ", rows_to_remove)        
    except FileNotFoundError as e:
        print(e)