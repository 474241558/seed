#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'feixu@iflytek.com'

from TestCase import TestCase
from seed import seed_logger
import time
import sys
import os

class TestSuit(object):

	'''
	测试集类
	'''
	test_suit_arr = []
	def __init__(self,suit_name,suit_setup = None,suit_teardown = None):
		if TestSuit.is_exists(suit_name):
			sys.exit("no test suit and case!")
		seed_logger.info("create test suit:{0}".format(suit_name))
		self.suit_name = suit_name
		self.suit_setup = suit_setup
		self.suit_teardown = suit_teardown
		self.test_case_arr = []
		self.suit_log_dir = os.path.join('logs',suit_name)
		TestSuit.test_suit_arr.append(self)

	@staticmethod
	def is_exists(suit_n):
		flag = False
		for suit in TestSuit.test_suit_arr:
			if suit.suit_name == suit_n:
				flag = True
		return flag


	def add_case(self,test_case_dict,case_run_fun):
		self.test_case_arr.append(TestCase(test_case_dict,case_run_method = case_run_fun))
		seed_logger.info("create test case id:[{0}] in suit:[{1}]".format(test_case_dict['id'],self.suit_name))

	@staticmethod
	def get_all_case():
		case_arr = []
		for suit in TestSuit.test_suit_arr:
			for case in suit.test_case_arr:
				case_arr.append(case)

		return case_arr

