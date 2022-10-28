import time
import random


def random_number_generator(pathname):
    while True:
        time.sleep(1)
        f = open(pathname, 'r+')
        text = f.readline()

        if text == 'run':
            random_num = str(random.randint(0, 2))
            f.seek(0)
            f.truncate(0)
            f.write(random_num)

        f.close()

