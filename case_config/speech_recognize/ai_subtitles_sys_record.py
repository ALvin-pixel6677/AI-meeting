import os
import threading

from assembly_base.core.runner import BaseCaseRunner
from assembly_base.model.pc.markov.EVCapture import EVCapture
from assembly_base.model.pc.markov.YoYo import YoYo
from case_config.aw.Utils import Utils


class AISubtitlesSysRecord(BaseCaseRunner):

    def __init__(self):
        BaseCaseRunner.__init__(self)
        self.capture = EVCapture.WindowEVCapture()

        self.ai = YoYo.YoYoAiSubtitle()
        self.yoyo_window = YoYo.WindowYoYo()
        self.yoyo_float = YoYo.YoYoFloatingBall()

    def setUp(self, runner, config, case):
        self.capture.action_open_capture(case.ev_path)
        self.capture.app.sleep(5)
        self.capture.action_switch_capture('仅系统声音')
        self.capture.app.sleep(3)
        self.capture.action_start_record()

    def test(self, runner, config, case):
        self.yoyo_window.action_open_yoyo()
        self.yoyo_window.app.sleep(5)
        self.yoyo_window.action_close_window()
        self.yoyo_float.open_module('AI\s*字幕')
        self.yoyo_float.app.sleep(10)

        self.logger.info(f'视频文件地址：{case.video_name}')
        if not os.path.exists(case.video_name):
            raise Exception('指定的视频文件不存在')

        t = threading.Thread(target=Utils().open_video, args=(case.video_name,))
        t.start()

        self.yoyo_float.app.sleep(int(case.play_time))

        self.logger.info('关闭视频播放')
        Utils().close_video()

        file_name = f'{case.id}.mp4'
        mp4_path = os.path.join(self.reportPath, case.id)
        self.capture.action_stop_record(file_name, mp4_path)

        self.logger.info('关闭录屏')
        self.capture.action_close_capture()

        self.ai.action_active_window()
        html_name = os.path.join(self.reportPath, case.id, case.id + '.txt')
        self.ai.action_save_subtitle(html_name)

    def end(self, runner, config, case):
        self.ai.action_close_subtitle()
