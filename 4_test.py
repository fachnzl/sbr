import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
# from gsheetsdb import connect
# import collection import Iterable
# import gsheetsdb

sheets_url = st.secrets["public_gsheets_url"]
csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
st.markdown(sheets_url)
data1 = pd.read_csv(csv_url)

st.table(data1.head())

data1.head().to_csv(sheets_url)

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
# conn = connect(credentials=credentials)
client=gspread.authorize(credentials)

sheet_id = '/1G_lfh5RQUqUeIbdDdJnzgloelzxaGlpGD6V1Gf0cTVw'
# csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
csv_url = "https://docs.google.com/spreadsheets/d/1G_lfh5RQUqUeIbdDdJnzgloelzxaGlpGD6V1Gf0cTVw/edit#gid=1182878670"
database_df = pd.read_csv(csv_url, on_bad_lines='skip')

st.table(database_df)