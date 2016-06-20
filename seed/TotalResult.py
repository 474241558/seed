#!/usr/bin/python
#-*-coding:utf-8-*-

class TotalResult(object):
	"""最终结果类，封装一些对最终结果的一些常用操作"""
	def __init__(self, suit_arr,run_all_case_elapsed_time,run_time):
		self.suit_arr = suit_arr
		self.run_time = run_time
		self.run_all_case_elapsed_time = run_all_case_elapsed_time
		self.results = []
		for suit in suit_arr:
			for test_case in suit.test_case_arr:
				if(test_case.has_run):
					self.results.append(test_case.run_res)

	def passed(self):
		'''本次测试是否通过'''
		passed = True
		for res in self.results:
			if not res.passed:
				passed = False
		return passed

	def get_json_res(self):
		res_dict = {}
		for suit in self.suit_arr:
			res_dict[suit.suit_name] = []
			for test_case in suit.test_case_arr:
				case_res_dict = {}
				case_res_dict["id"] = test_case.id
				case_res_dict['desc']=test_case.desc
				case_res_dict["has_run"] = test_case.has_run
				case_res_dict["run_res"] = {}
				case_res_dict["run_res"]["why"] = {}
				case_res_dict["run_res"]["case_log"] = []
				if(test_case.has_run):
					case_res_dict["run_res"]["passed"] = test_case.run_res.passed
					case_res_dict["run_res"]["elapsed_ime"] = test_case.run_res.elapsed_time
					if(test_case.run_res.why):
						case_res_dict["run_res"]["why"]["traceback"] = test_case.run_res.why.traceback
						case_res_dict["run_res"]["why"]["message"] = test_case.run_res.why.message
					if(test_case.run_res.case_log):
						case_res_dict["run_res"]["case_log"] = test_case.run_res.case_log
				res_dict[suit.suit_name].append(case_res_dict)
		return res_dict

	def get_all_run_count(self):
		return len(self.results)

	def get_passed_count(self):
		return len(self.get_passed_res())

	def get_failed_count(self):
		return len(self.get_failed_res())

	def get_skip_case_count(self):
		sum = 0
		for suit in self.suit_arr:
			for test_case in suit.test_case_arr:
				if not test_case.has_run:
					sum+=1
		return sum


	def get_passed_res(self):
		return filter(lambda x:x.passed,self.results)

	def get_failed_res(self):
		return filter(lambda x:not x.passed,self.results)
