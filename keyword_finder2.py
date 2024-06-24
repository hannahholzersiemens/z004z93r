import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import streamlit as st

# Ensure nltk resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Define the function to find keywords in text
def find_keywords_in_text(text, keyword_dict):
    found_keywords = {}
    # Convert the input text to lowercase
    text = text.lower()
    words = word_tokenize(text)
    text_tokens = ' '.join(words)  # Create a single string of tokens

    for keyword in keyword_dict.keys():
        # Convert each keyword to lowercase for case-insensitive comparison
        if keyword.lower() in text_tokens:
            found_keywords[keyword] = keyword_dict[keyword]

    return found_keywords

# Streamlit application
st.title("Keyword Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file with keywords", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Select industry
    industry_options = ["AD", "AT", "CPR", "ES", "HE", "IM", "MA", "EU", "MD", "SMB"]
    industry = st.selectbox("Select your industry", industry_options)
    
    if industry:
        # Filter keywords by the selected industry and those for all industries
        industry_keywords = df[(df['industry'] == industry) | (df['industry'].str.lower() == 'all')]
        keywords = industry_keywords['keyword'].tolist()
        hyperlinks = industry_keywords['hyperlink'].tolist()
        
        # Create a dictionary of keywords and their associated hyperlinks
        keyword_dict = dict(zip(keywords, hyperlinks))
        
        # Prompt user for text input
        text = st.text_area("Please enter the text to analyze")
        
        if st.button("Analyze"):
            if text:
                found_keywords = find_keywords_in_text(text, keyword_dict)
                
                # Convert the found keywords dictionary to a pandas DataFrame
                output_df = pd.DataFrame(list(found_keywords.items()), columns=['Keyword', 'Hyperlink'])
                
                # Display the DataFrame
                st.write(output_df)
            else:
                st.warning("Please enter text to analyze.")
else:
    st.info("Please upload a CSV file to proceed.")
