import streamlit as st

#EDA pkg
import pandas as pd
import numpy as np

# Model Load/Save
from joblib import load
import joblib
import os

import sys, fitz


#NLP
import spacy
import pickle
import random
import re
import json
import random
import logging

# Emoji
#import emoji

def re_f(doc):

  rf ={}
  for ent in doc.ents:
    if ent.label_.upper() not in rf:
      i={ent.label_.upper():set([ent.text])}
      rf.update(i)
    rf[ent.label_.upper()].add(ent.text)
  

  final= {}
  for k,v in rf.items():
    if k == 'NAME' or k=='SKILLS':
      i={k:list(v)}
      final.update(i)

  return final
 	

  #from print_dict import pd

  #print('Complete Dictionary\n')
  #pd(rf)

  #print('\n\n\n\n')

  #print('Required Dictionary\n')
  #pd(final)


def clean_data(df):
    clean_df = re.sub(r"[\(\[].*?[\)\]]", "", df)
    return (clean_df)


def resume_parser(file):
	doc = fitz.open(file)
	text = ""
	for page in doc:
		text = text + str(page.getText())
		tx = " ".join(text.split('\n'))
		nlp_model = spacy.load('my_nlp_model')
		c_data=clean_data(tx)
		doc = nlp_model(c_data)
		clean_dict =re_f(doc)
	return clean_dict



## Load Models
def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model


# Main
def main():
	"""Drugs Entities Recognition Web App """
	st.title("Drugs Entities Recognition Web App")
	activities = ["Drugs NER","About"]
	choice = st.sidebar.selectbox("Choice",activities)

	# Choice = Sentiment
	if choice == 'Drugs NER':
		st.subheader("Drugs Entities Recognition")
		#st.write(emoji.emojize('Everyone :red_heart: Streamlit ',use_aliases=True))

		uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
		if uploaded_file is not None:
			file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
			st.write(file_details)
			d=resume_parser(uploaded_file)
			st.json(d)


	if choice == 'About':
		st.subheader("About")
		st.markdown("""
			#### Drugs Entities Recognition Web App
			##### Built with Streamlit

			#### By
			+ Hrishikesh Sharad Malkar
			""")
		#st.write(emoji.emojize('Everyone :red_heart: Streamlit ',use_aliases=True))
		



if __name__ == '__main__':
	main()

