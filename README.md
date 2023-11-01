# MannBot

## Overview

MannBot is an AI-powered chatbot and analysis tool designed to provide insights into "Mann ki Baat," a popular radio program in India hosted by Prime Minister Narendra Modi. MannBot offers several features that make it a valuable resource for understanding and interacting with the program:

- **Summarization:** MannBot provides summarized versions of Mann ki Baat episodes. The summarization is based on fine-tuning the T5-base model from Hugging Face.

- **Sentiment Analysis:** It offers sentiment analysis of YouTube comments related to Mann ki Baat. This feature helps gauge the public's sentiment and feedback on the program.

- **Chat Interaction:** Users can have conversations with MannBot to gain more insights and information about Mann ki Baat.

## Requirements

Before using this repository, make sure you have the following:

- Python environment
- Libraries and dependencies specified in `requirements.txt`
- A Hugging Face API key for fine-tuned models
- Local path for database storage
- Firebase Admin API key to access the database and authentication
- Authentication links (specified in `links.txt`)
- Google Developer  (specified in `links.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/MannBot.git

Usage
To run the MannBot app:

streamlit run home.py

This is the deployed app
https://mannbot.streamlit.app/

In the chat.py, you can use the following prompt  or any other prompt based on Mann ki Baat. Make sure the prompt is detailed.

Questions:
What is the significance of observing 2 minutes of silence at 11 A.M. on January 30?

How did Sardar Patel describe the importance of khadi to India?

What is Modi talking about cleanliness?

What is Modi talking about the Vijay Vijay Dashami?

What is Modi's take on drugs?

What is Modi's take on drugs? What is his plan to reduce them? Does he think youth should do drugs?





