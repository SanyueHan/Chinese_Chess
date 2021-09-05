"""
The purpose of encoding chinese characters to letters is to simplify internal logic:
"""


ENCODE = {
    '进': '+',
    '退': '-',
    '平': '=',
    '前': '^',  # front
    '后': '$',  # back
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '车': 'r',  # rook
    '马': 'k',  # knight
    '炮': 'c',  # cannon
    '相': 'm',  # minister
    '士': 'a',  # assistant
    '帅': 'g',  # general
    '兵': 'p',  # pawn
    '車': 'R',
    '馬': 'K',
    '砲': 'C',
    '象': 'M',
    '仕': 'A',
    '将': 'G',
    '卒': 'P',
}


DECODE = {e: c for c, e in ENCODE.items()}
