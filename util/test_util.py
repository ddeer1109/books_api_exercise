from datetime import date
from unittest import TestCase

import util


class Test(TestCase):

    def test_parse_date(self):
        date1 = "2020-01-01"
        assert util.parse_date(date1) == date(2020, 1, 1)

        date2 = "2020-03"
        date4 = "2020"
        self.assertTrue(util.parse_date(date2) == date(2020, 3, 1))
        self.assertTrue(util.parse_date(date4) == date(2020, 1, 1))

        date3 = "20222"
        date5 = "2020-0f-1"
        date6 = "2020-00--1"
        date7 = "20-11-2000"
        none_date = None
        num_date = 20200101
        self.assertRaises(ValueError, util.parse_date, date3)
        self.assertRaises(ValueError, util.parse_date, date5)
        self.assertRaises(ValueError, util.parse_date, date6)
        self.assertRaises(ValueError, util.parse_date, date7)
        self.assertRaises(TypeError, util.parse_date, none_date)
        self.assertRaises(TypeError, util.parse_date, num_date)

    def test_filter_out_empty_dict_entries(self):
        dictionary = {"key1": "", "key2": None, "key3": "non-empty"}
        cleaned = util.filter_out_empty_dict_entries(dictionary)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.get("key1"), None)
