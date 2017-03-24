# coding: utf-8

import re
from datetime import time

stop_regex = re.compile(u"(SQLProxy)|(P2_COD)", flags=re.UNICODE)

def line_processing(line):
    # функция, которая обрабатывает строку и возвращает словарь с нужными атрибутами

    global stop_regex

    result = None

    if len(stop_regex.findall(line)) > 0:
        result = dict()
        line_temp = line.split(u'|')
        log_time = line_temp[0]
        line = u'|'.join(line_temp[1:]).split(u';')

        time_to_seconds = log_time.split(u'.')[0]
        id = line[0]
        result['time'] = time.strftime(log_time, '%h:%m:%s.%f')

    return (time_to_seconds, id, result)


def __main__(*argv):

    if argv and argv[0] > 2:
        path_to_data = argv[1]

        # путь к файлу с результатами
        path_to_result = u''

        # нам не указана кодировка файла
        f = open(path_to_data, 'r')

        f_out = open(path_to_result, 'w', encoding='utf8')

        for line in f:
            # для каждого момента времени час-минута-секунда имеем структуру со следующими атрибутами
            #   1 количество запросов
            #   2 количество ответов
            #   3 из этого ли момента времени приходят сейчас запросы? или мы можем получить еще новых

            # Если количество запросов == количество ответов и 3 == False -> считаем статистику
            # по этому моменту и пишем ее в файл

            # нужно проверить, что секунда пишутся последовательно
            
            line_processed = line_processing(line)

        # тут что то происходит

        f.close()
        f_out.close()