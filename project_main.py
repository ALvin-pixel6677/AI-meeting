"""
@Author  :  z00017273
@Software:  AAT(Assembly Automatic Test/融合自动化测试)
@File    :  project_main.py
@Time    :  2021-10-27
@Desc    :  pc
"""

# 导入系统包
import optparse

from analyzer.CompareFileAnalyzer import CompareFileAnalyzer
from assembly_base.core.builder import *
from assembly_base.runner.runner_aat_common import AATCommonRunner

from collector.ev_record_collector import EVRecordCollector


# 融合自动化测试
# 融合自动化测试框架有4部分组成: 用例集合(TestCase)、用例执行器(Runner)、数据抓取器(Collector)、数据分析器(Analyzer).
# 四个部分之前做到完全解耦(TestCase 需要和Runner配套，未完全解耦)各部分之前通过消息(Action)相关协调和通信；
# 除了TestCase和Runner是绑定的，其他部分(Collector,Analyzer)要做到随意替换组合而不影响整个执行过程
# Runner、Collector、Analyzer通过继承onAction并对相关消息处理实现业务流程的同步。
# 各部分介绍：
# 用例集合(TestCase)用来管理用例的配置, 通过xml来管理，该部分仅用来管理用例配置，不包含用例依赖的资源，环境, 执行差异化等数据
# 用例执行器(Runner)与特定用例结合绑定，唯一实现用例的执行，不对执行的数据，测试结果等进行管理。
# 数据抓取器(Collector) 负责从手机或其他设备中获取日志，截图，状态等信息，不负责信息的分析和判断
# 数据分析器(Analyzer)负责数据的分析，处理，判断等逻辑，并对执行结果进行判定

# 用例执行框架

class TestMain(object):

    def start(self, product, version, filter, parameter, config_file, interpreter, argv):
        testbuilder = TestBuilder()

        testbuilder.set_python_env(interpreter, argv)

        # 添加用例集合(TestCase)
        testbuilder.addCaseConfig("case_config\config.xml", filter, parameter, config_file)

        # 配置产品和版本信息(一般是由命令行传入)
        testbuilder.initProductAndVersion(product, version)

        # 设置用例执行器(Runner)
        testbuilder.setRunner(AATCommonRunner())

        # 设置数据抓取器(Collector)
        testbuilder.addCollector(EVRecordCollector())

        # 设置数据分析器(Analyzer)
        testbuilder.addAnalyzer(CompareFileAnalyzer())

        # 设置当前的执行设备为Windows
        testbuilder.setDeviceType(Const.Mode_Device_type_Windows)

        # 设置整个工程执行2遍
        testbuilder.setValue(TestBuilder.Config_Project_round, 1)

        # 设置每条用例执行5轮
        testbuilder.setValue(TestBuilder.Config_TestCase_round, 1)

        # 设置用例随机执行
        testbuilder.setValue(TestBuilder.Config_TestCase_Random, False)

        # 设置预置模式为:每个TestSuit开始之前做完当前TestSuit中所有的预置操作
        testbuilder.setValue(TestBuilder.Config_PrePare_Mode, Const.Mode_TestSuite)

        # 开始执行测试
        testbuilder.start()


if __name__ == "__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("-p", "--P", dest="Product", default="STARK", help="product")  # 参数: 产品名
    optparser.add_option("-v", "--V", dest="Version", default="V100B001", help="version")  # 参数：版本号
    optparser.add_option("-f", "--F", dest="Filter", default="", help="filter")  # 参数： 用例过滤器
    optparser.add_option("-c", "--C", dest="CustomParameter", default="Parameter01:1000,Parameter02:1000",
                         help="CustomParameter")  # 参数:业务自定义参数
    optparser.add_option("-j", "--jsonfile", dest="JsonFile", default="", help="config_json_file")  # 参数:业务自定义参数

    opts, args = optparser.parse_args()
    _p = opts.Product
    _v = opts.Version
    _f = opts.Filter
    _c = opts.CustomParameter
    _config_file = opts.JsonFile

    Test = TestMain()
    Test.start(_p, _v, _f, _c, _config_file, sys.executable, sys.argv)
