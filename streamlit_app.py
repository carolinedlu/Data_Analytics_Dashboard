import pandas as pd
import streamlit as st
import altair as alt
#import plotly.express as px#
#import plotly.graph_objects as go#

st.set_page_config(page_title=" Provider Engagement Data Review ",
                   page_icon="📊", layout="wide")


@st.cache(allow_output_mutation=True)
# -- Function to read from excel file  --#
def get_data_from_excel(file_name_path, sheet_name):
    dataframe1 = pd.read_excel(
        io=file_name_path,
        engine="openpyxl",
        sheet_name=sheet_name,
        #skiprows=3,
        usecols="A:BR",
        nrows=45000,
    )

    return dataframe1


df = get_data_from_excel("Easter Seals_09012022_104104.xlsx", "Sheet1")

# -- pandas really doesn't like spaces, removed spaces and added underscore --#
df.columns = df.columns.str.replace(' ', '_')

data_load_state = st.text('Loading data...')
data_load_state.text("Done! (using st.cache)")

# ----Sidebar------ #

st.sidebar.header("Filter Here:")

claim_state = st.sidebar.multiselect(
    " Claim State: ",
    options=df["CLAIM_STATE"].unique(),
    default=df["CLAIM_STATE"].unique()
)

claim_status = st.sidebar.multiselect(
    "Claim Status: ",
    options=df["CLAIM_STATUS"].unique(),
    default=df["CLAIM_STATUS"].unique(),
)

line_of_business = st.sidebar.multiselect(
    "Line of Business: ",
    options=df["LOB_NAME"].unique(),
    default=df["LOB_NAME"].unique(),
)

dataframe_selection = df.query(
    "CLAIM_STATE == @claim_state & CLAIM_STATUS == @claim_status & LOB_NAME == @line_of_business "
)

total_claims_sum = float(dataframe_selection["TOTAL_BILLED"].sum())

total_claim_denial = int(df.CLAIM_STATUS.value_counts().DENIED)

total_claim_paid = int(df.CLAIM_STATUS.value_counts().CLEAN)

total_claim_count = int(dataframe_selection["CLAIM_ID"].count())

percentage_claims_denied = (total_claim_denial / total_claim_count)

percentage_claims_paid = (total_claim_paid / int(dataframe_selection["LOB_NAME"].count()))

# st.dataframe(dataframe_selection)

#monthly_count = df.resample(rule="M", on="DATE_RECEIVED")["DATE_RECEIVED"]
#st.bar_chart(df, x=monthly_count, y=["CLAIM_ID"].count())


bar_chart = alt.Chart(df).mark_bar().encode(
        x="month(DATE_RECEIVED):O",
        y="count(CLAIM_ID):Q",
        color="LOB_NAME:N"
    )

st.altair_chart(bar_chart, use_container_width=True)

# 11.1.2022 added data elements into columns for readability #
column_1, column_2, column_3, column_4 = st.columns(4)
with column_1:
    st.header("Total Billed Amount of Submitted Claims: ")
    st.subheader(f" ${total_claims_sum:,.2f}")
with column_2:
    st.header("Total Denied Claims: ")
    st.subheader(f"{total_claim_denial}")
with column_3:
    st.header("Total Paid Claims: ")
    st.subheader(f"{total_claim_paid}")
with column_4:
    st.header("Bill to pay ratio: ")
    st.subheader(f"{percentage_claims_paid:.1%} of claims submitted are paid. ")
