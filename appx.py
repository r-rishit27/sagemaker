from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyDpDOxW0mDJ97EqnDosH2DJeUTE7jEoRvI")

# Initialize model and embeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load and split PDF into multiple pages
loader = PyPDFLoader("item_list1.pdf")
pages = loader.load_and_split()

# Initialize VectorDB and Retriever
vectordb = Chroma.from_documents(pages, embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

# Define retrieval chain
template = """
You are a helpful AI assistant.
Your work is to give the link of input.
In the PDF format is 
input1  input1_link 
input2  input2_link 
and so on
input: {input}
Context: {context}
Please provide only the link associated with the input:
answer:
"""
prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

def get_link_from_db(item_name):
    try:
        response = retrieval_chain.invoke({"input": item_name})
        link = response.get("answer", "#")
        return link
    except Exception as e:
        return f"An error occurred: {e}"

# Initialize Streamlit app
st.set_page_config(page_title="SageMaker")
logo_url = 'bot-modified.png'  # Replace with your logo's path or URL

# Create columns to arrange the logo and title side by side
col1, col2 = st.columns([1, 3])  # Adjust column ratios as needed

with col1:
    st.image(logo_url, width=125)  # Adjust the width of the logo as needed

with col2:
    st.markdown("""
    <style>
        .header {
            text-align: center;
            color: #fbc02d; /* Yellow text */
            background-color: #1e88e5; /* Blue background */
            padding: 20px;
            border-radius: 12px;
            font-family: 'Arial', sans-serif;
            font-size: 40px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            border: 3px solid #fbc02d; /* Yellow border */
            width: fit-content;
            margin: auto;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
    <h1 class="header">SageMaker</h1>
""", unsafe_allow_html=True)

input_text = st.text_input("Welcome to SageMaker! How can I assist you today?", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="file_uploader")

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input_prompt = """
You are a creator who wants to create an item shown in the image or mentioned in the text. List down all the required items you will need to create that item.
List all those items in the following format:
    1. Item 1
    2. Item 2
    3. Item 3
    and so on.
Make sure to only give items, no extra text, and don't group similar items.
Do not separate items and tools, list them without any extra heading.
Never give extra information or comments, just show item names only. It is very important to just show only item names.
Avoid using random sentences like "your favorite" or "as per your choice".
Give only top priority requirements.
"""

# Initialize the Google Generative AI model
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    try:
        if input_text and image:
            response = model.generate_content([input_text, image, prompt])
        elif input_text:
            response = model.generate_content([input_text, prompt])
        elif image:
            response = model.generate_content([image, prompt])
        else:
            response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


submit = st.button("Essentials / Consumables")
# Creating answer buttons with unique keys
col1, col2, col3 = st.columns(3)
with col1:
    ask_requirements = st.button("Ask for requirements", key="ask_requirements")
with col2:
    get_steps = st.button("Steps to create", key="get_steps")
with col3:
    related_videos = st.button("Related videos", key="related_videos")

# Redirect button
redirect_url = 'http://localhost:8502'

button_html = f'''
    <style>
        .button {{
            display: inline-block;
            padding: 15px 15px;
            font-size: 15px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            background-color: #4CAF50;
            border: none;
            border-radius: 15px;
        }}
        .button:hover {{background-color: #3e8e41}}
        .button:active {{
            background-color: #3e8e41;
            box-shadow: 0 5px #666;
            transform: translateY(4px);
        }}
    </style>
    <a href="{redirect_url}" target="_blank"><button class="button">Go to Cart</button></a>
'''

st.write(button_html, unsafe_allow_html=True)

# Add process of creating product generating function
input_prompt_steps = """
If it ia food item YOU ARE A MASTERCHEF, if it is a mechanical item you are MECHNAICAL EXPERT , if it is an electrical or electronics related item YOU ARE ELECTRONICS EXPERT and if any other you are expert of related field. 

TITLE

*PROCEDURE:*

Describe the detailed procedure or recipe INVOLVED step-by-step IN A PARAGRAPH FORMAT DETAIL EXPLANATION NEEDED

Avoid using random sentences, personal preferences, or additional headings. Only list the top priority requirements instructions and procedure.
 
"""
if submit:
    response_steps = get_gemini_response(input_text, image, input_prompt)
    st.subheader("Essential Items Required:")
    st.write(response_steps)

if get_steps:
    response_steps = get_gemini_response(input_text, image, input_prompt_steps)
    st.subheader("Steps to Create the Product:")
    st.write(response_steps)

# Display requirements and options for items
if ask_requirements:
    response = get_gemini_response(input_text, image, input_prompt)
    st.subheader("Requirements:")

    # Assume response is a list of items in text format
    items_list = response.strip().split('\n')
    for idx, item in enumerate(items_list):
        item_name = item.strip().split('.', 1)[-1].strip()  # Extract the item name
        if item_name:
            # Retrieve the associated link from the database
            link = get_link_from_db(item_name)
            
            # URL for searching the item on your Django site
            search_url = f"http://localhost:8000/search/?q={item_name}"

            # Display the item with "Go" and "Buy" buttons
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(item_name)
            with col2:
                # Use markdown to create a clickable "Top choices(my website)" button
                st.markdown(
                    f'<a href="{search_url}" target="_blank" class="action-button">Top Choices</a>',
                    unsafe_allow_html=True
                )
            with col3:
                # Use markdown to create a clickable "Buy More(host)" button
                st.markdown(
                    f'<a href="{link}" target="_blank" class="action-button">Buy More</a>',
                    unsafe_allow_html=True
                )

video_url = 'https://www.youtube.com/embed/sv3TXMSv6Lw?loop=1&autoplay=1'  # Replace with your desired YouTube video URL

if related_videos:
    st.write("Tutorial Video")
    st.markdown(f'''
        <iframe width="560" height="315" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    ''', unsafe_allow_html=True)

# Add some CSS to style the buttons
st.markdown("""
    <style>
        .action-button {
            display: inline-block;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            background-color: #D0D0D0;
            border-radius: 4px;
            text-decoration: none;
        }
        .action-button:hover {
            background-color: #A9A9A9;
        }
    </style>
""", unsafe_allow_html=True)
