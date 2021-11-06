import sqlite3
from pprint import pprint
import pandas
from settings import main_dct, way_db


def fun(conn, cur, name_table='streets', where="street = 'улица Бичурина'",
        create_new=('street', "'улица Бичурина'")):
    request = f"""SELECT id FROM {name_table}
            WHERE {where}"""
    # print(request)
    # pprint(f'{request=}')
    result = cur.execute(request).fetchall()  # SELECT
    # pprint(f'{result=}')
    if len(result) == 0:
        request_create = f"""INSERT INTO {name_table}({create_new[0]}) 
                        VALUES({create_new[1]})"""
        # pprint(f'{request_create=}')
        cur.execute(request_create)  # INSERT INTO
        conn.commit()
        result = cur.execute(request).fetchall()  # SELECT
    id = int(result[0][0])
    # pprint(f'{where=}: {id=}')
    return id


def start(way):
    print('start create db')
    pn = pandas.read_excel(way)

    conn = sqlite3.connect(way_db)
    cur = conn.cursor()

    for i in range(len(pn)):
        r = pn.loc[i, :]
        coord1 = r['коорд1']
        coord2 = r['коорд2']
        street = r['улица']
        house = r['дом']
        date = '.'.join(r['дата'].split()[0].split('-'))
        MainCriterions = r['глав_параметр'].split(', ')
        SecondaryCriterions = r['под_параметр'].split(', ')
        problem = r['проблема']
        for MainCriterion in MainCriterions:
            streetId = fun(conn, cur, 'streets', f"street = '{street}'", ('street', f"'{street}'"))

            MainCriterionId = fun(conn, cur, 'MainCriterion', f"Name = '{MainCriterion}'",
                                  ('Name', f"'{MainCriterion}'"))

            ProblemId = fun(conn, cur, 'problems', f"problem = '{problem}'", (
                'streetId, dom, coord1, coord2, time, problem',
                f"{streetId}, '{house}', '{coord1}', '{coord2}', '{date}', '{problem}'"))

            for SecondaryCriterion in SecondaryCriterions:
                if SecondaryCriterion in main_dct[MainCriterion]:
                    SecondaryCriterionId = fun(conn, cur, 'SecondaryCriterion',
                                               f"Name = '{SecondaryCriterion}' and MainCriterionId={MainCriterionId}",
                                               ('Name, MainCriterionId',
                                                f"'{SecondaryCriterion}', {MainCriterionId}"))

                    req = fun(conn, cur, 'Main',
                              f"ProblemId = {ProblemId} AND SecondaryCriterionId = {SecondaryCriterionId}",
                              ('ProblemId, SecondaryCriterionId',
                               f"{ProblemId}, {SecondaryCriterionId}"))
                    # request = f"""INSERT INTO Main(ProblemId, SecondaryCriterionId)
                    #            VALUES({ProblemId}, {SecondaryCriterionId}); """

                    # pprint(request)
                    # cur.execute(request)
                    conn.commit()
    print('end create db')

# start('output.xlsx')
