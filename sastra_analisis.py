# -*- coding: utf-8 -*-
"""sastra_analisis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uBttuhlTYd9Pm5HFZ2D9FuKReFAHRpxS
"""

!pip install nltk
!pip install spacy
!python -m spacy download de_core_news_sm
!pip install streamlit

import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
import streamlit as st
import io
import pandas as pd
import spacy

# Function to analyze the text
def analyze_text(text):
    # Tokenisasi dan Menghitung Frekuensi Kata (Tanpa Tanda Baca)
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords

    words = nltk.word_tokenize(text)
    punctuation = set(stopwords.words('german'))
    words = [word for word in words if word.isalnum() and word.lower() not in punctuation]
    fdist = FreqDist(words)
    df_frequencies = pd.DataFrame(fdist.items(), columns=['Word', 'Frequency'])
    df_frequencies = df_frequencies.sort_values(by='Frequency', ascending=False)

    # Analisis Kelas Kata dan Grammatik dengan SpaCy (Bahasa Jerman)
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    grammatical_data = []
    for token in doc:
        if token.is_alpha:
            grammatical_data.append([token.text, token.pos_, token.dep_, token.head.text])

    df_grammar = pd.DataFrame(grammatical_data, columns=['Word', 'POS', 'Dependency', 'Head'])

    return df_frequencies, df_grammar

# Streamlit app
st.title("German Text Analysis")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    text = io.TextIOWrapper(uploaded_file, encoding='utf-8').read()

    st.subheader("Uploaded Text:")
    st.write(text[:500])  # Menampilkan 500 karakter pertama dari teks

    df_frequencies, df_grammar = analyze_text(text)

    st.subheader("Word Frequencies:")
    st.dataframe(df_frequencies.head(10))

    st.subheader("Grammatical Analysis:")
    st.dataframe(df_grammar.head(10))

    # Download buttons
    st.download_button(
        label="Download Word Frequencies",
        data=df_frequencies.to_csv(index=False).encode('utf-8'),
        file_name='word_frequencies.csv',
        mime='text/csv',  # Corrected mime type
    )
    st.download_button(
        label="Download Grammatical Analysis",
        data=df_grammar.to_csv(index=False).encode('utf-8'),
        file_name='word_grammar.csv',
        mime='text/csv',  # Corrected mime type
    )