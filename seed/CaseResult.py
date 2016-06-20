#!/usr/bin/python
#-*-coding:utf-8-*-

class CaseResult(object):
	"""docstring for CaseResult"""
	def __init__(self,test_case):
		self.test_case = test_case
		self.passed = True
		self.why = None
		self.elapsed_time = 0
		self.case_log = None
		