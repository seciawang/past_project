import MeCab
from keras.preprocessing.text import Tokenizer
import numpy as np
import re
from tensorflow.keras.utils import to_categorical
from googletrans import Translator
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import concatenate
from keras import Model
from keras import Input
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import io
import json
from importlib import reload
import os
import string
import matplotlib.pyplot as plt
#from sklearn.model_selection import KFold
import argparse
import importlib
import tensorflow as tf
import logging 
import datetime
import itertools
import random
from tkinter import *
from time import sleep

'''
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
'''


#physical_devices = tf.config.experimental.list_physical_devices('GPU')

#physical_devices = tf.config.experimental.list_physical_devices('GPU')


#tf.get_logger().setLevel(logging.ERROR

#logging.getLogger('tensorflow').disabled = True
#logging.getLogger("tensorflow").setLevel(logging.WARNING)

list_target_particle = ["は", "と", "も", "が", "に", "へ", "を", "の", "で", "や"]
list_model_type = ["func_lstm_combined", "func_lstm", "lstm"]

english_symbol = [".", "...", "?", "!"]
japanese_symbol = ["。","…","？","！"]
exclude_english_symbol = string.punctuation


dict_total_particle = {}
dict_total_ignored_particle = {}

list_identifier = []
dict_total_identifier = {}

dict_identifier_pattern = {}



particle_limit = 200
total_sentence = 10000
neighbour = 2

identifier_type = 1

def info_particle():

    global dict_total_particle
    global dict_total_ignored_particle

    #print("dict_total_particle: \n", dict_total_particle)
    #print("\ndict_total_ignored_particle: \n", dict_total_ignored_particle, "\n")

def info_identifier():

    global list_identifier
    global dict_total_identifier

    #print("list_identifier: \n", list_identifier)
    #print("\ndict_total_identifier: \n", dict_total_identifier, "\n")

def info_pattern():

    global dict_identifier_pattern

    #print("Total pattern: ", len(dict_identifier_pattern))
    #print("Most pattern: ", max(dict_identifier_pattern, key=dict_identifier_pattern.get), " with total of ", max(dict_identifier_pattern.values()) , "\n")
    #max(dict_identifier_pattern, key=dict_identifier_pattern.get)

def info_tokenizer(_tokenizer):
  pass
  #print("\nTokenizer.word_index:\n", _tokenizer.word_index)
  #print("\nVocabulary Size: ", len(_tokenizer.word_counts)+1, "\n")

def info_tokenizers(_tokenizer):
  print("\nTokenizer.word_index:\n", _tokenizer.word_index)
  print("\nVocabulary Size: ", len(_tokenizer.word_counts)+1, "\n")

def get_model():

    global list_model_type

    folder_name = "Model"

    folder = os.listdir(folder_name)

    model_list = []
    tokenizer_list = []
    neighbour_list = []
    identifier_list = []
    file_name_list = []
    model_type_list = []


    for x in folder:



        if(x.endswith("_model.h5")):

            file_valid = False

            print("\n")

            model_path = folder_name + "/" + x
            model = load_model(model_path)
            seq_len = model.input_shape[1]
            print("model_path(www): ", model_path)
            if(model_path.find("func_lstm")!=-1):
                seq_len = seq_len[1]

            print(model.input_shape)
            print("Seq_len: ", seq_len)

            if(model_path.find("func_lstm")!=-1):
                neighbour = seq_len
            else:
                neighbour = int(seq_len/2)

            file_name = x[0:x.find("_model.h5")]
            target_file = file_name + "_tokenizer.json"
            print("x (the model): ", x)
            print("target_file: ", target_file)
            print("neighbour: ", neighbour)

            for y in folder:

                if(y == target_file):

                    tokenizer_path = folder_name + "/" + y
                    print("y: ", y)

                    with open(tokenizer_path) as f:
                        data = json.load(f)
                        tokenizer = tokenizer_from_json(data)

                    identifier_type = y[0:1]

                    if(identifier_type=="f"):
                        identifier_type = 1
                    elif(identifier_type=="s"):
                        identifier_type = 2
                    elif(identifier_type=="a"):
                        identifier_type = 3
                    else:
                        file_valid = False
                        break

                    for i in range(len(list_model_type)):
                      if(target_file.find(list_model_type[i])!=-1):
                        model_type = list_model_type[i]
                        file_valid = True
                        break

                    if(not file_valid):
                      break
                    '''
                    if(target_file.find("lstm")!=-1):
                      model_type = "lstm"
                    elif(target_file.find("func_lstm")!=-1):
                      model_type = "func_lstm"
                    else:
                      file_valid = False
                      break

                    file_valid = True
                    break
                    '''

            if(file_valid):
                print("File appended!")
                model_list.append(model)
                tokenizer_list.append(tokenizer)
                neighbour_list.append(neighbour)
                identifier_list.append(identifier_type)
                file_name_list.append(file_name)
                model_type_list.append(model_type)
            else:
                print("There is something wrong with the file model, error for: ", file_name)

    #@@print(neighbour_list)

    return model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list
    #return model_list,tokenizer_list, neighbour_list

def compile_raw(train_name):

    global total_sentence

    #f = open("/content/gdrive/MyDrive/Corpus/raw", "r", encoding='utf8')
    f = open("raw", "r", encoding='utf8')

    sentences = []

    f1 = f.readlines()
    count = 0;

    for x in f1:

        sentences.append(x)
        count += 1
        if (count==total_sentence):
            break

    clean_string(sentences, "_" + train_name)
    f.close()

    print("Succes! corpora.py and corpora_pos.py has been created/updated!")

def compile_raw_alt(s_index, e_index, tag_name):

    global total_sentence

    #f = open("/content/gdrive/MyDrive/Corpus/raw", "r", encoding='utf8')
    f = open("raw", "r", encoding='utf8')

    sentences = []

    f1 = f.readlines()
    count = 0;

    f1 = f1[s_index:e_index]

    for x in f1:

        sentences.append(x)

    clean_string(sentences, tag_name)
    f.close()

    print("Succes raw_alt! corpora.py and corpora_pos.py has been created/updated!")

def sentence_tokenizing(text, token_list):

    cleaned = text

    sentence_count = 0
    page_traverse = 0
    previous_page_traverse = 0
    len_cleaned = len(cleaned)

    while True:

        page_traverse += cleaned[page_traverse:].find("\n")

        if(cleaned[previous_page_traverse:].find("\n")!=-1):
            token_list.append(cleaned[previous_page_traverse:page_traverse])
        else:
            token_list.append(cleaned[page_traverse+1:])
            break;

        page_traverse += 1
        previous_page_traverse = page_traverse

        sentence_count += 1

def word_tokenizing(sentence, token_list):

    prev_index = 0
    current_index = 0

    while True:

        current_index += sentence[current_index:].find(" ")

        if(sentence[prev_index:].find(" ")!=-1):
            token_list.append(sentence[prev_index:current_index])
        else:
            token_list.append(sentence[current_index+1:])
            break;

        current_index += 1
        prev_index = current_index

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#1 - Function for Training Side

def clean_string(sentence, tag_name):

    file_w = open("corpora" + tag_name+ ".py", "w", encoding='utf8')
    file_w.write("training_jpn = \"\"\"")

    file_w_pos = open("corpora_pos"+tag_name+".py", "w", encoding='utf8')
    file_w_pos.write("training_jpn_pos = \"\"\"")

    count = 0


    global identifier_type
    print("Identifier type from clean_string: ", identifier_type)

    for i in sentence:

        skip_flag = 1

        #0 = no skip
        #1 = skip after parse,
        #2 = skip before parse, (nevermind, not used anymore)
        #3 = stop until symbol (procceed, no skip)
        #4 = skip inside parse
        #5 = skip when symbol detected, but no particle


        count += 1

        index = i.find("\t", 0, len(i))
        clean_sentence = i[index+1:len(i)-1]

        '''
        symbol_list = string.punctuation.replace("?","").replace("!","").replace(".","") #NEW LINE 2
        '''


        '''
        if(clean_sentence.find("!?")!=-1 or clean_sentence.find("!?")!=-1):
            skip_flag = 2
            print("found !?")
            break
        '''

        '''

        if(clean_sentence.find("...")!=1): #NEW LINE 2
            skip_flag = 2
            print("found the triple dots ...")
            continue
        '''

        '''
        for char_punc in symbol_list: #NEW LINE 2

            if(clean_sentence.find(char_punc)!=-1):#NEW LINE 2
                skip_flag = 2
                print("found foreign symbol: ", char_punc)
                break
        '''

        '''
        for char_sentence in clean_sentence: #NEW LINE 2

            if(is_alpha(char_sentence)):
                skip_flag=2
                print("found alphabet: ", char_sentence)
                break
        '''

        '''
        if(skip_flag == 2): #NEW LINE 2 (Invalid Symbol Identified, beside from this:     . ? !)
            continue
        '''

        pos_sentence = ""
        valid_symbol = ""

        t = MeCab.Tagger()
        #t = MeCab.Tagger('-r /dev/null -d /usr/local/lib/python3.7/dist-packages/ipadic/dicdir')
        m = t.parseToNode(clean_sentence)



        #'''

        if(identifier_type==3): #use all identifier 助詞,格助詞,引用 etc

            #print("procceed to identifier_type 2")

            while m:

                if(skip_flag==3 or skip_flag==4 or skip_flag==5):
                    break

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                #Update 2 Yeyyyy

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    skip_flag = 0
                    pos_sentence += m.surface
                    pos_sentence += " "

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    skip_flag = 0
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    if(m.feature.find("BOS/EOS")==-1):

                        if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE (EDITED)
                            if(m.surface=="？" or m.surface=="！" or m.surface=="。"):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the japanese ？ ！and 。 [", m.surface, "]")
                                m = m.next #this is not needed
                                continue
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found other japanese symbol [", m.surface, "]")
                                m = m.next #this is not needed
                                continue

                        if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"): #NEW LINE 2 (remove alphabet + symbol + katakana)

                            if(m.surface=="?" or m.surface=="!" or m.surface=="."):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the english ? ! and . [", m.surface, "]")
                                m = m.next #haiyaaa
                                continue
                            #elif(weird_sec_pos):
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                                m = m.next #like i said, not needed
                                continue

                        #if(m.feature.find("サ変接続")!=-1): #NEW LINE
                        #    print(m.surface)

                        sec_pos_sentence = m.feature
                        real_sec_pos = ""

                        for i in range(0,6):

                          i_pos = sec_pos_sentence.find(",")
                          the_pos = sec_pos_sentence[0:i_pos]

                          if(the_pos != "*"):

                            if(i!=0):
                              real_sec_pos += "丶"

                            real_sec_pos += the_pos

                            #if(i!=5):
                            #  real_sec_pos += "丶"

                          sec_pos_sentence = sec_pos_sentence[i_pos+1:]

                        pos_sentence += real_sec_pos

                        '''
                        sec_pos_sentence = m.feature[m.feature.find(",")+1:len(m.feature)]
                        real_sec_pos = sec_pos_sentence[0:sec_pos_sentence.find(",")]

                        while(sec_pos_sentence!="*"):



                          real_sec_pos = real_sec_pos + "丶" + sec_pos_sentence[0:sec_pos_sentence.find(",")]
                          #weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]
                          sec_pos_sentence = sec_pos_sentence[sec_pos_sentence.find(",")+1:len(sec_pos_sentence)]
                        '''

                        '''
                        if(sec_pos_sentence!="一般" and sec_pos_sentence!="*"):

                            if(sec_pos_sentence.find("／")==-1):
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence
                                #pos_sentence += ")"
                            else:
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence[0:sec_pos_sentence.find("／")]
                                #pos_sentence += ")"

                        else:

                            pos_sentence += m.feature[0:m.feature.find(",")]
                        '''

                        pos_sentence += " "

                m = m.next
        #'''

        #'''

        #Use the second identifier (noun　名詞 + pronoun　代名詞)

        if(identifier_type==2):

            #print("procceed to identifier_type 2")

            while m:

                if(skip_flag==3 or skip_flag==4 or skip_flag==5):
                    break

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                #Update 2 Yeyyyy

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    skip_flag = 0
                    pos_sentence += m.surface
                    pos_sentence += " "

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    skip_flag = 0
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    if(m.feature.find("BOS/EOS")==-1):

                        if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE (EDITED)
                            if(m.surface=="？" or m.surface=="！" or m.surface=="。"):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the japanese ？ ！and 。 [", m.surface, "]")
                                m = m.next #this is not needed
                                continue
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found other japanese symbol [", m.surface, "]")
                                m = m.next #this is not needed
                                continue

                        if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"): #NEW LINE 2 (remove alphabet + symbol + katakana)

                            if(m.surface=="?" or m.surface=="!" or m.surface=="."):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the english ? ! and . [", m.surface, "]")
                                m = m.next #haiyaaa
                                continue
                            #elif(weird_sec_pos):
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                                m = m.next #like i said, not needed
                                continue

                        #if(m.feature.find("サ変接続")!=-1): #NEW LINE
                        #    print(m.surface)

                        sec_pos_sentence = m.feature[m.feature.find(",")+1:len(m.feature)]
                        sec_pos_sentence = sec_pos_sentence[0:sec_pos_sentence.find(",")]

                        if(sec_pos_sentence!="一般" and sec_pos_sentence!="*"):

                            if(sec_pos_sentence.find("／")==-1):
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence
                                #pos_sentence += ")"
                            else:
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence[0:sec_pos_sentence.find("／")]
                                #pos_sentence += ")"

                        else:

                            pos_sentence += m.feature[0:m.feature.find(",")]

                        pos_sentence += " "

                m = m.next
        #'''


        #Use the first identifier (noun 名詞)

        #'''
        if(identifier_type==1):

            #print("procceed to identifier_type 1")

            while m:

                if(skip_flag==3 or skip_flag==4 or skip_flag==5):
                    break

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    skip_flag = 0
                    pos_sentence += m.surface
                    pos_sentence += " "

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    skip_flag = 0
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    '''
                    if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE
                        m = m.next
                        continue
                    '''

                    if(m.feature.find("BOS/EOS")==-1):

                        if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE (EDITED)
                            if(m.surface=="？" or m.surface=="！" or m.surface=="。"):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the japanese ？ ！and 。 [", m.surface, "]")
                                m = m.next #this is not needed
                                continue
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found other japanese symbol [", m.surface, "]")
                                m = m.next #this is not needed
                                continue

                        if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"): #NEW LINE 2 (remove alphabet + symbol)

                            weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                            weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                            if(m.surface=="?" or m.surface=="!" or m.surface=="."):

                                if(skip_flag==0):
                                    skip_flag = 3
                                    valid_symbol = m.surface
                                else:
                                    skip_flag = 5

                                #-print("found the english ? ! and . [", m.surface, "]")
                                m = m.next #haiyaaa
                                continue
                            #elif(weird_sec_pos):
                            else:
                                skip_flag=4
                                #-print("[EXCLUDED]found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                                m = m.next #like i said, not needed
                                continue

                        pos_sentence += m.feature[0:m.feature.find(",")]
                        pos_sentence += " "

                m = m.next
        #'''


        if (skip_flag == 1 or skip_flag == 4 or skip_flag == 5):
            continue

        if (skip_flag == 3):
            clean_sentence = clean_sentence[0:clean_sentence.find(valid_symbol)]


        if(i!=sentence[0]):
            file_w.write("\n")
            file_w_pos.write("\n")

        pos_sentence = pos_sentence[:-1]

        file_w.write(clean_sentence)
        file_w_pos.write(pos_sentence)

    file_w.write("\"\"\"")
    file_w.close()
    file_w_pos.write("\"\"\"")
    file_w_pos.close()

def compile_target_sequence(sentence, sequence_list, model_type):

    if(model_type=="func_lstm_combined"):
      model_type = "func_lstm"

    global list_target_particle
    return_flag = 0

    '''
    cancel_flag = 0

    for i in list_target_particle:
        if(total_list_particle[i]>=500):
            cancel_flag = 1

    if (cancel_flag==1):
        return None

    #Other than above, let's also code... to see how many variation are there for each particle
    #は - >  '無開始', '代名詞', '自立', '助動詞'
    #but let's also code the normal version which is は - >  '無開始', '代名詞', 'は', '自立', '助動詞'
    '''

    t = MeCab.Tagger()
    #t = MeCab.Tagger('-r /dev/null -d /usr/local/lib/python3.7/dist-packages/ipadic/dicdir')
    m = t.parseToNode(sentence)

    temp_sentence_list = []
    target_index = []

    index = 0

    prev_index = 0
    current_index = 0

    while True:

        current_index += sentence[current_index:].find(" ")

        if(sentence[prev_index:].find(" ")!=-1):

            temp_sentence_list.append(sentence[prev_index:current_index])

            if(sentence[prev_index:current_index] in list_target_particle):
                target_index.append(index)
        else:

            temp_sentence_list.append(sentence[current_index+1:])

            if(sentence[current_index+1:] in list_target_particle):
                target_index.append(index)

            break;

        current_index += 1
        prev_index = current_index

        index += 1

    #「百合は綺麗」

    global neighbour
    global particle_limit

    for i in target_index:

        if(dict_total_particle[temp_sentence_list[i]]>=particle_limit):
            #print("Particle ", temp_sentence_list[i], " was ignored from sentence ", temp_sentence_list)
            dict_total_ignored_particle[temp_sentence_list[i]] += 1
            continue

        target_sentence = []

        left_index = i-neighbour
        right_index = i+neighbour

        dict_total_particle[temp_sentence_list[i]] += 1

        for idx in range(left_index, right_index+1):

            if(idx<0):
                target_sentence.append("無開始")
            elif(idx>len(temp_sentence_list)-1):
                target_sentence.append("無停止")
            else:
                target_sentence.append(temp_sentence_list[idx])

            if(idx!=right_index+1):
                pass

        #From sentence: 君のことが好き
        # to transformed sentence:

        #1     2    4     5   3
        #開始　君　こと　が　の (の model: last word, last prediction model)

        #1     2     4    5     3
        #の　こと　好き　停止　が (が model: last word, last prediction model)

        #use one model for every particle instead, and take same ammount of data for every particle

        #transformed_target_sentence_list = [target_sentence[1-1], target_sentence[2-1],
        #                                    target_sentence[4-1], target_sentence[5-1],
        #                                    target_sentence[3-1]]


        #print(transformed_target_sentence_list)
        #sequence_list.append(target_sentence)

        last_trans_index = (neighbour*2) + 1
        pattern_trans = ''

        if(model_type=="func_lstm" ): # [1] [2] [3*] [4] [5]  -> [1] [2] [3*]  and [5] [4] [3*]
          #transformed_target_sentence_list.appen
          forward_target_sentence = []
          backward_target_sentence = []

          for wi in range(neighbour):
            forward_target_sentence.append(target_sentence[wi])
            backward_target_sentence.append(target_sentence[last_trans_index-1-wi])

          forward_target_sentence.append(target_sentence[neighbour])
          backward_target_sentence.append(target_sentence[neighbour])

          sequence_list.append(forward_target_sentence)
          sequence_list.append(backward_target_sentence)
          #print("debug yey: ", sequence_list)

          pattern_trans = ' '.join(target_sentence[0:last_trans_index])

        elif(model_type=="lstm"): # [1][2][3*][4][5] -> [1][2][4][5] [3*]

          transformed_target_sentence_list = []

          for wi in range(neighbour):
            transformed_target_sentence_list.append(target_sentence[wi])

          for wi in range(neighbour):
            transformed_target_sentence_list.append(target_sentence[wi+1+neighbour])

          transformed_target_sentence_list.append(target_sentence[neighbour])

          sequence_list.append(transformed_target_sentence_list)
          pattern_trans = ' '.join(transformed_target_sentence_list[0:last_trans_index])


        global dict_identifier_pattern

        if(bool(dict_identifier_pattern.get(pattern_trans))):
            dict_identifier_pattern[pattern_trans] += 1
        else:
            #print("daijoubu", bool(dict_identifier_pattern.get(pattern_trans)))
            dict_identifier_pattern[pattern_trans] = 1

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#2 - Function for User Side

