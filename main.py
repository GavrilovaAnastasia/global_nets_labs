#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Лабораторная 2: Код Хэмминга
Вариант 15
Длина слова с контрольными битами: 47
Алгоритм контрольной суммы: CRC-64
"""

from crc64iso.crc64iso import crc64
from typing import List
from math import log2, ceil
from random import randrange


def hamming_core(src: List[List[int]], s_num: int, encode=True) -> int:
    s_range = range(s_num)
    errors = 0
    fixed_errors = 0
    for i in src:
        sindrome = 0
        for s in s_range:
            sind = 0
            for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                for j in range(2 ** s):
                    if (p + j) > len(i):
                        break
                    sind ^= i[p + j - 1]

            if encode:
                i[2 ** s - 1] = sind
            else:
                sindrome += (2 ** s * sind)

        if (not encode) and sindrome:
            try:
                i[sindrome - 1] = int(not i[sindrome - 1])
                fixed_errors += 1
            except IndexError:
                errors += 1
    if not encode:
        print(f'Исправлено ошибок: {fixed_errors}')

    return errors


def encoding(txt: str, lngth: int = 8) -> str:
    result = ""
    msg_b = txt.encode("utf8")
    s_num = ceil(log2(log2(lngth + 1) + lngth + 1))
    bit_seq = []
    for byte in msg_b:
        bit_seq += list(map(int, f"{byte:08b}"))

    res_len = ceil((len(msg_b) * 8) / lngth)
    bit_seq += [0] * (res_len * lngth - len(bit_seq))

    to_hamming = []

    for i in range(res_len):
        code = bit_seq[i * lngth:i * lngth + lngth]
        for j in range(s_num):
            code.insert(2 ** j - 1, 0)
        to_hamming.append(code)

    for i in to_hamming:
        result += "".join(map(str, i))

    return result


def decoding(txt: str, lngth: int = 8):
    result = ""

    s_num = ceil(log2(log2(lngth + 1) + lngth + 1))
    res_len = len(txt) // (lngth + s_num)
    code_len = lngth + s_num

    to_hamming = []

    for i in range(res_len):
        code = list(map(int, txt[i * code_len:i * code_len + code_len]))
        to_hamming.append(code)

    errors = hamming_core(to_hamming, s_num, False)

    for i in to_hamming:
        for j in range(s_num):
            i.pop(2 ** j - 1 - j)
        result += "".join(map(str, i))

    msg_l = []

    for i in range(len(result) // 8):
        val = "".join(result[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))
    try:
        result = bytes(msg_l).decode("utf-8")
    except UnicodeDecodeError:
        pass

    return result, errors


def less_than_one_error(txt: str, lngth: int) -> str:
    sequence = list(map(int, txt))
    s_num = ceil(log2(log2(lngth + 1) + lngth + 1))
    code_len = lngth + s_num
    cnt = len(txt) // code_len
    result = ""
    print(f'Всего ошибок: {cnt}')
    for i in range(cnt):
        to_noize = sequence[i * code_len:i * code_len + code_len]
        noize = randrange(code_len)
        to_noize[noize] = int(not to_noize[noize])
        result += "".join(map(str, to_noize))

    return result


def more_than_one_error(txt: str, lngth: int) -> str:
    sequence = list(map(int, txt))
    s_num = ceil(log2(log2(lngth + 1) + lngth + 1))
    code_len = lngth + s_num
    cnt = len(txt) // code_len
    result = ""
    print(f'Всего ошибок: {cnt}')
    for i in range(cnt):
        to_noize = sequence[i * code_len:i * code_len + code_len]
        noize1 = randrange(code_len)
        noize2 = randrange(code_len)
        noize3 = randrange(code_len)
        to_noize[noize1] = int(not to_noize[noize1])
        to_noize[noize2] = int(not to_noize[noize2])
        to_noize[noize3] = int(not to_noize[noize3])
        result += "".join(map(str, to_noize))

    return result


def sending(encoded_txt: str, lngth: int):
    print(f'Результат кодирования: {encoded_txt}')
    decoded_text, e = decoding(encoded_txt, lngth)
    print(f'Результат декодирования: {decoded_text}')
    checksum_after = crc64(decoded_text)
    print(f'Контрольная сумма: {checksum_after}')
    print(f'Контрольные суммы до и после совпадают: {checksum_after == checksum}')


if __name__ == '__main__':
    text = '''
    В начале и середине 1970-х годов сеть в основном либо спонсировалась государством (NPL network в Великобритании, ARPANET в США, CYCLADES во Франции), либо разрабатывалась вендорами с использованием собственных стандартов, таких как IBM Systems Network Architecture и Digital Equipment Corporation DECnet. Общественные сети передачи данных только начинали появляться, и в конце 1970-х годов они использовали стандарт X.25.
    Экспериментальная система коммутации пакета в Великобритании примерно в 1973—1975 годах выявила необходимость определения протоколов более высокого уровня. После публикации британского Национального вычислительного центра «Для чего нужны распределенные вычисления», ставшей результатом крупных исследований будущих конфигураций компьютерных систем, Великобритания представила аргументы в пользу создания Международной комиссии по стандартам для охвата этой области на совещании Международной организации по стандартизации (ISO) в Сиднее в марте 1977 года.
    С 1977 года ИСО реализовала программу по разработке общих стандартов и методов сетевого взаимодействия. Аналогичный процесс развивался в Международном консультационном комитете по телеграфии и телефонии (CCITT). Оба органа разработали документы, определяющие схожие сетевые модели. Модель OSI была впервые определена в исходном виде в Вашингтоне в феврале 1978 года французом Хьюбертом Циммерманом, немного доработанный проект стандарта был опубликован ИСО в 1980 году.
    Разработчикам модели пришлось столкнуться с конкурирующими приоритетами и интересами. Темпы технологических изменений обусловили необходимость определения стандартов, к которым новые системы могли бы сходиться, а не стандартизировать процедуры постфактум, тогда как традиционный подход к разработке стандартов был противоположным. Хотя это и не был сам стандарт, он представлял собой основу, на базе которой можно было бы определить будущие стандарты.
    В 1983 году документы CCITT и ISO были объединены и таким образом была сформирована базовая эталонная модель взаимосвязи открытых систем, обычно и называемая эталонной моделью взаимосвязи открытых систем (англ. Open Systems Interconnection, OSI) или просто моделью OSI. Объединённый документ был опубликован в 1984 году и ISO — как стандарт ISO 7498, и переименованным CCITT (ныне сектор стандартизации электросвязи Международного союза электросвязи или МСЭ-Т) — как стандарт X. 200.
    OSI состояла из двух основных компонентов: абстрактной модели сети, называемой базовой эталонной моделью или семислойной моделью, и набора сетевых протоколов. Основываясь на идее согласованной модели уровней протоколов, определяющей взаимодействие между сетевыми устройствами и программным обеспечением, эталонная модель OSI стала крупным достижением в стандартизации концепций сетевого взаимодействия.
    '''
    print(f'Исходный текст: {text}')
    length = 41  # т. к. длина слова с контрольными битами - 47, то значащих битов - 41
    checksum = crc64(text)
    print(f'Контрольная сумма: {checksum}')

    print('\n### Первая отправка (без ошибок)')
    encoded_text = encoding(text, length)
    sending(encoded_text, length)

    print('\n### Вторая отправка (не более 1 ошибки на слово)')
    modified_text = less_than_one_error(encoded_text, length)
    sending(modified_text, length)

    print('\n### Третья отправка (больше 1 ошибки на слово)')
    modified_text = more_than_one_error(encoded_text, length)
    sending(modified_text, length)
