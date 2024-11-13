
import streamlit as st

# Sidebar
st.sidebar.header("User Information")
user_id = st.sidebar.text_input("Enter ID")
user_name = st.sidebar.text_input("Enter Name")

print(user_id, user_name, type(user_id))

st.sidebar.header("Model and Database Settings")

# Model Selection
model = st.sidebar.selectbox("Select ML Model", ["Model1", "Model2", "Model3"])

# Database Details
db_username = st.sidebar.text_input("Enter DB Username")
db_password = st.sidebar.text_input("Enter DB Password", type="password")
db_hostname = st.sidebar.text_input("Enter Hostname")
db_name = st.sidebar.text_input("Enter DB Name")
table_name = st.sidebar.text_input("Enter Table Name")

if st.sidebar.button("Store Data"):
    # Code to connect to MySQL and store the data
    st.write("Data stored successfully in the database.")




st.title('Obesity Risk Prediction')

st.write("Please fill in the details below")




# Buttons in Main Area
if st.button("Predict"):
    # Call your prediction function here
    obesity_type = "Predicted Type of Obesity"  # Replace with actual prediction
    st.write("Type of Obesity:", obesity_type)
