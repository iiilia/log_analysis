# coding: utf-8

import re
import numpy as np
from datetime import time, timedelta

stop_regex = re.compile(u"(SQLProxy)|(P2_COD)", flags=re.UNICODE)


def process_result(time_type_structure, f_out, last_time_write):
    for key in list(time_type_structure.keys()):
        in_second_structure = time_type_structure[key]
        if in_second_structure.get('count_in', 0) == in_second_structure.get('count_in', 0) \
                and not in_second_structure.get('now_or_past', True) \
                and time.strftime(key[0], '%h:%m:%s') == (time.strftime(last_time_write, '%h:%m:%s') + \
                                                                  timedelta(seconds=1)):
            # это условие нужно переписать нормально (ПРОВЕРИТЬ)
            result_line = count_stat_by_second(in_second_structure)
            f_out.write(result_line)


def count_stat_by_second(in_second_structure):
    res = list()
    # считаем статистику
    return u';'.join([str(x) for x in res])


def line_processing(line):
    # функция, которая обрабатывает строку и возвращает словарь с нужными атрибутами

    # q_or_a - запрос или ответ

    global stop_regex

    result = None

    if len(stop_regex.findall(line)) > 0:
        line_temp = line.split(u'|')
        log_time = line_temp[0]
        line = u'|'.join(line_temp[1:]).split(u';')

        time_to_seconds = log_time.split(u'.')[0]
        id = line[0]
        # получение типа сообщения
        type_of_line = u''
        q_or_a = u''
        time_full = time.strftime(log_time, '%h:%m:%s.%f')

    return (time_to_seconds, id, type_of_line, q_or_a, time_full)


def __main__(*argv):
    if argv and argv[0] > 2:
        path_to_data = argv[1]

        # путь к файлу с результатами
        path_to_result = u''

        # нам не указана кодировка файла
        f = open(path_to_data, 'r')

        f_out = open(path_to_result, 'w', encoding='utf8')

        # структура для каждого момента времени и каждого типа
        # {(время, тип):{
        #       id: {
        #           q: время запроса
        #           a: время ответа
        #           },
        #       count_in: int       количество запросов
        #       count_out: int      количество ответов
        #       now_or_past: bool   из этого ли момента времени приходят сейчас запросы? или мы можем получить еще новых
        #   }
        # }
        time_type_structure = dict()

        # последнее время, за которое записана статистика
        last_time_write = None
        last_q_time = None

        for line in f:

            # Если count_in == count_out и now_or_past == False -> считаем статистику
            # по этому моменту и пишем ее в файл

            # нужно проверить, что секунды пишутся последовательно

            # вопрос? теряются ли запросы? или на каждый запрос приходит ответ обязательно?
            # если теряются, то как их считать?

            structure = line_processing(line)
            if structure:
                (time_to_seconds, id, type_of_line, q_or_a, time_full) = structure
                if last_q_time < time_to_seconds and q_or_a == u'q':
                    last_q_time = time_to_seconds
                temp_structure = time_type_structure.get((time_to_seconds, type_of_line), dict())
                temp_id_structure = temp_structure.get(id, dict())
                temp_id_structure[q_or_a] = time_full

                # обновляем статистику по секунде и по типу
                count_in = temp_structure.get(u'count_in', 0)
                count_out = temp_structure.get(u'count_out', 0)
                now_or_past = temp_structure.get(u'now_or_past', True)

                if q_or_a == u'q':
                    count_in += 1
                    # проверяем что запрос пришел из новой секунды
                elif q_or_a == 'a':
                    count_out += 1

                if last_q_time > time_to_seconds:
                    now_or_past = False

                temp_structure['now_or_past'] = now_or_past
                temp_structure[u'count_in'] = count_in
                temp_structure[u'count_out'] = count_out

                temp_structure[id] = temp_id_structure
                time_type_structure[(time_to_seconds, type_of_line)] = temp_structure

            process_result(time_type_structure, f_out, last_time_write)

        f.close()
        f_out.close()
