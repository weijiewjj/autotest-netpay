import unittest

import time
import config.HTMLTestRunner

case_dir="./testcase/bc_tcp_json"

#discover = unittest.defaultTestLoader.discover(case_dir, pattern='test*.py')
discover = unittest.defaultTestLoader.discover(case_dir,pattern='*.py',top_level_dir=None)


now=time.strftime('%Y-%m-%d %H_%M_%S')
suite = unittest.TestSuite()  # 定义一个测试套件
for test_suite in discover:
    for test_case in test_suite:
        suite.addTests(test_case)
print(suite)  # 打印一下可以看到suite中添加了哪些测试用例

filename="./testresult/"+now+"_result.html"

fp = open(filename,'wb')
runner = config.HTMLTestRunner.HTMLTestRunner(stream=fp,title='NETPAY front system Test Report',description='Implementation description: ',verbosity=2)
runner.run(suite)

fp.close()

