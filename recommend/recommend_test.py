# coding: UTF-8

import unittest
from recommend import HISTORY_WEIGHT, memoized_weight, Customer, parse_customer_list, parse_sales_ranking

class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_memoized_weight(self):
        for i in range(100):
            for j in range(-100, 100):
                ans = HISTORY_WEIGHT ** j
                self.assertEqual(memoized_weight(j), ans)

    def test_parse_customer_list(self):
        customer_dict = parse_customer_list("CodeIQ_customer_list_utf8.txt")
        self.assertIsInstance(customer_dict["001"], Customer)
        self.assertIsInstance(customer_dict["002"], Customer)
        self.assertIsInstance(customer_dict["003"], Customer)
        self.assertIsInstance(customer_dict["004"], Customer)
        self.assertIsInstance(customer_dict["005"], Customer)
        self.assertIsInstance(customer_dict["006"], Customer)
        self.assertEqual(customer_dict["001"].name, u"太郎")
        self.assertEqual(customer_dict["002"].name, u"次郎")
        self.assertEqual(customer_dict["003"].name, u"陽子")
        self.assertEqual(customer_dict["004"].name, u"おさむ")
        self.assertEqual(customer_dict["005"].name, u"美香")
        self.assertEqual(customer_dict["006"].name, u"華子")

    def test_parse_customer_list_invalid_input_file(self):
        self.assertRaises(UnicodeDecodeError,
                          parse_customer_list, "CodeIQ_customer_list_sjis.txt")
        self.assertRaises(IndexError,
                          parse_customer_list, "CodeIQ_customer_list_invalid.txt")
        self.assertRaises(IOError,
                          parse_customer_list, "CodeIQ_customer_list_nosuch.txt")

    def test_parse_sales_ranking(self):
        sales_rank_list = parse_sales_ranking("CodeIQ_sales_ranking_utf8.txt")
        ans = [{"name": u"1週間で200万円貯める！", "genre": u"一般"},
               {"name": u"サンフランシスコの老人", "genre": u"文学"},
               {"name": u"もうPythonしか愛せない", "genre": u"技術"},
               {"name": u"2013年の運勢", "genre": u"一般"},
               {"name": u"デフレと政治", "genre": u"経済"},
               {"name": u"これからのインド市場と日本", "genre": u"経済"},
               {"name": u"なんでもPythonプログラミング", "genre": u"技術"},
               {"name": u"墨堤通り物語", "genre": u"文学"},
               {"name": u"日本のがん医療", "genre": u"一般"},
               {"name": u"Pythonを加速するためのC++", "genre": u"技術"},
               {"name": u"徳島阿波踊り空港殺人事件", "genre": u"文学"},
               {"name": u"老後に備える外貨預金の真実", "genre": u"経済"},
               {"name": u"もてる！話し方入門", "genre": u"一般"},
               {"name": u"井戸水の中のバクテリア", "genre": u"文学"},
               {"name": u"土俵際の日本経済「再生への道筋」", "genre": u"経済"}]
        for i, book in enumerate(sales_rank_list):
            self.assertEqual(book, ans[i])

    def test_parse_sales_ranking_invalid_input_file(self):
        self.assertRaises(UnicodeDecodeError,
                          parse_sales_ranking, "CodeIQ_sales_ranking_sjis.txt")
        self.assertRaises(IndexError,
                          parse_sales_ranking, "CodeIQ_sales_ranking_invalid.txt")
        self.assertRaises(IOError,
                          parse_sales_ranking, "CodeIQ_sales_ranking_nosuch.txt")

    def test_customer_recommends(self):
        customer_dict = parse_customer_list("CodeIQ_customer_list_utf8.txt")
        sales_rank_list = parse_sales_ranking("CodeIQ_sales_ranking_utf8.txt")

        ans = {u"陽子": [u"サンフランシスコの老人",
                         u"墨堤通り物語",
                         u"徳島阿波踊り空港殺人事件"],
               u"次郎": [u"もうPythonしか愛せない",
                         u"なんでもPythonプログラミング",
                         u"Pythonを加速するためのC++"],
               u"太郎": [u"デフレと政治",
                         u"これからのインド市場と日本",
                         u"老後に備える外貨預金の真実"],
               u"華子": [u"サンフランシスコの老人",
                         u"墨堤通り物語",
                         u"徳島阿波踊り空港殺人事件"],
               u"美香": [u"サンフランシスコの老人",
                         u"墨堤通り物語",
                         u"徳島阿波踊り空港殺人事件"],
               u"おさむ": [u"もうPythonしか愛せない",
                           u"なんでもPythonプログラミング",
                           u"Pythonを加速するためのC++"]}

        for cus in customer_dict.values():
            self.assertEqual(ans[cus.name],
                             cus.get_recommends(sales_rank_list)[:3])

if __name__ == '__main__':
    unittest.main()
