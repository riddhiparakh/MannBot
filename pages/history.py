import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
from streamlit_chat import message
if not firebase_admin._apps:
    cred = credentials.Certificate('FIREBASE')  #add cred for firebase
    firebase_admin.initialize_app(cred)

def main():
    db=firestore.client()
    if "signedout"  not in st.session_state:
        st.warning('Please Login or Sign Up to chat with MannBot') 
         
    else:
        name=st.session_state.username
        st.title(f"{name}'s Chat History")
        if st.button("🗑️"):
            st.session_state.conversation = []  # Clear conversation history
            st.session_state.chat_history = []
        docs=db.collection('prompt').get()
        for doc in docs:
            d = doc.to_dict()
            if 'prompt' in d and 'answer' in d and 'username' in d:
                if d['username'] ==name:  # Check if the username matches the user's name
                    #for testing
                    # st.write(f"Username: {d['username']}")
                    # st.write(f"Prompt: {d['prompt']}")
                    # st.write(f"Answer: {d['answer']}")
                    st.session_state.conversation.append(f" {d['answer']}")
                    st.session_state.chat_history.append(f"{d['prompt']}")
                    print(st.session_state.chat_history)
                    if st.session_state['conversation']:
                
                        for i in range(len(st.session_state['chat_history'])-1,-1,-1):
                                message(f"{name}:{st.session_state['chat_history'][i]}", key=str(i),is_user=True,)
                                message(st.session_state['conversation'][i],  key=str(i) + '_user')
                                data = {
                            'username': name,
                            'prompt': d['prompt'],
                            'answer': d['answer']
                            }
                
                                print("adding to history")
                                db.collection("prompt").document(name).update(data)   
                                pos=db.collection('prompt').document(st.session_state.username)
                                pos.update({u'Prompt': firestore.ArrayUnion([u'{}'.format(d)])})



if __name__ == '__main__':
    main()
