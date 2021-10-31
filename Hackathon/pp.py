import sqlite3
from pprint import pprint

import pandas
import csv

pn = pandas.read_excel('output_2.xlsx')

conn = sqlite3.connect('hahaton.sqlite')
cur = conn.cursor()

for i in range(len(pn)):
    r = pn.loc[i, :]
    coord1 = r['коорд1']
    coord2 = r['коорд2']
    street = r['улица']
    house = r['дом']
    date = '.'.join(r['дата'].split()[0].split('-'))
    MainCriterion = r['глав_параметр']
    SecondaryCriterion = r['под_параметр']
    problem = r['проблема']

    req = f"""SELECT id FROM streets
        WHERE street = '{street}'"""
    print(req)
    res = cur.execute(req).fetchall()
    print(f'{res=}')
    if len(res) == 0:
        cur.execute(
            f"""INSERT INTO streets(street) 
                    VALUES('{street}')"""
        )
        conn.commit()
        res = cur.execute(
            f"""SELECT id FROM streets
                    WHERE street = '{street}'"""
        ).fetchall()
        print(f'Create new street with id = {res[0][0]}')
    res = res[0]
    streetId = int(res[0])
    print(f'{streetId=}')

    res = cur.execute(
        f"""SELECT id FROM MainCriterion
        WHERE Name = '{MainCriterion}'"""
    ).fetchall()
    print(f'{res=}')
    if len(res) == 0:
        cur.execute(
            f"""INSERT INTO MainCriterion(Name) 
                    VALUES('{MainCriterion}')"""
        )
        conn.commit()
        res = cur.execute(
            f"""SELECT id FROM MainCriterion
            WHERE Name = '{MainCriterion}'"""
        ).fetchall()
        print(f'Create new MainCriterion with id = {res[0][0]}')
    res = res[0]
    MainCriterionId = int(res[0])
    print(f'{MainCriterionId=}')

    res = cur.execute(
        f"""SELECT id FROM SecondaryCriterion
            WHERE Name = '{SecondaryCriterion}' and MainCriterionId={MainCriterionId}"""
    ).fetchall()
    print(f'{res=}')
    if len(res) == 0:
        cur.execute(
            f"""INSERT INTO SecondaryCriterion(Name, MainCriterionId) 
                    VALUES('{SecondaryCriterion}', '{MainCriterionId}')"""
        )
        conn.commit()
        res = cur.execute(
            f"""SELECT id FROM SecondaryCriterion
                WHERE Name = '{SecondaryCriterion}' and MainCriterionId={MainCriterionId}"""
        ).fetchall()
        print(f'Create new SecondaryCriterion with id = {res[0][0]}')
    res = res[0]
    SecondaryCriterionId = int(res[0])
    print(f'{SecondaryCriterionId=}')

    request = f"""INSERT INTO problems(streetId, dom, coord1, coord2, time, problem, SecondaryCriterionId) 
               VALUES({streetId}, '{house}', '{coord1}', '{coord2}', '{date}', '{problem}', '{SecondaryCriterionId}');"""

    pprint(request)
    cur.execute(request)
    conn.commit()
