

from assembly_base.core.runner import BaseCollector, Const
from assembly_base.model.pc.markov.EVCapture import EVCapture


class EVRecordCollector(BaseCollector):

    def __init__(self):
        BaseCollector.__init__(self)
        self.ev_capture = EVCapture.WindowEVCapture()


    def onAction(self, action: str, obj: object, param: object):

         if action == Const.Action_TestCase_Start:
             pass








