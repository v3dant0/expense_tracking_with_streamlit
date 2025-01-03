import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.title("Expenditure Form")
st.markdown("Enter the expense details below")


conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Sheet1", usecols=list(range(11)), ttl=5)


bank_account = [
    "Kotak Mahindra Bank",
    "State Bank of India",
    "SBM Credelio Credit Card"
]

spend_location = [
    "Recharge",
    "Travel Tickets",
    "Canteen",
    "College Bill",
    "Utilities",
    "Shopping",
    "Swiggy/Zomato",
    "Groceries"
]


current_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"Date: {current_date}")


Amount = st.number_input(label="Amount?*", min_value=0, step=1)
bank_account = st.selectbox("Select Bank Account", options=bank_account, index=None)
spend_type = st.selectbox("Where did you spend the money?*", options=spend_location, index=None)


travel_mode = None
mobile_operator = None
food_item = None
bill_type = None
utility_type = None
shopping_type = None

if spend_type == "Travel Tickets":
    travel_mode = st.selectbox("Select Travel Mode", options=["Aeroplane", "Train"])
elif spend_type == "Recharge":
    mobile_operator = st.selectbox("Select Mobile Operator", options=["Jio", "VI"])
elif spend_type == "Canteen":
    food_item = st.selectbox("Food type", options=["Order", "Snacks"])
elif spend_type == "College Bill":
    bill_type = st.selectbox("Bill Type", options=["Mess + Electricity", "Semester fees"])
elif spend_type == "Utilities":
    utility_type = st.selectbox("What Utility", options=["Spotify"])
elif spend_type == "Shopping":
    shopping_type = st.selectbox("Where did you shop?", options=["Amazon", "Other online platform", "Local shop"])


info = st.text_input("Product Info")


if st.button(label="Submit"):
    
    expense_data = pd.DataFrame(
        [
            {
                "Amount": Amount,
                "Bank Account": bank_account,
                "Spend Location": spend_type,
                "Mobile Operator": mobile_operator,
                "Travel Mode": travel_mode,
                "Food Type": food_item,
                "Bill Type": bill_type,
                "Utility Type": utility_type,
                "Shopping Type": shopping_type,
                "Product Info": info,
                "Date": current_date,
            }
        ]
    )

    
    required_columns = [
        "Amount", "Bank Account", "Spend Location", "Mobile Operator", "Travel Mode", 
        "Food Type", "Bill Type", "Utility Type", "Shopping Type", "Product Info", "Date"
    ]
    
    
    if existing_data.empty:
        existing_data = pd.DataFrame(columns=required_columns)

    
    missing_columns = [col for col in required_columns if col not in existing_data.columns]
    for col in missing_columns:
        existing_data[col] = None

    
    updated_df = pd.concat([existing_data, expense_data], ignore_index=True)
    
   
    try:
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("Expense registered successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
