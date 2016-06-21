#!/usr/bin/env python
# -*- coding: utf-8 -*-

import seed
from seed import TestSuit
import logging

#假设这是开发的接口【想象成各种形式，jar包、dll、http接口等等】
def add(a,b):
	return 1+1

#假设这是我们的测试方法，用来测试add这个接口的测试方法
def test_add(test_case):
	
	#从用例中获取数值1
	num1 = test_case.n1

	#从用例中获取数值2
	num2 = test_case.n2

	#从用例中获取预期结果
	exp_res = test_case.res

	#调用开发的add接口，传入测试用例中的两个数字，获取调用接口后的实际结果
	act_res = add(num1,num2)
	logging.info("num1:{0},num2:{1},act_res:{2}".format(num1,num2,act_res))
	#调用接口后的实际值与预期值进行比较断言
	assert exp_res == act_res , "{0} add {1} not equal {2}".format(num1,num2,exp_res)

#定义测试用例字典，来存储用例信息
case1_dict = {'id':'10001','desc':'test case 10001 desc','n1':1,'n2':1,'res':2}
case2_dict = {'id':'10002','desc':'test case 10002 desc','n1':1,'n2':2,'res':3}
case3_dict = {'id':'10003','desc':'test case 10003 desc','n1':1,'n2':3,'res':4}

add_suit = TestSuit("add_suit")

add_suit.add_case(case1_dict,test_add)
add_suit.add_case(case2_dict,test_add)
add_suit.add_case(case3_dict,test_add)

seed.run()
