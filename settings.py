import logging


logger = logging.getLogger('App')

logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('src/log.log')
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(module)s:  %(message)s', datefmt='%d-%b-%y %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Проверка кодировки
