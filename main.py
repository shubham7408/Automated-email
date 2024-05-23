from datetime import date
import pandas as pd
from send_email import send_email  # Assuming the function is named send_email

SHEET_ID = "1rR444KqAHJmAZL8xPDPKnGeVISUmJwdz27QmYuE5IbY"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    date_format = "%d/%m/%Y"
    df = pd.read_csv(url, parse_dates=parse_dates, dayfirst=True, date_format=date_format)
    return df

def query_data_and_send_email(df):
    present = pd.Timestamp(date.today())
    email_counter = 0
    for _, row in df.iterrows():
        if (present >= row["reminder_date"]) and (row["has_paid"].lower() == "no"):
            send_email(
                subject=f'[Coding Is Fun] Invoice: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1
    return f"Total emails sent: {email_counter}"

# Load data and send emails
df = load_df(URL)
result = query_data_and_send_email(df)
print(result)
