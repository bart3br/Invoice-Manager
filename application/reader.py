import PyPDF2
import re
from datetime import datetime
from random import randint
import os

#reading pdf file and returning its content as a string
def read_file(filename: str) -> str:
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for i in range(num_pages):
            page = reader.pages[i]
            text += page.extract_text()
    return text


#extracting the title of the invoice
def extract_title(text: str) -> str:
    title_pattern = r'Faktura nr (\d+)'
    title_match = re.search(title_pattern, text)
    invoice_title = title_match.group(0) if title_match else None
    return invoice_title


#extracting the information about the seller
def extract_seller(text:str) -> str:
    seller_pattern = r"Sprzedawca\n([^D]+)"
    seller_match = re.search(seller_pattern, text)
    seller_info = seller_match.group(1).strip() if seller_match else None
    seller_info = seller_info.replace('\n', ', ')
    return seller_info

#extracting the date of the invoice
def extract_date(text: str) -> datetime:
    
    date_pattern = r"Data wystawienia: (\d{4}-\d{2}-\d{2})"
    date_match = re.search(date_pattern, text)
    date_issued = date_match.group(1) if date_match else None
    date_object = datetime.strptime(date_issued, '%Y-%m-%d')
    #adding random hour and minute to the date
    hour = randint(0, 23)
    minute = randint(0, 59)
    date_object = date_object.replace(hour=hour, minute=minute)
    return date_object

#extracting the information about the buyer
def extract_buyer(text: str) -> str:
    buyer_pattern = r"NABYWCA\n([^N]+)"
    buyer_match = re.search(buyer_pattern, text)
    buyer_info = buyer_match.group(1).strip() if buyer_match else None
    buyer_info = buyer_info.replace('\n', ', ')
    return buyer_info

def extract_entries(text: str) -> list[dict]:
    entry_pattern = r"([A-Za-z\s]+?) (\d+) ([\d.,]+) ([\d.,]+)"
    entries = re.findall(entry_pattern, text)

    invoice_entries = []
    for entry in entries:
        name, quantity, price, total_price, tax = process_entry(entry)
        
        entry_data = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'total_price': total_price,
            'tax': tax
        }
        invoice_entries.append(entry_data)

    for entry in invoice_entries:
        if entry['name'].startswith('TOWARU ILOŚĆ WARTOŚĆ NETTO VAT\n'):
            entry['name'] = entry['name'][len('TOWARU ILOŚĆ WARTOŚĆ NETTO VAT\n'):]
        elif entry['name'].startswith('NETTO VAT\n'):
            entry['name'] = entry['name'][len('NETTO VAT\n'):]
            
    return invoice_entries

def process_entry(entry: list[str]) -> tuple:
    name, quantity, price, total_price = entry
    
    name = name.strip()
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1
    try:
        price = round(float(price.replace(',', '.')), 2)
    except ValueError:
        price = 0.0
    try:
        total_price = round(float(total_price.replace(',', '.')),2)
    except ValueError:
        total_price = round(quantity * price, 2)
        
    tax = round(float(0.23 * total_price),2)
    return (name, quantity, price, total_price, tax)

#counting the total amount of the invoice
def extract_total_amount(entries: list[dict]) -> float:
    amount = 0.0
    for entry in entries:
        amount += entry['total_price']
    return round(amount, 2)


def get_invoice_data(filename: str) -> dict:
    text = read_file(filename)
    invoice_title = extract_title(text)
    seller_info = extract_seller(text)
    date_object = extract_date(text)
    buyer_info = extract_buyer(text)
    invoice_entries = extract_entries(text)
    total_amount = extract_total_amount(invoice_entries)
    
    invoice_data = {
        'name': invoice_title,
        'seller': seller_info,
        'date': date_object,
        'buyer': buyer_info,
        'entries': invoice_entries,
        'total_amount': total_amount
    }
    return invoice_data

def convert_entries_to_string(entries: list[dict]) -> str:
    entries_str = ''
    for entry in entries:
        entries_str += f"{entry['name']}\t{entry['quantity']}\t{entry['price']}\t{entry['total_price']}\t{entry['tax']}\n"
    return entries_str

#testing the functions
def reading_test():
    for root, dirs, files in os.walk('application\static\pdf_files'):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                print(file_path)
                text = read_file(file_path)
                
                print('Invoice Title:', extract_title(text))
                print('Seller:', extract_seller(text))
                print('Date:', extract_date(text))
                print('Buyer:', extract_buyer(text))
                print('Entries:', extract_entries(text))
                print('Total Amount:', extract_total_amount(extract_entries(text)))
                
if __name__ == '__main__':
    #reading_test()
    pass