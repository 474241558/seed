#!/usr/bin/python
#-*-coding:utf-8-*-

from CaseResult import CaseResult
from Exceptions import FailReason
from Exceptions import CaseLoseArgumentException
from seed import seed_logger
from SeedLog import SeedLog
import time


class TestCase(object):

	'''
	测试用例类
	这里尽量做到与所有的业务用低耦合
	'''

	def __init__(self,case_dict,case_run_method = None):
		'''
		case_dict为Loader构建用例时传来的用例字典
		'''
		self.case_dict = case_dict
		self.argument_check(case_dict)
		self.__dict__.update(case_dict)
		self.case_run_method = case_run_method
		self.has_run = False
		self.case_log_path = ''


	def argument_check(self,case_dict):
		'''检查用例中的必要参数'''
		if not case_dict.has_key('id'):
			raise CaseLoseArgumentException('id')

		if not case_dict.has_key('desc'):
			raise CaseLoseArgumentException('desc')

	def __getattr__(self,attr):
		return getattr(attr)

	def run(self):
		self.has_run = True
		self.run_res = CaseResult(self)
		start_time = time.clock()
		try:
			SeedLog.rec_flag = True
			self.case_run_method(self)
		except Exception, e:
			self.run_res.passed = False
			self.run_res.why = FailReason(e)			#why是为什么失败,失败的原因
		finally:
			self.run_res.case_log = SeedLog.get_rec_log()
			SeedLog.clear_rec_log_arr()
			self.run_res.elapsed_ime = time.clock()-start_time
		return self.run_res