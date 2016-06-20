#!/usr/bin/python
#-*-coding:utf-8-*-
import codecs

class ReportFactory(object):
	"""报告工厂类"""
	@staticmethod
	def create_report(out_type,total_result):
		if out_type=='cmd':
			return CmdReport(total_result)
		elif out_type=='html':
			return HtmlReport(total_result)
		elif out_type=='xml':
			return XmlReport(total_result)
		else:
			return None

class Report(object):
	"""报告类，所有具体报告类的父类"""
	def out_put_report(self):
		pass

class CmdReport(object):
	"""命令行报告类"""
	def __init__(self,total_result):
		self.total_result = total_result

	def out_put_report(self):
		print "Run Time:[{0}]".format(self.total_result.run_time)
		print "Case Execution Time:[{0}]".format(self.total_result.run_time)
		print "Run Case Count:[{0}]".format(self.total_result.get_all_run_count())
		print "Pass Count:[{0}]".format(self.total_result.get_passed_count())
		print "Fail Count:[{0}]".format(self.total_result.get_failed_count())
		print "Total Elapsed Time:[{0}]".format(self.total_result.run_all_case_elapsed_time)
		for res in self.total_result.results:
			print "CaseId:[{0}],CaseDesc:[{1}],CaseRes:[{2}]------ElapsedTime:[{3}]".format(res.test_case.id,res.test_case.desc,"Pass" if res.passed else "Fail" ,res.elapsed_ime)
			if not res.passed:
				print res.why.traceback


class XmlReport(object):
        """Xml报告类"""
       
        def __init__(self,total_result):
		self.total_result = total_result

	def out_put_report(self):
                executeResXml = ""
                xml_header='''<?xml version="1.0" encoding="UTF-8"?>'''
                xml_overview='''<testng-results skipped="%s" failed="%s" total="%s" passed="%s">''' % (self.total_result.get_skip_case_count(), self.total_result.get_failed_count(), self.total_result.get_all_run_count(),self.total_result.get_passed_count())
                xml_suites=''' <suite name="Suites" duration-ms="%s" started-at="%s" finished-at="">''' % (self.total_result.run_all_case_elapsed_time, self.total_result.run_time)
                executeResXml = xml_header + xml_overview + xml_suites
                
                for item,value in self.total_result.get_json_res().items():
                        xml_suite='''<test name="%s" ><class >''' % item
                        executeResXml = executeResXml + xml_suite
                        for case in value:
                                if case['has_run']: 
                                        xml_case_header='''<test-method status="{passed}" name="{case_id}" duration-ms="{elapsed_time}" description="{desc}" started-at="0">'''.format(passed=("PASS" if case['run_res']['passed'] else "FAIL"),case_id=case['id'],elapsed_time=case['run_res']['elapsed_ime'], desc=case['desc'])
                                        executeResXml = executeResXml + xml_case_header
                                        if not case['run_res']['passed']:
                                                xml_case_error = '''<exception > <message>{error_message}</message> <full-stacktrace>{error_trace}</full-stacktrace> </exception> '''.format(error_message='<![CDATA['+case['run_res']['why']['message']+']]>', error_trace='<![CDATA['+case['run_res']['why']['traceback']+']]>')
                                                executeResXml = executeResXml + xml_case_error
                                else:
                                        xml_case_header='''<test-method status="SKIP" name="{case_id}" duration-ms="0" started-at="0">'''.format(case_id=case['id'])
                                        executeResXml = executeResXml + xml_case_header
                                xml_case_end='''</test-method>'''
                                executeResXml = executeResXml + xml_case_end
                        xml_suite_end='''</class></test>'''
                        executeResXml = executeResXml + xml_suite_end
                xml_end='''</suite></testng-results>'''
                executeResXml = executeResXml + xml_end

                report_xml = codecs.open('report.xml','w','utf-8')
                report_xml.write(executeResXml.decode('u8'))
                report_xml.close()
                
        
        


class HtmlReport(Report):
	"""HTML报告类"""
	html_template = '''
	<html><head>  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>{report_name}</title>  <style>  
<!--.datalist{  border:1px solid #0058a3;   /* 表格边框 */  font-family:Arial;  border-collapse:collapse;   /* 边框重叠 */  background-color:#72C43C;   /* 表格背景色 */  font-size:14px;  }  
.datalist caption{padding-bottom:5px;font:bold 1.4em;  text-align:left;  }  
.datalist th{  border:1px solid #0058a3;   /* 行名称边框 */  background-color:#4bacff;   /* 行名称背景色 */  color:#FFFFFF;              /* 行名称颜色 */  font-weight:bold;  padding-top:4px; padding-bottom:4px;  padding-left:12px; padding-right:12px;text-align:center;}.datalist td{  border:1px solid #0058a3;   /* 单元格边框 */  text-align:left;  padding-top:4px; padding-bottom:4px;  padding-left:10px; padding-right:10px;  }.datalist tr.fail{background-color:#FF0000;   /* 隔行变色 */}.datalist tr.pass{  background-color:#72C43C;   /* 隔行变色 */}--></style></head>  
<body><h2>{report_name}</h2><p>执行时间：{run_time}</p><p>执行总量：{all_case_count}</p><p>成功数量：{pass_case_count}</p><p>失败数量：{fail_case_count}</p><p>总耗时：{elapsed_time}秒</p>
<table class="datalist" summary="{report_name}">    <tr>  <th scope="col">用例编号</th><th scope="col">用例名称</th><th scope="col">结果</th><th scope="col">耗时</th></tr>{case_execute_res}</table>  
</body>  
</html>  
	'''
	def __init__(self,total_result):
		self.total_result = total_result

	def out_put_report(self):
		html_report = HtmlReport.html_template
		executeResHtml = ""
		report_fo = codecs.open('report.html','w','utf-8')
		html_report = html_report.replace('''{report_name}''','测试报告')
		html_report = html_report.replace('''{run_time}''',self.total_result.run_time)
		html_report = html_report.replace('''{all_case_count}''',str(self.total_result.get_all_run_count()))
		html_report = html_report.replace('''{pass_case_count}''',str(self.total_result.get_passed_count()))
		html_report = html_report.replace('''{fail_case_count}''',str(self.total_result.get_failed_count()))
		html_report = html_report.replace('''{elapsed_time}''',str(self.total_result.run_all_case_elapsed_time))

		for result in self.total_result.results:
			executeResHtml+='''<tr class="{css}"><td>{case_id}</td><td><a href="{case_log_path}" target="_blank">{case_desc}</a></td><td>{passed}</td><td>{elapsed_time}</td></tr>'''.format(css = ("pass" if result.passed else "fail"),case_id=result.test_case.id,case_log_path=result.test_case.case_log_path,case_desc=result.test_case.desc,passed=("pass" if result.passed else "fail"),elapsed_time=result.elapsed_ime)
			if not result.passed:
				#executeResHtml+='''<tr class="fail"><td>错误信息</td><td colspan="3">{error_info}</td></tr>'''.format(error_info='<br>'.join(result.why.traceback.splitlines()))
				executeResHtml+='''<tr class="fail"><td>错误信息</td><td colspan="3">{error_info}</td></tr>'''.format(error_info=(result.why.message))
				#executeResHtml+='''<tr class="fail"><td>错误信息</td><td colspan="3">{error_info}</td></tr>'''.format(error_info=(result.why.message)+'<br>==========Log Info==========<br>'+'<br>'.join(result.case_log))
		html_report = html_report.replace('''{case_execute_res}''',executeResHtml)
		report_fo.write(html_report.decode('u8'))
		report_fo.close()
