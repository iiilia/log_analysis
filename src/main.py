# coding: utf-8

import re
stop_regex = re.compile(u"(SQLProxy)|(P2_COD)", flags=re.UNICODE)

def line_processing(line):
    # функция, которая обрабатывает строку и возвращает словарь с нужными атрибутами

    global stop_regex

    result = None

    if len(stop_regex.findall(line)) > 0:
        result = dict()
        line_temp = line.split(u'|')
        time = line_temp[0]
        line = u'|'.join(line_temp[1:]).split(u';')

    return result


def __main__(*argv):
    if argv and argv[0] > 2:
        path_to_data = argv[1]
        f = open(path_to_data, 'r') # нам не указана кодировка файла
        for line in f:
            line_processed = line_processing(line)
