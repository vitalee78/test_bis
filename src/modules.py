import datetime
import json
import os
import platform


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file, encoding="utf-8") as f:
        target = json.loads(f.read())
    return target


def get_platform():
    return platform.system() + ' ' + platform.release()


def get_date_now():
    """
        получить текущею дату для подстановки в название файла/папки
    :return: date
    """
    date_format = '%d-%m-%Y'
    today = datetime.datetime.now()
    return today.strftime(date_format)


def create_folder():
    """
        создаёт папку на текущий день
        в ней складываются screenshots Failed/Broken тесты
    :return:
    """
    path = '//bf/common/IT/testing/screenshots'
    folder = path + '/' + f'failed_{get_date_now()}'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    directory = os.path.join(folder)
    return directory