

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from data_injection import data_injuction
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-base-e2e-qg")
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-base-e2e-qg")



def retrieve_question(model, chunks):
    all_questions=[]
    for chunk in chunks:
        inputs= tokenizer(chunk, return_tensors='pt',truncation=True, max_length=512)
        output= model.generate(**inputs, max_length=128,num_beams=2)
        questions= [ tokenizer.decode(q, skip_special_tokens=True) for q in output]
        print('questions')
        print(questions)
        all_questions.append(questions)
    return all_questions


chunks= data_injuction()
print('chinks \n')
print(chunks)
retrieve_question(model, chunks)