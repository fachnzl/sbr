import streamlit as st
import pandas as pd
import datetime
import openpyxl

st.markdown("### Update Data")

st.markdown("Data Repo")


# st.markdown(now.strftime("%Y-%m-%d %H:%M:%S"))
repo_upload = st.file_uploader(
    "Please upload an data repo (xlsx)", type=["xlsx"])

st.markdown("Data Wilkerstat")

wilkerstat_upload = st.file_uploader("Please upload an data wilkerstat (csv)", type=["csv"],
                                     accept_multiple_files=False)
if wilkerstat_upload is not None:
    wilkerstat = pd.read_csv(wilkerstat_upload, sep=";")
    now = datetime.datetime.now()
    last_update = pd.DataFrame([[now.strftime("%Y-%m-%d %H:%M:%S")]])
    last_update.to_csv('data/last_update.csv')
    st.table(wilkerstat.head())
    wilkerstat.to_csv("data/wilkerstat.csv", index=False)
else:
    try:
        wilkerstat = pd.read_csv("data/wilkerstat.csv")
    except:
        st.markdown("")

if repo_upload is not None:
    repo = pd.read_excel(repo_upload)
    now = datetime.datetime.now()
    last_update = pd.DataFrame([[now.strftime("%Y-%m-%d %H:%M:%S")]])
    last_update.to_csv('data/last_update.csv')
    st.table(repo.head())
    repo.to_csv("data/repo.csv", index=False)
else:
    try:
        repo = pd.read_csv("data/repo.csv")
    except:
        st.markdown("")