def preprocess_string(sentence, identifier_type, model_type):

    t = MeCab.Tagger()
    #t = MeCab.Tagger('-r /dev/null -d /usr/local/lib/python3.7/dist-packages/ipadic/dicdir')
    m = t.parseToNode(sentence)

    pos_sentence = ""
    raw_sentence = ""
    marked_sentence = []

    have_particle = 0

    global list_target_particle

    #list_target_particle = ["は", "と", "が", "に", "を", "の", "で"]

    #global identifier_type

    #Use the second identifier (noun　名詞 -> pronoun　代名詞)
    #'''
    if(identifier_type==3):

           while m:

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                #Update 2 Yeyyyy

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    have_particle = 1
                    pos_sentence += m.surface
                    pos_sentence += " "
                    raw_sentence += m.surface
                    raw_sentence += " "
                    marked_sentence.append((m.surface, 1))
                    

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    skip_flag = 0
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    if(m.feature.find("BOS/EOS")==-1):

                        if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE (EDITED)
                            if(m.surface=="？" or m.surface=="！" or m.surface=="。"):
                                #-print("found the japanese ？ ！and 。 [", m.surface, "]")
                                m = m.next #this is not needed
                                continue
                            else:
                                #-print("[EXCLUDED]found other japanese symbol [", m.surface, "]")
                                m = m.next #this is not needed
                                continue

                        if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"): #NEW LINE 2 (remove alphabet + symbol + katakana)

                            if(m.surface=="?" or m.surface=="!" or m.surface=="."):
                                #-print("found the english ? ! and . [", m.surface, "]")
                                m = m.next #haiyaaa
                                continue
                            #elif(weird_sec_pos):
                            else:
                                #-print("[EXCLUDED]found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                                m = m.next #like i said, not needed
                                continue

                        #if(m.feature.find("サ変接続")!=-1): #NEW LINE
                        #    print(m.surface)

                        sec_pos_sentence = m.feature
                        real_sec_pos = ""

                        for i in range(0,6):

                          i_pos = sec_pos_sentence.find(",")
                          the_pos = sec_pos_sentence[0:i_pos]

                          #JUST ERASE THE ・ THIS THING!

                          if(the_pos != "*"):

                            if(i!=0):
                              real_sec_pos += "丶"

                            the_pos = the_pos.replace('・', '宀')
                            the_pos = the_pos.replace('−', '囗')

                            real_sec_pos += the_pos

                            #if(i!=5):
                            #  real_sec_pos += "丶"

                          sec_pos_sentence = sec_pos_sentence[i_pos+1:]

                        pos_sentence += real_sec_pos
                        pos_sentence += " "
                        raw_sentence += m.surface
                        raw_sentence += " "
                        marked_sentence.append((m.surface, 0))

                m = m.next

    if(identifier_type==2):

            while m:

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    have_particle = 1
                    pos_sentence += m.surface
                    pos_sentence += " "
                    raw_sentence += m.surface
                    raw_sentence += " "
                    marked_sentence.append((m.surface, 1))

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    have_particle = 1
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    if(m.feature.find("BOS/EOS")==-1):

                        if(m.surface == "　"):
                            #^%$#print("found space")
                            m = m.next
                            continue

                        if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE
                            #^%$#print("found japanese symbol ", m.surface)
                            m = m.next
                            continue

                        if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"):
                            #^%$#print("found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                            m = m.next
                            continue

                        #if(m.feature[0:m.feature.find(",")] == "記号"):
                        #    m = m.next
                        #    continue

                        sec_pos_sentence = m.feature[m.feature.find(",")+1:len(m.feature)]
                        sec_pos_sentence = sec_pos_sentence[0:sec_pos_sentence.find(",")]

                        if(sec_pos_sentence!="一般" and sec_pos_sentence!="*"):

                            if(sec_pos_sentence.find("／")==-1):
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence
                                #pos_sentence += ")"
                            else:
                                pos_sentence += m.feature[0:m.feature.find(",")] #NEW LINE
                                pos_sentence += "丶"
                                pos_sentence += sec_pos_sentence[0:sec_pos_sentence.find("／")]
                                #pos_sentence += ")"

                            raw_sentence += m.surface
                            marked_sentence.append((m.surface, 0))

                        else:
                            pos_sentence += m.feature[0:m.feature.find(",")]
                            raw_sentence += m.surface
                            marked_sentence.append((m.surface, 0))

                        pos_sentence += " "
                        raw_sentence += " "

                m = m.next
    #'''


    #Use the first identifier (noun 名詞)
    #'''
    if(identifier_type==1):


            while m:

                weird_sec_pos = m.feature[m.feature.find(",")+1:len(m.feature)]
                weird_sec_pos = weird_sec_pos[0:weird_sec_pos.find(",")]

                if((m.feature.find("助詞")!=-1)
                   and (m.surface in list_target_particle)
                   and (m.feature.find("接続助詞")==-1 and m.feature.find("終助詞")==-1)):

                    have_particle = 1
                    pos_sentence += m.surface
                    pos_sentence += " "
                    raw_sentence += m.surface
                    raw_sentence += " "
                    marked_sentence.append((m.surface, 1))

                #elif(m.feature.find("助動詞")!=-1 and m.surface=="な"):
                #
                #    have_particle = 1
                #    pos_sentence += m.surface
                #    pos_sentence += " "

                else:

                    if(m.feature[0:m.feature.find(",")] == "記号"): #NEW LINE
                        #^%$#print("found japanese symbol ", m.surface)
                        m = m.next
                        continue

                    if(m.feature[0:m.feature.find(",")] == "名詞" and m.feature[-1]=="*" and weird_sec_pos!="数"):
                        #^%$#print("found alphabet or another english symbol or unknown japanese word (katakana mostly) [", m.surface, "]")
                        m = m.next
                        continue

                    if(m.surface == "　"):
                        #^%$#print("found space")
                        m = m.next
                        continue

                    if(m.feature.find("BOS/EOS")==-1):
                        pos_sentence += m.feature[0:m.feature.find(",")]
                        pos_sentence += " "
                        raw_sentence += m.surface
                        raw_sentence += " "
                        marked_sentence.append((m.surface, 0))

                m = m.next
        #'''

    pos_sentence = pos_sentence[:-1]
    raw_sentence = raw_sentence[:-1]

    return pos_sentence, raw_sentence, marked_sentence, have_particle

def transform_string(sentence, raw_sentence, neighbour, model_type):

    if(model_type=="func_lstm_combined"):
      model_type = "func_lstm"

    global list_target_particle
    transformed_sequence_list = []
    transformed_raw_sequence_list = []
    return_flag = 0

    '''
    cancel_flag = 0

    for i in list_target_particle:
        if(total_list_particle[i]>=500):
            cancel_flag = 1

    if (cancel_flag==1):
        return None

    #Other than above, let's also code... to see how many variation are there for each particle
    #は - >  '無開始', '代名詞', '自立', '助動詞'
    #but let's also code the normal version which is は - >  '無開始', '代名詞', 'は', '自立', '助動詞'
    '''

    t = MeCab.Tagger()
    #t = MeCab.Tagger('-r /dev/null -d /usr/local/lib/python3.7/dist-packages/ipadic/dicdir')
    m = t.parseToNode(sentence)

    temp_sentence_list = []
    #temp_raw_sentence_list = []
    temp_raw_sentence_list = raw_sentence.split(" ")

    #^%$#print("")
    #@@print("\ttemp_raw_sentence_list(preprocess_string): ", end="")

    #@@for ti in temp_raw_sentence_list:

        #@@print(ti, " ", end="")

    #^%$#print("\n")

    target_index = []

    index = 0

    prev_index = 0
    current_index = 0

    while True:

        current_index += sentence[current_index:].find(" ")

        if(sentence[prev_index:].find(" ")!=-1):

            temp_sentence_list.append(sentence[prev_index:current_index])
            #temp_raw_sentence_list.append(raw_sentence[prev_index:current_index])

            if(sentence[prev_index:current_index] in list_target_particle):
                target_index.append(index)
        else:

            temp_sentence_list.append(sentence[current_index+1:])
            #temp_raw_sentence_list.append(raw_sentence[current_index+1:])

            if(sentence[current_index+1:] in list_target_particle):
                target_index.append(index)

            break

        current_index += 1
        prev_index = current_index

        index += 1

    #「百合は綺麗」

    #global neighbour

    for i in target_index:

        target_sentence = []
        raw_target_sentence = []

        left_index = i-neighbour
        right_index = i+neighbour

        #dict_total_particle[temp_sentence_list[i]] += 1

        for idx in range(left_index, right_index+1):

            if(idx<0):
                target_sentence.append("無開始")
                raw_target_sentence.append("[]")
            elif(idx>len(temp_sentence_list)-1):
                target_sentence.append("無停止")
                raw_target_sentence.append("[]")
            else:
                target_sentence.append(temp_sentence_list[idx])
                raw_target_sentence.append(temp_raw_sentence_list[idx])

            if(idx!=right_index+1):
                pass

        #From sentence: 君のことが好き
        # to transformed sentence:

        #1     2    4     5   3
        #開始　君　こと　が　の (の model: last word, last prediction model)

        #1     2     4    5     3
        #の　こと　好き　停止　が (が model: last word, last prediction model)

        #use one model for every particle instead, and take same ammount of data for every particle

        #transformed_target_sentence_list = [target_sentence[1-1], target_sentence[2-1],
        #                                    target_sentence[4-1], target_sentence[5-1],
        #                                    target_sentence[3-1]]

        transformed_target_sentence_list = []
        transformed_raw_target_sentence_list = []
        last_trans_index = (neighbour*2) + 1
        #print("target_sentence(transform_string): ", target_sentence)
        #print("raw_sentence(transform_string): ", raw_sentence)

        if(model_type=="lstm"):

            for wi in range(neighbour):
                transformed_target_sentence_list.append(target_sentence[wi])
                #transformed_raw_target_sentence_list.append(raw_target_sentence[wi])

            for wi in range(neighbour):
                transformed_target_sentence_list.append(target_sentence[wi+1+neighbour])
                #transformed_raw_target_sentence_list.append(raw_target_sentence[wi+1+neighbour])

            transformed_target_sentence_list.append(target_sentence[neighbour])
            #transformed_raw_target_sentence_list.append(raw_target_sentence[neighbour])

            #-print("")
            #-print("transformed_target_sentence_list(transform_string): ", transformed_target_sentence_list)
            #-print("transformed_raw_target_sentence_list(transform_string): ", transformed_raw_target_sentence_list)
            #-print("")

            #print(transformed_target_sentence_list)
            #sequence_list.append(target_sentence)
            #sequence_list.append(transformed_target_sentence_list)
            transformed_sequence_list.append(transformed_target_sentence_list)
            transformed_raw_sequence_list.append(transformed_raw_target_sentence_list)

        elif(model_type=="func_lstm"):

            forward_target_sentence = []
            backward_target_sentence = []

            for wi in range(neighbour):
                forward_target_sentence.append(target_sentence[wi])
                backward_target_sentence.append(target_sentence[last_trans_index-1-wi])

            forward_target_sentence.append(target_sentence[neighbour])
            backward_target_sentence.append(target_sentence[neighbour])

            transformed_sequence_list.append(forward_target_sentence)
            transformed_sequence_list.append(backward_target_sentence)
            transformed_raw_sequence_list.append(forward_target_sentence)
            transformed_raw_sequence_list.append(backward_target_sentence)

        for wi in raw_target_sentence:
            transformed_raw_target_sentence_list.append(wi)

    return transformed_sequence_list, transformed_raw_sequence_list

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#2.5 - Function for User Side (Particle judge)

def judge_particles(first_suggestion, second_suggestion):

    for i in range(len(first_suggestion)):
        pass
        #@@print("first suggestion: \n", first_suggestion[i])
        #@@print("second suggestion: \n", second_suggestion[i])

    judge_count = len(first_suggestion)
    particle_count = len(first_suggestion[0])

    suggestion_particle_list = []

    list_correct_particle = [] #inside -> array of tuple (2 element)
    list_possible_correct_particle = [] #inside -> array of tuple (3 element)

    for h in range(judge_count):

        list_correct_particle.append([])
        list_possible_correct_particle.append([])

        for i in range(particle_count):

            first_correct_count = list(first_suggestion[h].values())[i]
            second_correct_count = list(second_suggestion[h].values())[i]
            particle = list(first_suggestion[0].keys())[i]

            if (first_correct_count >=3 ):
                list_correct_particle[h].append((particle, "high"))

        for i in range(particle_count):

            first_correct_count = list(first_suggestion[h].values())[i]
            second_correct_count = list(second_suggestion[h].values())[i]
            particle = list(first_suggestion[0].keys())[i]

            if ((second_correct_count + first_correct_count >=4) and (first_correct_count < 3)):
                list_correct_particle[h].append((particle, "medium"))
            elif ((second_correct_count + first_correct_count < 4) and (first_correct_count < 3)):
                list_possible_correct_particle[h].append((particle, second_correct_count + first_correct_count))

    #print("\n", list_correct_particle, "\n")
    #print(list_possible_correct_particle, "\n")

    return list_correct_particle, list_possible_correct_particle

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#3 - Train function (Evaluation function is in another section)

