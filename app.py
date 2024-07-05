import streamlit as st
import requests

st.set_page_config(
    page_title="WordWhiz",
    page_icon="logo.png",
    menu_items={
        "About":"""Elevate your language skills with WordWhiz! Our comprehensive online dictionary provides detailed parts of speech, synonyms, antonyms, and example sentences to help you master every word. Perfect for students, writers, and language lovers. Start your word journey with WordWhiz today!"""
    }
)

st.write("<h2 style='color:#ff6a00;'>Unraveling the Secrets of Words</h2>",unsafe_allow_html=True)

word=st.text_input("Type a Word")

btn=st.button("Search")

if btn:
    try:
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url)
        dict=response.json()

        # Displaying the Word with phonetics
        for i in range(0,len(dict[0]["phonetics"])):
            if("text" not in dict[0]["phonetics"][i]):
                continue
            elif(len(dict[0]["phonetics"][i]["text"])>=1):
                st.write(f'<h4><span style=color:#1fa2ff;>Word:</span>  {dict[0]["word"]} ({dict[0]["phonetics"][i]["text"]})</h4>',unsafe_allow_html=True)
            break
        else:
            st.write(f'<h4><span style=color:#1fa2ff;>Word:</span>  {dict[0]["word"]}</h4>',unsafe_allow_html=True)

        # Getting Audio
        for i in range(0,len(dict[0]["phonetics"])):
            if("audio" not in dict[0]["phonetics"][i]):
                continue
            elif(len(dict[0]["phonetics"][i]["audio"])>=3):
                st.write(f'<h4><span style=color:#1fa2ff;>Listen:</span></h4>',unsafe_allow_html=True)
                st.audio(dict[0]["phonetics"][i]["audio"])
                break

        parts_of_speech=[]
        # Getting all parts of speech
        for i in range(0,len(dict[0]["meanings"])):
            if(dict[0]["meanings"][i]['partOfSpeech'] is ""):
                continue
            elif(len(dict[0]["meanings"][i]['partOfSpeech'])>=2):
                # checking that the parts of speech should not duplicate
                if(dict[0]["meanings"][i]['partOfSpeech'] not in parts_of_speech):
                    # Showing parts of speech separetly
                    st.write(f'<h4><span style=color:#1fa2ff;>{dict[0]["meanings"][i]['partOfSpeech']}:</span></h4>',unsafe_allow_html=True)
                    parts_of_speech.append(dict[0]["meanings"][i]['partOfSpeech'])
                    # Iterating each parts of speech
                    for j in range(0,len(dict[0]["meanings"][i]['definitions'])):
                        if("example" not in dict[0]["meanings"][i]['definitions'][j]):
                            # If it does not contain example then use this
                            st.write(f"<li style='font-size:20px;'>{dict[0]["meanings"][i]['definitions'][j]["definition"]}</li>",unsafe_allow_html=True)
                        else:
                            # If it contains example then use this 
                            st.write(f"<li style='font-size:20px;'>{dict[0]["meanings"][i]['definitions'][j]["definition"]} For Example: {dict[0]["meanings"][i]['definitions'][j]["example"]}</li>",unsafe_allow_html=True)

        synonyms=[]
        antonyms=[]
        def syn_anto(data,synonyms,synonym):
            for i in range(0,len(dict[0]["meanings"])):
                if(len(dict[0]["meanings"][i][data])==0):
                    continue
                else:
                    for j in range(0,len(dict[0]["meanings"][i][data])):
                        synonyms.append(dict[0]["meanings"][i][data][j])
            if(list(set(synonyms))==[]):
                st.empty()
            else:
                st.write(f'<h4><span style=color:#1fa2ff;>{data.title()}:</span></h4>',unsafe_allow_html=True)
                for synonym in list(set(synonyms)):
                    st.write(f"<li style='font-size:20px;'>{synonym}</li>",unsafe_allow_html=True)
        syn_anto('synonyms',synonyms,'synonym')
        syn_anto('antonyms',antonyms,'antonym')
    except:
        st.error("Sorry pal, we couldn't find definitions for the word you were looking for.")