import time
import json
from profesor.server import Sender
from profesor.server_thread import ThreadedListener , listen


def title_bar():
    print("\t**********************************************")
    print("\t**************  Professor  app  **************")
    print("\t**********************************************")


def user_choice():
    print("[1] Send broadcast message\n")
    print("[2] Check attendance\n")
    print("[3] Change ip broadcast\n")
    print("[q] Quit.")
    return input("What would you like to do? ")


if __name__ == '__main__':
    title_bar()

    s = ThreadedListener(target=listen)
    s.start()

    sender = Sender()
    sender.set_broadcast_ip()

    choice = ''
    while choice != 'q':
        choice = user_choice()
        if choice == "1":
            message = str(input("Message to send: "))
            message_json = json.dumps({"message": message, "who": "professor", "type": "message"})
            sender.send_broadcast_message(message_json.encode("utf-8"))
            time.sleep(1)
        if choice == "2":
            message = str("Attendance check")
            message_json = json.dumps({"message": message, "who": "professor", "type": "attendance"})
            sender.send_broadcast_message(message_json.encode("utf-8"))
            time.sleep(1)
        if choice == "3":
            sender.set_broadcast_ip()
            time.sleep(1)

    s.kill()
    s.join()
    if not s.is_alive():
        print("Stopped listening for presence")
