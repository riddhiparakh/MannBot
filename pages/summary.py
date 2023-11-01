import streamlit as st
from transformers import pipeline
import pandas as pd
from datetime import datetime

def main():
    df = pd.read_csv('/summary_data/fine_tuned_summaries.csv', sep=',', encoding='latin-1')#add path to summary which is in summary_data
    print(df.head(1))
    st.title("Text Summary")
    st.text("Add a text file to generate a summary, the text file should be in dd_mon_yyyy.txt:")
    uploaded_files = st.file_uploader("Choose a text file", accept_multiple_files=True)
    summaries = []

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        text_data = uploaded_file.read().decode("utf-8")
        st.text(text_data)  # Display the text

        # Extract the date from the uploaded file name
        date_str = uploaded_file.name.split(".")[0]
        date_obj = datetime.strptime(date_str, "%d_%b_%Y")
        formatted_date = date_obj.strftime("%d-%b-%y")
        
        # Check if the date exists in the DataFrame
        matching_summary = df[df['Date'] == formatted_date]['summary'].values
        if matching_summary:
            summaries.append(matching_summary[0])
        else:
            summarizer = pipeline("summarization", model="riddhiparakh/mannbot", device=0)
            result = summarizer(uploaded_file )
            st.write(result[0]['summary_text'])

    if st.button("Process"):
        with st.spinner("Processing"):
            for summary in summaries:
                st.write("Summary for",formatted_date)
                st.write(summary)  # Display the summaries

if __name__ == "__main__":
    main()

