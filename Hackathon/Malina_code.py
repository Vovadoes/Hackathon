import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import pymorphy2
from geopy.geocoders import Nominatim
from typing import Tuple
from Maps import find_coordinates
from settings import unpleasant_smell, roads_and_transport, yard, landscaping

from Create_db import start


def ssdd(d, s):
    res = []
    for k, v in d.items():
        if s in v:
            res.append(k)
    return res


def resulation(con):
    name1 = []
    name2 = []
    # ['ремонт', 'третий']
    for i in con:
        s = ssdd(unpleasant_smell, i)
        if len(s) != 0:
            name1.append('неприятный запах')
            name2 += s

        s = ssdd(roads_and_transport, i)
        if len(s) != 0:
            name1.append('дороги и транспорт')
            name2 += s

        s = ssdd(yard, i)
        if len(s) != 0:
            name1.append('содержание двора')
            name2 += s

        s = ssdd(landscaping, i)
        if len(s) != 0:
            name1.append('благоустройство')
            name2 += s
    return list(set(name1)), list(set(name2))


def pre_resulation(content):
    nlp = spacy.load('en_core_web_sm')  # python -m spacy download en_core_web_sm
    doc = nlp(content := content.lower())
    sentences = []
    morph = pymorphy2.MorphAnalyzer()
    for sent in doc.sents:
        selected_words = []
        for token in sent:
            if token.is_stop is False:
                selected_words.append(morph.parse(str(token))[0].normal_form)
        sentences += selected_words
    q = []
    for i in sentences:
        r = morph.parse(i)[0]
        # print(r.tag.POS, end=', ')
        if r.tag.POS in ['NOUN', 'ADJF']:
            q.append(i)
    # print(sentences)
    return q


def main(input_way, output='output.xlsx'):
    df = pd.read_excel(input_way)
    # df.drop_duplicates(subset='текст обращения', inplace = True)
    df2 = pd.DataFrame()
    qq = ['коорд1', 'коорд2', 'улица', 'дом', 'дата', 'глав_параметр', 'под_параметр', 'проблема']
    for i in qq:
        df2[i] = []
    for i in range(len(df)):
        print(i)
        al = df.loc[i, :]
        content = al['текст обращения'].lower()
        arr = resulation(pre_resulation(content))
        a1 = ', '.join(arr[0])
        a2 = ', '.join(arr[1])
        if len(arr[0]) != 0:
            coord = find_coordinates(
                'Чувашская республика ' + ', '.join([al['Адрес обращения'], al['Дом']]))
            if coord:
                res = list(coord) + [al['Адрес обращения'], al['Дом'],
                                     str(al['Дата'])[:-7]] + [a1, a2] + [al['текст обращения']]
                print(res)
                df2.loc[len(df2), :] = res
    df2.to_excel(output)
    start(output)
