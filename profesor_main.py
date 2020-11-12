import time
from profesor.server import Sender
from profesor.server_thread import ThreadedListener , listen


def title_bar():
    print("\t**********************************************")
    print("\t**************   Communicator   **************")
    print("\t**********************************************")


def user_choice():
    print("[1] Send broadcast message\n")
    print("[2] Check attendance\n")
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
            message = str(input("Message to send: ")).encode("utf-8")
            sender.send_broadcast_message(message)
            time.sleep(1)
        if choice == "2":
            message = str("Attendance check").encode("utf-8")
            sender.send_broadcast_message(message)
            time.sleep(1)

    s.kill()
    s.join()
    if not s.is_alive():
        print("Stopped listening for presence")
