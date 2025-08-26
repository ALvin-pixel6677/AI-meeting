import os

from assembly_base.core.base import TestCase
from assembly_base.core.runner import BaseAnalyzer, Const
from case_config.aw.Utils import Utils
from case_config.aw.file_compare_utils import FileCompareUtils


class CompareFileAnalyzer(BaseAnalyzer):
    def __init__(self):
        BaseAnalyzer.__init__(self)
        self.compare = FileCompareUtils()

    def onAction(self, action: str, obj: TestCase, param: object):

        if action == Const.Action_TestCase_End:
            if 'note_sys' in obj.id:
                note_text_file_user = os.path.join(self.reportPath, obj.id, 'note_user.txt')
                note_text_file_user_res = os.path.join(self.reportPath, obj.id, 'note_user_res.txt')
                gt_file = obj.gt_file
                if len(gt_file) > 0:
                    self.compare.compare_file(gt_file, note_text_file_user, note_text_file_user_res)
                else:
                    self.logger.error('真值文件为空：请添加真值比对文件')
            else:
                txt_name = os.path.join(self.reportPath, obj.id, obj.id + '.txt')
                deal_text_name = os.path.join(self.reportPath, obj.id, obj.id + '_副本.txt')
                Utils().remove_line_break(txt_name, deal_text_name)
                txt_name_res = os.path.join(self.reportPath, obj.id, obj.id + '_res.txt')
                gt_file = obj.gt_file
                if len(gt_file) > 0:
                    self.compare.compare_file(gt_file, deal_text_name, txt_name_res)
                else:
                    self.logger.error('真值文件为空：请添加真值比对文件')