def train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit):

    #print("_identifier type, _neighbour: ", _identifier_type, _neighbour)

    global list_model_type
    flag_model_type = 0

    for model_type in list_model_type:
      if(_model_type == model_type):
        flag_model_type = 1
        break

    if(flag_model_type==0):
      print("Wrong model_type.\nAvailable model type: ", list_model_type)
      return



    global dict_total_particle
    global dict_total_ignored_particle

    global list_identifier
    global dict_total_identifier

    global dict_identifier_pattern

    dict_total_particle = {}
    dict_total_ignored_particle = {}

    list_identifier = []
    dict_total_identifier = {}

    dict_identifier_pattern = {}

    for i in list_target_particle:
        dict_total_particle[i] = 0
        dict_total_ignored_particle[i] = 0


    global identifier_type
    global neighbour
    global total_sentence
    global particle_limit

    identifier_type = _identifier_type

    identifier_name=""

    if(identifier_type==1):
        #print("identifier_type==1")
        identifier_name = "f" #first only
    elif(identifier_type==2):
        #print("identifier_type==2")
        identifier_name = "s" #second (and first)
    elif(identifier_type==3):
        identifier_name = "a" #all


    #print("identifier_name = ", identifier_name)

    neighbour = _neighbour
    total_sentence = _total_sentence
    particle_limit = _particle_limit

    return_flag = 0

    if(identifier_type<1 or identifier_type>3):
        print("identifier_type only accepts 1-3 (first identifier type, second identifier type, all identifier type")
        return_flag = 1

    if(neighbour<=0 or neighbour >=4):
        print("neighbour only accepts 1 to 3 neighbour")
        return_flag = 1

    if(return_flag==1):
        return None

    compile_raw(_train_name)
    print("_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit:")
    print("> ", _model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit)

    #---------VERSION OS
    '''
    import corpora_pos
    #from corpora_pos import training_jpn_pos
    #import content/gdrive/MyDrive/Preproccess Data/corpora_pos
    os.system("python content/gdrive/MyDrive/Preproccess Data/corpora_pos.py")
    my_module = reload(corpora_pos)
    #print(corpora_pos.training_jpn_pos)
    '''

    #---------VERSION without OS
    corpora_module = "corpora_pos" + "_" + _train_name
    corpora_pos = importlib.import_module(corpora_module)
    reload(corpora_pos)
    #print("> [corpora thingy!] \n", corpora_pos.training_jpn_pos)
    #print("\n> Yatta")

    cleaned = corpora_pos.training_jpn_pos
    token_sentence = []
    target_sequence = []
    token_word = []

    sentence_tokenizing(cleaned, token_sentence)

    for i in token_sentence:

        word_tokenizing(i, token_word)

    for i in token_word:

        if((i not in list_identifier) and (i not in list_target_particle)):
            list_identifier.append(i)
            dict_total_identifier[i] = 1

    for i in token_word:

        if(i not in list_target_particle):
            dict_total_identifier[i] += 1

    print("\n")

    for i in token_sentence:

        compile_target_sequence(i, target_sequence, _model_type)

        #for j in list_target_particle:

    print("\n")

    #4 lenght(word to be predicted) + 1 lenght(word for confirmation)
    train_len = 0
    target_forward_sequence = []
    target_backward_sequence = []

    if(_model_type=="lstm"):
      train_len = (neighbour*2)+1

    elif(_model_type=="func_lstm" or _model_type == "func_lstm_combined"):
      train_len = neighbour+1
      temp_target_sequence = []
      for i in range(len(target_sequence)):
        if(i%2==0):
          target_forward_sequence.append(target_sequence[i])
        else:
          target_backward_sequence.append(target_sequence[i])


    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(target_sequence)
    vocabulary_size = len(tokenizer.word_counts)+1 #sebenarnya ini setelah "sequences = tokenizer.texts_to_sequences(target_sequence)", tapi ku yakin aman

    info_tokenizer(tokenizer)

    sequences = []
    sequences_forw = []
    sequences_back = []

    n_sequences = []
    n_sequences_forw = []
    n_sequences_back = []

    train_inputs = []
    train_inputs_forw = []
    train_inputs_back = []

    train_targets = []

    seq_len = 0
    seq_len_forw = 0
    seq_len_back = 0

    if(_model_type=="lstm"):
      sequences = tokenizer.texts_to_sequences(target_sequence)

      n_sequences = np.empty([len(sequences),train_len], dtype='int32')

      for i in range(len(sequences)):
        n_sequences[i] = sequences[i]

      train_inputs = n_sequences[:,:-1]
      train_targets = n_sequences[:,-1]
      train_targets = to_categorical(train_targets, num_classes=vocabulary_size)

      seq_len = train_inputs.shape[1]

      #train_inputs.shape


    elif(_model_type=="func_lstm" or _model_type == "func_lstm_combined"):
      sequences_forw = tokenizer.texts_to_sequences(target_forward_sequence)
      sequences_back = tokenizer.texts_to_sequences(target_backward_sequence)

      n_sequences_forw = np.empty([len(sequences_forw),train_len], dtype='int32') #len for sequences_forw and sequences_back should be identical
      n_sequences_back = np.empty([len(sequences_back),train_len], dtype='int32')

      for i in range(len(sequences_forw)):
        n_sequences_forw[i] = sequences_forw[i]
        n_sequences_back[i] = sequences_back[i]

      train_inputs_forw = n_sequences_forw[:,:-1]
      train_inputs_back = n_sequences_back[:,:-1]
      train_targets = n_sequences_forw[:,-1]
      train_targets = to_categorical(train_targets, num_classes=vocabulary_size)

      seq_len_forw = train_inputs_forw.shape[1]
      seq_len_back = train_inputs_back.shape[1]

    print("-----Data preparation complete!-----\n")

    info_identifier()
    info_particle()
    info_pattern()

    #model = load_model("jpn_particle_transformed_model.h5")

    #'''

    var_history = ''

    if(_model_type == "lstm"):

      model = Sequential()
      model.add(Embedding(vocabulary_size, seq_len, input_length=seq_len))

      model.add(LSTM(50,return_sequences=True)) #LSTM Layer
      model.add(LSTM(50))
      model.add(Dense(50,activation='relu')) #Hidden Layer, maybe change to vocabulary_size?
      model.add(Dense(vocabulary_size, activation='softmax')) #Maybe try particle size instead? This is the output layer right....?
                                                            #Use len(list_target_particle)

      print(model.summary())
      # compile network
      model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

      #@#$%OLD MODEL.FIT???
      #model.fit(train_inputs,train_targets,epochs=500,verbose=0)

      #-plot_model(model, "lstm_model_input.png")
      var_history = model.fit(train_inputs,train_targets,epochs=500,verbose=0, validation_split=0.15)

    elif(_model_type == "func_lstm"): #THIS IS THE FIRST FUNC_LSTM, which use seperate LSTM :) .... does input_length not needed if we have Input()? and vice versa?

      #input 1 (1, 2) with output (3*)
      input_forw = Input(shape=(seq_len_forw,))
      embedding_forw = Embedding(vocabulary_size, seq_len_forw, input_length=seq_len_forw)(input_forw)
      lstm_forw_1 = LSTM(50,return_sequences=True)(embedding_forw)
      lstm_forw_2 = LSTM(50)(lstm_forw_1)

      #input 2(5,4) with output (3*)
      input_back = Input(shape=(seq_len_back,))
      embedding_back = Embedding(vocabulary_size, seq_len_back, input_length=seq_len_back)(input_back)
      lstm_back_1 = LSTM(50,return_sequences=True)(embedding_back)
      lstm_back_2 = LSTM(50)(lstm_back_1)

      concat = concatenate([lstm_forw_2, lstm_back_2])

      dense1 = Dense(50, activation="relu")(concat)
      output = Dense(vocabulary_size, activation="softmax")(dense1)

      input = [input_forw, input_back]

      model = Model(inputs=input, outputs=output, name="func_lstm_model")

      print(model.summary())
      model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

      #-plot_model(model, "func_lstm_model_input.png")

      var_history = model.fit([train_inputs_forw, train_inputs_back],train_targets,epochs=500,verbose=0, validation_split=0.15)



    elif(_model_type == "func_lstm_combined"): #Second FUNC_LSTM, which use same LSTM :) .... does input_length not needed if we have Input()? and vice versa?

      #input 1 (1, 2) with output (3*)
      input_forw = Input(shape=(seq_len_forw,))
      embedding_forw = Embedding(vocabulary_size, seq_len_forw, input_length=seq_len_forw)(input_forw)

      #input 2(5,4) with output (3*)
      input_back = Input(shape=(seq_len_back,))
      embedding_back = Embedding(vocabulary_size, seq_len_back, input_length=seq_len_back)(input_back)

      concat = concatenate([embedding_forw, embedding_back])

      lstm_1 = LSTM(50, return_sequences=True)(concat)
      lstm_2 = LSTM(50)(lstm_1)

      dense1 = Dense(50, activation="relu")(lstm_2)
      output = Dense(vocabulary_size, activation="softmax")(dense1)

      input = [input_forw, input_back]

      model = Model(inputs=input, outputs=output, name="func_lstm_combined_model")

      print(model.summary())
      model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

      #-plot_model(model, "func_lstm_combined_model_input.png")

      var_history = model.fit([train_inputs_forw, train_inputs_back],train_targets,epochs=500,verbose=0, validation_split=0.15)

      #this is for the application! :)
      #model.predict([np_2_gram_in,np_3_gram_in])

    plt.plot(var_history.history['accuracy'])
    plt.plot(var_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(var_history.history['loss'])
    plt.plot(var_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    model.save("Model/"+identifier_name+"_"+str(neighbour)+"_"+str(total_sentence)
               +"_"+str(particle_limit) +"_"+ _model_type + "_model.h5")

    tokenizer_json = tokenizer.to_json()

    with io.open('Model/'+identifier_name+'_'+str(neighbour)+'_'+str(total_sentence)
                 +'_'+str(particle_limit)+"_"+ _model_type +'_tokenizer.json', 'w', encoding='utf-8') as f:

        f.write(json.dumps(tokenizer_json, ensure_ascii=False))

    print("\n")
    #'''

    #print("identifier_type, neighbour, total_sentence, particle_limit: ", identifier_type, neighbour, total_sentence, particle_limit)
    print("first target sequence: ", target_sequence[0])
    print("\n-----Create model complete!----- Time now:", datetime.datetime.now(),"\n")

def cross_train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold):

    #print("_identifier type, _neighbour: ", _identifier_type, _neighbour)

    global list_model_type
    flag_model_type = 0

    for model_type in list_model_type:
      if(_model_type == model_type):
        flag_model_type = 1
        break

    if(flag_model_type==0):
      print("Wrong model_type.\nAvailable model type: ", list_model_type)
      return



    global dict_total_particle
    global dict_total_ignored_particle

    global list_identifier
    global dict_total_identifier

    global dict_identifier_pattern

    dict_total_particle = {}
    dict_total_ignored_particle = {}

    list_identifier = []
    dict_total_identifier = {}

    dict_identifier_pattern = {}

    for i in list_target_particle:
        dict_total_particle[i] = 0
        dict_total_ignored_particle[i] = 0


    global identifier_type
    global neighbour
    global total_sentence
    global particle_limit

    identifier_type = _identifier_type

    identifier_name=""

    if(identifier_type==1):
        #print("identifier_type==1")
        identifier_name = "f" #first only
    elif(identifier_type==2):
        #print("identifier_type==2")
        identifier_name = "s" #second (and first)
    elif(identifier_type==3):
        identifier_name = "a" #all


    #print("identifier_name = ", identifier_name)

    neighbour = _neighbour
    total_sentence = _total_sentence
    particle_limit = _particle_limit

    return_flag = 0

    if(identifier_type<1 or identifier_type>3):
        print("identifier_type only accepts 1-3 (first identifier type, second identifier type, all identifier type")
        return_flag = 1

    if(neighbour<=0 or neighbour >=4):
        print("neighbour only accepts 1 to 3 neighbour")
        return_flag = 1

    if(return_flag==1):
        return None

    compile_raw(_train_name)
    print("_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold:")
    print("> ", _model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)

    #---------VERSION OS
    '''
    import corpora_pos
    #from corpora_pos import training_jpn_pos
    #import content/gdrive/MyDrive/Preproccess Data/corpora_pos
    os.system("python content/gdrive/MyDrive/Preproccess Data/corpora_pos.py")
    my_module = reload(corpora_pos)
    #print(corpora_pos.training_jpn_pos)
    '''

    #---------VERSION without OS
    corpora_module = "corpora_pos" + "_" + _train_name
    corpora_pos = importlib.import_module(corpora_module)
    reload(corpora_pos)
    #print("> [corpora thingy!] \n", corpora_pos.training_jpn_pos)
    #print("\n> Yatta")

    cleaned = corpora_pos.training_jpn_pos
    token_sentence = []
    target_sequence = []
    token_word = []

    sentence_tokenizing(cleaned, token_sentence)

    for i in token_sentence:

        word_tokenizing(i, token_word)

    for i in token_word:

        if((i not in list_identifier) and (i not in list_target_particle)):
            list_identifier.append(i)
            dict_total_identifier[i] = 1

    for i in token_word:

        if(i not in list_target_particle):
            dict_total_identifier[i] += 1

    print("\n")

    for i in token_sentence:

        compile_target_sequence(i, target_sequence, _model_type)

        #for j in list_target_particle:

    print("\n")

    #4 lenght(word to be predicted) + 1 lenght(word for confirmation)
    train_len = 0
    target_forward_sequence = []
    target_backward_sequence = []

    if(_model_type=="lstm"):
      train_len = (neighbour*2)+1

    elif(_model_type=="func_lstm" or _model_type == "func_lstm_combined"):
      train_len = neighbour+1
      temp_target_sequence = []
      for i in range(len(target_sequence)):
        if(i%2==0):
          target_forward_sequence.append(target_sequence[i])
        else:
          target_backward_sequence.append(target_sequence[i])


    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(target_sequence)
    vocabulary_size = len(tokenizer.word_counts)+1 #sebenarnya ini setelah "sequences = tokenizer.texts_to_sequences(target_sequence)", tapi ku yakin aman

    info_tokenizer(tokenizer)

    sequences = []
    sequences_forw = []
    sequences_back = []

    n_sequences = []
    n_sequences_forw = []
    n_sequences_back = []

    train_inputs = []
    train_inputs_forw = []
    train_inputs_back = []

    train_targets = []

    seq_len = 0
    seq_len_forw = 0
    seq_len_back = 0

    var_history = ''

    #num_folds = 10 #changed to _fold in parameter
    acc_per_fold = []
    loss_per_fold = []
    model_per_fold = []
    sequence_per_fold = []
    tokenizer_per_fold = []
    var_history_per_fold = []

    #kfold = KFold(n_splits=num_folds, shuffle=True)
    #fold_no = 1

    if(_model_type=="lstm"):
      sequences = tokenizer.texts_to_sequences(target_sequence)

      n_sequences = np.empty([len(sequences),train_len], dtype='int32')

      for i in range(len(sequences)):
        n_sequences[i] = sequences[i]

      data_per_fold = int(len(n_sequences) / _fold)
      print("data_per_fold: ", data_per_fold, "\n")

      for k_fold in range(_fold):

        #cross_train_inputs = []
        #cross_train_targets = []
        cross_train_inputs = np.empty([0,train_len-1], dtype='int32')#np.empty([0,0], dtype='int32')
        cross_train_targets = np.empty([0], dtype='int32')
        cross_test_inputs = []
        cross_test_targets = []

        for n_fold in range(_fold):

          start_index_data = data_per_fold * n_fold
          end_index_data = data_per_fold * (n_fold+1) - 1

          if(n_fold != k_fold):
            cross_train_inputs = np.concatenate((cross_train_inputs, n_sequences[start_index_data:end_index_data+1, :-1]))
            cross_train_targets = np.concatenate((cross_train_targets, n_sequences[start_index_data:end_index_data+1, -1]))
          else:
            cross_test_inputs = n_sequences[start_index_data:end_index_data+1, :-1]
            cross_test_targets = n_sequences[start_index_data:end_index_data+1, -1]

        train_inputs = cross_train_inputs
        train_targets = to_categorical(cross_train_targets, num_classes=vocabulary_size)
        test_inputs = cross_test_inputs
        test_targets = to_categorical(cross_test_targets, num_classes=vocabulary_size)

        seq_len = train_inputs.shape[1]
        seq_len_test = test_inputs.shape[1]

        #train_inputs.shape

        print("-----Data preparation complete!-----\n")
        info_identifier()
        info_particle()
        info_pattern()
        #print(train_inputs[0])
        first_seq_debug = tokenizer.sequences_to_texts([test_inputs[0]])
        print("\nfirst test_inputs sequence: ", first_seq_debug)
        #print("ITS NOT HERE YET")
        #sequence_per_fold.append(target_sequence[0])
        sequence_per_fold.append(first_seq_debug)
        #print("cross_train_inputs len: ", len(cross_train_inputs))
        print("cross_train_targets len: ", len(cross_train_targets))
        #print("cross_test_inputs len: ", len(cross_test_inputs))
        print("cross_test_targets len: ", len(cross_test_targets))

        model = Sequential()
        model.add(Embedding(vocabulary_size, seq_len, input_length=seq_len))

        model.add(LSTM(50,return_sequences=True)) #LSTM Layer
        model.add(LSTM(50))
        model.add(Dense(50,activation='relu')) #Hidden Layer, maybe change to vocabulary_size?
        model.add(Dense(vocabulary_size, activation='softmax')) #Maybe try particle size instead? This is the output layer right....?
                                                              #Use len(list_target_particle)

        if(k_fold==0):
            print(model.summary())
        # compile network
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        #-plot_model(model, "lstm_model_input.png")
        # Generate a print
        print('------------------------------------------------------------------------')
        print(f'Training for fold {k_fold+1} ... \nTime fold now: {datetime.datetime.now()}')

        var_history = model.fit(train_inputs,train_targets,epochs=500,verbose=0, validation_split=0.10)

        #CONSTRUCTION - CONTINUE HERE
        #THIS IS ACTUALLY WHAT I NEED WHEN EVALUATING THINGS!
        # Generate generalization metrics
        #scores = model.evaluate(inputs[test], targets[test], verbose=0)
        scores = model.evaluate(test_inputs, test_targets, verbose=0)
        #print(f'\nScore for fold {k_fold+1}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
        acc_per_fold.append(scores[1] * 100)
        loss_per_fold.append(scores[0])
        model_per_fold.append(model)
        tokenizer_per_fold.append(tokenizer)
        var_history_per_fold.append(var_history)

        #print("identifier_type, neighbour, total_sentence, particle_limit: ", identifier_type, neighbour, total_sentence, particle_limit, "\n\n")

        # == Provide average scores ==

        #print('\tTest loss:', score[0])
        #print('\tTest accuracy:', score[1])
        #print('\tThis is model named: ', file_name)
        #THIS IS ACTUALLY WHAT I NEED WHEN EVALUATING THINGS!







    elif(_model_type=="func_lstm"):

      sequences_forw = tokenizer.texts_to_sequences(target_forward_sequence)
      sequences_back = tokenizer.texts_to_sequences(target_backward_sequence)

      n_sequences_forw = np.empty([len(sequences_forw),train_len], dtype='int32') #len for sequences_forw and sequences_back should be identical
      n_sequences_back = np.empty([len(sequences_back),train_len], dtype='int32')

      for i in range(len(sequences_forw)):
        n_sequences_forw[i] = sequences_forw[i]
        n_sequences_back[i] = sequences_back[i]

      data_per_fold = int(len(n_sequences_forw)/_fold)
      print("data_per_fold: ", data_per_fold, "\n")

      for k_fold in range(_fold):

        #cross_train_inputs = []
        #cross_train_targets = []
        cross_train_inputs_forw = np.empty([0,train_len-1], dtype='int32')#np.empty([0,0], dtype='int32')
        cross_train_inputs_back = np.empty([0,train_len-1], dtype='int32')#np.empty([0,0], dtype='int32')
        cross_train_targets = np.empty([0], dtype='int32')
        cross_test_inputs_forw = []
        cross_test_inputs_back = []
        cross_test_targets = []

        for n_fold in range(_fold):

          start_index_data = data_per_fold * n_fold
          end_index_data = data_per_fold * (n_fold+1) - 1

          if(n_fold != k_fold):
            cross_train_inputs_forw = np.concatenate((cross_train_inputs_forw, n_sequences_forw[start_index_data:end_index_data+1, :-1]))
            cross_train_inputs_back = np.concatenate((cross_train_inputs_back, n_sequences_back[start_index_data:end_index_data+1, :-1]))
            cross_train_targets = np.concatenate((cross_train_targets, n_sequences_forw[start_index_data:end_index_data+1, -1]))
          else:
            cross_test_inputs_forw = n_sequences_forw[start_index_data:end_index_data+1, :-1]
            cross_test_inputs_back = n_sequences_back[start_index_data:end_index_data+1, :-1]
            cross_test_targets = n_sequences_forw[start_index_data:end_index_data+1, -1]

        train_inputs_forw = cross_train_inputs_forw
        train_inputs_back = cross_train_inputs_back
        train_targets = to_categorical(cross_train_targets, num_classes=vocabulary_size)
        test_inputs_forw = cross_test_inputs_forw
        test_inputs_back = cross_test_inputs_back
        test_targets = to_categorical(cross_test_targets, num_classes=vocabulary_size)

        seq_len_forw = train_inputs_forw.shape[1]
        seq_len_back = train_inputs_back.shape[1]
        seq_len_test_forw = test_inputs_forw.shape[1]
        seq_len_test_back = test_inputs_back.shape[1]

        #train_inputs_forw = n_sequences_forw[:,:-1]
        #train_inputs_back = n_sequences_back[:,:-1]
        #train_targets = n_sequences_forw[:,-1]
        #train_targets = to_categorical(train_targets, num_classes=vocabulary_size)

        #seq_len_forw = train_inputs_forw.shape[1]
        #seq_len_back = train_inputs_back.shape[1]

        print("-----Data preparation complete!-----\n")
        info_identifier()
        info_particle()
        info_pattern()

        #sequence_per_fold.append(tokenizer.sequences_to_texts(train_inputs_forw[0]) + " " + tokenizer.sequences_to_texts(train_inputs_forw[1]))


        first_seq_debug = tokenizer.sequences_to_texts([test_inputs_forw[0]]) + tokenizer.sequences_to_texts([test_inputs_back[0]])
        print("\nfirst test_inputs sequence (forw and back): ", first_seq_debug)
        sequence_per_fold.append(first_seq_debug)
        #print("cross_train_inputs_forw len: ", len(cross_train_inputs_forw))
        #print("cross_train_inputs_back len: ", len(cross_train_inputs_back))
        print("cross_train_targets len: ", len(cross_train_targets))
        #print("cross_test_inputs_forw len: ", len(cross_test_inputs_forw))
        #print("cross_test_inputs_back len: ", len(cross_test_inputs_back))
        print("cross_test_targets len: ", len(cross_test_targets))

        #input 1 (1, 2) with output (3*)
        input_forw = Input(shape=(seq_len_forw,))
        embedding_forw = Embedding(vocabulary_size, seq_len_forw, input_length=seq_len_forw)(input_forw)
        lstm_forw_1 = LSTM(50,return_sequences=True)(embedding_forw)
        lstm_forw_2 = LSTM(50)(lstm_forw_1)

        #input 2(5,4) with output (3*)
        input_back = Input(shape=(seq_len_back,))
        embedding_back = Embedding(vocabulary_size, seq_len_back, input_length=seq_len_back)(input_back)
        lstm_back_1 = LSTM(50,return_sequences=True)(embedding_back)
        lstm_back_2 = LSTM(50)(lstm_back_1)

        concat = concatenate([lstm_forw_2, lstm_back_2])

        dense1 = Dense(50, activation="relu")(concat)
        output = Dense(vocabulary_size, activation="softmax")(dense1)

        input_ = [input_forw, input_back]

        model = Model(inputs=input_, outputs=output, name="func_lstm_model")

        if(k_fold==0):
            print(model.summary())
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        #-plot_model(model, "func_lstm_model_input.png")

        # Generate a print
        print('------------------------------------------------------------------------')
        print(f'Training for fold {k_fold+1} ... \nTime fold now: {datetime.datetime.now()}')

        var_history = model.fit([train_inputs_forw, train_inputs_back],train_targets,epochs=500,verbose=0, validation_split=0.10)

        scores = model.evaluate([test_inputs_forw, test_inputs_back], test_targets, verbose=0)
        #print(f'\nScore for fold {k_fold+1}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
        acc_per_fold.append(scores[1] * 100)
        loss_per_fold.append(scores[0])
        model_per_fold.append(model)
        tokenizer_per_fold.append(tokenizer)
        var_history_per_fold.append(var_history)

        print("identifier_type, neighbour, total_sentence, particle_limit: ", identifier_type, neighbour, total_sentence, particle_limit, "\n\n")

    elif(_model_type=="func_lstm_combined"):

      sequences_forw = tokenizer.texts_to_sequences(target_forward_sequence)
      sequences_back = tokenizer.texts_to_sequences(target_backward_sequence)

      n_sequences_forw = np.empty([len(sequences_forw),train_len], dtype='int32') #len for sequences_forw and sequences_back should be identical
      n_sequences_back = np.empty([len(sequences_back),train_len], dtype='int32')

      for i in range(len(sequences_forw)):
        n_sequences_forw[i] = sequences_forw[i]
        n_sequences_back[i] = sequences_back[i]

      data_per_fold = int(len(n_sequences_forw)/_fold)
      print("data_per_fold: ", data_per_fold, "\n")

      for k_fold in range(_fold):

        #cross_train_inputs = []
        #cross_train_targets = []
        cross_train_inputs_forw = np.empty([0,train_len-1], dtype='int32')#np.empty([0,0], dtype='int32')
        cross_train_inputs_back = np.empty([0,train_len-1], dtype='int32')#np.empty([0,0], dtype='int32')
        cross_train_targets = np.empty([0], dtype='int32')
        cross_test_inputs_forw = []
        cross_test_inputs_back = []
        cross_test_targets = []

        for n_fold in range(_fold):

          start_index_data = data_per_fold * n_fold
          end_index_data = data_per_fold * (n_fold+1) - 1

          if(n_fold != k_fold):
            cross_train_inputs_forw = np.concatenate((cross_train_inputs_forw, n_sequences_forw[start_index_data:end_index_data+1, :-1]))
            cross_train_inputs_back = np.concatenate((cross_train_inputs_back, n_sequences_back[start_index_data:end_index_data+1, :-1]))
            cross_train_targets = np.concatenate((cross_train_targets, n_sequences_forw[start_index_data:end_index_data+1, -1]))
          else:
            cross_test_inputs_forw = n_sequences_forw[start_index_data:end_index_data+1, :-1]
            cross_test_inputs_back = n_sequences_back[start_index_data:end_index_data+1, :-1]
            cross_test_targets = n_sequences_forw[start_index_data:end_index_data+1, -1]

        train_inputs_forw = cross_train_inputs_forw
        train_inputs_back = cross_train_inputs_back
        train_targets = to_categorical(cross_train_targets, num_classes=vocabulary_size)
        test_inputs_forw = cross_test_inputs_forw
        test_inputs_back = cross_test_inputs_back
        test_targets = to_categorical(cross_test_targets, num_classes=vocabulary_size)

        seq_len_forw = train_inputs_forw.shape[1]
        seq_len_back = train_inputs_back.shape[1]
        seq_len_test_forw = test_inputs_forw.shape[1]
        seq_len_test_back = test_inputs_back.shape[1]

      #train_inputs_forw = n_sequences_forw[:,:-1]
      #train_inputs_back = n_sequences_back[:,:-1]
      #train_targets = n_sequences_forw[:,-1]
      #train_targets = to_categorical(train_targets, num_classes=vocabulary_size)

      #seq_len_forw = train_inputs_forw.shape[1]
      #seq_len_back = train_inputs_back.shape[1]

        print("-----Data preparation complete!-----\n")
        info_identifier()
        info_particle()
        info_pattern()

        first_seq_debug = tokenizer.sequences_to_texts([test_inputs_forw[0]]) + tokenizer.sequences_to_texts([test_inputs_back[0]])
        print("\nfirst test_inputs sequence (forw and back): ", first_seq_debug)
        sequence_per_fold.append(first_seq_debug)
        #print("cross_train_inputs_forw len: ", len(cross_train_inputs_forw))
        #print("cross_train_inputs_back len: ", len(cross_train_inputs_back))
        print("cross_train_targets len: ", len(cross_train_targets))
        #print("cross_test_inputs_forw len: ", len(cross_test_inputs_forw))
        #print("cross_test_inputs_back len: ", len(cross_test_inputs_back))
        print("cross_test_targets len: ", len(cross_test_targets))

        #input 1 (1, 2) with output (3*)
        input_forw = Input(shape=(seq_len_forw,))
        embedding_forw = Embedding(vocabulary_size, seq_len_forw, input_length=seq_len_forw)(input_forw)

        #input 2(5,4) with output (3*)
        input_back = Input(shape=(seq_len_back,))
        embedding_back = Embedding(vocabulary_size, seq_len_back, input_length=seq_len_back)(input_back)

        concat = concatenate([embedding_forw, embedding_back])

        lstm_1 = LSTM(50, return_sequences=True)(concat)
        lstm_2 = LSTM(50)(lstm_1)

        dense1 = Dense(50, activation="relu")(lstm_2)
        output = Dense(vocabulary_size, activation="softmax")(dense1)

        input_ = [input_forw, input_back]

        model = Model(inputs=input_, outputs=output, name="func_lstm_combined_model")

        if(k_fold==0):
            print(model.summary())

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        #-plot_model(model, "func_lstm_combined_model_input.png")

        # Generate a print
        print('------------------------------------------------------------------------')
        print(f'Training for fold {k_fold+1} ... \nTime fold now: {datetime.datetime.now()}')

        var_history = model.fit([train_inputs_forw, train_inputs_back],train_targets,epochs=500,verbose=0, validation_split=0.10)

        scores = model.evaluate([test_inputs_forw, test_inputs_back], test_targets, verbose=0)
        #print(f'\nScore for fold {k_fold+1}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
        acc_per_fold.append(scores[1] * 100)
        loss_per_fold.append(scores[0])
        model_per_fold.append(model)
        tokenizer_per_fold.append(tokenizer)
        var_history_per_fold.append(var_history)

        print("identifier_type, neighbour, total_sentence, particle_limit: ", identifier_type, neighbour, total_sentence, particle_limit, "\n\n")
      #this is for the application! :)
      #model.predict([np_2_gram_in,np_3_gram_in])

    #model = load_model("jpn_particle_transformed_model.h5")

    #'''
    print("_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold:")
    print("> ", _model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)
    print('------------------------------------------------------------------------')
    print('Score per fold')
    for i in range(0, len(acc_per_fold)):
      print('------------------------------------------------------------------------')
      print(f'> Fold {i+1} - Loss: {loss_per_fold[i]} - Accuracy: {acc_per_fold[i]}%')
      print(f'> First sequence [{i}]: {sequence_per_fold[i]}\n')
      print(f'> Model {i+1} - Loss Model: {var_history_per_fold[i].history["loss"][-1]} - Accuracy Model: {var_history_per_fold[i].history["accuracy"][-1]*100}%')   
    print('------------------------------------------------------------------------')
    print('Average scores for all folds:')
    print(f'> Accuracy: {np.mean(acc_per_fold)} (+- {np.std(acc_per_fold)})')
    print(f'> Loss: {np.mean(loss_per_fold)}')
    print('------------------------------------------------------------------------')

    #manual way to pick model
    input_model_save = 0

    #while(input_model_save<=0 or input_model_save >= _fold+1):
    #  input_model_save = int(input("Pick model to save: "))
    #input_model_save -= 1

    #auto way to pick model
    max_acc = 0

    for i in range(0, len(acc_per_fold)):
        if(max_acc < acc_per_fold[i]):
          max_acc = acc_per_fold[i]
          input_model_save = i

    print("\n")
    model = model_per_fold[input_model_save]
    tokenizer = tokenizer_per_fold[input_model_save]
    var_history = var_history_per_fold[input_model_save]
    print("model_per_fold len [Total Model/Fold]: ", len(model_per_fold))
    print("input_model_save [Model # saved, but array]: ", input_model_save)
    print("type of model: ", type(model))
    #scores = model.evaluate(test_inputs, test_targets, verbose=0)
    print(f'Score for fold {input_model_save+1}: {model.metrics_names[0]} of ???; {model.metrics_names[1]} of ???%')
    print(f'Score for model {input_model_save+1}: Loss [{var_history.history["loss"][-1]}] ; Accuracy [{var_history.history["accuracy"][-1]*100}%]')
        


    #model.save("/content/gdrive/MyDrive/Model/"+identifier_name+"_"+str(neighbour)+"_"+str(total_sentence)
    model.save("Model/"+identifier_name+"_"+str(neighbour)+"_"+str(total_sentence)
               +"_"+str(particle_limit) +"_"+ _model_type + "_model.h5")

    tokenizer_json = tokenizer.to_json()

    #with io.open('/content/gdrive/MyDrive/Model/'+identifier_name+'_'+str(neighbour)+'_'+str(total_sentence)
    with io.open('Model/'+identifier_name+'_'+str(neighbour)+'_'+str(total_sentence)
                 +'_'+str(particle_limit)+"_"+ _model_type +'_tokenizer.json', 'w', encoding='utf-8') as f:

        f.write(json.dumps(tokenizer_json, ensure_ascii=False))

    plt.plot(var_history.history['accuracy'])
    plt.plot(var_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(var_history.history['loss'])
    plt.plot(var_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    print("\n")
    #'''
    print("-----Create model complete!----- Time now: ", datetime.datetime.now(),"\n")

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#4 - Evaluation function (actually don't forget the newly added validation_split=0.2 in model.fit)

'''
def model_test(s_index, e_index):

    #print("_identifier type, _neighbour: ", _identifier_type, _neighbour)

    model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = get_model()

    global dict_total_particle
    global dict_total_ignored_particle

    global list_identifier
    global dict_total_identifier

    global dict_identifier_pattern

    global identifier_type
    global neighbour
    global total_sentence
    global particle_limit
    particle_limit = 1000000

    #x#identifier_type = _identifier_type

    #print("identifier_name = ", identifier_name)

    #x#neighbour = _neighbour
    #x#total_sentence = _total_sentence
    #x#particle_limit = _particle_limit

    identifier_type = 1
    identifier_name = "f"
    compile_raw_alt(s_index, e_index, "_evaluate_f")

    identifier_type = 2
    identifier_name = "s"
    compile_raw_alt(s_index, e_index, "_evaluate_s")

    identifier_type = 3
    identifier_name = "a"
    compile_raw_alt(s_index, e_index, "_evaluate_a")

    for ix in range(len(model_list)):

            #i=1

            model = model_list[ix]
            tokenizer = tokenizer_list[ix]
            neighbour = neighbour_list[ix]
            identifier = identifier_list[ix]
            identifier_type = identifier_list[ix]
            file_name = file_name_list[ix]
            model_type = model_type_list[ix]

            my_module = ''

            dict_total_particle = {}
            dict_total_ignored_particle = {}

            list_identifier = []
            dict_total_identifier = {}

            dict_identifier_pattern = {}

            for i in list_target_particle:
                dict_total_particle[i] = 0
                dict_total_ignored_particle[i] = 0

    #from corpora_pos import training_jpn_pos

            cleaned = ''

            if(identifier==1):
                import corpora_pos_evaluate_f
                print("loaded corpora: corpora_pos_evaluate_f")
                my_module = reload(corpora_pos_evaluate_f)
                cleaned = corpora_pos_evaluate_f.training_jpn_pos
            elif(identifier==2):
                import corpora_pos_evaluate_s
                print("loaded corpora: corpora_pos_evaluate_s")
                my_module = reload(corpora_pos_evaluate_s)
                cleaned = corpora_pos_evaluate_s.training_jpn_pos
    #print(corpora_pos.training_jpn_pos)


            token_sentence = []
            target_sequence = []
            token_word = []

            sentence_tokenizing(cleaned, token_sentence)

            for i in token_sentence:

                word_tokenizing(i, token_word)

            for i in token_word:

                if((i not in list_identifier) and (i not in list_target_particle)):
                    list_identifier.append(i)
                    dict_total_identifier[i] = 1

            for i in token_word:

                if(i not in list_target_particle):
                    dict_total_identifier[i] += 1

            print("len dict_total_identifier: ", len(dict_total_identifier))
            info_identifier()

            #print("\n")

            for i in token_sentence:

                compile_target_sequence(i, target_sequence, _model_type)

                #for j in list_target_particle:

            print("\n")

            #4 lenght(word to be predicted) + 1 lenght(word for confirmation)
            train_len = (neighbour*2)+1

            print("\nTokenizer.word_index:\n", tokenizer.word_index)

            #tokenizer = Tokenizer()
            #tokenizer.fit_on_texts(target_sequence)
            sequences = tokenizer.texts_to_sequences(target_sequence)

            testing_seq = np.array(sequences)
            print("sequences shape test: ", testing_seq.shape, testing_seq[0])
            deleted_sequence = 0

            for i in range(len(testing_seq)):
              if(len(testing_seq[i])!=train_len):
                print("Outlier: ", testing_seq[i])
                sequences.remove(sequences[i-deleted_sequence])
                deleted_sequence+=1

            vocabulary_size = len(tokenizer.word_counts)+1

            n_sequences = np.empty([len(sequences),train_len], dtype='int32')

            for i in range(len(sequences)):
                n_sequences[i] = sequences[i]
                #shape(3,)      #shape(2,)
                #or actually add TRY AND CATCH HERE, and we forfeit the "for i in range(len(testing_seq)):" thingy

            print("n_sequences shape test: ", n_sequences.shape, n_sequences[0])

            print("n_sequences[0], n_sequences[1]: ", n_sequences[0], n_sequences[1])
            eval_inputs = n_sequences[:,:-1]
            eval_targets = n_sequences[:,-1]
            print("eval_targets[0], eval_targets[1] before: ", eval_targets[0], eval_targets[1])
            eval_targets = to_categorical(eval_targets, num_classes=vocabulary_size)
            print("vocabulary_size: ", vocabulary_size)

            seq_len = eval_inputs.shape[1]

            print("eval_inputs.shape: \n", eval_inputs.shape)
            print("eval_inputs: \n", eval_inputs)
            print("eval_targets: \n", eval_targets)
            print("eval_targets_.shape: \n", eval_targets.shape)
            print("eval_targets[0], eval_targets[1]: \n", eval_targets[0], eval_targets[1])



            print("-----Data preparation complete!-----\n")

            info_identifier()
            info_particle()
            info_pattern()

            #THIS IS ACTUALLY WHAT I NEED WHEN EVALUATING THINGS!
            #model = load_model(model_path)
            score = model.evaluate(eval_inputs, eval_targets, verbose=0)
            #score = model.evaluate(X_test, y_test, verbose=0)
            print('\tTest loss:', score[0])
            print('\tTest accuracy:', score[1])
            print('\tThis is model named: ', file_name)
            #THIS IS ACTUALLY WHAT I NEED WHEN EVALUATING THINGS!

            print("identifier_type, neighbour, total_sentence, particle_limit: ", identifier_type, neighbour)
            print("first target sequence: ", target_sequence[0])
            print("\n-----Create model complete!-----\n")
'''

def app_test(s_index, e_index, train_name): #evaluating the app, by combining the 6 model or so :)

    model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = get_model()

    global identifier_type

    global particle_limit
    particle_limit = 1000000

    identifier_type = 1
    identifier_name = "f"
    _train_name = "_evaluate_" + train_name
    compile_raw_alt(s_index, e_index, _train_name)
    '''
    identifier_type = 2
    identifier_name = "s"
    compile_raw_alt(s_index, e_index, "_evaluate_s")

    identifier_type = 3
    identifier_name = "a"
    compile_raw_alt(s_index, e_index, "_evaluate_a")
    '''

    stop_flag_lel = False

    while (not stop_flag_lel):

        stop_flag_lel = True

        my_module = ''

        cleaned = ''

        #import corpora_evaluate_f
        #reload(corpora_evaluate_f)
        #cleaned = corpora_evaluate_f.training_jpn

        corpora_module = "corpora_evaluate" + "_" + train_name
        corpora_pos = importlib.import_module(corpora_module)
        reload(corpora_pos)
        cleaned = corpora_pos.training_jpn

        #print(corpora_pos.training_jpn_pos)

        token_sentence = []
        #target_sequence = []
        #token_word = []

        sentence_tokenizing(cleaned, token_sentence)

        token_sentence = token_sentence[1:]

        #print(token_sentence[0]+"wut")
        #print(token_sentence[1]+"\n", token_sentence[2])
        print(len(token_sentence))
        #print("\nInput: ", end="")
        #input_text = input().strip()

        #if(input_text=="exit"):
        #    break

        correct_handan = 0
        incorrect_handan = 0
        low_prio_handan = 0
        no_particle_count = 0

        for input_text in token_sentence:

            #print("loop for input_text: ", input_text, "\n")

            particle_exists = 0
            first_suggestion_particle = []
            second_suggestion_particle = []

            for i in range(len(model_list)):

                model = model_list[i]
                tokenizer = tokenizer_list[i]
                neighbour = neighbour_list[i]
                identifier = identifier_list[i]
                file_name = file_name_list[i]
                model_type = model_type_list[i]

                transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

                no_particle_flag = 0

                if(particle_exists==0):
                    print("---No particle was found---\n>", transformed_raw_input_text, "\n")
                    #print("Partile List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                    no_particle_flag = 1
                    no_particle_count += 1
                    break

                list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

                target_number=0
                i_target_text=0

                for i_index in range(len(list_transformed_input_text)):

                    if(i_target_text>=len(list_transformed_input_text)):
                        break       

                    if(model_type == "lstm"):       

                        target_text = list_transformed_input_text[i_target_text]      

                        encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                        pad_encoded = pad_sequences([encoded_text], truncating='pre')

                        i_target_text+=1
                    
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                        target_text_forw = list_transformed_input_text[i_target_text]
                        target_text_back = list_transformed_input_text[i_target_text+1]

                        print("Inside the target_text_forw: ", target_text_forw)
                        print("Inside the target_text_back: ", target_text_back)
                        print("What if we do this to forw: ", ' '.join(target_text_forw[0:-1]))
                        print("What if we do this to back: ", ' '.join(target_text_back[0:-1]))
                        encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                        encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                        #pad_encoded = pad_sequences([encoded_text_forw, encoded_text_back], truncating='pre')
                        pad_encoded_forw = pad_sequences([encoded_text_forw], truncating='pre')
                        pad_encoded_back = pad_sequences([encoded_text_back], truncating='pre')

                        i_target_text+=2

                    '''
                    for wox in (list_transformed_raw_input_text[target_number]):

                        if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                            pass
                            #@@print("[", wox, "] ", end="")
                        else:
                            pass
                            #@@print(wox, " ", end="")
                    '''



                    #print("")
                    target_number += 1

                    suggestion_number=1

                    if(model_type == "lstm"):  
                        len_list_transformed_input_text = len(list_transformed_input_text)
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                        len_list_transformed_input_text = len(list_transformed_input_text)/2

                    if(len(first_suggestion_particle)!=len_list_transformed_input_text):
                        first_suggestion_particle.append({})
                        second_suggestion_particle.append({})

                        for p in list_target_particle:

                            first_suggestion_particle[target_number-1][p] = 0
                            second_suggestion_particle[target_number-1][p] = 0

                    skip_ayam = 0

                    #CHECK THIS ONE LATER OKE!
                    #CHECK THIS ONE LATER OKE!
                    #CHECK THIS ONE LATER OKE!
                    #CHECK THIS ONE LATER OKE!
                    #CHECK THIS ONE LATER OKE!
                    #CHECK THIS ONE LATER OKE!
                    #CHECK WHAT HAPPEN INSIDE THE THINGY

                    if(model_type == "lstm"):  

                        for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:

                            pred_word = tokenizer.index_word[i]

                        
                            try:
                                if(suggestion_number==1):
                                    first_suggestion_particle[target_number-1][pred_word] += 1
                                elif(suggestion_number==2):
                                    second_suggestion_particle[target_number-1][pred_word] += 1
                            except:
                                skip_ayam = 1
                                print("SOMETHING WAS EXPECTED! ", pred_word)

                            suggestion_number += 1

                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                        for i in (model.predict([pad_encoded_forw, pad_encoded_back], verbose=0)[0]).argsort()[-3:][::-1]:

                            pred_word = tokenizer.index_word[i]

                        
                            try:
                                if(suggestion_number==1):
                                    first_suggestion_particle[target_number-1][pred_word] += 1
                                elif(suggestion_number==2):
                                    second_suggestion_particle[target_number-1][pred_word] += 1
                            except:
                                skip_ayam = 1
                                print("SOMETHING WAS EXPECTED: ", pred_word)

                            suggestion_number += 1

                    if(skip_ayam==1):
                        continue

                        

            if(no_particle_flag == 1):
                continue

            list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)

            particle_correct = []
            unchanged_marked_input_text = marked_input_text

            for h in range(len(list_correct_particle)):

                particle_correct.append(False)

                for i in range(len(marked_input_text)):

                    if(marked_input_text[i][1] == 1):

                        for particle in list_correct_particle[h]:

                            if(particle[0] == marked_input_text[i][0]):
                                particle_correct[h] = True
                                break

                        marked_input_text[i] = (marked_input_text[i][0], 2)
                        break

            #$%^print("-----Original Sentence-----")
            #$%^for token in unchanged_marked_input_text:
                #$%^if(token[1]==2):
                    #$%^print("[", token[0], "]", end="")
                #$%^else:
                    #$%^print(token[0], end="")

            #$%^print("\n\n-----Corrected Sentence-----")

            p_n = 0
            string_suggestion = [""]
            corrected_sentence = ""
            clean_corrected_sentence = ""
            final_particle = []

            ignore_low_prio = False

            for token in unchanged_marked_input_text:

                #correct particle [this is wrong]
                if(token[1]==2 and p_n<len(list_correct_particle)):


                    #correct particle
                    if(particle_correct[p_n]):
                        correct_handan += 1
                        #$%^print("[", token[0], "]", end="")
                        corrected_sentence += "[" + token[0] + "]"
                        clean_corrected_sentence += token[0]

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(token[0]==list_correct_particle[p_n][n][0]):
                                fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                                final_particle.append(fp)

                            if(len(list_correct_particle[p_n])>1):
                                if(n==0):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(list_correct_particle[p_n][n][0]!=token[0]):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                    #wrong particle (but there are suggestion)
                    elif(len(list_correct_particle[p_n]) != 0):

                        incorrect_handan += 1

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(len(list_correct_particle[p_n])!=0):
                                if(n==1):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(n!=0):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                                if(n==0):
                                    #$%^print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                    corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                    clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                    fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                    #final_particle.append(list_correct_particle[p_n][0][0])
                                    final_particle.append(fp)

                    else:
                        ignore_low_prio = True
                        low_prio_handan += 1
                        #$%^print("#########LOW PRIO DETECTED##########", end="")

                    #wrong particle (no suggestion, only low prio)
                    #@@#@@#@@else:
                        #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")


                    p_n += 1

                    if(p_n < len(list_correct_particle)):
                        string_suggestion.append("")

                else:
                    #$%^print(token[0], end="")
                    corrected_sentence += token[0]
                    clean_corrected_sentence += token[0]

            #$%^print("\n")

            if(ignore_low_prio):
                continue

            #$%^for i in range(len(list_correct_particle)):
                #$%^print("\t", final_particle[i])
                #$%^if(len(string_suggestion[i])==0):
                    #$%^print( "\tNo other suggestion\n")
                #$%^else:
                    #$%^print(string_suggestion[i])

            '''
            translator = Translator()
            translation = translator.translate(clean_corrected_sentence)
            print("\nTranslation: ", translation.text, "\n")
            '''

        #total_handan = correct_handan + incorrect_handan + low_prio_handan

        total_handan = correct_handan + incorrect_handan + low_prio_handan
        correct_acc = round(correct_handan/total_handan*100, 2)
        incorrect_acc = round(incorrect_handan/total_handan*100, 2)
        low_prio_acc = round(low_prio_handan/total_handan*100, 2)

        time_now = datetime.datetime.now()

        print(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}')
        print(f'Name of model: {file_name_list}')
        print(f'Correct Judgement: {correct_handan} ({correct_acc}%)')
        print(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)')
        print(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')

        #correct_handan_list.append(correct_handan)
        #incorrect_handan_list.append(incorrect_handan)
        #low_prio_list.append(low_prio_handan)

        #correct_acc_list.append(correct_acc)
        #incorrect_acc_list.append(incorrect_acc)
        #low_prio_acc_list.append(low_prio_acc)

        file_acc_name = "app_test_acc_" + train_name + ".txt"

        file_acc_handan = open(file_acc_name, "a", encoding='utf8')
        file_acc_handan.write(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}------\n')
        file_acc_handan.write("--------------------------------\n")
        file_acc_handan.write(f'Name of model: {file_name_list}\n\n')

        for ihan in file_name_list:
            file_acc_handan.write(ihan + "\n")

        file_acc_handan.write(f'\nCorrect Judgement: {correct_handan} ({correct_acc}%)\n')
        file_acc_handan.write(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)\n')
        file_acc_handan.write(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')
        file_acc_handan.write("--------------------------------\n\n")

        file_acc_handan.close()

def backup_revert_but_sad_app_test(s_index, e_index, train_name): #evaluating the app, by combining the 6 model or so :)

    model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = get_model()

    global identifier_type

    global particle_limit
    particle_limit = 1000000

    identifier_type = 1
    identifier_name = "f"
    _train_name = "_evaluate_" + train_name
    compile_raw_alt(s_index, e_index, _train_name)

    '''
    identifier_type = 2
    identifier_name = "s"
    compile_raw_alt(s_index, e_index, "_evaluate_s")

    identifier_type = 3
    identifier_name = "a"
    compile_raw_alt(s_index, e_index, "_evaluate_a")
    '''
    correct_handan_list = []
    incorrect_handan_list = []
    low_prio_list = []

    correct_acc_list = []
    incorrect_acc_list = []
    low_prio_acc_list = []

    total_model = len(model_list)
    if(total_model!=6):
        print("ERROR: Your model file count is not 6")
        return

    #cleaned = ''

    corpora_module = "corpora_evaluate" + "_" + train_name
    corpora_pos = importlib.import_module(corpora_module)
    reload(corpora_pos)

    cleaned = corpora_pos.training_jpn

    #import corpora_evaluate_f
    #reload(corpora_evaluate_f)
    #cleaned = corpora_evaluate_f.training_jpn

    #print(corpora_pos.training_jpn_pos)

    token_sentence = []
    #target_sequence = []
    #token_word = []

    sentence_tokenizing(cleaned, token_sentence)

    token_sentence = token_sentence[1:]

    #print(token_sentence[0]+"wut")
    #print(token_sentence[1]+"\n", token_sentence[2])
    print("How many token_sentence: ", len(token_sentence))
    #print("\nInput: ", end="")
    #input_text = input().strip()

    #if(input_text=="exit"):
    #    break

    '''

    all_combination_model = itertools.combinations(full_model_list, 6)
    all_combination_tokenizer = itertools.combinations(full_tokenizer_list, 6)
    all_combination_neighbour = itertools.combinations(full_neighbour_list, 6)
    all_combination_identifier = itertools.combinations(full_identifier_list, 6)
    all_combination_file_name = itertools.combinations(full_file_name_list, 6)
    all_combination_model_type = itertools.combinations(full_model_type_list, 6)

    #i_want_to_shuffle = (all_combination_model, all_combination_tokenizer, all_combination, neighbour)

    all_model_list=[]
    all_tokenizer_list=[]
    all_neighbour_list=[]
    all_identifier_list=[]
    all_file_name_list=[]
    all_model_type_list=[]

    for temp_model_list in all_combination_model:
        all_model_list.append(temp_model_list)

    for temp_tokenizer_list in all_combination_tokenizer:
        all_tokenizer_list.append(temp_tokenizer_list)

    for temp_neighbour_list in all_combination_neighbour:
        all_neighbour_list.append(temp_neighbour_list)

    for temp_identifier_list in all_combination_identifier:
        all_identifier_list.append(temp_identifier_list)

    for temp_file_name_list in all_combination_file_name:
        all_file_name_list.append(temp_file_name_list)

    for temp_model_type_list in all_combination_model_type:
        all_model_type_list.append(temp_model_type_list)

    '''

    
    
    #for temp_model_list in all_combination_model:
    #for i_combination in range(len(all_model_list)):
    for i_combination in range(0,1):

        #model_list = all_model_list[i_combination]
        #tokenizer_list = all_tokenizer_list[i_combination]
        #neighbour_list = all_neighbour_list[i_combination]
        #identifier_list = all_identifier_list[i_combination]
        #file_name_list = all_file_name_list[i_combination]
        #model_type_list = all_model_type_list[i_combination]

        #skip_flag_train_name = False

        #alter10000 -> 250000 260000
        #alt10000 -> 200000 210000
        #alt_x_10000 -> 350000 360000
        #alt_150000_10000 -> 150000 160000

        #if(train_name == "alt10000" or train_name == "alter10000" or train_name == "alt_x_10000" or train_name == "alt_150000_10000"):
        #    for model_type_thing in model_type_list:
        #        if(model_type_thing!="lstm"):
        #            skip_flag_train_name = True
        #            break

        #if(skip_flag_train_name):
        #    continue



        correct_handan = 0
        incorrect_handan = 0
        low_prio_handan = 0
        no_particle_count = 0

        for input_text in token_sentence:

            #print("loop for input_text: ", input_text, "\n")

            particle_exists = 0
            first_suggestion_particle = []
            second_suggestion_particle = []

            for i in range(len(model_list)):

                model = model_list[i]
                tokenizer = tokenizer_list[i]
                neighbour = neighbour_list[i]
                identifier = identifier_list[i]
                file_name = file_name_list[i]
                model_type = model_type_list[i]

                transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

                no_particle_flag = 0

                if(particle_exists==0):
                    print("---No particle was found---\n>", transformed_raw_input_text, "\n")
                    #print("Partile List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                    no_particle_flag = 1
                    no_particle_count += 1
                    break

                list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

                target_number=0
                i_target_text=0

                #info_tokenizers(tokenizer)

                for i_index in range(len(list_transformed_input_text)):

                    if(i_target_text>=len(list_transformed_input_text)):
                        break       

                    if(model_type == "lstm"):       

                        target_text = list_transformed_input_text[i_target_text]      

                        encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                        pad_encoded = pad_sequences([encoded_text], truncating='pre')

                        i_target_text+=1
                    
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                        target_text_forw = list_transformed_input_text[i_target_text]
                        target_text_back = list_transformed_input_text[i_target_text+1]

                        encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                        encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                        pad_encoded_forw = pad_sequences([encoded_text_forw], truncating='pre')
                        pad_encoded_back = pad_sequences([encoded_text_back], truncating='pre')

                        i_target_text+=2

                    '''
                    for wox in (list_transformed_raw_input_text[target_number]):

                        if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                            pass
                            #@@print("[", wox, "] ", end="")
                        else:
                            pass
                            #@@print(wox, " ", end="")
                    '''

                    #print("")
                    target_number += 1

                    suggestion_number=1

                    if(model_type == "lstm"):  
                        len_list_transformed_input_text = len(list_transformed_input_text)
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                        len_list_transformed_input_text = len(list_transformed_input_text)/2

                    if(len(first_suggestion_particle)!=len_list_transformed_input_text):
                        first_suggestion_particle.append({})
                        second_suggestion_particle.append({})

                        for p in list_target_particle:

                            first_suggestion_particle[target_number-1][p] = 0
                            second_suggestion_particle[target_number-1][p] = 0

                    try:
                        if(model_type=="lstm"):
                            predict_list = model.predict(pad_encoded, verbose=0)[0]
                        elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                            predict_list = model.predict([pad_encoded_forw, pad_encoded_back], verbose=0)[0]
                    except:
                        print("something goes wrong, pad_encoded")
                        continue

                    #print("inside the predict_list with model type [", model_type, "]: ", predict_list)

                    '''
                    predict_listo = []
                    
                    for i_plist in predict_list.argsort()[-25:][::-1]:
                        try:
                            pred_word = tokenizer.index_word[i_plist]
                            predict_listo.append(pred_word)
                        except:
                            continue
                    
                        
                    print("the predict_list [", len(predict_listo), "]: ", predict_listo)
                    '''

                    skip_ayam = 0

                    for i_plist in predict_list.argsort()[-3:][::-1]:
                    #for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:

                        pred_word = tokenizer.index_word[i_plist]
                        #print("the pred_word: ", pred_word)

                        try:
                            if(suggestion_number==1):
                                first_suggestion_particle[target_number-1][pred_word] += 1
                            elif(suggestion_number==2):
                                second_suggestion_particle[target_number-1][pred_word] += 1
                        except:
                            skip_ayam = 1
                            print("SOMETHING WAS EXPECTED! (second_suggestion_particle_thingy)")

                    if(skip_ayam==1):
                        continue


                        suggestion_number += 1


            if(no_particle_flag == 1):
                continue

            list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)

            particle_correct = []
            unchanged_marked_input_text = marked_input_text

            for h in range(len(list_correct_particle)):

                particle_correct.append(False)

                for i in range(len(marked_input_text)):

                    if(marked_input_text[i][1] == 1):

                        for particle in list_correct_particle[h]:

                            if(particle[0] == marked_input_text[i][0]):
                                particle_correct[h] = True
                                break

                        marked_input_text[i] = (marked_input_text[i][0], 2)
                        break

            #$%^print("-----Original Sentence-----")
            #$%^for token in unchanged_marked_input_text:
                #$%^if(token[1]==2):
                    #$%^print("[", token[0], "]", end="")
                #$%^else:
                    #$%^print(token[0], end="")

            #$%^print("\n\n-----Corrected Sentence-----")

            p_n = 0
            string_suggestion = [""]
            corrected_sentence = ""
            clean_corrected_sentence = ""
            final_particle = []

            ignore_low_prio = False

            for token in unchanged_marked_input_text:

                #correct particle [this is wrong]
                if(token[1]==2 and p_n<len(list_correct_particle)):


                    #correct particle
                    if(particle_correct[p_n]):
                        correct_handan += 1
                        #$%^print("[", token[0], "]", end="")
                        corrected_sentence += "[" + token[0] + "]"
                        clean_corrected_sentence += token[0]

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(token[0]==list_correct_particle[p_n][n][0]):
                                fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                                final_particle.append(fp)

                            if(len(list_correct_particle[p_n])>1):
                                if(n==0):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(list_correct_particle[p_n][n][0]!=token[0]):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                    #wrong particle (but there are suggestion)
                    elif(len(list_correct_particle[p_n]) != 0):

                        incorrect_handan += 1

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(len(list_correct_particle[p_n])!=0):
                                if(n==1):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(n!=0):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                                if(n==0):
                                    #$%^print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                    corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                    clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                    fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                    #final_particle.append(list_correct_particle[p_n][0][0])
                                    final_particle.append(fp)

                    else:
                        ignore_low_prio = True
                        low_prio_handan += 1
                        #$%^print("#########LOW PRIO DETECTED##########", end="")

                    #wrong particle (no suggestion, only low prio)
                    #@@#@@#@@else:
                        #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")


                    p_n += 1

                    if(p_n < len(list_correct_particle)):
                        string_suggestion.append("")

                else:
                    #$%^print(token[0], end="")
                    corrected_sentence += token[0]
                    clean_corrected_sentence += token[0]

            #$%^print("\n")

            if(ignore_low_prio):
                continue

            #$%^for i in range(len(list_correct_particle)):
                #$%^print("\t", final_particle[i])
                #$%^if(len(string_suggestion[i])==0):
                    #$%^print( "\tNo other suggestion\n")
                #$%^else:
                    #$%^print(string_suggestion[i])

            '''
            translator = Translator()
            translation = translator.translate(clean_corrected_sentence)
            print("\nTranslation: ", translation.text, "\n")
            '''

        total_handan = correct_handan + incorrect_handan + low_prio_handan
        correct_acc = round(correct_handan/total_handan*100, 2)
        incorrect_acc = round(incorrect_handan/total_handan*100, 2)
        low_prio_acc = round(low_prio_handan/total_handan*100, 2)

        time_now = datetime.datetime.now()

        print(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}')
        print(f'Name of model: {file_name_list}')
        print(f'Correct Judgement: {correct_handan} ({correct_acc}%)')
        print(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)')
        print(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')

        correct_handan_list.append(correct_handan)
        incorrect_handan_list.append(incorrect_handan)
        low_prio_list.append(low_prio_handan)

        correct_acc_list.append(correct_acc)
        incorrect_acc_list.append(incorrect_acc)
        low_prio_acc_list.append(low_prio_acc)

        file_acc_handan = open("app_test_acc_fixed.txt", "a", encoding='utf8')
        file_acc_handan.write(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}------\n')
        file_acc_handan.write("--------------------------------\n")
        file_acc_handan.write(f'Name of model: {file_name_list}\n')

        for ihan in file_name_list:
            file_acc_handan.write(ihan + "\n")

        file_acc_handan.write(f'Correct Judgement: {correct_handan} ({correct_acc}%)\n')
        file_acc_handan.write(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)\n')
        file_acc_handan.write(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')
        file_acc_handan.write("--------------------------------\n\n")

        file_acc_handan.close()


def backup_app_test(s_index, e_index, train_name): #evaluating the app, by combining the 6 model or so :)

    full_model_list, full_tokenizer_list, full_neighbour_list, full_identifier_list, full_file_name_list, full_model_type_list = get_model()

    global identifier_type

    global particle_limit
    particle_limit = 1000000

    identifier_type = 1
    identifier_name = "f"
    _train_name = "_evaluate_" + train_name
    compile_raw_alt(s_index, e_index, _train_name)

    '''
    identifier_type = 2
    identifier_name = "s"
    compile_raw_alt(s_index, e_index, "_evaluate_s")

    identifier_type = 3
    identifier_name = "a"
    compile_raw_alt(s_index, e_index, "_evaluate_a")
    '''
    correct_handan_list = []
    incorrect_handan_list = []
    low_prio_list = []

    correct_acc_list = []
    incorrect_acc_list = []
    low_prio_acc_list = []

    total_model = len(full_model_list)
    if(total_model<6):
        print("ERROR: Your model file count is less than 6")
        return

    #cleaned = ''

    corpora_module = "corpora_evaluate" + "_" + train_name
    corpora_pos = importlib.import_module(corpora_module)
    reload(corpora_pos)

    cleaned = corpora_pos.training_jpn

    #import corpora_evaluate_f
    #reload(corpora_evaluate_f)
    #cleaned = corpora_evaluate_f.training_jpn

    #print(corpora_pos.training_jpn_pos)

    token_sentence = []
    #target_sequence = []
    #token_word = []

    sentence_tokenizing(cleaned, token_sentence)

    token_sentence = token_sentence[1:]

    #print(token_sentence[0]+"wut")
    #print(token_sentence[1]+"\n", token_sentence[2])
    print("How many token_sentence: ", len(token_sentence))
    #print("\nInput: ", end="")
    #input_text = input().strip()

    #if(input_text=="exit"):
    #    break

    all_combination_model = itertools.combinations(full_model_list, 6)
    all_combination_tokenizer = itertools.combinations(full_tokenizer_list, 6)
    all_combination_neighbour = itertools.combinations(full_neighbour_list, 6)
    all_combination_identifier = itertools.combinations(full_identifier_list, 6)
    all_combination_file_name = itertools.combinations(full_file_name_list, 6)
    all_combination_model_type = itertools.combinations(full_model_type_list, 6)

    #i_want_to_shuffle = (all_combination_model, all_combination_tokenizer, all_combination, neighbour)

    all_model_list=[]
    all_tokenizer_list=[]
    all_neighbour_list=[]
    all_identifier_list=[]
    all_file_name_list=[]
    all_model_type_list=[]

    for temp_model_list in all_combination_model:
        all_model_list.append(temp_model_list)

    for temp_tokenizer_list in all_combination_tokenizer:
        all_tokenizer_list.append(temp_tokenizer_list)

    for temp_neighbour_list in all_combination_neighbour:
        all_neighbour_list.append(temp_neighbour_list)

    for temp_identifier_list in all_combination_identifier:
        all_identifier_list.append(temp_identifier_list)

    for temp_file_name_list in all_combination_file_name:
        all_file_name_list.append(temp_file_name_list)

    for temp_model_type_list in all_combination_model_type:
        all_model_type_list.append(temp_model_type_list)

    
    
    #for temp_model_list in all_combination_model:
    for i_combination in range(len(all_model_list)):

        model_list = all_model_list[i_combination]
        tokenizer_list = all_tokenizer_list[i_combination]
        neighbour_list = all_neighbour_list[i_combination]
        identifier_list = all_identifier_list[i_combination]
        file_name_list = all_file_name_list[i_combination]
        model_type_list = all_model_type_list[i_combination]

        skip_flag_train_name = False

        #alter10000 -> 250000 260000
        #alt10000 -> 200000 210000
        #alt_x_10000 -> 350000 360000
        #alt_150000_10000 -> 150000 160000

        if(train_name == "alt10000" or train_name == "alter10000" or train_name == "alt_x_10000" or train_name == "alt_150000_10000"):
            for model_type_thing in model_type_list:
                if(model_type_thing!="lstm"):
                    skip_flag_train_name = True
                    break

        if(skip_flag_train_name):
            continue



        correct_handan = 0
        incorrect_handan = 0
        low_prio_handan = 0
        no_particle_count = 0

        for input_text in token_sentence:

            #print("loop for input_text: ", input_text, "\n")

            particle_exists = 0
            first_suggestion_particle = []
            second_suggestion_particle = []

            for i in range(len(model_list)):

                model = model_list[i]
                tokenizer = tokenizer_list[i]
                neighbour = neighbour_list[i]
                identifier = identifier_list[i]
                file_name = file_name_list[i]
                model_type = model_type_list[i]

                transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

                no_particle_flag = 0

                if(particle_exists==0):
                    print("---No particle was found---\n>", transformed_raw_input_text, "\n")
                    #print("Partile List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                    no_particle_flag = 1
                    no_particle_count += 1
                    break

                list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

                target_number=0
                i_target_text=0

                #info_tokenizers(tokenizer)

                for i_index in range(len(list_transformed_input_text)):

                    if(i_target_text>=len(list_transformed_input_text)):
                        break       

                    if(model_type == "lstm"):       

                        target_text = list_transformed_input_text[i_target_text]      

                        encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                        pad_encoded = pad_sequences([encoded_text], truncating='pre')

                        i_target_text+=1
                    
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                        target_text_forw = list_transformed_input_text[i_target_text]
                        target_text_back = list_transformed_input_text[i_target_text+1]

                        encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                        encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                        pad_encoded_forw = pad_sequences([encoded_text_forw], truncating='pre')
                        pad_encoded_back = pad_sequences([encoded_text_back], truncating='pre')

                        i_target_text+=2

                    '''
                    for wox in (list_transformed_raw_input_text[target_number]):

                        if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                            pass
                            #@@print("[", wox, "] ", end="")
                        else:
                            pass
                            #@@print(wox, " ", end="")
                    '''

                    #print("")
                    target_number += 1

                    suggestion_number=1

                    if(model_type == "lstm"):  
                        len_list_transformed_input_text = len(list_transformed_input_text)
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                        len_list_transformed_input_text = len(list_transformed_input_text)/2

                    if(len(first_suggestion_particle)!=len_list_transformed_input_text):
                        first_suggestion_particle.append({})
                        second_suggestion_particle.append({})

                        for p in list_target_particle:

                            first_suggestion_particle[target_number-1][p] = 0
                            second_suggestion_particle[target_number-1][p] = 0

                    try:
                        if(model_type=="lstm"):
                            predict_list = model.predict(pad_encoded, verbose=0)[0]
                        elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                            predict_list = model.predict([pad_encoded_forw, pad_encoded_back], verbose=0)[0]
                    except:
                        print("something goes wrong, pad_encoded")
                        continue

                    #print("inside the predict_list with model type [", model_type, "]: ", predict_list)

                    '''
                    predict_listo = []
                    
                    for i_plist in predict_list.argsort()[-25:][::-1]:
                        try:
                            pred_word = tokenizer.index_word[i_plist]
                            predict_listo.append(pred_word)
                        except:
                            continue
                    
                        
                    print("the predict_list [", len(predict_listo), "]: ", predict_listo)
                    '''

                    skip_ayam = 0

                    for i_plist in predict_list.argsort()[-3:][::-1]:
                    #for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:

                        pred_word = tokenizer.index_word[i_plist]
                        #print("the pred_word: ", pred_word)

                        try:
                            if(suggestion_number==1):
                                first_suggestion_particle[target_number-1][pred_word] += 1
                            elif(suggestion_number==2):
                                second_suggestion_particle[target_number-1][pred_word] += 1
                        except:
                            skip_ayam = 1
                            print("SOMETHING WAS EXPECTED! (second_suggestion_particle_thingy)")

                    if(skip_ayam==1):
                        continue


                        suggestion_number += 1


            if(no_particle_flag == 1):
                continue

            list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)

            particle_correct = []
            unchanged_marked_input_text = marked_input_text

            for h in range(len(list_correct_particle)):

                particle_correct.append(False)

                for i in range(len(marked_input_text)):

                    if(marked_input_text[i][1] == 1):

                        for particle in list_correct_particle[h]:

                            if(particle[0] == marked_input_text[i][0]):
                                particle_correct[h] = True
                                break

                        marked_input_text[i] = (marked_input_text[i][0], 2)
                        break

            #$%^print("-----Original Sentence-----")
            #$%^for token in unchanged_marked_input_text:
                #$%^if(token[1]==2):
                    #$%^print("[", token[0], "]", end="")
                #$%^else:
                    #$%^print(token[0], end="")

            #$%^print("\n\n-----Corrected Sentence-----")

            p_n = 0
            string_suggestion = [""]
            corrected_sentence = ""
            clean_corrected_sentence = ""
            final_particle = []

            ignore_low_prio = False

            for token in unchanged_marked_input_text:

                #correct particle [this is wrong]
                if(token[1]==2 and p_n<len(list_correct_particle)):


                    #correct particle
                    if(particle_correct[p_n]):
                        correct_handan += 1
                        #$%^print("[", token[0], "]", end="")
                        corrected_sentence += "[" + token[0] + "]"
                        clean_corrected_sentence += token[0]

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(token[0]==list_correct_particle[p_n][n][0]):
                                fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                                final_particle.append(fp)

                            if(len(list_correct_particle[p_n])>1):
                                if(n==0):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(list_correct_particle[p_n][n][0]!=token[0]):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                    #wrong particle (but there are suggestion)
                    elif(len(list_correct_particle[p_n]) != 0):

                        incorrect_handan += 1

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(len(list_correct_particle[p_n])!=0):
                                if(n==1):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(n!=0):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                                if(n==0):
                                    #$%^print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                    corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                    clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                    fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                    #final_particle.append(list_correct_particle[p_n][0][0])
                                    final_particle.append(fp)

                    else:
                        ignore_low_prio = True
                        low_prio_handan += 1
                        #$%^print("#########LOW PRIO DETECTED##########", end="")

                    #wrong particle (no suggestion, only low prio)
                    #@@#@@#@@else:
                        #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")


                    p_n += 1

                    if(p_n < len(list_correct_particle)):
                        string_suggestion.append("")

                else:
                    #$%^print(token[0], end="")
                    corrected_sentence += token[0]
                    clean_corrected_sentence += token[0]

            #$%^print("\n")

            if(ignore_low_prio):
                continue

            #$%^for i in range(len(list_correct_particle)):
                #$%^print("\t", final_particle[i])
                #$%^if(len(string_suggestion[i])==0):
                    #$%^print( "\tNo other suggestion\n")
                #$%^else:
                    #$%^print(string_suggestion[i])

            '''
            translator = Translator()
            translation = translator.translate(clean_corrected_sentence)
            print("\nTranslation: ", translation.text, "\n")
            '''

        total_handan = correct_handan + incorrect_handan + low_prio_handan
        correct_acc = round(correct_handan/total_handan*100, 2)
        incorrect_acc = round(incorrect_handan/total_handan*100, 2)
        low_prio_acc = round(low_prio_handan/total_handan*100, 2)

        time_now = datetime.datetime.now()

        print(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}')
        print(f'Name of model: {file_name_list}')
        print(f'Correct Judgement: {correct_handan} ({correct_acc}%)')
        print(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)')
        print(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')

        correct_handan_list.append(correct_handan)
        incorrect_handan_list.append(incorrect_handan)
        low_prio_list.append(low_prio_handan)

        correct_acc_list.append(correct_acc)
        incorrect_acc_list.append(incorrect_acc)
        low_prio_acc_list.append(low_prio_acc)

        file_acc_handan = open("app_test_acc_mixed.txt", "a", encoding='utf8')
        file_acc_handan.write(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}------\n')
        file_acc_handan.write("--------------------------------\n")
        file_acc_handan.write(f'Name of model: {file_name_list}\n')

        for ihan in file_name_list:
            file_acc_handan.write(ihan + "\n")

        file_acc_handan.write(f'Correct Judgement: {correct_handan} ({correct_acc}%)\n')
        file_acc_handan.write(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)\n')
        file_acc_handan.write(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')
        file_acc_handan.write("--------------------------------\n\n")

        file_acc_handan.close()

def temp_app_test(s_index, e_index): #evaluating the app, by combining the 6 model or so :)

    full_model_list, full_tokenizer_list, full_neighbour_list, full_identifier_list, full_file_name_list, full_model_type_list = get_model()

    global identifier_type

    global particle_limit
    particle_limit = 1000000

    identifier_type = 1
    identifier_name = "f"
    compile_raw_alt(s_index, e_index, "_evaluate_xy")

    '''
    identifier_type = 2
    identifier_name = "s"
    compile_raw_alt(s_index, e_index, "_evaluate_s")

    identifier_type = 3
    identifier_name = "a"
    compile_raw_alt(s_index, e_index, "_evaluate_a")
    '''
    correct_handan_list = []
    incorrect_handan_list = []
    low_prio_list = []

    correct_acc_list = []
    incorrect_acc_list = []
    low_prio_acc_list = []

    total_model = len(full_model_list)
    if(total_model<6):
        print("ERROR: Your model file count is less than 6")
        return

    #cleaned = ''

    import corpora_evaluate_xy
    reload(corpora_evaluate_xy)
    cleaned = corpora_evaluate_xy.training_jpn

    #print(corpora_pos.training_jpn_pos)

    token_sentence = []
    #target_sequence = []
    #token_word = []

    sentence_tokenizing(cleaned, token_sentence)

    token_sentence = token_sentence[1:]

    #print(token_sentence[0]+"wut")
    #print(token_sentence[1]+"\n", token_sentence[2])
    print("How many token_sentence: ", len(token_sentence))
    #print("\nInput: ", end="")
    #input_text = input().strip()

    #if(input_text=="exit"):
    #    break

    all_combination_model = itertools.combinations(full_model_list, 6)
    all_combination_tokenizer = itertools.combinations(full_tokenizer_list, 6)
    all_combination_neighbour = itertools.combinations(full_neighbour_list, 6)
    all_combination_identifier = itertools.combinations(full_identifier_list, 6)
    all_combination_file_name = itertools.combinations(full_file_name_list, 6)
    all_combination_model_type = itertools.combinations(full_model_type_list, 6)

    #i_want_to_shuffle = (all_combination_model, all_combination_tokenizer, all_combination, neighbour)

    all_model_list=[]
    all_tokenizer_list=[]
    all_neighbour_list=[]
    all_identifier_list=[]
    all_file_name_list=[]
    all_model_type_list=[]

    for temp_model_list in all_combination_model:
        all_model_list.append(temp_model_list)

    for temp_tokenizer_list in all_combination_tokenizer:
        all_tokenizer_list.append(temp_tokenizer_list)

    for temp_neighbour_list in all_combination_neighbour:
        all_neighbour_list.append(temp_neighbour_list)

    for temp_identifier_list in all_combination_identifier:
        all_identifier_list.append(temp_identifier_list)

    for temp_file_name_list in all_combination_file_name:
        all_file_name_list.append(temp_file_name_list)

    for temp_model_type_list in all_combination_model_type:
        all_model_type_list.append(temp_model_type_list)

    
    
    #for temp_model_list in all_combination_model:
    for i_combination in range(len(all_model_list)):

        model_list = all_model_list[i_combination]
        tokenizer_list = all_tokenizer_list[i_combination]
        neighbour_list = all_neighbour_list[i_combination]
        identifier_list = all_identifier_list[i_combination]
        file_name_list = all_file_name_list[i_combination]
        model_type_list = all_model_type_list[i_combination]


        correct_handan = 0
        incorrect_handan = 0
        low_prio_handan = 0
        no_particle_count = 0

        for input_text in token_sentence:

            #print("loop for input_text: ", input_text, "\n")

            particle_exists = 0
            first_suggestion_particle = []
            second_suggestion_particle = []

            for i in range(len(model_list)):

                model = model_list[i]
                tokenizer = tokenizer_list[i]
                neighbour = neighbour_list[i]
                identifier = identifier_list[i]
                file_name = file_name_list[i]
                model_type = model_type_list[i]

                transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

                no_particle_flag = 0

                if(particle_exists==0):
                    print("---No particle was found---\n>", transformed_raw_input_text, "\n")
                    #print("Partile List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                    no_particle_flag = 1
                    no_particle_count += 1
                    break

                list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

                target_number=0
                i_target_text=0

                #info_tokenizers(tokenizer)

                for i_index in range(len(list_transformed_input_text)):

                    if(i_target_text>=len(list_transformed_input_text)):
                        break       

                    if(model_type == "lstm"):       

                        target_text = list_transformed_input_text[i_target_text]      

                        encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                        pad_encoded = pad_sequences([encoded_text], truncating='pre')

                        i_target_text+=1
                    
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                        target_text_forw = list_transformed_input_text[i_target_text]
                        target_text_back = list_transformed_input_text[i_target_text+1]

                        encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                        encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                        pad_encoded_forw = pad_sequences([encoded_text_forw], truncating='pre')
                        pad_encoded_back = pad_sequences([encoded_text_back], truncating='pre')

                        i_target_text+=2

                    '''
                    for wox in (list_transformed_raw_input_text[target_number]):

                        if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                            pass
                            #@@print("[", wox, "] ", end="")
                        else:
                            pass
                            #@@print(wox, " ", end="")
                    '''

                    #print("")
                    target_number += 1

                    suggestion_number=1

                    if(model_type == "lstm"):  
                        len_list_transformed_input_text = len(list_transformed_input_text)
                    elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                        len_list_transformed_input_text = len(list_transformed_input_text)/2

                    if(len(first_suggestion_particle)!=len_list_transformed_input_text):
                        first_suggestion_particle.append({})
                        second_suggestion_particle.append({})

                        for p in list_target_particle:

                            first_suggestion_particle[target_number-1][p] = 0
                            second_suggestion_particle[target_number-1][p] = 0

                    try:
                        if(model_type=="lstm"):
                            predict_list = model.predict(pad_encoded, verbose=0)[0]
                        elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                            predict_list = model.predict([pad_encoded_forw, pad_encoded_back], verbose=0)[0]
                    except:
                        print("something goes wrong, pad_encoded")
                        continue

                    #print("inside the predict_list with model type [", model_type, "]: ", predict_list)

                    '''
                    predict_listo = []
                    
                    for i_plist in predict_list.argsort()[-25:][::-1]:
                        try:
                            pred_word = tokenizer.index_word[i_plist]
                            predict_listo.append(pred_word)
                        except:
                            continue
                    
                        
                    print("the predict_list [", len(predict_listo), "]: ", predict_listo)
                    '''

                    skip_ayam = 0

                    for i_plist in predict_list.argsort()[-3:][::-1]:
                    #for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:

                        pred_word = tokenizer.index_word[i_plist]
                        #print("the pred_word: ", pred_word)

                        try:
                            if(suggestion_number==1):
                                first_suggestion_particle[target_number-1][pred_word] += 1
                            elif(suggestion_number==2):
                                second_suggestion_particle[target_number-1][pred_word] += 1
                        except:
                            skip_ayam = 1
                            print("SOMETHING WAS EXPECTED! (second_suggestion_particle_thingy)")

                    if(skip_ayam==1):
                        continue


                        suggestion_number += 1


            if(no_particle_flag == 1):
                continue

            list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)

            particle_correct = []
            unchanged_marked_input_text = marked_input_text

            for h in range(len(list_correct_particle)):

                particle_correct.append(False)

                for i in range(len(marked_input_text)):

                    if(marked_input_text[i][1] == 1):

                        for particle in list_correct_particle[h]:

                            if(particle[0] == marked_input_text[i][0]):
                                particle_correct[h] = True
                                break

                        marked_input_text[i] = (marked_input_text[i][0], 2)
                        break

            #$%^print("-----Original Sentence-----")
            #$%^for token in unchanged_marked_input_text:
                #$%^if(token[1]==2):
                    #$%^print("[", token[0], "]", end="")
                #$%^else:
                    #$%^print(token[0], end="")

            #$%^print("\n\n-----Corrected Sentence-----")

            p_n = 0
            string_suggestion = [""]
            corrected_sentence = ""
            clean_corrected_sentence = ""
            final_particle = []

            ignore_low_prio = False

            for token in unchanged_marked_input_text:

                #correct particle [this is wrong]
                if(token[1]==2 and p_n<len(list_correct_particle)):


                    #correct particle
                    if(particle_correct[p_n]):
                        correct_handan += 1
                        #$%^print("[", token[0], "]", end="")
                        corrected_sentence += "[" + token[0] + "]"
                        clean_corrected_sentence += token[0]

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(token[0]==list_correct_particle[p_n][n][0]):
                                fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                                final_particle.append(fp)

                            if(len(list_correct_particle[p_n])>1):
                                if(n==0):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(list_correct_particle[p_n][n][0]!=token[0]):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                    #wrong particle (but there are suggestion)
                    elif(len(list_correct_particle[p_n]) != 0):

                        incorrect_handan += 1

                        for n in range(0, len(list_correct_particle[p_n])):

                            if(len(list_correct_particle[p_n])!=0):
                                if(n==1):
                                    string_suggestion[p_n] += "\tAnother particle suggestion: "
                                if(n!=0):
                                    string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                                if(n==0):
                                    #$%^print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                    corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                    clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                    fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                    #final_particle.append(list_correct_particle[p_n][0][0])
                                    final_particle.append(fp)

                    else:
                        ignore_low_prio = True
                        low_prio_handan += 1
                        #$%^print("#########LOW PRIO DETECTED##########", end="")

                    #wrong particle (no suggestion, only low prio)
                    #@@#@@#@@else:
                        #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")


                    p_n += 1

                    if(p_n < len(list_correct_particle)):
                        string_suggestion.append("")

                else:
                    #$%^print(token[0], end="")
                    corrected_sentence += token[0]
                    clean_corrected_sentence += token[0]

            #$%^print("\n")

            if(ignore_low_prio):
                continue

            #$%^for i in range(len(list_correct_particle)):
                #$%^print("\t", final_particle[i])
                #$%^if(len(string_suggestion[i])==0):
                    #$%^print( "\tNo other suggestion\n")
                #$%^else:
                    #$%^print(string_suggestion[i])

            '''
            translator = Translator()
            translation = translator.translate(clean_corrected_sentence)
            print("\nTranslation: ", translation.text, "\n")
            '''

        total_handan = correct_handan + incorrect_handan + low_prio_handan
        correct_acc = round(correct_handan/total_handan*100, 2)
        incorrect_acc = round(incorrect_handan/total_handan*100, 2)
        low_prio_acc = round(low_prio_handan/total_handan*100, 2)

        time_now = datetime.datetime.now()

        print(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}')
        print(f'Name of model: {file_name_list}')
        print(f'Correct Judgement: {correct_handan} ({correct_acc}%)')
        print(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)')
        print(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')

        correct_handan_list.append(correct_handan)
        incorrect_handan_list.append(incorrect_handan)
        low_prio_list.append(low_prio_handan)

        correct_acc_list.append(correct_acc)
        incorrect_acc_list.append(incorrect_acc)
        low_prio_acc_list.append(low_prio_acc)

        file_acc_handan = open("app_test_acc.txt", "a", encoding='utf8')
        file_acc_handan.write(f'------TIME DONE: {time_now.hour}:{time_now.minute}:{time_now.second}------\n')
        file_acc_handan.write("--------------------------------\n")
        file_acc_handan.write(f'Name of model: {file_name_list}\n')

        for ihan in file_name_list:
            file_acc_handan.write(ihan + "\n")

        file_acc_handan.write(f'Correct Judgement: {correct_handan} ({correct_acc}%)\n')
        file_acc_handan.write(f'Incorrect Judgement: {incorrect_handan} ({incorrect_acc}%)\n')
        file_acc_handan.write(f'Unable to Judge: {low_prio_handan} ({low_prio_acc}%)\n')
        file_acc_handan.write("--------------------------------\n\n")

        file_acc_handan.close()

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#5 - User/Application function

def user_mode():

    model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = get_model()

    if(len(model_list)!=6):
        print("You need to have exactly 6 model. [Total Model: ", len(model_list))
        return

    while True:

        particle_exists = 0

        first_suggestion_particle = []

        second_suggestion_particle = []

        print("Time right now: ", datetime.datetime.now())
        print("\nInput: ", end="")
        input_text = input().strip()

        if(input_text=="exit"):
            break

        #This is where the shenanigans happen (but need to confirm if there are actually any particle first!)
        #FIX THIS PART YEAH! :V
        for i in range(len(model_list)):

            #i=1

            model = model_list[i]
            tokenizer = tokenizer_list[i]
            neighbour = neighbour_list[i]
            identifier = identifier_list[i]
            file_name = file_name_list[i]
            model_type = model_type_list[i]

            #@@print("the identifier: ", identifier)
            #@@print("File name: ", file_name)

            '''
            model = model_list[0]
            tokenizer = tokenizer_list[0]
            neighbour = neighbour_list[0]
            identifier = identifier_list[0]
            if(identifier=="f"):
                identifier = 1
            elif(identifier=="s"):
                identifier = 2
            '''

            '''
            model = load_model("jpn_particle_transformed_model.h5")
            seq_len = model.input_shape[1]
            neighbour = int(seq_len / 2)
            tokenizer = Tokenizer()
            with open('tokenizer_test.json') as f:
                data = json.load(f)
                tokenizer = tokenizer_from_json(data)

            identifier_type =
            '''

            #How to differentiate which identifier was used:
            #put some code to the filename, like (one_ , two_) or  (f_ , s_) or something

            transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

            #-print("transformed_input_text: ", transformed_input_text)
            #-print("transformed_raw_input_text: ", transformed_raw_input_text)

            no_particle_flag = 0

            if(particle_exists==0):
                print("No particle was found")
                print("Partile List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                no_particle_flag = 1
                break

            list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

            #-print("list_transformed_input_text: ", list_transformed_input_text)
            #-print("list_transformed_raw_input_text: ", list_transformed_raw_input_text)


            #tokenizer = Tokenizer()

            '''
            tokenizer = Tokenizer()

            with open('tokenizer_test.json') as f:
                data = json.load(f)
                tokenizer = tokenizer_from_json(data)
            '''

            #print("seq_len, neighbour = ", seq_len, " ", neighbour)

            target_number=0
            i_target_text=0

            for i_index in range(len(list_transformed_input_text)):
            #for target_text in list_transformed_input_text:

                if(i_target_text>=len(list_transformed_input_text)):
                  break

                

                if(model_type == "lstm"):

                  target_text = list_transformed_input_text[i_target_text]

                  encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                  pad_encoded = pad_sequences([encoded_text], truncating='pre')

                  i_target_text+=1

                elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                  target_text_forw = list_transformed_input_text[i_target_text]
                  target_text_back = list_transformed_input_text[i_target_text+1]

                  encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                  encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                  pad_encoded = pad_sequences([encoded_text_forw, encoded_text_back], truncating='pre')

                  i_target_text+=2
                  


                  #for index in range(len(target_text)):
                  #  if(index % 2 == 0):
                  #    encoded_text_forw = 
                  
                #-print(tokenizer.texts_to_sequences([target_text[0:-1]])[0], "\n")
                #-print(target_text[0:-1], "\n")
                #-print([' '.join(target_text[0:-1])] , "\n")

                #-------------------encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                #encoded_text = tokenizer.texts_to_sequences([' '.join(list_transformed_input_text[0][0:-1])])[0]
                #encoded_text = tokenizer.texts_to_sequences([input_text])[0]

                #pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
                #-------------------pad_encoded = pad_sequences([encoded_text], truncating='pre')

                #-print(target_text)
                #-print(encoded_text, pad_encoded, "\n")

                #-for wox in encoded_text:
                #-    print(tokenizer.index_word[wox])

                #@@print("\t", end="")
                
                '''
                for wox in (list_transformed_raw_input_text[target_number]):

                    if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                        pass
                        #@@print("[", wox, "] ", end="")
                    else:
                        pass
                        #@@print(wox, " ", end="")
                '''

                print("")
                target_number += 1

                suggestion_number=1

                if(len(first_suggestion_particle)!=len(list_transformed_input_text)):
                    first_suggestion_particle.append({})
                    second_suggestion_particle.append({})

                    for p in list_target_particle:

                        first_suggestion_particle[target_number-1][p] = 0
                        second_suggestion_particle[target_number-1][p] = 0

                for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:
                    #print(model.predict(pad_encoded)[0].argsort()[-3:][::-1])

                    pred_word = tokenizer.index_word[i]

                    if(suggestion_number==1):
                        first_suggestion_particle[target_number-1][pred_word] += 1
                    elif(suggestion_number==2):
                        second_suggestion_particle[target_number-1][pred_word] += 1

                    suggestion_number += 1

                    #@@print("\tParticle suggestion:", pred_word)

                #@@print("")

            #@@print("")

        if(no_particle_flag == 1):
            continue

        #INSERT JUDGMENT SYSTEM HERE
        #suggestion_particle_list = judge_particles(first_suggestion_particle, second_suggestion_particle)

        list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)

        #@@print("\n", "list_correct_particle: ", list_correct_particle, "\n")
        #@@print("list_possible_correct_particle: ", list_possible_correct_particle, "\n")
        #NOW THE ACTUAL JUDGEMENT
        particle_correct = []
        unchanged_marked_input_text = marked_input_text

        for h in range(len(list_correct_particle)):
            #print(list_transformed_raw_input_text[h])
            #print(list_transformed_input_text[h])

            #-print(transformed_raw_input_text)
            #-print(marked_input_text)
            #-print(list_correct_particle[h])

            particle_correct.append(False)

            #break_flag = False

            for i in range(len(marked_input_text)):

                if(marked_input_text[i][1] == 1):

                    #print("enter here: ", marked_input_text[i])

                    for particle in list_correct_particle[h]:

                        if(particle[0] == marked_input_text[i][0]):
                            particle_correct[h] = True
                            break

                        #if(i == len(marked_input_text)-1):
                            #marked_input_text[i] = (marked_input_text[i][0], 2)

                    marked_input_text[i] = (marked_input_text[i][0], 2)
                    break #marked_input_text[i][1] = 2

        #@@print("\nparticle_correct: ", particle_correct)

        #@@print("unchanged_marked_input_text: ", unchanged_marked_input_text)
        #@@print("marked_input_text: ", marked_input_text, "\n")

        #print original

        print("-----Original Sentence-----")
        for token in unchanged_marked_input_text:
            if(token[1]==2):
                print("[", token[0], "]", end="")
            else:
                print(token[0], end="")

        #print corrected

        print("\n\n-----Corrected Sentence-----")
        #for i in range(len(list_correct_particle)):

        p_n = 0
        string_suggestion = [""]
        corrected_sentence = ""
        clean_corrected_sentence = ""
        final_particle = []
        ignore_low_prio = False

        for token in unchanged_marked_input_text:


            if(token[1]==2 and p_n<len(list_correct_particle)):

                #correct particle
                if(particle_correct[p_n]):
                    print("[", token[0], "]", end="")
                    corrected_sentence += "[" + token[0] + "]"
                    clean_corrected_sentence += token[0]


                    #final_particle.append(token[0])

                    for n in range(0, len(list_correct_particle[p_n])):

                        if(token[0]==list_correct_particle[p_n][n][0]):
                            fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                            final_particle.append(fp)

                        if(len(list_correct_particle[p_n])>1):
                            if(n==0):
                                string_suggestion[p_n] += "\tAnother particle suggestion: "
                            if(list_correct_particle[p_n][n][0]!=token[0]):
                                string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                #wrong particle (but there are suggestion)
                elif(len(list_correct_particle[p_n]) != 0):

                    for n in range(0, len(list_correct_particle[p_n])):

                    #for c_particle in range(len(list_correct_particle[i])):
                        if(len(list_correct_particle[p_n])!=0):
                            if(n==1):
                                string_suggestion[p_n] += "\tAnother particle suggestion: "
                            if(n!=0):
                                string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                            if(n==0):
                                print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                #final_particle.append(list_correct_particle[p_n][0][0])
                                final_particle.append(fp)

                #wrong particle (no suggestion, only low prio)
                #@@#@@#@@else:
                    #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")
                else:
                  print("This is low prio")
                  ignore_low_prio = True


                p_n += 1

                if(p_n < len(list_correct_particle)):
                    string_suggestion.append("")

             #not particle
            else:
                print(token[0], end="")
                corrected_sentence += token[0]
                clean_corrected_sentence += token[0]

        #just a quick measure for low prio, fix later maybe :)
        if(ignore_low_prio):
          continue


                #for c_particle in range(len(list_correct_particle[i])):
                #    if(c_particle[0]==

        #print("\n\nCorrected Sentence: ", corrected_sentence, "\n")
        print("\n")

        for i in range(len(list_correct_particle)):
            print("\t", final_particle[i])
            if(len(string_suggestion[i])==0):
                print( "\tNo other suggestion\n")
            else:
                print(string_suggestion[i])

        translator = Translator()
        #old translation
        #translation = translator.translate(input_text)
        translation = translator.translate(clean_corrected_sentence)
        print("\nTranslation: ", translation.text, "\n")


#def tag_str(tag_int):
#    tag_int = "1."

def UI_user_mode():

    def UI_user_mode_clicked(event=None):
        
        str_text_answer=""
        #tag_str_text_answer=[]
        btn.configure(state=DISABLED)
        root.update_idletasks()
        text_answer.configure(state='normal')
        text_answer2.configure(state='normal')
        text_error.configure(state='normal')
        #lbl_answer.configure(text="")
        #lbl_error.configure(text="")
        text_answer.delete("1.0", END)
        text_answer2.delete("1.0", END)
        text_error.delete("1.0", END)

        #btn.grid(row=1)
        particle_exists = 0

        first_suggestion_particle = []

        second_suggestion_particle = []

        print("Time right now: ", datetime.datetime.now(), "\n")

        #print("\nInput: ", end="")
        #input_text = input().strip()
        input_text = entry_txt.get().strip()

        #if(input_text=="exit"):
        #    return

        #This is where the shenanigans happen (but need to confirm if there are actually any particle first!)
        #FIX THIS PART YEAH! :V
        for i in range(len(model_list)):

            #i=1

            model = model_list[i]
            tokenizer = tokenizer_list[i]
            neighbour = neighbour_list[i]
            identifier = identifier_list[i]
            file_name = file_name_list[i]
            model_type = model_type_list[i]

            #@@print("the identifier: ", identifier)
            print("File name: ", file_name)

            '''
            model = model_list[0]
            tokenizer = tokenizer_list[0]
            neighbour = neighbour_list[0]
            identifier = identifier_list[0]
            if(identifier=="f"):
                identifier = 1
            elif(identifier=="s"):
                identifier = 2
            '''

            '''
            model = load_model("jpn_particle_transformed_model.h5")
            seq_len = model.input_shape[1]
            neighbour = int(seq_len / 2)
            tokenizer = Tokenizer()
            with open('tokenizer_test.json') as f:
                data = json.load(f)
                tokenizer = tokenizer_from_json(data)

            identifier_type =
            '''

            #How to differentiate which identifier was used:
            #put some code to the filename, like (one_ , two_) or  (f_ , s_) or something

            transformed_input_text, transformed_raw_input_text, marked_input_text, particle_exists = preprocess_string(input_text, identifier, model_type)

            #-print("transformed_input_text: ", transformed_input_text)
            #-print("transformed_raw_input_text: ", transformed_raw_input_text)

            no_particle_flag = 0

            if(particle_exists==0):
                print("No particle was found")
                print("Particle List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
                no_particle_flag = 1
                break

            list_transformed_input_text, list_transformed_raw_input_text = transform_string(transformed_input_text, transformed_raw_input_text, neighbour, model_type)

            #-print("list_transformed_input_text: ", list_transformed_input_text)
            #-print("list_transformed_raw_input_text: ", list_transformed_raw_input_text)


            #tokenizer = Tokenizer()

            '''
            tokenizer = Tokenizer()

            with open('tokenizer_test.json') as f:
                data = json.load(f)
                tokenizer = tokenizer_from_json(data)
            '''

            #print("seq_len, neighbour = ", seq_len, " ", neighbour)

            target_number=0
            i_target_text=0

            for i_index in range(len(list_transformed_input_text)):
            #for target_text in list_transformed_input_text:
                #print("does it go i_index?")

                if(i_target_text>=len(list_transformed_input_text)):
                    #print("break?")
                    break

                

                if(model_type == "lstm"):

                    #print("does it go lstm?")

                    target_text = list_transformed_input_text[i_target_text]
                    #print("target:", target_text)

                    encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                    #print("encode: ", encoded_text)
                    pad_encoded = pad_sequences([encoded_text], truncating='pre')

                    i_target_text+=1

                elif(model_type == "func_lstm" or model_type == "func_lstm_combined"):

                    target_text_forw = list_transformed_input_text[i_target_text]
                    #print("forw:", target_text_forw)
                    target_text_back = list_transformed_input_text[i_target_text+1]
                    #print("back:", target_text_back)

                    encoded_text_forw = tokenizer.texts_to_sequences([' '.join(target_text_forw[0:-1])])[0]
                    #print("encode forw: ", encoded_text_forw)
                    encoded_text_back = tokenizer.texts_to_sequences([' '.join(target_text_back[0:-1])])[0]
                    #print("encode back: ", encoded_text_back)
                    #pad_encoded = pad_sequences([encoded_text_forw, encoded_text_back], truncating='pre')
                    pad_encoded_forw = pad_sequences([encoded_text_forw], truncating='pre')
                    pad_encoded_back = pad_sequences([encoded_text_back], truncating='pre')
                    pad_encoded=[pad_encoded_forw, pad_encoded_back]
                    i_target_text+=2
                    


                    #for index in range(len(target_text)):
                    #  if(index % 2 == 0):
                    #    encoded_text_forw = 
                    
                #-print(tokenizer.texts_to_sequences([target_text[0:-1]])[0], "\n")
                #-print(target_text[0:-1], "\n")
                #-print([' '.join(target_text[0:-1])] , "\n")

                #-------------------encoded_text = tokenizer.texts_to_sequences([' '.join(target_text[0:-1])])[0]
                #encoded_text = tokenizer.texts_to_sequences([' '.join(list_transformed_input_text[0][0:-1])])[0]
                #encoded_text = tokenizer.texts_to_sequences([input_text])[0]

                #pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
                #-------------------pad_encoded = pad_sequences([encoded_text], truncating='pre')

                #-print(target_text)
                #-print(encoded_text, pad_encoded, "\n")

                #-for wox in encoded_text:
                #-    print(tokenizer.index_word[wox])

                #@@print("\t", end="")
                
                '''
                for wox in (list_transformed_raw_input_text[target_number]):

                    if(wox == list_transformed_raw_input_text[target_number][neighbour]):
                        pass
                        #@@print("[", wox, "] ", end="")
                    else:
                        pass
                        #@@print(wox, " ", end="")
                '''

                #print("")
                target_number += 1

                suggestion_number=1

                if(model_type == "func_lstm" or model_type == "func_lstm_combined"):
                    len_list_transformed_input_text = len(list_transformed_input_text)/2
                elif(model_type == "lstm"):
                    len_list_transformed_input_text = len(list_transformed_input_text)


                if(len(first_suggestion_particle)!=len_list_transformed_input_text):

                    first_suggestion_particle.append({})
                    second_suggestion_particle.append({})

                    for p in list_target_particle:

                        first_suggestion_particle[target_number-1][p] = 0
                        second_suggestion_particle[target_number-1][p] = 0

                for i in (model.predict(pad_encoded, verbose=0)[0]).argsort()[-3:][::-1]:
                    #print(model.predict(pad_encoded)[0].argsort()[-3:][::-1])

                    pred_word = tokenizer.index_word[i]

                    if(suggestion_number==1):
                        first_suggestion_particle[target_number-1][pred_word] += 1
                    elif(suggestion_number==2):
                        second_suggestion_particle[target_number-1][pred_word] += 1

                    suggestion_number += 1

                    #@@print("\tParticle suggestion:", pred_word)

                #@@print("")

            print("")

        '''NO PARTICLE FLAG MESSAGE HERE'''
        if(no_particle_flag == 1):
            btn.configure(state=NORMAL)
            #lbl_answer.configure(text="")
            #lbl_error.configure(text="[NO PARTICLE WAS FOUND] \n Particle List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
            text_answer.delete("1.0", END)
            text_answer2.delete("1.0", END)
            #text_error.insert(END, "[PARTICLE NOT FOUND]\nPlease enter Japanese sentence that has a particle\n\nParticle List: \"は\", \"と\", \"も\", \"が\", \"に\", \"へ\", \"を\", \"の\", \"で\", \"や\", \"な\"")
            text_error.insert(END, "[PARTICLE NOT FOUND]\nPlease enter Japanese sentence that has a particle.\n\nParticle List: は, と, も, が, に, へ, を, の, で, や, な")
            text_answer.configure(state='disabled')
            text_answer2.configure(state='disabled')
            text_error.configure(state='disabled')
            text_answer.grid_remove()
            text_answer2.grid_remove()
            text_error.grid()
            #lbl_answer.grid(row=2, column=0, sticky=W)
            return

        #INSERT JUDGMENT SYSTEM HERE
        #suggestion_particle_list = judge_particles(first_suggestion_particle, second_suggestion_particle)

        list_correct_particle, list_possible_correct_particle = judge_particles(first_suggestion_particle, second_suggestion_particle)
        #print_stack = []
        #@@print("\n", "list_correct_particle: ", list_correct_particle, "\n")
        #@@print("list_possible_correct_particle: ", list_possible_correct_particle, "\n")
        #NOW THE ACTUAL JUDGEMENT
        particle_correct = []
        unchanged_marked_input_text = marked_input_text

        for h in range(len(list_correct_particle)):
            #print(list_transformed_raw_input_text[h])
            #print(list_transformed_input_text[h])

            #-print(transformed_raw_input_text)
            #-print(marked_input_text)
            #-print(list_correct_particle[h])

            particle_correct.append(False)

            #break_flag = False

            for i in range(len(marked_input_text)):

                if(marked_input_text[i][1] == 1):

                    #print("enter here: ", marked_input_text[i])

                    for particle in list_correct_particle[h]:

                        if(particle[0] == marked_input_text[i][0]):
                            particle_correct[h] = True
                            break

                        #if(i == len(marked_input_text)-1):
                            #marked_input_text[i] = (marked_input_text[i][0], 2)

                    marked_input_text[i] = (marked_input_text[i][0], 2)
                    break #marked_input_text[i][1] = 2

        #@@print("\nparticle_correct: ", particle_correct)

        #@@print("unchanged_marked_input_text: ", unchanged_marked_input_text)
        #@@print("marked_input_text: ", marked_input_text, "\n")

        #print original
        i_particle_correct=0

        str_text_answer += "-----Original Sentence-----\n"
        text_answer.insert('end', "Original Sentence\n")
        #print("-----Original Sentence-----")
        for token in unchanged_marked_input_text:
            if(token[1]==2):
                #str_text_answer += "[" + token[0] + "]"
                
                if(particle_correct[i_particle_correct]):
                    text_answer.insert('end', token[0], ('tag_particle_correct'))
                else:
                    text_answer.insert('end', token[0], ('tag_particle_incorrect'))
                #print("[", token[0], "]", end="")
                i_particle_correct+=1
                 
            else:
                #str_text_answer += token[0]
                text_answer.insert('end', token[0])
                #print(token[0], end="")

            

        #print corrected

        #print("\n\n-----Corrected Sentence-----")
        #str_text_answer += "\n\n-----Corrected Sentence-----"
        text_answer.insert('end', "\n\nCorrected Sentence\n")
        #for i in range(len(list_correct_particle)):

        p_n = 0

        string_suggestion = [""]
        #tag_string_suggestion = []

        corrected_sentence = ""
        #tag_corrected_sentence = []

        clean_corrected_sentence = ""
        #tag_clean_corrected_sentence = []

        final_particle = []
        #tag_final_particle = []

        ignore_low_prio = False

        for token in unchanged_marked_input_text:


            if(token[1]==2 and p_n<len(list_correct_particle)):

                #correct particle
                if(particle_correct[p_n]):
                    #print("[", token[0], "]", end="")
                    #str_text_answer += token[0]
                    text_answer.insert('end', token[0], ('tag_particle_correct'))
                    corrected_sentence += "[" + token[0] + "]"
                    clean_corrected_sentence += token[0]


                    #final_particle.append(token[0])

                    for n in range(0, len(list_correct_particle[p_n])):

                        if(token[0]==list_correct_particle[p_n][n][0]):
                            fp = "[" + token[0] + "] - " + list_correct_particle[p_n][n][1]
                            final_particle.append(fp)

                        if(len(list_correct_particle[p_n])>1):
                            if(n==0):
                                #str_text_answer += "\tAnother particle suggestion: "
                                #text_answer.insert('end',"\tAnother particle suggestion: ")
                                #string_suggestion[p_n] += "\tAnother particle suggestion: "
                                string_suggestion[p_n] += "Another particle suggestion:\n"
                            if(list_correct_particle[p_n][n][0]!=token[0]):
                                #str_text_answer += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"
                                #text_answer.insert('end',"\tAnother particle suggestion: ")
                                string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] +"\n"

                #wrong particle (but there are suggestion)
                elif(len(list_correct_particle[p_n]) != 0):

                    for n in range(0, len(list_correct_particle[p_n])):

                    #for c_particle in range(len(list_correct_particle[i])):
                        if(len(list_correct_particle[p_n])!=0):
                            if(n==1):
                                #string_suggestion[p_n] += "\tAnother particle suggestion: "
                                string_suggestion[p_n] += "Another particle suggestion:\n"
                            if(n!=0):
                                string_suggestion[p_n] += list_correct_particle[p_n][n][0] + " - " + list_correct_particle[p_n][n][1] + "\n"
                            if(n==0):
                                #print("[", list_correct_particle[p_n][0][0], "]", end="*")
                                #str_text_answer += token[0]
                                text_answer.insert('end', list_correct_particle[p_n][0][0], ('tag_particle_corrected'))
                                corrected_sentence += "[" + list_correct_particle[p_n][0][0] + "]*"
                                clean_corrected_sentence += list_correct_particle[p_n][0][0]
                                fp = "[" + list_correct_particle[p_n][0][0] + "]* - " + list_correct_particle[p_n][n][1]
                                #final_particle.append(list_correct_particle[p_n][0][0])
                                final_particle.append(fp)

                #wrong particle (no suggestion, only low prio)
                #@@#@@#@@else:
                    #@@#@@#@@print("Yeah low prio PLEASE FIX THIS")
                else:
                    print("This is low prio")
                    ignore_low_prio = True


                p_n += 1

                if(p_n < len(list_correct_particle)):
                    string_suggestion.append("")

                #not particle
            else:
                #print(token[0], end="")
                #str_text_answer += token[0]
                text_answer.insert('end', token[0])
                corrected_sentence += token[0]
                clean_corrected_sentence += token[0]

        #just a quick measure for low prio, fix later maybe :)
        if(ignore_low_prio):
            btn.configure(state=NORMAL)
            #lbl_answer.configure(text="")
            #lbl_error.configure(text="Found low prio! Cannot be assessed!")
            text_answer.delete("1.0", END)
            text_answer2.delete("1.0", END)
            text_error.insert(END, "Cannot give recommendation for this sentence!\nSorry for inconvenience~")
            text_answer.configure(state='disabled')
            text_answer2.configure(state='disabled')
            text_error.configure(state='disabled')
            text_answer.grid_remove()
            text_answer2.grid_remove()
            text_error.grid()
            return


                #for c_particle in range(len(list_correct_particle[i])):
                #    if(c_particle[0]==

        #print("\n\nCorrected Sentence: ", corrected_sentence, "\n")
        print("\n")
        text_answer.insert('end', "\n\n")

        for i in range(len(list_correct_particle)):

            #print("\t", final_particle[i])

            #text_answer2.insert('end', "\t")
            if(final_particle[i][3]=='*'):
                text_answer2.insert('end', final_particle[i][:3], ("tag_particle_corrected"))
                text_answer2.insert('end', final_particle[i][4:])
            else:
                text_answer2.insert('end', final_particle[i][:3], ("tag_particle_correct"))
                text_answer2.insert('end', final_particle[i][3:])
            text_answer2.insert('end', "\n")

            if(len(string_suggestion[i])==0):
                #print( "\tNo other suggestion\n")
                #text_answer2.insert('end', "\tNo other suggestion\n\n")
                text_answer2.insert('end', "No other suggestion\n\n")
            else:
                #print(string_suggestion[i])
                text_answer2.insert('end', "" + string_suggestion[i][:28]+" ")
                #29 because of \n
                text_answer2.insert('end', "" + string_suggestion[i][29:]+"\n")

        try:
            translator = Translator()
            #old translation
            #translation = translator.translate(input_text)
            translation = translator.translate(clean_corrected_sentence)
            #print("\nTranslation: ", translation.text, "\n")
            text_answer.insert('end', "\nTranslation\n\n"+ translation.text+ "\n\n")
        except:
            text_answer.insert('end', "\nTranslation\n\n"+ "(no internet connection for translation)"+"\n\n")

        #lbl_answer.configure(text=translation.text)
        #lbl_answer.configure(text=str_text_answer)
        #lbl_error.configure(text="")
        #text_answer.insert(END, str_text_answer)
        #text_answer.insert(END, translation.text)
        text_error.delete("1.0", END)
        btn.configure(state=NORMAL)
        text_answer.configure(state='disabled')
        text_answer2.configure(state='disabled')
        text_error.configure(state='disabled')
        text_answer.grid()
        text_answer2.grid()
        text_error.grid_remove()

        #frame2.rowconfigure(tuple(range(1)), weight=1)
        #frame2.columnconfigure(tuple(range(1)), weight=1)
        
    def UI_user_mode_start():

        nonlocal model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list
        model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = get_model()
        #sleep(0.5)

        if(len(model_list)!=6):
            print("You need to have exactly 6 model. [Total Model: ", len(model_list))
            print("Button: わかりました！")
            return
        

        lbl_loading.configure(text="Loading Complete!")
        root.update_idletasks()
        sleep(0.5)

        print("loading complete")
        
        print("after root.after")

        #lbl_loading.after(250, lambda: lbl_loading.configure(text="Preparing application..."))
        #UI_user_mode_start_load_complete()

        lbl_loading.configure(text="Preparing Application...")
        root.update_idletasks()      

        UI_user_mode_clicked()
        #sleep(0.5)

        #lbl_answer.configure(text="")
        #lbl_error.configure(text="")
        text_answer.configure(state="normal")
        text_answer2.configure(state="normal")
        text_error.configure(state="normal")
        text_answer.delete("1.0", END)
        text_answer2.delete("1.0", END)
        text_error.delete("1.0", END)
        text_answer.configure(state="disabled")
        text_answer2.configure(state="disabled")
        text_error.configure(state="disabled")
        entry_txt.delete(0, END)
        lbl_loading.grid_remove()

        root.geometry('1080x600')

        frame1.grid(row=0, column=0, sticky=W)
        
        root.bind('<Return>', UI_user_mode_clicked)
        lbl.grid(row=0, column=0, sticky=W)
        entry_txt.grid(row=1, column=0, sticky=W, pady=10)
        btn.grid(row=1, column=1, sticky=W, padx=15)
        btn_clear.grid(row=1, column=2, sticky=W, padx=0)
        
        frame2.grid(row=1, column=0) 

        #lbl_answer.grid(row=2, column=0, sticky=W)
        #lbl_error.grid(row=3, column=0, sticky=W)
        #text_answer.grid(row=0, column=0, sticky=W,pady=25)
        #text_error.grid(row=1, column=0, sticky=W, pady=25)
        text_answer.grid(row=0, column=0, pady=15, padx=15, sticky=N)
        text_answer2.grid(row=0, column=1, pady=15, padx=30, sticky=N)
        text_answer.grid_remove()
        text_answer2.grid_remove()
        text_error.grid(row=0, column=0, pady=15, padx=15, sticky=N)
        root.update_idletasks()  
        text_error.grid_remove()
        #frame2.grid(row=1, column=0, sticky="nsew") 

        #click_clear()

    model_list, tokenizer_list, neighbour_list, identifier_list, file_name_list, model_type_list = [[0,0,0,0,0,0],0,0,0,0,0]

    root = Tk()
    root.title("Recommendation for Japanese Particle")
    root.geometry('350x75')
    root.resizable(0,0)
    root.configure(padx=35, pady=15)
    root.rowconfigure(1, weight=1)
    #root.columnconfigure(0, weight=1)

    frame1 = Frame(root)
    frame2 = Frame(root)
    #frame2.rowconfigure(0, weight=1)
    #frame2.columnconfigure(0, weight=1)
    frame2.configure(height=240, width=900, bg="white", highlightbackground="gray", highlightthickness=1)

    Font_tuple = ("Meiryo", 16)
    Font_tuple_entry = ("Meiryo", 16)
    Font_tuple_bold = ("Meiryo", 16)
    FONT_TAG = ("Yu Gothic", 14, "bold")
    FONT_TAG2 = ("Yu Gothic", 12, "bold")
    FONT_TEXT = ("Yu Gothic", 14)
    FONT_TEXT2 = ("Yu Gothic", 12)


    lbl_loading = Label(root, text = "Loading Model...", justify=LEFT)
    lbl_loading.grid(row=0, column=1, sticky=W, pady=5)

    lbl = Label(frame1, text = "Enter your Japanese sentence:", justify=LEFT, font=Font_tuple)

    entry_txt = Entry(frame1, width=40, justify=LEFT, font=Font_tuple_entry)
    entry_txt.insert(0, "君の花")
    
    btn = Button(frame1, text = "Predict", fg="blue", state=NORMAL, command=UI_user_mode_clicked, justify=LEFT, font=("Meiryo", 12))
    #def UI_user_mode_clear():
    #    entry_txt.delete(0, END)
    def click_clear():
        text_answer.configure(state="normal")
        text_answer2.configure(state="normal")
        text_error.configure(state="normal")
        text_answer.delete("1.0", END)
        text_answer2.delete("1.0", END)
        text_error.delete("1.0", END)
        text_answer.configure(state="disabled")
        text_answer2.configure(state="disabled")
        text_error.configure(state="disabled")
        text_answer.grid_remove()
        text_answer2.grid_remove()
        text_error.grid_remove()
        entry_txt.delete(0, END)
        btn.configure(state=NORMAL)

    btn_clear = Button(frame1, text = "Clear", fg="black", state=NORMAL, command=lambda: click_clear(), justify=LEFT, font=("Meiryo", 12))

    

    #lbl_answer = Label(root, text = "", justify=LEFT, font=Font_tuple, wraplength=500)
    #lbl_error = Label(root, text="", justify=LEFT, font=("Meiryo", 12), fg="red", wraplength=500)
    text_answer = Text(frame2, wrap=WORD)
    text_answer2 = Text(frame2, wrap=WORD)
    text_error = Text(frame2, wrap=WORD)
    #text_answer.configure(height=20, bg="#f0f0f0", highlightthickness=0, font=Font_tuple, state="disabled", bd=0, borderwidth=0, autoseparators=True)
    #text_error.configure(height=20, bg="#f0f0f0", highlightthickness=0, font=("Meiryo", 12), fg="red", state="disabled", bd=0, borderwidth=0, autoseparators=True)
    text_answer.configure(padx=5, pady=5, height=17, width=44, bg="white", highlightthickness=0, font=FONT_TEXT, state="disabled", bd=0, borderwidth=1, autoseparators=True)
    text_answer2.configure(padx=5, pady=5, height=20, width=43, bg="white", highlightthickness=0, font=FONT_TEXT2, state="disabled", bd=0, borderwidth=1, autoseparators=True)
    text_error.configure(height=17, width=80, bg="white", highlightthickness=0, font=FONT_TEXT, fg="red", state="disabled", bd=0, borderwidth=0, autoseparators=True)

    #font='TkFixedFont', relief='raised'
    text_answer.tag_configure('tag_particle_corrected', background='yellow', foreground="black", font=FONT_TAG)
    text_answer.tag_configure('tag_particle_correct', background='green', foreground="white",font=FONT_TAG)
    text_answer.tag_configure('tag_particle_incorrect', background='red', foreground="white",font=FONT_TAG)
    text_answer.tag_configure('tag_particle', font=("Meiryo", 12, "bold"))
    text_answer2.tag_configure('tag_particle_corrected', background='yellow', foreground="black", font=FONT_TAG2)
    text_answer2.tag_configure('tag_particle_correct', background='green', foreground="white",font=FONT_TAG2)
    text_answer2.tag_configure('tag_particle_incorrect', background='red', foreground="white",font=FONT_TAG2)
    text_answer2.tag_configure('tag_particle', font=("Meiryo", 12, "bold"))

    root.after(100, UI_user_mode_start)
    root.mainloop()
    



'''
parser = argparse.ArgumentParser()



parser.add_argument("--model_type", type=str, required=False)
parser.add_argument("--train_name", type=str, required=False)
parser.add_argument("--identifier_type", type=int, required=False)
parser.add_argument("--neighbour", type=int, required=False)
parser.add_argument("--total_sentence", type=int, required=False)
parser.add_argument("--particle_limit", type=int, required=False)

parser.add_argument("--fold", type=int, required=False)

parser.add_argument("--s_index", type=int, required=False)
parser.add_argument("--e_index", type=int, required=False)

parser.add_argument("--mode", type=int, required=True)
#1 - train_model          def train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit):
#2 - cross_train_model    def cross_train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold):
#3 - user_mode            def user_mode():
#4 - app_test             def app_test(s_index, e_index):

args = parser.parse_args()

mode = args.mode
_model_type = args.model_type
_train_name = args.train_name
_identifier_type = args.identifier_type
_neighbour = args.neighbour
_total_sentence = args.total_sentence
_particle_limit = args.particle_limit
_fold = args.fold
s_index = args.s_index
e_index = args.e_index

if(mode==1):
    train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit)
elif(mode==2):
    cross_train_model(_model_type, _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)
elif(mode==3):
    user_mode()
elif(mode==4):
    app_test(s_index, e_index)

elif(mode==5): #loop thingy (all shurui. but one model type)
    for i_loop in range(1, 3+1):
        for y_loop in range(1, 3+1):
            cross_train_model(_model_type, _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            
elif(mode==6): #loop thingy (all shurui, all model)
    for i_loop in range(1, 3+1):
        for y_loop in range(1, 3+1):
            cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==7): # singular - all model at once
    cross_train_model("lstm", _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)
    cross_train_model("func_lstm", _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)
    #cross_train_model("func_lstm_combined", _train_name, _identifier_type, _neighbour, _total_sentence, _particle_limit, _fold)

elif(mode==8):
    print("Time right now: ", datetime.datetime.now())

elif(mode==9): #SPECIAL MODE
    for i_loop in range(1, 3+1):
        for y_loop in range(1, 3+1):
            if(i_loop == 1 and y_loop == 1):
                continue
            cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==10): #SPECIAL MODE
    for i_loop in range(1, 3+1):
        for y_loop in range(1, 3+1):

            if(i_loop == 1 and y_loop == 1):
                pass
            else:
                cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==11): #SPECIAL MODE
    for i_loop in reversed(range(1, 3+1)):
        for y_loop in reversed(range(1, 3+1)):

            if(i_loop == 1 and y_loop == 1):
                continue

            if(i_loop == 1 and y_loop == 2):
                continue

            cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==12): #SPECIAL MODE
    for i_loop in reversed(range(1, 2+1)):
        for y_loop in reversed(range(1, 3+1)):

            if(i_loop == 1 and y_loop == 1):
                continue

            if(i_loop == 1 and y_loop == 2):
                continue

            cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==13): #SPECIAL MODE
    for i_loop in reversed(range(1, 3+1)):
        for y_loop in reversed(range(1, 3+1)):

            if(i_loop == 1 and y_loop == 3):
                cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
                cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
                cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            else:
                continue

elif(mode==14): #SPECIAL MODE
    for i_loop in reversed(range(1, 3+1)):
        for y_loop in reversed(range(1, 3+1)):

            if(i_loop == 3 and y_loop == 2):
                cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
                cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
                cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            else:
                continue

elif(mode==15): #SPECIAL MODE
    for i_loop in reversed(range(1, 3+1)):
        for y_loop in reversed(range(1, 3+1)):

            cross_train_model("lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)
            cross_train_model("func_lstm_combined", _train_name, i_loop, y_loop, _total_sentence, _particle_limit, _fold)

elif(mode==16):
    temp_app_test(s_index, e_index)
elif(mode==17):
    app_test(s_index, e_index, _train_name)

elif(mode==18):
    pass
'''

UI_user_mode()

