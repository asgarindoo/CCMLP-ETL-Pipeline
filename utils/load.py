import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine

SERVICE_ACCOUNT_FILE = 'google-sheets-api.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def save_to_csv(dataframe, filename='products.csv'):
    try:
        dataframe.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Error in saving to CSV: {e}")


def save_to_google_sheets(data):
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key('1nR6fobk15VNJwdSFa6hjZYqDh71eq3XBQheeUCb6JCA').sheet1
        
        if not data.empty:
            header = ['Title', 'Price', 'Rating', 'Gender', 'Colors', 'Size', 'Timestamp']
            rows = [list(item.values()) for item in data.to_dict(orient='records')]
            sheet.clear()
            sheet.append_rows([header] + rows)
            print("Data berhasil disimpan ke Google Sheets")
        else:
            print("Tidak ada data untuk disimpan")
    except Exception as e:
        print(f"Error in saving to Google Sheets: {e}")

def store_to_database(data, db_url):
  try:
    engine = create_engine(db_url)
    with engine.connect() as con:
      data.to_sql('product_databases', con=con, if_exists='append', index=False)
      print("Data berhasil disimpan ke database")
  except Exception as e:
    print(f"Error: {e}")
