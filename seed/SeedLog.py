#!/usr/bin/python
#-*-coding:utf-8-*-

import logging

class SeedLog(object):
	"""docstring for SeedLog"""
	logger = None
	rec_flag = False
	rec_log_arr = []

	def __init__(self):
		self.initLog()

	def initLog(self):
		SeedLog.logger = logging.getLogger('seed_log')
		SeedLog.logger.setLevel(logging.DEBUG)
		fh = logging.FileHandler('seed.log')
		fh.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		SeedLog.logger.addHandler(fh)
		SeedLog.logger.addHandler(ch)

	def info(self,log_msg):
		if SeedLog.rec_flag:
			SeedLog.logger.info(log_msg)
			SeedLog.rec_log_arr.append(log_msg)
		else:
			SeedLog.logger.info(log_msg)

	@staticmethod
	def clear_rec_log_arr():
		SeedLog.rec_log_arr = []
		SeedLog.rec_flag = False

	@staticmethod
	def get_rec_log():
		return SeedLog.rec_log_arr




		