import streamlit as st
import pandas as pd
import mysql.connector



#---------------------Hide default multipage sidebar---------------------------------------------------------------------------

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)



# ---------------- DATABASE CONNECTION -----------------------------------------------------------------------------------------

db = mysql.connector.connect(

    host="127.0.0.1",
    user="root",
    password="Parasite7",
    database="cqms",
    port=3306

)
cursor = db.cursor()

# ---------------- STREAMLIT WEB PAGE ----------------------------------------------------------------------------------------------------------

# -----------------creating a button with functionality of showing the data base in web page -----------------------------------------------------------------
st.header("🖥️Support Side")

if st.button("View Queries :"):
    query = "select * from data_sheet"
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns = (col[0] for col in cursor.description ))
    st.dataframe(df)
    if cursor.rowcount == 0:
        st.success("THERE IS NO QUERIES AS OF NOW")

# -----------CREATING A BUTTON WITH FUNCTIONALITY OF CLOSING THE QUERIES IN THE DATA BASE WHICH IS OPEN IN STATUS----------------------------------------------------------

query_id = st.text_input("Enter the User_id of the query to close")

if st.button("Close the Queries"):
    query = """UPDATE data_sheet SET query_status = 'CLOSED' , query_closed_time = (select current_date) WHERE query_id = %s AND  query_status = 'OPEN' """
    values = (query_id,)
    cursor.execute(query,values)
    db.commit() ## SAVING THE FILE PERMANENTLY
    
    if cursor.rowcount == 0:
        st.warning("❌ Invalid ID or Query is not OPEN")
    else:
        st.success("✅ Query closed successfully!")
if st.button("HOME PAGE:"):
    st.switch_page("login_flow.py")
