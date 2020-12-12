#!/usr/bin/env python3
import subprocess
import time
import os
from operator import itemgetter

# -- set update/round time (seconds)
period = 5 
# -- set sorting order. up = most used first, use either "up" or "down"
order = "up"

# don change anything below
home = os.environ["HOME"]
logdir = home+"/.usagelogs"

def currtime(tformat=None):
    return time.strftime("%Y_%m_%d_%H_%M_%S") if tformat == "file"\
           else time.strftime("%Y-%m-%d %H:%M:%S")

try:
    os.mkdir(logdir)
except FileExistsError:
    pass

# path to your logfile
log = logdir+"/"+currtime("file")+".txt"; startt = currtime()

def get(command):
    try:
        return subprocess.check_output(command).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        pass

def time_format(s):
    # convert time format from seconds to h:m:s
    m, s = divmod(s, 60); h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def summarize():
    with open(log, "wt" ) as report:
        totaltime = sum([it[2] for it in winlist]) # total time
        report.write("")
        alldata = []      
        for app in applist:
            appdata = []; windata = []
            apptime = sum([it[2] for it in winlist if it[0] == app])
            appperc = round(100*apptime/totaltime)            
            for d in [app, apptime, appperc]:
                appdata.append(d)
            wins = [r for r in winlist if r[0] == app]            
            for w in wins:
                wperc = str(round(100*w[2]/totaltime))
                windata.append([w[1], w[2], wperc])                
            windata = sorted(windata, key=itemgetter(1))
            windata = windata[::-1] if order == "up" else windata
            appdata.append(windata); alldata.append(appdata)            
        alldata = sorted(alldata, key = itemgetter(1))
        alldata = alldata[::-1] if order == "up" else alldata        
        for item in alldata:
            app = item[0]; apptime = item[1]; appperc = item[2]
            report.write(
                ("-"*60)+"\n"+app+"\n"+time_format(apptime)\
                +" ("+str(appperc)+"%)\n"+("-"*60)+"\n"
                )            
            for w in item[3]:
                wname = w[0]; time = w[1]; perc = w[2]
                report.write(
                    "   "+time_format(time)+" ("+perc+"%)"\
                    +(6-len(perc))*" "+wname+"\n"
                    )
        report.write(
            "\n"+"="*60+"\nstarted: "+startt+"\t"+"updated: "\
            +currtime()+"\n"+"="*60
            )

t = 0; applist = []; winlist = []

while True:
    time.sleep(period)
    frpid = get(["xdotool", "getactivewindow", "getwindowpid"])
    frname = get(["xdotool", "getactivewindow", "getwindowname"])
    app = get([
        "ps", "-p", frpid, "-o", "comm="
        ]) if frpid != None else "Unknown"
    # fix a few names
    if "gnome-terminal" in app:
        app = "gnome-terminal"
    elif app == "soffice.bin":
        app = "libreoffice"
    # add app to list
    if not app in applist:
        applist.append(app)
    checklist = [item[1] for item in winlist]
    if not frname in checklist:
        winlist.append([app, frname, 1*period])
    else:
        winlist[checklist.index(frname)][
            2] = winlist[checklist.index(frname)][2]+1*period
    if t == 60/period:
        summarize()
        t = 0
    else:
        t += 1