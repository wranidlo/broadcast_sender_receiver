#!/usr/bin/env python3
import json
import subprocess
import time
from operator import itemgetter


def get_active_app_pid(command):
    try:
        return subprocess.check_output(command).decode("utf-8").strip()
    except subprocess.CalledProcessError:  # No active apps
        pass


def get_active_name(command):
    try:
        return subprocess.check_output(command).decode("utf-8").strip()
    except subprocess.CalledProcessError:  # No active windows
        return "nothing"


class ActivityLogger:
    def __init__(self):
        self.period = 5
        self.start_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.t = 0
        self.list_of_active_apps = []
        self.windows_app_time = {}
        self.cycles_to_save = 9

    def run(self):
        while True:
            app_pid = get_active_app_pid(["xdotool", "getactivewindow", "getwindowpid"])
            window_name = get_active_name(["xdotool", "getactivewindow", "getwindowname"])
            if app_pid is not None:
                app_name = get_active_name(["ps", "-p", app_pid, "-o", "comm="])
            else:
                app_name = get_active_name(["ps", "-p", "Unknown window", "-o", "comm="])
            if app_name not in self.list_of_active_apps:
                self.list_of_active_apps.append(app_name)
            old_windows = self.windows_app_time.keys()
            if window_name not in old_windows:
                self.windows_app_time[window_name] = {"app": app_name, "time": self.period}
            else:
                self.windows_app_time[window_name]["time"] += self.period
            if self.t == self.cycles_to_save:
                self.save_activity_log()
                self.t = 0
            else:
                self.t += 1
            time.sleep(self.period)

    def save_activity_log(self):
        total_time = sum([self.windows_app_time[e]["time"] for e in self.windows_app_time])
        all_data = []
        for app in self.list_of_active_apps:
            appdata = []
            window_data = []
            app_time = sum(self.windows_app_time[e]["time"] for e in self.windows_app_time
                           if self.windows_app_time[e]["app"] == app)
            app_percents = round(100 * app_time / total_time, 2)
            for d in [app, app_time, app_percents]:
                appdata.append(d)
            windows = [[e, self.windows_app_time[e]] for e in self.windows_app_time
                    if self.windows_app_time[e]["app"] == app]
            for window in windows:
                window_percents = str(round(100*(window[1]["time"] / total_time), 2))
                window_data.append([window[0], window[1]["time"], window_percents])
            window_data = sorted(window_data, key=itemgetter(1))
            appdata.append(window_data)
            all_data.append(appdata)
        all_data = sorted(all_data, key=itemgetter(1))
        list_to_save = []

        for one_app_data in all_data:
            dict_app = {}
            app = one_app_data[0]
            app_time = one_app_data[1]
            app_percents = one_app_data[2]
            dict_app["app"] = str(app)
            dict_app["time"] = time.strftime('%H:%M:%S', time.gmtime(app_time))
            dict_app["percentage"] = str(app_percents) + " %"
            windows_list = []
            for window in one_app_data[3]:
                window_dict = {}
                window_name = window[0]
                window_time = window[1]
                window_percents = window[2]
                window_dict["window_name"] = str(window_name)
                window_dict["window_time"] = time.strftime('%H:%M:%S', time.gmtime(window_time))
                window_dict["window_percentage"] = window_percents  + " %"
                windows_list.append(window_dict)
            dict_app["windows"] = windows_list
            list_to_save.append(dict_app)
        with open('log_activity.json', 'w') as out: #  /etc/virtualab/vm-communicator/
            json.dump(list_to_save, out, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    logger = ActivityLogger()
    logger.run()
