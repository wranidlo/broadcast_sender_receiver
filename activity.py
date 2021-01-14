#!/usr/bin/env python3
import json
import subprocess
import time
from operator import itemgetter
import os


def time_format(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def get(command):
    try:
        return subprocess.check_output(command).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        pass


class ActivityLogger:
    def __init__(self):
        self.period = 5
        self.start_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.t = 0
        self.list_of_active_apps = []
        self.list_of_activity_in_apps = []

    def run(self):
        while True:
            window_pid = get(["xdotool", "getactivewindow", "getwindowpid"])
            window_name = get(["xdotool", "getactivewindow", "getwindowname"])
            if window_pid is not None:
                app = get(["ps", "-p", window_pid, "-o", "comm="])
            else:
                app = get(["ps", "-p", "Unknown window", "-o", "comm="])
            if app not in self.list_of_active_apps:
                self.list_of_active_apps.append(app)
            checklist = [item[1] for item in self.list_of_activity_in_apps]
            if window_name not in checklist:
                self.list_of_activity_in_apps.append([app, window_name, 1 * self.period])
            else:
                self.list_of_activity_in_apps[checklist.index(window_name)][
                    2] = self.list_of_activity_in_apps[checklist.index(window_name)][2] + 1 * self.period
            if self.t == 30 / self.period:
                self.summarize()
                self.t = 0
            else:
                self.t += 1
            time.sleep(self.period)

    def summarize(self):
        total_time = sum([it[2] for it in self.list_of_activity_in_apps])
        all_data = []
        for app in self.list_of_active_apps:
            appdata = []
            window_data = []
            app_time = sum([it[2] for it in self.list_of_activity_in_apps if it[0] == app])
            app_percents = round(100 * app_time / total_time)
            for d in [app, app_time, app_percents]:
                appdata.append(d)
            wins = [r for r in self.list_of_activity_in_apps if r[0] == app]
            for w in wins:
                window_percents = str(round(100 * w[2] / total_time))
                window_data.append([w[1], w[2], window_percents])
            window_data = sorted(window_data, key=itemgetter(1))
            window_data = window_data[::-1]
            appdata.append(window_data)
            all_data.append(appdata)
        all_data = sorted(all_data, key=itemgetter(1))
        all_data = all_data[::-1]

        list_to_save = []

        for item in all_data:
            dict_app = {}
            app = item[0]
            app_time = item[1]
            app_percents = item[2]
            dict_app["app"] = str(app)
            dict_app["time"] = time_format(app_time)
            dict_app["percentage"] = str(app_percents)
            windows_list = []
            for w in item[3]:
                window_dict = {}
                window_name = w[0]
                window_time = w[1]
                window_percents = w[2]
                window_dict["window_name"] = str(window_name)
                window_dict["window_time"] = time_format(window_time)
                window_dict["window_percentage"] = window_percents
                windows_list.append(window_dict)
            dict_app["windows"] = windows_list
            list_to_save.append(dict_app)
        with open('/etc/virtualab/vm-communicator/log_activity.json', 'w') as out:
            json.dump(list_to_save, out, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    logger = ActivityLogger()
    logger.run()
