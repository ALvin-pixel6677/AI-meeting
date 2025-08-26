import ctypes
import json
import os.path
import random
import re
import subprocess
import time
from ctypes import wintypes
from pathlib import Path

import cv2
import win32con
import win32gui
from assembly_base.action_word.aat_ui_control import AAT_UIControlWindows, AAT_UIControlAndroid
from assembly_base.action_word.device.windows_device import WindowsDevice
from assembly_base.action_word.win_monkey.event.RandomEvents import RandomEvents
from assembly_base.action_word.win_monkey.win32.WinUtils import WinUtils
from assembly_base.common.common import SystemLogger
from case_config.aw.base_interface import Base_fun_api


class Utils(SystemLogger):

    def __init__(self):
        self.app = AAT_UIControlWindows()

    def open_video(self, video_path):

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"文件不存在：{video_path}")

        try:
            subprocess.run(['cmd', '/c', 'start', '', video_path], check=True, shell=True, stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL
                           )
        except subprocess.CalledProcessError as e:
            self.logger.error(f'播放失败：{str(e)}')

        start_time = time.time()
        while time.time() - start_time < 5:
            if WinUtils.is_espect_window('媒体播放器'):
                w = Base_fun_api.get_top_page_info()
                time.sleep(1)
                Base_fun_api.set_page_min(w['hwnd'])

    def close_video(self):
        self.app.attach_process('Microsoft.Media.Player.exe')
        self.app.sleep(2)
        self.app.stop()

    def read_file_to_path(self, file_name):
        """
            读取录音笔记译文
        """
        dir_name = os.path.dirname(file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        user_home = os.path.expanduser('~')
        res_path = os.path.join(user_home, '.config', 'hihonornote', 'resources')
        self.logger.info(f'获取录音笔记内容存储路径：{res_path}')
        dirs = [d for d in Path(res_path).iterdir() if d.is_dir()]
        target_path = max((d for d in dirs), key=lambda x: x.stat().st_mtime_ns)
        self.logger.info(f'最新目录：{target_path}')
        for root, _, files in os.walk(target_path):
            for file in files:
                if '_card_asr_' in file and file.endswith('.json'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            data = json.loads(f.read())
                        content_list = data.get('list')

                        with (open(file_name, 'a', encoding='utf-8')) as f:
                            for content in content_list:
                                f.write(content.get('content'))


                    except json.JSONDecodeError as e:
                        self.logger.error(f'JSON解析错误：{e}')
                    except Exception as e:
                        self.logger.error(f'获取笔记译文失败：{e}')

    def play_video_phone(self, video_path="/sdcard/test.mp4"):
        app_phone = AAT_UIControlAndroid()
        adb_command = f"am start -a android.intent.action.VIEW -d file://{video_path} -t video/mp4"
        try:
            app_phone.input_obj.shell(adb_command)
            self.logger.info("已尝试启动视频播放。")
        except Exception as e:
            self.logger.error(f"执行命令时出现错误: {e}")

    def stop_video_phone(self):
        app_phone = AAT_UIControlAndroid()
        app_phone.device_obj.stop_apk("com.hihonor.hnvideoplayer")

    def get_duration(self, file_path):
        cap = cv2.VideoCapture(file_path)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps
            cap.release()
            return duration
        return 0


    def remove_line_break(self, old_file, new_file):
        with open(old_file, 'r', encoding='utf-8') as f:
            content = re.sub(r'[\r\n]+', '', f.read())
        with open(new_file, 'w', encoding='utf-8') as f:
            if content.startswith('<麦克风><原文字幕>'):
                content = content.replace('<麦克风><原文字幕>', '')
            f.write(content)


if __name__ == '__main__':
    # WindowsDevice.debug_flag = True
    # time.sleep(3)
    # a = WinUtils.get_foregroud_window()
    # print(a)


    Utils().open_video(
        r'D:\code\aat_project_pc_speech_recognize\reports\project_main\20250425_143318\note_sys\note_sys.mp4')

    Utils().read_file_to_path(r'D:\123.txt')

    Utils().open_video(r'D:\code\aat_project_pc_speech_recognize\reports\project_main\20250425_143318\note_sys\note_sys.mp4')

    Utils().read_file_to_path(r'D:\123.txt')
    Utils().remove_line_break(r'D:\123.txt', r'D:\1234.txt')
    # Utils().open_video(
    #     r'D:\code\aat_project_pc_speech_recognize\reports\project_main\20250425_143318\note_sys\note_sys.mp4')
    #
    # Utils().read_file_to_path(r'D:\123.txt')
    # Utils().read_file_to_path(r'D:\123.txt')
    # Utils().play_video_phone()
    # time.sleep(5)
    # Utils().stop_video_phone()

    # print(Utils.get_target_windows(['三国杀', 'aat_project_pc_game_manager']))
    # Utils.switch_windows(['百度一下', '荒野行动'], 10)
    # Utils().send_alt_tab()
    # while True:
    #     a = Utils.get_cursor_style()
    #     print(a.hCursor)
    #     time.sleep(1)
