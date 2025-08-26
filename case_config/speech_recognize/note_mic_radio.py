import os
import threading

from assembly_base.core.runner import BaseCaseRunner
from assembly_base.model.pc.markov.EVCapture import EVCapture
from assembly_base.model.pc.markov.HonorNote import HihonorNote
from case_config.aw.Utils import Utils


class NoteMicRadio(BaseCaseRunner):

    def __init__(self):
        BaseCaseRunner.__init__(self)
        self.capture = EVCapture.WindowEVCapture()
        self.note = HihonorNote.WindowHihonornote()

    def setUp(self, runner, config, case):
        self.capture.action_open_capture(case.ev_path)
        self.capture.app.sleep(5)
        self.capture.action_switch_capture('仅麦克风')
        self.capture.app.sleep(3)
        self.capture.action_start_record()

    def test(self, runner, config, case):
        self.note.action_start_Hihonornote()

        self.logger.info("打开荣耀笔记")
        self.note.action_to_note()

        self.logger.info("新建笔记")
        self.note.action_create_note()

        self.note.action_full_page_note()

        self.note.action_record_audio()

        self.note.action_setting_record()

        self.note.action_quit_full_page()

        self.note.action_show_speaker()

        self.logger.info(f'视频文件地址：{case.video_path}')
        t = threading.Thread(target=Utils().play_video_phone, args=(case.video_path,))
        t.start()

        self.note.app.sleep(int(case.play_time))

        self.logger.info('关闭视频播放')
        Utils().close_video()
        self.note.app.sleep(5)

        file_name = f'{case.id}.mp4'
        mp4_path = os.path.join(self.reportPath, case.id)
        self.capture.action_stop_record(file_name, mp4_path)

        self.logger.info('关闭录屏')
        self.capture.action_close_capture()

        self.note.app.sleep(5)
        pic_path = os.path.join(self.comResPath, 'pic', 'stop_record.jpg')
        self.note.action_stop_record(pic_path)

        self.note.app.sleep(5)
        self.logger.info('保存全部译文')
        self.note.action_show_speaker()
        self.note.app.sleep(5)
        note_text_file = os.path.join(self.reportPath, case.id, 'note.txt')
        self.note.action_save_document(note_text_file)

        note_text_file_user = os.path.join(self.reportPath, case.id, 'note_user.txt')
        Utils().read_file_to_path(note_text_file_user)

        meeting_text_file = os.path.join(self.reportPath, case.id, 'meeting.txt')
        self.note.action_create_meeting_minutes(meeting_text_file)

        self.note.app.sleep(5)


def end(self, runner, config, case):

        self.note.action_close_Hihonornote()
        self.note.app.sleep(5)
