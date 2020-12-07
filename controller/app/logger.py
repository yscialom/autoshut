import logging


def getLogger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt="%Y-%m-%d %H:%M:%S %Z")
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger
