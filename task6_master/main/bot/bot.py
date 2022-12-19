import os
import re
from doctest import master
from os import path

from task6_master.main.data_base.base_connect import BaseConnect


# from processor import Processor

#                 Hello, bot!
#             _____________________
#             |   Hello! Can I    |
#             |     help u?       |
#             |___________________|
#                       |
#               I want to sing up!
#                       |
#             __________V__________          _____________________        ______________________        _______________
#             | Okay! I can sign  |  When?   |      For          |        |                    | Thanks!|             |
#     ------->| you up for the    | -------> | {near date        |        |    I sign u up!    | ------>|  Good bye!  |
#     |       |   near time.      |          |     from base}    |        |____________________|        |_____________|
#     |       |___________________|          |___________________|                   ^                         ^
#     |                 \                             /         |                    |                         |
#     |                  \___________________________/          |                    |                         |
#     |                                  |                      | Okay               |                         |
#     |                            No, can I sign up            |                    |                         |
#     |                 _______________on {date}?  -------      |                    |                         |
#     |                 |                                |      |                    |                         |
#     |       __________V__________            __________V______V___                 |                         |
#     |  Yes  |  No, this day is  |            |    What time      |   {time}        |                         |
#     ------- |full! Do you still |            |    from this?     |------------------                         |
#             |  want to sign up? |            |     {arr_time}    |                                           |
#             |___________________|            |___________________|                                           |
#                     | No                                                                                     |
#                     ------------------------------------------------------------------------------------------


class Bot:

    def __init__(self):
        print("ok")

    ANSWER_START_DIALOG = "\nПривет!) Чем могу помочь?\n"
    ANSWER_NOT_UNDERSTAND = "\nЯ не понимаю о чем Вы! Пожалуйста, переформулируйте запрос.\n"
    ANSWER_NEAR_DAY_SIGN_UP = "\nОтлично! Могу записать вас на ближайшее число.\n"
    ANSWER_WHICH_DAY_SIGN_UP = "\nЭто будет "
    ANSWER_DAY_IS_FULL = "\nЭтот день весь занят. Вы всё еще хотите записаться?\n"
    ANSWER_WHICH_TIME = "\nПожалуйста, уточните, на какое время Вас записать? "
    ANSWER_SUCCESSFUL_SIGN_UP = "\nЗаписал! :)\n"
    ANSWER_GOOD_BYE = "\nХорошего дня!\n"

    QUESTION_HELLO = "([Пп]ривет|[Зз]дравствуй)"
    QUESTION_SIGN_UP = "([Хх]о[чт]|[Мм]ожн).+(ног|маник)"
    QUESTION_WHAT_IS_NEAR_DAY = "([Чч]то|[Кк]ако|[Кк]огда).+"
    QUESTION_NEAR_DAY_IS_GOOD = "([Оо]тлич|[Хх]орош|[Дд]авай||[Зз]апи[сш])"
    QUESTION_OWN_DATE = "(\d{1,2}.\d{1,2})"
    QUESTION_STILL_WANT_SIGN_UP = "([Дд]а|[Кк]онечно|[Хх]о)"
    QUESTION_WANT_FINISH = "([Нн]е)"
    QUESTION_WHICH_TIME = "(\d{1,2}:\d{1,2})"
    QUESTION_THANKS = "([Сс]паси)"

    def check_start(self, ask_client, link_dialog):
        start_dialog = re.findall(r"{}".format(self.QUESTION_HELLO), ask_client)
        if start_dialog or not path.exists(link_dialog):  # Если фраза начала диалога, чистим файл, указываем study:0
            self.set_study(link_dialog, 0)
            return True
        return False
        #     with open(link_dialog, 'w') as file:
        #         file.write("study: 0 \n")
        #         study = 0
        # else:
        #     study = self.get_Study(link_dialog)
        #     study = float(study)

    def doing_study0(self, link_dialog, is_start):
        if is_start:
            self.write_in_dialog_file(self.ANSWER_START_DIALOG, link_dialog)
            # file.write(self.ANSWER_START_DIALOG)
            self.set_study(link_dialog, 1)

    def doing_study1(self, ask_client, link_dialog):
        want_sign_up = re.findall(r"{}".format(self.QUESTION_SIGN_UP), ask_client)
        if want_sign_up:
            self.write_in_dialog_file(self.ANSWER_NEAR_DAY_SIGN_UP, link_dialog)
            # file.write(self.ANSWER_NEAR_DAY_SIGN_UP)
            self.set_study(link_dialog, 2)

    def doing_study2(self, ask_client, link_date, link_dialog):
        if not self.check_own_date(ask_client, link_date, link_dialog):
            what_day = re.findall(r"{}".format(self.QUESTION_WHAT_IS_NEAR_DAY), ask_client)
            if what_day:  # если уточняет когда

                self.set_date(link_date, self.get_near_time())

                line = self.ANSWER_WHICH_DAY_SIGN_UP + self.get_date(link_date) + "\n"
                self.write_in_dialog_file(line, link_dialog)
                self.set_study(link_dialog, 3)

    def check_own_date(self, ask_client, link_date, link_dialog):
        what_day = re.findall(r"{}".format(self.QUESTION_OWN_DATE), ask_client)
        print(what_day)
        if what_day:  # Если есть свободное место в этот день
            what_day = what_day[0].split(".")
            line = what_day[0] + "." + what_day[1]
            self.set_date(link_date, line)
            res = BaseConnect().check_date(what_day[1], what_day[0])
            if res:
                line = self.ANSWER_WHICH_TIME
                for i in res:
                    line += re.search(r"(\d{1,2}:\d{1,2})", str(i))[0]
                    line += " "
                line += "?\n"
                self.write_in_dialog_file(line, link_dialog)
                self.set_study(link_dialog, 4.1)
            else:
                self.write_in_dialog_file(self.ANSWER_DAY_IS_FULL, link_dialog)
                self.set_study(link_dialog, 4.2)
            return True
        return False

    def doing_study3(self, ask_client, link_date, link_dialog):
        if not self.check_own_date(ask_client, link_date, link_dialog):
            what_day = re.findall(r"{}".format(self.QUESTION_NEAR_DAY_IS_GOOD), ask_client)
            if what_day:
                line = self.get_date(link_date).split(".")
                res = BaseConnect().check_date(line[1], line[0])
                if res:
                    line = self.ANSWER_WHICH_TIME
                    for i in res:
                        line += re.search(r"(\d{1,2}:\d{1,2})", str(i))[0]
                        line += " "
                    line += "?\n"
                    self.write_in_dialog_file(line, link_dialog)
                    self.set_study(link_dialog, 4.1)

    def doing_study4_1(self, ask_client, link_date, link_dialog, id_client):
        what_time = re.search(r"{}".format(self.QUESTION_WHICH_TIME), ask_client)[0]
        if what_time:
            self.write_in_dialog_file(self.ANSWER_SUCCESSFUL_SIGN_UP, link_dialog)
            self.set_study(link_dialog, 5)
            line = (self.get_date(link_date)).split(".")
            print(line)
            BaseConnect().sing_up(line[1], line[0], str(what_time), id_client)

    def doing_study4_2(self, ask_client, link_dialog):
        want_or_not = re.findall(r"{}".format(self.QUESTION_STILL_WANT_SIGN_UP), ask_client)
        if want_or_not:
            self.write_in_dialog_file(self.ANSWER_NEAR_DAY_SIGN_UP, link_dialog)
            self.set_study(link_dialog, 2)
        else:
            want_or_not = re.findall(r"{}".format(self.QUESTION_WANT_FINISH), ask_client)
            if want_or_not:
                self.write_in_dialog_file(self.ANSWER_GOOD_BYE, link_dialog)
                self.set_study(link_dialog, 5)

    def generate_answer_v2(self, id_client, ask_client, link):
        link = self.make_dir(id_client, link)
        link_dialog = link + "\\dialog.txt"
        link_date = link + "\\date.txt"
        is_start = self.check_start(ask_client, link_dialog)
        study = self.get_study(link_dialog)
        self.write_in_dialog_file(ask_client, link_dialog)
        if study == 0:  # Поздороваться
            self.doing_study0(link_dialog, is_start)
        elif study == 1:  # хочу на ноготочки
            self.doing_study1(ask_client, link_dialog)
        elif study == 2:  # предлагаем ближайшее время
            self.doing_study2(ask_client, link_date, link_dialog)
        elif study == 3:
            self.doing_study3(ask_client, link_date, link_dialog)
        elif study == 4.1:
            self.doing_study4_1(ask_client, link_date, link_dialog, id_client)
        elif study == 4.2:
            self.doing_study4_2(ask_client, link_dialog)
        if study == self.get_study(link_dialog):  # Сообщаем пользователю, что запрос непонятен
            self.write_in_dialog_file(self.ANSWER_NOT_UNDERSTAND, link_dialog)

    def get_answer(self, id_client, ask_client, link):
        self.generate_answer_v2(id_client, ask_client, link)
        link_dialog = str(link) + str(id_client) + "\\dialog.txt"
        with open(link_dialog, 'r') as file:
            arr_message = file.readlines()
        arr_message.pop(0)
        arr_message.reverse()
        return arr_message

    @staticmethod
    def write_in_dialog_file(line, link):
        with open(link, 'a') as file:
            file.write(line)

    @staticmethod
    def get_date(link_date):
        with open(link_date, 'r') as f:
            return f.readline()

    @staticmethod
    def set_date(link_date, line):
        with open(link_date, 'w') as f:
            f.write(line)

    @staticmethod
    def get_study(link):
        with open(link) as file:
            line = file.readline()
        study_reg = "(\d\s|(\d.\d))"
        return float(re.search(r"{}".format(study_reg), line)[0])

    @staticmethod
    def set_study(link, study):
        line_study = "study: " + str(study) + " \n"
        if study == 0:
            with open(link, 'w') as file:
                file.write(line_study)
        else:
            with open(link, 'r') as file:
                lines = file.readlines()
            lines[0] = line_study
            with open(link, 'w') as file:
                for line in lines:
                    file.write(line)

    @staticmethod
    def get_near_time():
        res = BaseConnect().find_near_time()
        return str(res[1]) + '.' + str(res[0])

    @staticmethod
    def make_dir(id_client, link):
        try:
            link = str(link) + str(id_client)
            os.mkdir(link)
        except FileExistsError:
            print("уже есть")

        return link
