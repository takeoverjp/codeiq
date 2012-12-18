# coding: UTF-8

"""
[INPUT]
 - customer_list
    顧客ID	顧客名	購買実績（;区切り）

 - sales_ranking
    ランク	書名	ジャンル

[OUTPUT]
 - python recommend.py CodeIQ_customer_list_utf8.txt CodeIQ_sales_ranking_utf8.txt 
    customer1 : book11, book12, book13
    customer2 : book21, book22, book23
    customer3 : book31, book32, book33

[ALGORYTHM]
 1. ジャンルを各顧客の購買履歴に応じて順位付け
   1.1. もっとも最近購入したジャンルに+1
   1.2. 次に最近購入したジャンルに+HIS_WEIGHT   （0<HIS_WEIGHT<1）
   1.3. 次に最近購入したジャンルに+HIS_WEIGHT^2
   1.4. 次に最近購入したジャンルに+HIS_WEIGHT^3
               ・
               ・
               ・
 2. 1.で求めた１位のジャンルの中で売り上げの多い順にrecommend_listに追加
 3. 1.で求めた２位のジャンルの中で売り上げの多い順にrecommend_listに追加
             ・
             ・
             ・
 4. 好みのジャンルがなくなったら、売り上げの多い順にrecommend_listに追加
"""

import sys
from operator import itemgetter

HIS_WEIGHT = 0.9

class Customer:
    def __init__(self, name, history):
        self.name = name
        self.__history = history
        self.__favorites = self.__get_favorites(history)

    def __get_favorites(self, history):
        # ALGORYTHM-1
        score = {}
        for genre in history:
            score[genre] = 0.0
        for i, genre in enumerate(history):
            score[genre] += HIS_WEIGHT ** i
            i += 1

        favorites = []
        for ge, sc in sorted(score.items(), key=itemgetter(1), reverse=True): #sort by score
            favorites.append(ge)
            #print self.name + " : " + ge + ", " + "%s" % sc
        return favorites

    def get_recommends(self, sales_rank_list):
        recommends = []

        # ALGORYTHM-2,3
        for fav in self.__favorites:
            for book in sales_rank_list:
                if book["genre"] == fav:
                    recommends.append(book["name"])
                    #print self.name + " : " + book["name"]

        # ALGORYTHM-4
        for book in sales_rank_list:
            is_recommended = False
            for rec in recommends:
                if rec == book["name"]:
                    is_recommended = True
            if not is_recommended:
                recommends.append(book["name"])
                #print self.name + " : " + book["name"]
            
        return recommends
        

def parse_customer_list(fname):
    cus_dict = {}
    for i, line in enumerate(open(fname, 'r')):
        if (i == 0):
            continue
        cus_list = line[:-1].split('\t')
        id = cus_list[0]
        name = cus_list[1]
        history = cus_list[2].split(';')
        extra_dict = {id: Customer(name, history)}
        cus_dict.update(extra_dict)

    return cus_dict

def parse_sales_ranking(fname):
    list = []
    for i, line in enumerate(open(fname, 'r')):
        if (i == 0):
            continue
        book_list = line[:-1].split('\t')
        
        book_dict = {"name": book_list[1], "genre": book_list[2]}
        list.append(book_dict)

    return list



if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 3):
        print 'Usage: "python %s customer_list sales_ranking' % argvs[0]
        quit()

    clist_fname = argvs[1]
    sales_rank_fname = argvs[2]

    customer_dict = parse_customer_list(clist_fname)
    sales_rank_list = parse_sales_ranking(sales_rank_fname)

    for cus in customer_dict.values():
        rec = cus.get_recommends(sales_rank_list)
        print cus.name + " : " + rec[0] + ", " + rec[1] + ", " + rec[2]
