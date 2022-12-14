import math

class Constants:
    TRIANGLE_SLICES = (((13, 17, 4, 8), (9, 13, 9, 13), (4, 8, 13, 17), (0, 4, 9, 13), (4, 8, 4, 8), (9, 13, 0, 4)),
                       ((10, 13, 3, 6), (7, 10, 7, 10), (3, 6, 10, 13), (0, 3, 7, 10), (3, 6, 3, 6), (7, 10, 0, 3)))
    OVAL_RADIUS = (15, 19.5)
    OVAL_LIST_COL_OFFSET = ((12, 11, 10, 9, 4, 4, 4, 4, 4, 3, 2, 1, 0, 4, 4, 4, 4),
                            (9, 8, 7, 3, 3, 3, 3, 2, 1, 0, 3, 3, 3))
    SLEEP_TIME = 0.2
    BOARD_SIZES = (17, 13)
    LROW_SIZE = (4, 3)
    TARGET_PITS = (((0, 12, -12), (4, 4, -8), (12, 0, -12), (16, 4, -20), (12, 12, -24), (4, 16, -20)), ((0, 9, -9), (3, 3, -6), (9, 0, -9), (12, 3, -15), (9, 9, -18), (3, 12, -15)))
    ROW_MIDDLES = ((12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4), (9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3))
    W1 = 0.9
    W2 = 0.2
    W3 = 0.4
    TWO_PLAYERS_OPTIONS = ((1, 4), (2, 5), (3, 6))
    PLAYERS_LISTS_THREE_AND_UP = ((1, 3, 5), (1, 2, 4, 5), (1, 2, 3, 5, 6), (1, 2, 3, 4, 5, 6))