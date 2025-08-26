#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
@Author  : ww0020089
@Software:
@File    :check_precondition_aw.py
@Time    : 2022/1/25
@Desc    : 基础功能接口api
"""

import os
from datetime import datetime

import win32com.client
import wmi
import time
import json
import random
import shutil
import psutil
import zipfile
import win32api
import win32con
import win32gui
import pyautogui
import pyperclip
import win32print
import win32process
import func_timeout
from PIL import ImageGrab
from win32com.client import GetObject
from func_timeout import func_set_timeout

from assembly_base.action_word.aat_ui_control import AAT_UIControlWindows
from assembly_base.action_word.device.windows_device import WindowsDevice, WindowsKey


class Base_fun_api():
    ACTION_TYPE_CLICK = "ACTION_TYPE_CLICK"
    ACTION_TYPE_DCLICK = "ACTION_TYPE_DCLICK"
    ACTION_TYPE_RETURN_NODE = "ACTION_TYPE_RETURN_NODE"
    ACTION_TYPE_MOVE = "ACTION_TYPE_MOVE"

    @staticmethod
    def get_target_window_info(name=None):
        window = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                text = win32gui.GetWindowText(hwnd)
                classname = win32gui.GetClassName(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                x = rect[0]
                y = rect[1]
                w = rect[2]
                h = rect[3]
                window.append(
                    {'hwnd': hwnd, 'text': text, 'classname': classname, 'process_name': process.name(), 'x': x, 'y': y,
                     'weight': w, 'height': h})

        win32gui.EnumWindows(callback, None)
        for item in window:
            if name and name in item['text']:
                return item
            else:
                print(item)

    @staticmethod
    def custom_time_attach_process(aat_obj, process_name):
        """使特定窗口最小化"""

        @func_set_timeout(20)
        def fun_custom_time_attach_process(aat_obj, process_name):
            # 检查窗口是否最小化，如果是最大化
            try:
                aat_obj.attach_process(process_name)
            except:
                print("WARNING WARNING attach_process失败 WARNING WARNING")

        try:
            fun_custom_time_attach_process(aat_obj, process_name)
        except func_timeout.exceptions.FunctionTimedOut:
            print("ERROR attach_process 函数执行超时")
            pass

    @staticmethod
    def get_active_window_process_info():
        """获取最上层窗口的进程Id和进程名字"""

        @func_set_timeout(20)
        def inner_get_active_window_process_info():
            try:
                _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                return pid, psutil.Process(pid).name()
            except:
                return "", ""

        try:
            return inner_get_active_window_process_info()
        except func_timeout.exceptions.FunctionTimedOut:
            print("ERROR attach_process 函数执行超时")
            pass

    @staticmethod
    def get_json_file_data_info_to_dict(json_path):
        """读取json文件到字典"""
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as load_file:
                    json_file_dict = json.load(load_file)
                    return json_file_dict
            except:
                with open(json_path, 'r', encoding="utf-8") as load_file:
                    json_file_dict = json.load(load_file)
                    return json_file_dict
        return False

    @staticmethod
    def wmi_check_processes_is_run(pname):
        """检查特定进程是否运行"""
        _wmi = GetObject('winmgmts:')
        processes = _wmi.ExecQuery("Select * from win32_process where name= '%s'" % (pname))
        try:
            return processes[0].ProcessId
        except:
            return False

    @staticmethod
    def send_cmd_str_and_return(cmd_str, is_waiting_for_results=False):
        """发送cmd命令行返回结果"""
        if is_waiting_for_results:
            with os.popen(cmd_str) as ret:
                cmd_ret = ret.read()
            return cmd_ret
        else:
            os.popen(cmd_str)
            return None

    @staticmethod
    def check_element_no_refresh(aat_obj, check_name, regex=False, check_frequency=7):
        """检查元素并返回(二次封装加强版)"""
        for i in range(int(check_frequency)):
            check_ret = aat_obj.find(check_name, regex=regex)
            if check_ret:
                return check_ret
            if i >= 5:
                aat_obj.refresh_page()
            time.sleep(2)
        time.sleep(3)
        return aat_obj.find(check_name, regex=regex)

    @staticmethod
    def to_work_exe(exe_path, wait_time=5):
        """运行exe文件（可作为打开应用）"""
        Base_fun_api.send_cmd_str_and_return(r'"{}"'.format(exe_path))
        time.sleep(wait_time)

    @staticmethod
    def zip_dir():
        """压缩文件夹"""
        shutil.make_archive(r"D:\WER", 'zip', r"D:\WER")

    @staticmethod
    def zip_files(files_path_list, zip_bag_all_path):
        """将列表中的文件打包成一个zip包"""
        zip_ = zipfile.ZipFile(zip_bag_all_path, 'w', zipfile.ZIP_DEFLATED)
        for file in files_path_list:
            if os.path.exists(zip_.filename):
                zip_.write(file)
        zip_.close()

    @staticmethod
    def unzip_zip_file(unzip_target_file_path, unzip_result_dir):
        """解压zip包"""
        unzip = zipfile.ZipFile(unzip_target_file_path, 'r', compression=zipfile.ZIP_DEFLATED)
        unzip.extractall(unzip_result_dir)
        unzip.close()

    @staticmethod
    def write_json_file_to_dict(json_path):
        """读取json到字典"""
        if os.path.exists(json_path):
            with open(json_path, 'r') as load_file:
                return json.load(load_file)
        return False

    @staticmethod
    def random_weighted_value(target_dict):
        """随机加权取值"""
        all_data = []
        for v, w in target_dict.items():
            temp = []
            for i in range(w):
                temp.append(v)
            all_data.extend(temp)
        n = random.randint(0, len(all_data) - 1)
        return all_data[n]

    @staticmethod
    def paste_text():
        """将剪切板的东西拷贝出来"""
        # 执行ctrl + V 粘贴地址
        win32api.keybd_event(WindowsKey.VK_CONTROL, 0, 0, 0)
        time.sleep(0.3)
        win32api.keybd_event(WindowsKey.VK_V, 0, 0, 0)
        win32api.keybd_event(WindowsKey.VK_V, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(WindowsKey.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def input_text(text_content, wait_time=0.3):
        """输入特定文本"""
        pyperclip.copy(text_content)
        # 执行ctrl + V 粘贴地址
        win32api.keybd_event(WindowsKey.VK_CONTROL, 0, 0, 0)
        time.sleep(wait_time)
        win32api.keybd_event(WindowsKey.VK_V, 0, 0, 0)
        win32api.keybd_event(WindowsKey.VK_V, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(WindowsKey.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def get_app_path(device_obj, app_name):
        app_info = device_obj.get_instaled_apps()
        for k, v in app_info.items():
            if (app_name.lower() in k.lower() or app_name.lower() in v.display_name.lower()) and 'setup' not in k:
                if v.install_location:
                    return v.install_location
                else:
                    return v.uninstall_location

    @staticmethod
    def get_top_page_flag_button(aat_obj, num):
        all_button = aat_obj.find_all_class(r"KPromeTab")
        temp_list1 = []
        temp_list2 = []
        for i in all_button:
            temp_list1.append(i.rect.center_x)
            temp_list2.append(i)
        temp_list3 = sorted(temp_list1)
        print("temp_list1", temp_list1)
        print("temp_list2", temp_list2)
        print("temp_list3", temp_list3)
        return temp_list2, temp_list2[temp_list1.index(temp_list3[num])]

    @staticmethod
    def key_combination(combination_list, sleep_time=0.3):
        """给pc发送键盘命令模仿按压键盘"""
        if len(combination_list) == 1:
            # 两位组合键
            win32api.keybd_event(combination_list[0], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[0], 0, win32con.KEYEVENTF_KEYUP, 0)
        elif len(combination_list) == 2:
            # 两位组合键
            win32api.keybd_event(combination_list[0], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[1], 0, 0, 0)
            win32api.keybd_event(combination_list[1], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[0], 0, win32con.KEYEVENTF_KEYUP, 0)
        elif len(combination_list) == 3:
            # 三位组合键
            win32api.keybd_event(combination_list[0], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[1], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[2], 0, 0, 0)
            win32api.keybd_event(combination_list[2], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[1], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[0], 0, win32con.KEYEVENTF_KEYUP, 0)
        elif len(combination_list) == 4:
            # 四位组合键
            win32api.keybd_event(combination_list[0], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[1], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[2], 0, 0, 0)
            time.sleep(sleep_time)
            win32api.keybd_event(combination_list[3], 0, 0, 0)
            win32api.keybd_event(combination_list[3], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[2], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[1], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(combination_list[0], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def open_dir_page(dir_path):
        """打开文件夹窗口并且返回窗口句柄"""
        Base_fun_api.send_cmd_str_and_return(r'explorer "{}"'.format(dir_path), True)
        time.sleep(2)
        check = Base_fun_api.get_top_page_info()
        if check['class'] == "CabinetWClass":
            Base_fun_api.set_page_max(check['hwnd'])
            return check['hwnd']
        else:
            time.sleep(3)
            check = Base_fun_api.get_top_page_info()
            Base_fun_api.set_page_max(check['hwnd'])
            return check['hwnd']

    @staticmethod
    def open_app_and_return_hwnd(app_path, check_class_flag, is_max=True):
        """打开app并且返回窗口句柄"""
        if "不是内部或外部命令" in Base_fun_api.send_cmd_str_and_return(r'"{}"'.format(app_path), True):
            Base_fun_api.send_cmd_str_and_return(r'{}'.format(app_path), True)
        time.sleep(2)
        check = Base_fun_api.get_top_page_info()
        if check_class_flag in check['class']:
            if is_max:
                Base_fun_api.set_page_max(check['hwnd'])
            return check['hwnd']
        else:
            time.sleep(5)
            check = Base_fun_api.get_top_page_info()
            if is_max:
                Base_fun_api.set_page_max(check['hwnd'])
            return check['hwnd']

    @staticmethod
    def turn_off_desktop_all_page(check_num, click_coordinate, hwnd_model_type=True):
        """关闭桌面显示出来的所有窗口"""
        if hwnd_model_type:
            for i in range(check_num):
                pyautogui.moveTo(click_coordinate[0], click_coordinate[1], duration=0.5)
                pyautogui.click()
                check = Base_fun_api.get_top_page_info()
                print(check)
                if check['name'] != "":
                    Base_fun_api.set_page_close(check['hwnd'])
                time.sleep(1)
        else:
            for i in range(check_num):
                pyautogui.moveTo(click_coordinate[0], click_coordinate[1], duration=0.5)
                pyautogui.click()
                Base_fun_api.key_combination([WindowsKey.VK_ALT, WindowsKey.VK_F4])
                time.sleep(1)
            Base_fun_api.key_combination([WindowsKey.VK_ESCAPE])
            time.sleep(1)
            check = Base_fun_api.get_top_page_info()
            if check["name"] == "关闭 Windows":
                Base_fun_api.key_combination([WindowsKey.VK_ESCAPE])

    @staticmethod
    def set_pc_show_brightness(brightness):
        """设置pc的显示亮度,传递int百分比值"""
        wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)

    @staticmethod
    def get_pc_show_brightness():
        """获取pc的显示亮度返回int百分比"""
        return wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness

    @staticmethod
    def get_pc_resolution():
        """获取pc真实的分辨率"""
        hdc = win32gui.GetDC(0)
        pc_resolution = (win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES),
                         win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES))
        return pc_resolution

    @staticmethod
    def mouse_middle_slide_up_and_down(browser_time):
        """
        使用鼠标上下滚轮滑动浏览特定时间
        single_time：滑动浏览总时间几秒
        """
        start_time = time.time()
        while True:
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -400)
                time.sleep(0.1)
            time.sleep(1)
            now_time = time.time() - start_time
            if now_time >= browser_time:
                break
            for i in range(10):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 380)
                time.sleep(0.1)
            time.sleep(2)
            now_time = time.time() - start_time
            if now_time >= browser_time:
                break

    @staticmethod
    def press_the_button_up_and_down(browser_time):
        """
        使用鼠标上下键浏览特定时间
        browser_time：滑动浏览总时间几秒
        """
        start_time = time.time()
        while True:
            for i in range(10):
                Base_fun_api.key_combination([WindowsKey.VK_DOWN])
                time.sleep(0.1)
            time.sleep(1)
            now_time = time.time() - start_time
            if now_time >= browser_time:
                break
            for i in range(10):
                Base_fun_api.key_combination([WindowsKey.VK_UP])
                time.sleep(0.1)
            time.sleep(2)
            now_time = time.time() - start_time
            if now_time >= browser_time:
                break

    @staticmethod
    def get_default_storage_path():
        username = os.getlogin()
        home_path = os.path.join(os.environ['SystemDrive'], 'Users', username)
        wechat_path = os.path.join(home_path, 'Documents', 'WeChat Files')
        return wechat_path

    @staticmethod
    def get_top_page_info():
        """获取当前最上面窗口的信息"""
        try:
            page_info_dict = {}
            # 获取最上面窗口的句柄
            top_page_hwnd = win32gui.GetForegroundWindow()
            # 获取最上面窗口的窗口名
            page_name = win32gui.GetWindowText(top_page_hwnd)
            # 获取最上面窗口的类名
            time.sleep(2)
            page_class_name = win32gui.GetClassName(top_page_hwnd)
            page_info_dict["hwnd"] = top_page_hwnd
            page_info_dict["name"] = page_name
            page_info_dict["class"] = page_class_name
            return page_info_dict
        except:
            return {"hwnd": "", "name": "", "class": ""}

    @staticmethod
    def get_top_page_hwnd():
        """获取当前最上面窗口的句柄"""
        # 获取最上面窗口的句柄
        top_page_hwnd = win32gui.GetForegroundWindow()
        return top_page_hwnd

    @staticmethod
    def set_page_min(page_hwnd):
        """使特定窗口最小化"""

        @func_set_timeout(7)
        def fun_set_page_min(page_hwnd):
            # 检查窗口是否最小化，如果是最大化
            try:
                # 最小化
                win32gui.ShowWindow(page_hwnd, win32con.SW_MINIMIZE)
            except:
                print("WARNING WARNING 最小化失败WARNING WARNING")

        try:
            fun_set_page_min(page_hwnd)
        except func_timeout.exceptions.FunctionTimedOut:
            print("ERROR 窗口最小化函数执行超时")
            pass

    @staticmethod
    def set_page_max(page_hwnd, is_reduction=False):
        """使特定窗口最大化"""

        @func_set_timeout(7)
        def fun_set_page_max(page_hwnd, is_reduction):
            try:
                # 最大化
                win32gui.ShowWindow(page_hwnd, win32con.SW_MAXIMIZE)
            except:
                print("WARNING WARNING 最大化失败 WARNING WARNING")
                pass
            try:
                # 确保窗口在最上面
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(page_hwnd)
            except:
                print("WARNING WARNING 确保窗口在最上面失败 WARNING WARNING ")
                pass
            if is_reduction:
                try:
                    # 还原窗口
                    Base_fun_api.set_page_reduction(page_hwnd)
                except:
                    print("WARNING WARNING 还原窗口失败 WARNING WARNING ")
                    pass

        try:
            fun_set_page_max(page_hwnd, is_reduction)
        except func_timeout.exceptions.FunctionTimedOut:
            print("ERROR 函数执行超时")
            pass
        time.sleep(2)

    @staticmethod
    def set_page_close(page_hwnd):
        """关闭对应句柄的窗口"""

        @func_set_timeout(7)
        def fun_set_page_close(page_hwnd):
            # 检查窗口是否最小化，如果是最大化
            try:
                if (win32gui.IsIconic(page_hwnd)):
                    # 最大化
                    win32gui.ShowWindow(page_hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(2)
            except:
                print("WARNING WARNING 最大化失败 WARNING WARNING ")
            try:
                # 确保窗口在最上面
                win32gui.SetForegroundWindow(page_hwnd)
            except:
                print("WARNING WARNING 确保窗口在最上面失败 WARNING WARNING ")
                pass
            try:
                # 还原对应句柄的窗口
                win32gui.SendMessage(page_hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            except:
                print("WARNING WARNING 还原对应句柄的窗口失败 WARNING WARNING ")
                pass
            time.sleep(1)
            try:
                # 关闭对应句柄的窗口
                win32gui.SendMessage(page_hwnd, win32con.WM_CLOSE)
            except:
                print("WARNING WARNING 关闭对应句柄的窗口失败 WARNING WARNING ")
                pass

        try:
            fun_set_page_close(page_hwnd)
        except func_timeout.exceptions.FunctionTimedOut:
            Base_fun_api.key_combination([WindowsKey.VK_N])
            print("ERROR 函数执行超时")
            pass

    @staticmethod
    def set_page_reduction(page_hwnd):
        """还原对应句柄的窗口"""
        try:
            # 还原对应句柄的窗口
            win32gui.SendMessage(page_hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        except:
            print("WARNING WARNING 还原对应句柄的窗口失败 WARNING WARNING ")
            pass

    @staticmethod
    def gset_page_min_to_top(page_hwnd):
        """将对应句柄的窗口从最底下菜单栏弄到最上面页面"""
        Base_fun_api.set_page_max(page_hwnd)
        Base_fun_api.set_page_reduction(page_hwnd)

    @staticmethod
    def get_page_rect(page_hwnd):
        # 获取窗口的坐标尺寸数值----得到元组类型如(-7, -7, 1543, 831)
        page_rect = win32gui.GetWindowRect(page_hwnd)
        return page_rect

    @staticmethod
    def action_time_specification():
        """
        执行特定时间的动作
        """

        # 需要传参数的话需要两层嵌套，不需要装饰器传参的话只需要嵌套一层即可
        # 一层的话定义装饰器时装饰器的参数就是fun函数动作，两层的话装饰器传递自己需要传递的参数，装饰器下面第一层传递fun函数动作
        def wrapper(func):
            def deco(*args, **kwargs):
                # 真正执行函数的地方
                start_time = time.time()
                func(*args, **kwargs)
                flag_key = kwargs.get("action_target_time")
                if kwargs and flag_key:
                    action_target_time = int(flag_key)
                else:
                    action_target_time = int(args[-1])
                end_time = time.time()
                exe_time = end_time - start_time
                if exe_time < action_target_time:
                    add_time = action_target_time - exe_time
                    print("==========时长不能达到预期的目标，开始补时{}秒========".format(add_time))
                    Base_fun_api.progress_bar_sleep(add_time)
                    print("\n===================补时结束=========================")

            return deco

        return wrapper

    @staticmethod
    def progress_bar_sleep(target_time):
        target_time = int(target_time)
        for i in range(target_time):
            time.sleep(1)
            if target_time <= 100:
                a = "*" * (i + 1)
                b = "." * (target_time - i - 1)
                c = ((i + 1) / target_time) * 100
                print("\r Wait sleep [{}->{}] {:^3.0f}%".format(a, b, c), flush=True, end="")
            else:
                a = "*" * int((i + 1) / 10)
                b = "." * int((target_time - i - 1) / 10)
                c = ((i + 1) / target_time) * 100
                print("\r Wait sleep [{}->{}] {:^3.0f}%".format(a, b, c), flush=True, end="")

    @staticmethod
    def get_screenshot_v2(path):
        """ """

        @func_set_timeout(5)
        def fun_get_screenshot_v2(path):
            obj = ImageGrab.grab()
            obj.save(path)

        try:
            return fun_get_screenshot_v2(path)
        except func_timeout.exceptions.FunctionTimedOut:
            print("========================ERROR 函数执行超时==========================")
            return False

    @staticmethod
    def get_screenshot(pic_path):
        if not os.path.exists(pic_path):
            os.makedirs(pic_path, exist_ok=True)
        file_name = os.path.join(pic_path, '{}.jpg'.format(datetime.now().strftime('%y%m%d_%H%M%S')))
        obj = ImageGrab.grab()
        obj.save(file_name)

    @staticmethod
    def find_dir_all_files_path_to_list(dir_path, check_file_str=""):
        """便利文件夹中所有特定名称的文件，返回地址"""
        file_path_result_list = []

        def find_all_files(dir_path, check_file_str):
            # 首先遍历当前目录所有文件及文件夹
            file_list = os.listdir(dir_path)
            # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
            if not check_file_str:
                for file in file_list:
                    # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
                    cur_path = os.path.join(dir_path, file)
                    # 判断是否是文件夹
                    if os.path.isdir(cur_path):
                        find_all_files(cur_path, check_file_str)
                    else:
                        file_path_result_list.append([cur_path, file])
            else:
                for file in file_list:
                    # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
                    cur_path = os.path.join(dir_path, file)
                    # 判断是否是文件夹
                    if os.path.isdir(cur_path):
                        find_all_files(cur_path, check_file_str)
                    else:
                        if check_file_str in file:
                            file_path_result_list.append([cur_path, file])

        find_all_files(dir_path, check_file_str)
        return file_path_result_list

    @staticmethod
    def find_dir_all_need_dir_files_v2(dir_path, check_file_str=""):
        """便利文件夹中所有特定名称的文件，返回地址"""
        file_path_result_list = []

        def find_all_files(dir_path, check_file_str):
            # 首先遍历当前目录所有文件及文件夹
            file_list = os.listdir(dir_path)
            for file in file_list:
                # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
                cur_path = os.path.join(dir_path, file)
                if check_file_str in file:
                    file_path_result_list.append([cur_path, file])

        find_all_files(dir_path, check_file_str)
        return file_path_result_list

    @staticmethod
    def check_and_click_node(check_func_name, action_type, *args, **kwargs):
        temp = str(check_func_name)
        if "AAT_UIControlWindowsOCR" in temp:
            print("-=-=--=-=-=--=-=-=-=-=-=-=-=-==-=--==--==")
            for i in range(3):
                try:
                    ret = check_func_name(*args, **kwargs)
                    if ret:
                        if action_type == Base_fun_api.ACTION_TYPE_RETURN_NODE:
                            return ret
                        elif action_type == Base_fun_api.ACTION_TYPE_CLICK:
                            ret.moveto()
                            # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 1)
                            time.sleep(0.5)
                            ret.click()
                            time.sleep(2)
                            return True
                        elif action_type == Base_fun_api.ACTION_TYPE_DCLICK:
                            ret.moveto()
                            # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 1)
                            time.sleep(0.5)
                            ret.double_click()
                            time.sleep(2)
                            return True
                        elif action_type == Base_fun_api.ACTION_TYPE_MOVE:
                            ret.moveto()
                            # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 5)
                            time.sleep(2)
                            return True
                        else:
                            return ret
                except:
                    pass
                time.sleep(1.5)
            return False
        else:
            try:
                ret = check_func_name(*args, **kwargs)
            except:
                time.sleep(2)
                temp = AAT_UIControlWindows()
                temp = eval("temp.{}".format(check_func_name.__name__))
                ret = temp(*args, **kwargs)
            if ret:
                if action_type == Base_fun_api.ACTION_TYPE_RETURN_NODE:
                    return ret
                elif action_type == Base_fun_api.ACTION_TYPE_CLICK:
                    ret.moveto()
                    # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 5)
                    time.sleep(0.5)
                    ret.click()
                    time.sleep(2)
                    return True
                elif action_type == Base_fun_api.ACTION_TYPE_DCLICK:
                    ret.moveto()
                    # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 5)
                    time.sleep(0.5)
                    ret.double_click()
                    time.sleep(2)
                    return True
                elif action_type == Base_fun_api.ACTION_TYPE_MOVE:
                    ret.moveto()
                    # pyautogui.moveTo(ret.rect.center_x, ret.rect.center_y, 5)
                    time.sleep(2)
                    return True
                else:
                    return ret

            else:
                return False

    @staticmethod
    def from_all_page_close_target_page(target_page_name_list=["Edge", "主文件夹"]):
        visible_window = []
        target_window_hwnd_list = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                text = win32gui.GetWindowText(hwnd)
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                style_true = style_to(style)
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect
                visible_window.append((hwnd, text, style_true, left, right, top, bottom))
                for i in target_page_name_list:
                    if i in text:
                        target_window_hwnd_list.append(hwnd)

        def style_to(style):
            res = [name for name in dir(win32con) if name.startswith("WS_") and getattr(win32con, name) & style]
            return res

        win32gui.EnumWindows(callback, None)
        for j in target_window_hwnd_list:
            Base_fun_api.set_page_close(j)

    @staticmethod
    def from_all_page_find_target_page_hwnd(target_page_name_list=["Creative Cloud Desktop"]):
        visible_window = []
        target_window_hwnd_list = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                text = win32gui.GetWindowText(hwnd)
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                style_true = style_to(style)
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect
                visible_window.append((hwnd, text, style_true, left, right, top, bottom))
                for i in target_page_name_list:
                    if i in text:
                        target_window_hwnd_list.append(hwnd)

        def style_to(style):
            res = [name for name in dir(win32con) if name.startswith("WS_") and getattr(win32con, name) & style]
            return res

        win32gui.EnumWindows(callback, None)
        return target_window_hwnd_list


class Debug_print():
    @staticmethod
    def debug_print_all_app_install_info():
        """打印当前所有应用的安装信息"""
        windows_device = WindowsDevice()
        print(windows_device.get_instaled_apps())
        print(type(windows_device.get_instaled_apps()))
        print("--------------------------------")
        for i, n in windows_device.get_instaled_apps().items():
            print(i, type(i), n.__dict__)

    @staticmethod
    def debug_print_obj_all_property_value(obj):
        """打印当前duixiang对象所有属性值"""
        print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

    @staticmethod
    def debug_print_top_page_info():
        """打印当前最上层窗口的进程信息"""
        print(Base_fun_api.get_active_window_process_info())


if __name__ == '__main__':
    # Debug_print.debug_print_all_app_install_info()
    # time.sleep(5)
    # Debug_print.debug_print_top_page_info()
    # Base_fun_api.progress_bar_sleep(120)
    # Base_fun_api.set_page_close(658192)
    # Base_fun_api.set_page_close(1251544)
    Base_fun_api.get_target_window_info()
    # Base_fun_api.set_page_close(Base_fun_api.get_top_page_hwnd())
