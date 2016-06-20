#!/usr/bin/python
#-*-coding:utf-8-*-

import traceback

class FailReason(object):
	def __init__(self, exc):
		self.traceback = traceback.format_exc(exc)
		self.message = exc.message

class CaseLoseArgumentException(Exception):
	'''用例参数异常'''
	def __init__(self,argument):
		self.msg = "Argument:[{0}] is Lose".format(argument)
		print self.msg
		