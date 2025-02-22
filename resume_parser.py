# -*- coding: utf-8 -*-
"""Resume Parser

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GM8oeoAlJ0jc_OTNq3IcTdvXR1si76nK
"""

import docx2txt
from PyPDF2 import PdfReader, PdfFileWriter, PdfFileMerger

#Extracting text from DOCX
def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)

#Extracting text from PDF
def pdftotext(m):
    # pdf file object
    # you can find find the pdf file with complete code in below
    pdfFileObj = open(m, 'rb')

    # pdf reader object
    pdfFileReader = PdfReader(pdfFileObj)

    # number of pages in pdf
    num_pages = len(pdfFileReader.pages)

    currentPageNumber = 0
    text = ''

    # Loop in all the pdf pages.
    while(currentPageNumber < num_pages ):

        # Get the specified pdf page object.
        pdfPage = pdfFileReader.pages[currentPageNumber]

        # Get pdf page text.
        text = text + pdfPage.extract_text()

        # Process next page.
        currentPageNumber += 1
    return (text)

import re
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
print('Mail id: ',extract_email_addresses(textinput))

def extract_mobile_number(resume_text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)

    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return number
        else:
            return number
print('Mobile Number: ',extract_mobile_number(textinput))

import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')

# THIS Block of code will extract the skills
# which are already listed in a huge Dataset

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    colnames = ['skill']
    # reading the csv file
    data = pd.read_csv('skills.csv', names=colnames)

    # extract values
    skills = data.skill.tolist()
    print(skills)
    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]
print(extract_skills(textinput))

import spacy
import en_core_web_sm
from spacy.matcher import Matcher

# THIS Block of Code will extract NAME from a RESUME

# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME',[pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
textinput = pdftotext("/content/resume1.pdf")
print('Name: ',extract_name(textinput))

"""NOW COMBINE THESE ALL Data"""

print("Name:",extract_name(textinput))
print("Email:",extract_email_addresses(textinput))
print("Mobile Number:",extract_mobile_number(textinput))
print("Skills:",extract_skills(textinput))

