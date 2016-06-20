#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import time
import seed
import codecs
from TestSuit import TestSuit
from TotalResult import TotalResult
from seed import seed_logger
import logging

'''
Runner是运行器类，主要用来处理suit、test 根据传入的参数配置进行运行的逻辑处理
'''

class Runner(object):

	def __init__(self,suit_arr,tags,failfast,rerun,out_type):

		self.suit_arr = suit_arr
		self.tags = tags
		self.failfast = failfast
		self.rerun = rerun
		self.out_type = out_type

		self.rerun_case_id_arr = []
		if self.rerun:
			if os.path.exists('last_time_fail.txt'):
				fail_case_fo = codecs.open('last_time_fail.txt','r','utf-8')
				self.rerun_case_id_arr =  map(lambda x:x.strip(),filter(lambda x:x.strip(),fail_case_fo.readlines()))
				fail_case_fo.close()
		self.recombine_suits()

	def is_in_tags(self,tags_str):
		return filter(lambda x:x,[x if x in tags_str else None for x in self.tags])

	def recombine_suits(self):
		test_suits = TestSuit.test_suit_arr
		n = len(test_suits)
		while n:
			suit = test_suits[n-1]
			test_cases = suit.test_case_arr
			i = len(test_cases)
			while i:
				seed_logger.info("******test case id [{0}].".format(test_cases[i-1].id))
				seed_logger.info("******test case can run?: [{0}].".format(self.check_case_can_rerun(test_cases[i-1])))
				seed_logger.info("******test case tag can run?: [{0}].".format(self.check_case_tag_can_run(test_cases[i-1])))
				if not self.check_case_can_rerun(test_cases[i-1]) or not self.check_case_tag_can_run(test_cases[i-1]):
					seed_logger.info("remove a test case [{0}].".format(test_cases[i-1].id))
					del test_cases[i-1]
				i -= 1
			if not suit.test_case_arr:
				seed_logger.info("test suit lenth is [{0}],remove a test suit [{1}].".format(len(suit.test_case_arr),suit.suit_name))
				TestSuit.test_suit_arr.remove(suit)
			n -= 1

	def check_case_can_rerun(self,test_case):
		if not self.rerun:
			return True
		if not self.rerun_case_id_arr:
			return True
		if self.rerun and test_case.id in self.rerun_case_id_arr:
			return True
		else:
			return False

	def init_log_config(self,log_file_name):
		logging.root.handlers = []
		#############################################################################
		logging.basicConfig(level=logging.DEBUG,
		                format='[%(asctime)s][%(levelname)s]:%(message)s',
		                datefmt='%Y-%m-%d %H:%M:%S',
		                filename=log_file_name,
		                filemode='a')

		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)
		formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)
		##############################################################################

	def check_case_tag_can_run(self,test_case):
		if not self.tags:
			return True
		if self.tags and filter(lambda x:x,[x if x in test_case.tags else None for x in self.tags]):
			return True
		else:
			return False

	def run(self):

		last_time_fail_case_fo = codecs.open('last_time_fail.txt','w','utf-8')
		
		seed_logger.info("Start run all test case.")
		run_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		start_time = time.clock()

		if(seed.seed_setup):
			seed.seed_setup()

		for suit in TestSuit.test_suit_arr:
			if not os.path.exists(suit.suit_log_dir):
				os.makedirs(suit.suit_log_dir)

			suit_log_file_name = os.path.join(suit.suit_log_dir,suit.suit_name+'.log')
			self.init_log_config(suit_log_file_name)
			logging.info("*"*20+"["+suit.suit_name+' begin time:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+']'+"*"*20)
			
			if(suit.suit_setup):
				suit.suit_setup()

			for test_case in suit.test_case_arr:
				
				run_res = None
				if self.check_case_can_rerun(test_case) and self.check_case_tag_can_run(test_case):
					test_case.case_log_path = os.path.join(suit.suit_log_dir,test_case.id+'.log')
					self.init_log_config(test_case.case_log_path)
					logging.info("*"*20+"["+test_case.desc+' begin time:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+']'+"*"*20)
					
					seed_logger.info("Start run case id [{0}].".format(test_case.id))

					run_res = test_case.run()

					seed_logger.info("case id [{0}] run finished.".format(test_case.id))

					logging.info("*"*20+"["+test_case.desc+' end time:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+']'+"*"*20+'\n'*2)
					logging.root.handlers = []
				else:
					seed_logger.info("case id [{0}] is filtered.".format(test_case.id))
					continue

				if not run_res.passed:
					last_time_fail_case_fo.write("{0}\n".format(test_case.id))

			if(suit.suit_teardown):
				suit_log_file_name = os.path.join(suit.suit_log_dir,suit.suit_name+'.log')
				self.init_log_config(suit_log_file_name)
				suit.suit_teardown()
			logging.info("*"*20+"["+suit.suit_name+' end time:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+']'+"*"*20+'\n'*2)
			logging.root.handlers = []

		if(seed.seed_teardown):
			seed.seed_teardown()

		end_time = time.clock()
		seed_logger.info("All test case run finished.")
		last_time_fail_case_fo.close()
		return TotalResult(TestSuit.test_suit_arr,end_time-start_time,run_time)

		






