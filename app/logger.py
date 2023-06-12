import logging


class ColoredLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.red = "\033[91m"
        self.reset = "\033[0m"

    def red_message(self, message):
        return f"{self.red}{message}{self.reset}"

    def error(self, msg, *args, **kwargs):
        msg = self.red_message(msg)
        super().error(msg, *args, **kwargs)


def get_custom_logger(name):
    logger = ColoredLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
