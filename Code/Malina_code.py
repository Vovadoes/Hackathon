import pandas as pd
import spacy
import pymorphy2
from CoordinatesAddress import find_coordinates
from settings import main_lst


def fun(d, s):
    res = []
    for k, v in d.items():
        if s in v:
            res.append(k)
    return res


def resulation(con):
    name1 = []
    name2 = []
    for i in con:
        for j in main_lst:
            s = fun(main_lst[j], i)
            if len(s) != 0:
                name1.append(j)
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


class Recognition:
    def __init__(self, input_way, output='output.xlsx'):
        self.input_way = input_way
        self.output = output
        self.len_df = 0

    def main(self, fun=lambda j, i, len_df: None):
        df = pd.read_excel(self.input_way)
        # df.drop_duplicates(subset='текст обращения', inplace = True)
        df2 = pd.DataFrame()
        qq = ['коорд1', 'коорд2', 'улица', 'дом', 'дата', 'глав_параметр', 'под_параметр',
              'проблема']
        for i in qq:
            df2[i] = []
        self.len_df = len(df)
        for i in range(self.len_df):
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
                    print(f'{i=}, {res=}')
                    fun(*(i, self.len_df))
                    df2.loc[len(df2), :] = res
        df2.to_excel(self.output)
        return self.output
