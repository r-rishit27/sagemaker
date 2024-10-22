import streamlit as st
import requests
import pandas as pd
import google.generativeai as genai

# Replace with your Gemini Pro API key
api_key = "AIzaSyDpDOxW0mDJ97EqnDosH2DJeUTE7jEoRvI"

# Configure Google Gemini API key
genai.configure(api_key=api_key)

def fetch_data(endpoint):
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Define API endpoint
order_api_url = 'http://127.0.0.1:8000/api/orders/'

# Create a layout with three columns
col1, col2, col3 ,col4= st.columns(4)

with col1:
    if st.button('Current Cart Status'):
        # Refresh or trigger cart status update
        if 'refresh' not in st.session_state:
            st.session_state.refresh = 0
        st.session_state.refresh += 1

with col2:
    # Create a Home button with redirection
    home_button_html = '''
        <a href="http://localhost:8000" target="_blank" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
        ">Buy More </a>
    '''
    st.markdown(home_button_html, unsafe_allow_html=True)

with col3:
    # Create a Home button with redirection
    home_button_html = '''
        <a href="http://localhost:8500" target="_blank" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
        ">Home</a>
    '''
    st.markdown(home_button_html, unsafe_allow_html=True)

with col4:
    # Create a Home button with redirection
    home_button_html = '''
        <a href="http://localhost:8000/checkout" target="_blank" style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
        ">CheckOut </a>
    '''
    st.markdown(home_button_html, unsafe_allow_html=True)


def generate_recommendations(products_list):
    # Create a Gemini model instance
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    
    # Format the products list for the prompt
    products_str = ', '.join(products_list)
    
    # Create the prompt including the product list
    prompt = f"""read all the items from the string: {products_str}
    now predict what I might want to create from this.
    Your job is to give short and crisp 5 tips and suggestions so that I can buy which can help to make the product.
    Start by
    
    Hey! Are you making a product?
    You can also add items1 for tip
    also give 1 little emoji with each tip
    
    if you see many random not connected items suggest to clear the cart first and then only you can help"""

    # Generate recommendations
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating recommendations: {e}")
        return "Error generating recommendations"

# Fetch and display order data
data = fetch_data(order_api_url)

if data:
    df = pd.DataFrame(data)
    df1=df[['product_name','product_price','quantity']]
    st.dataframe(df1)
    
    df['total_price'] = df['quantity'] * df['product_price']
    total_price = df['total_price'].sum()
    
    st.subheader(f"Total Price: ₹{total_price:.2f}")
    
     # Button to show item location
    if 'show_location' not in st.session_state:
        st.session_state.show_location = False

    if st.button('Show Item Location'):
        st.session_state.show_location = True

    if st.session_state.show_location:
        location_df = df[['product_name', 'location']]
        st.dataframe(location_df)


    # Extract product names from the dataframe
    products_list = df['product_name'].unique().tolist()
    
    # Generate and display recommendations
    recommendations = generate_recommendations(products_list)
    st.subheader("Suggestions:")
    st.write(recommendations)
else:
    st.write("No data available.")

