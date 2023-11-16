# encoding=utf-8

"""

@author: SimmerChan

@contact: hsl7698590@gmail.com

@file: jena_sparql_endpoint.py

@time: 2017/12/20 14:49

@desc:利用SOARQKWrapper向Fuseki发送SPARQL查询，解析返回的结果

"""

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict


SPARQL_PREXIX = u"""
PREFIX : <http://www.kgdemo.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

class JenaFuseki:
    def __init__(self, endpoint_url='http://localhost:3030/kg_demo_movie/query'):
        self.sparql_conn = SPARQLWrapper(endpoint_url)

    def get_sparql_result(self, query):
        self.sparql_conn.setQuery(query)
        self.sparql_conn.setReturnFormat(JSON)
        return self.sparql_conn.query().convert()

    @staticmethod
    def parse_result(query_result):
        """
        解析返回的结果
        :param query_result:
        :return:
        """
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]['value']
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            return None, query_result['boolean']

    def print_result_to_string(self, query_result):
        """
        直接打印结果，用于测试
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)

        if query_head is None:
            if query_result is True:
                print('Yes')
            else:
                print('False')
        else:
            for h in query_head:
                print(h, ' ' * 5, end="")
            print()
            for qr in query_result:
                for _, value in qr.items():
                    print(value, ' ', end="")
                print()

    def get_sparql_result_value(self, query_result):
        """
        用列表存储结果的值
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)
        if query_head is None:
            return query_result
        else:
            values = list()
            for qr in query_result:
                for _, value in qr.items():
                    values.append(value)
            return values


def has_actor_question(word):
    """
    哪些演员参演了某电影
    :param word_objects:
    :return:
    """
    select = u"?x"

    sparql = None
    e = u"?m :movieTitle '{movie}'." \
        u"?m :hasActor ?a." \
        u"?a :personName ?x".format(movie=word)

    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                      select=select,
                                      expression=e)

    return sparql

def has_movie_question(word):
    """
    某演员演了什么电影
    :param word_objects:
    :return:
    """
    select = u"?x"

    sparql = None
    e = u"?s :personName '{person}'." \
        u"?s :hasActedIn ?m." \
        u"?m :movieTitle ?x".format(person=word)

    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                      select=select,
                                      expression=e)
    return sparql

def has_cooperation_question(word, word_extra):
    """
    演员A和演员B有哪些合作的电影
    :param word_objects:
    :return:
    """
    select = u"?x"

    person1 = None
    person2 = None


    e = u"?p1 :personName '{person1}'." \
        u"?p2 :personName '{person2}'." \
        u"?p1 :hasActedIn ?m." \
        u"?p2 :hasActedIn ?m." \
        u"?m :movieTitle ?x".format(person1=word, person2=word_extra)

    return SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                      select=select,
                                      expression=e)


def has_movie_type_question(word):
    """
    某演员演了哪些类型的电影
    :param word_objects:
    :return:
    """
    select = u"?x"

    sparql = None

    e = u"?s :personName '{person}'." \
        u"?s :hasActedIn ?m." \
        u"?m :hasGenre ?g." \
        u"?g :genreName ?x".format(person=word)

    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                      select=select,
                                      expression=e)
    return sparql

def has_specific_type_movie_question(word, word_extra):
    """
    某演员演了什么类型（指定类型，喜剧、恐怖等）的电影
    :param word_objects:
    :return:
    """
    select = u"?x"


    sparql = None
    e = u"?s :personName '{person}'." \
        u"?s :hasActedIn ?m." \
        u"?m :hasGenre ?g." \
        u"?g :genreName '{keyword}'." \
        u"?m :movieTitle ?x".format(person=word, keyword=word_extra)

    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                      select=select,
                                      expression=e)
    return sparql


def question():
    num = 1
    while num != 0:
        print("please input the number of question")
        print("0 for exit")
        print("1 for input a movie name to search who act in")
        print("2 for input an actor name to search his or her movie")
        print("3 for input two actor names to search which movie they act together")
        print("4 for input an actor name to search the genres of movies he or she has acted in")
        print("5 for input an actor name and a genre to search the movies which has the input genre and he or she has acted in")
        num = input()
        if num == '0':
            break
        if num == '1':
            word = input()
            my_query = has_actor_question(word)
        if num == '2':
            word = input()
            my_query = has_movie_question(word)
        if num == '3':
            word = input()
            word_extra = input()
            my_query = has_cooperation_question(word, word_extra)
        if num == '4':
            word = input()
            my_query = has_movie_type_question(word)
        if num == '5':
            word = input()
            word_extra = input()
            my_query = has_specific_type_movie_question(word, word_extra)
        fuseki = JenaFuseki()
        result = fuseki.get_sparql_result(my_query)
        fuseki.print_result_to_string(result)

# TODO 用于测试
if __name__ == '__main__':
    # fuseki = JenaFuseki()
    # my_query = has_movie_question("张曼玉")
    # result = fuseki.get_sparql_result(my_query)
    # fuseki.print_result_to_string(result)
    question()