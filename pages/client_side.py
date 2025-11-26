import streamlit as st
import mysql.connector



# Hide default multipage sidebar

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)




# ---------------- DATABASE CONNECTION ----------------

db = mysql.connector.connect(
     host="127.0.0.1",
    user="root",
    password="Parasite7",
    database="cqms",
    port=3306
)
cursor = db.cursor()

# ---------------- STREAMLIT UI ----------------

st.header("🧑‍💼Client Side")
mail_id = st.text_input("Enter Email ID :")
mobile_number = st.text_input("Enter Mobile Number: ")
query_heading = st.text_input("Query Heading: ")
query_description = st.text_area("Query Description")
query_status = "OPEN"

if st.button("SUBMIT") :

    ## the submit button tells about blank spaces 
    
    if mail_id == "" or mobile_number == "" or query_heading =="" or query_description == "" :
        st.warning("Please fill all the mentioned places")
    else:
        query = "INSERT INTO data_sheet (mail_id , mobile_number ,query_heading ,query_description,query_status,query_created_time) values (%s,%s,%s,%s,%s,(select current_date))"
        values = (mail_id , mobile_number ,query_heading ,query_description,query_status)
        cursor.execute(query,values)
        db.commit()
        st.success("Succesfully Entered the Query")
if st.button("HOME PAGE:"):
    st.switch_page("login_flow.py")


