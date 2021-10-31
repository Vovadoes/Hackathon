import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import pymorphy2
from geopy.geocoders import Nominatim
from typing import Tuple

unpleasant_smell = dict({
    'неприятный запах': ['неприятный', 'запах', 'вонь'], 'мусор': ['мусор']
})
roads_and_transport = dict({
    'дорога': ['дорога', 'тротуар', 'бордюр', 'лежачий', 'полицейский', 'остановка', 'пешеходный']
})

yard = dict({
    'парковочное место': ['парковочный', 'место', 'автостоянка'],
    'электроника дома': ['провод', 'щиток'], 'скамейка': ['скамейка'],
    'спортивная площадка': ['спорт', 'площадка', 'тренажёр', 'баскетбольный', 'волейбольный', 'хоккейный'],
    'детская площадка': ['детский', 'площадка'],
    'вода': ['разводка', 'вода']
})
landscaping = dict({
    'парк': ['парк'], 'садик': ['садик'], 'свет': ['свет', 'фонарь', 'освещение', 'лампочка'],
    'развлечения': ['клуб'], 'озеленение': ['кустарник', 'газон', 'сад', 'зелёный'],
    'зрдавоохранение': ['аптечный', 'пункт', 'стоматология', 'здоровье', 'лекарство', 'медицинский', 'заболевание',
                        'ковид', 'педиатор'],
    'каток': ['каток'], 'школа': ['школа'], 'банкомат': ['банкомат']
})


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
    content = content.lower()
    doc = nlp(content)
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


s = pre_resulation('Нужны дополнительные парковочные места.')
print(s)
resulation(s)


# @title Текст заголовка по умолчанию
def find_coordinates(location: str = "улица Алексея Талвира, 20"):
    # address we need to geocode
    loc = location

    # making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")

    # applying geocode method to get the location
    location = geolocator.geocode(loc)
    # print(location)
    # printing address and coordinates
    if location:
        # print((location.latitude, location.longitude))
        return (location.latitude, location.longitude)
    return None


load_way = "table.xlsx"
save_way = "output_test.xlsx"

df = pd.read_excel(load_way)
# df.drop_duplicates(subset='текст обращения', inplace = True)
df2 = pd.DataFrame()
qq = ['коорд1', 'коорд2', 'улица', 'дом', 'дата', 'глав_параметр', 'под_параметр', 'проблема']
for i in qq:
    df2[i] = []
for i in range(4000):
    print(i)
    al = df.loc[i, :]
    content = al['текст обращения'].lower()
    arr = resulation(pre_resulation(content))
    a1 = ', '.join(arr[0])
    a2 = ', '.join(arr[1])
    if len(arr[0]) != 0:
        coord = find_coordinates('Чувашская республика ' + ', '.join([al['Адрес обращения'], al['Дом']]))
        if coord:
            res = list(coord) + [al['Адрес обращения'], al['Дом'], str(al['Дата'])[:-7]] + [a1, a2] + [
                al['текст обращения']]
            print(res)
            df2.loc[len(df2), :] = res
    # (['дороги и транспорт'], ['дорога'])
# for i in qq:
#  df2[i] = []
# df2.loc[len(df2), :] = ['1', '1', '1', '1', '1', '1', '1']
df2.to_excel("save_way")
