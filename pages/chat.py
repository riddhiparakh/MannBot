import streamlit as st 
import streamlit as st 
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate
import os
from st_pages import show_pages_from_config, add_page_title,Page,show_pages
from streamlit_chat import message
import firebase_admin
from firebase_admin import credentials, firestore
 
api_key = os.getenv("HUGGING_FACE_API_KEY")
db_path='' # add the path to db_faiss
messages= []
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
previous_questions = []    

    
def main():
    load_dotenv()
    if "signedout"  not in st.session_state:
        st.warning('Please Login or Sign Up to chat with MannBot')
    else:
            
        prompt = st.chat_input("Ask about Mann ki Baat")  
        name=st.session_state.username
        message(f"Welcome,{name}") 
        if prompt:
            if st.session_state.signout:
                name=st.session_state.username
                 
            
            message(f"{name}: {prompt}",is_user=True)

                
            with st.spinner('Processing...'):
                print("processing")
                llm = HuggingFaceHub(repo_id="MBZUAI/LaMini-Flan-T5-783M", model_kwargs={"temperature":0.00005, "max_length":2048}, huggingfacehub_api_token=api_key)
                print("in llm")
                chain = load_qa_chain(llm,chain_type='refine')
                print("made chain")
                embeddings = HuggingFaceEmbeddings()
                print("embeddings")
                document_search = FAISS.load_local(db_path, embeddings)
                print("loading document")
                docs = document_search.similarity_search(prompt, k=5)
                print("searching document")
                result = chain.run(input_documents=docs, question=prompt)
                file_path = [doc.metadata['source'] for doc in docs][0]
                filename = os.path.basename(file_path)
                date_part = os.path.splitext(filename)[0]  # Remove the extension
                date = " ".join(date_part.split("_"))  # Replace underscores with spaces
                print(date)
                print("result and date is printed")
                message(result)
                message(f"The source of the answer is : {date}")
                print("process done")
                # st.session_state.messages.append({"role":prompt, "ans": result})
                db = firestore.client()
                user_data = {
                'username': name,
                # 'email': new_email,
                # Add more user-specific fields as needed
            }
                db.collection("prompt").document(name).set(user_data)
                data = {
                    'username': name,
                    'prompt': prompt,
                    'answer': result,
                    'source':date
                    }
      
                print("adding to history")
                db.collection("prompt").document(name).update(data)
                prompt_list=[]
                prompt_list.append(prompt)



if __name__=='__main__':
    main()
    

    
  




