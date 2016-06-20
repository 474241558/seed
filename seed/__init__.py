#!/usr/bin/python
#-*-coding:utf-8-*-
__version__ = '3.0.0'

world = {}
seed_setup = None
seed_teardown = None
import os
import sys
# seed_logger = None

# def initLog():
# 	global seed_logger
# 	seed_logger = logging.getLogger('seed_log')
# 	seed_logger.setLevel(logging.DEBUG)
# 	fh = logging.FileHandler('seed.log')
# 	fh.setLevel(logging.DEBUG)
# 	ch = logging.StreamHandler()
# 	ch.setLevel(logging.DEBUG)
# 	formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
# 	fh.setFormatter(formatter)
# 	ch.setFormatter(formatter)
# 	seed_logger.addHandler(fh)
# 	seed_logger.addHandler(ch)

# initLog()

cur_dir = os.getcwd()
case_fun_dir = os.path.join(cur_dir,'case_fun')
if os.path.exists(case_fun_dir):
	for dirName, subdirList, fileList in os.walk(case_fun_dir): 
		sys.path.insert(0, dirName)
		for fname in fileList:
			file_name_wo_ext = os.path.splitext(fname)[0]
			exec("from {0} import *".format(file_name_wo_ext))
			print "import {0} module all methods".format(file_name_wo_ext)

from SeedLog import SeedLog
seed_logger = SeedLog()
import optparse
from TestSuit import TestSuit
from Runner import Runner
from Report import ReportFactory
import sys

total_res = None

def run(args=sys.argv[1:]):
	global total_res
	parser = optparse.OptionParser()
	parser.add_option("-t", "--tag",
						dest="tags",
						default=None,
						action='append',
						help='Use case tag filter,eg:-t smoke -t module1 ,it is filter case tag contain smoke or module1 and run it')

	parser.add_option("-f","--failfast",
						dest="failfast",
						default=False,
						action="store_true",
						help='When the case is executed, the exception is stopped immediately.')

	parser.add_option("-r","--rerun",
						dest="rerun",
						default=False,
						action="store_true",
						help='The last failed case to run again')

	parser.add_option("-o","--out_type",
						dest="out_type",
						default="cmd",
						type="string",
						help='Type of output result')

	options, args = parser.parse_args(args)

	if (not TestSuit.test_suit_arr) and (not TestSuit.test_suit_arr[0].test_case_arr):
		sys.exit("no test suit and case!")

	if options.tags:
		for test_case in TestSuit.get_all_case():
			if not test_case.case_dict.has_key('tags'):
				sys.exit("caseId:[{0}] test case have no tags!".format(test_case.id))

	for test_case in TestSuit.get_all_case():
		if not test_case.case_run_method:
			sys.exit("caseId:[{0}] has no test case run method!".format(test_case.id))

	runner = Runner(TestSuit.test_suit_arr, options.tags, options.failfast, options.rerun, options.out_type)
	total_res = runner.run()

	report_obj = ReportFactory.create_report(options.out_type,total_res)
	report_obj.out_put_report()

