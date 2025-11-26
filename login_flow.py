import streamlit as st
import mysql.connector
import hashlib
import time

#-------------------Hide default multipage sidebar-------------------------------------

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)




# ---------------- DATABASE CONNECTION ----------------------------------------------------------------------------------------------
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Parasite7",
    database="cqms",
    port=3306
)
cursor = db.cursor()

# --------------- TABS CREATION ---------------------------------------------------------------------------------------------

st.title("Client Query Management System ")
st.header(" 🏠 HOME PAGE ")
tab1 , tab2 = st.tabs(["🆕 USER REGISTRATION", " 🔐 USER LOGIN"])

#-----------------USER REGISTRATION------------------------------------------------------------------------------------------
with tab1:
    st.header("🆕 User Registration")
    
    user_id_r = st.text_input("Enter User ID:",key= "userid_tab1")
    password_r = st.text_input("Enter Password:", type="password",key= "pass_tab1")
    role_r = st.selectbox("Enter Your Role:" , ["CLIENT","SUPPORT"] , key= "role_tab1")

    ## unique keys has to give otherwise stremlit showing an error of duplicate 

    if st.button("SUBMIT"):
    ## just a check for not keeping any empty spaces
        if user_id_r == "" or password_r == "" or role_r == "":
            st.warning("Please Fill all mentioned places")
        else:
            ## for unique user_id entry only !!!
            query1 ="SELECT * FROM login_flow WHERE user_name = %s "
            cursor.execute(query1, (user_id_r,))
            result = cursor.fetchone()
            if result :
               st.warning("User_id already exist, Please try something new ")
            else:
            # converting to hashed password-------------------
               hashed_password_r = hashlib.sha256(password_r.encode()).hexdigest() 
               query = """INSERT INTO login_flow(user_name,hashed_password ,user_role)
               values(%s,%s,%s)"""
               values = (user_id_r,hashed_password_r,role_r)
               cursor.execute(query,values)
               db.commit()
               st.success("Succesfully Registered")

        


        

#---------------- LOGIN BUTTON --------------------------------------------------------------------------------------------

with tab2:
    st.header("🔐 User Login")
    user_id = st.text_input("Enter User ID:" ,key= "userid_tab2")
    password = st.text_input("Enter Password:", type="password" ,key= "pass_tab2")
    hashed_password = hashlib.sha256(password.encode()).hexdigest() 
    role = st.selectbox("Enter Your Role:" , ["CLIENT","SUPPORT"] ,key= "role_tab2")

    if st.button("LOGIN"):

        if user_id == "" or password == "" or role == "" :
            st.warning("Please Fill all mentioned places")
        else:

            query = "SELECT * FROM login_flow WHERE user_name = %s AND hashed_password = %s AND user_role = %s "
            cursor.execute(query, (user_id, hashed_password, role))
            result = cursor.fetchone() # fetching first row 
  
            if result:
                st.success(f"Login Successful 🎉 - Transferring to {role} side pages")
                if role == "CLIENT":
                    with st.spinner("Transferring to next page⏳"):
                        time.sleep(2)  # wait for 2 seconds
                        st.switch_page("pages/client_side.py")
                elif role == "SUPPORT":
                    with st.spinner("Transferring to next page⏳"):
                        time.sleep(2)  # wait for 2 seconds
                        st.switch_page("pages/support_side.py")

            else:
                st.error("❌ Invalid User ID or Password")


