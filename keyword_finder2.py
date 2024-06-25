import nltk
nltk.download('punkt')  # Add this line to download the 'punkt' tokenizer data
import pandas as pd
from nltk.tokenize import word_tokenize
import streamlit as st

# Define the function to find keywords in text
def find_keywords_in_text(text, keyword_dict):
    found_keywords = {}
    text = text.lower()
    words = word_tokenize(text)
    text_tokens = ' '.join(words)

    keyword_positions = {}

    for keyword in keyword_dict.keys():
        keyword_lower = keyword.lower()
        position = text_tokens.find(keyword_lower)
        if position != -1:
            hyperlink = keyword_dict[keyword]
            # If the hyperlink is not already in the dictionary or this keyword appears earlier
            if hyperlink not in keyword_positions or position < keyword_positions[hyperlink]['position']:
                keyword_positions[hyperlink] = {'position': position, 'keyword': keyword}

    # Create the found_keywords dictionary from keyword_positions
    for hyperlink, info in keyword_positions.items():
        found_keywords[info['keyword']] = hyperlink

    # Sort found_keywords by their position in the text
    sorted_keywords = sorted(found_keywords.items(), key=lambda kv: keyword_positions[kv[1]]['position'])

    return sorted_keywords

# Streamlit application
st.title("Keyword Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload your file with keywords", type=["csv", "xlsx", "xls"])
if uploaded_file is not None:
    # Determine file type and load accordingly
    if uploaded_file.name.endswith('.csv'):
        try:
            df = pd.read_csv(uploaded_file, encoding='latin-1')  # Try different encodings if necessary
            df.columns = df.columns.str.strip()  # Strip whitespace from column names
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            st.stop()
    else:
        df = pd.read_excel(uploaded_file)
    
    # Select industry
    industry_options = ["AD", "AT", "CPR", "ES", "HE", "IM", "MA", "EU", "MD", "SMB"]
    industry = st.selectbox("Select your industry", industry_options)
    
    if industry:
        industry_keywords = df[(df['industry'] == industry) | (df['industry'].str.lower() == 'all')]
        keywords = industry_keywords['keyword'].tolist()
        hyperlinks = industry_keywords['hyperlink'].tolist()
        
        keyword_dict = dict(zip(keywords, hyperlinks))
        
        text = st.text_area("Please enter the text to analyze")
        
        if st.button("Analyze"):
            if text:
                found_keywords = find_keywords_in_text(text, keyword_dict)
                
                output_df = pd.DataFrame(found_keywords, columns=['Keyword', 'Hyperlink'])
                
                st.write(output_df)
            else:
                st.warning("Please enter text to analyze.")
else:
    st.info("Please upload a file to proceed.")
