import logging


class PipeFormatter(logging.Formatter):
    def format(self, record):
        dt = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = record.levelname.ljust(8)
        return f"{dt} | {level} | {record.name} - {record.getMessage()}"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setFormatter(PipeFormatter())
        logger.addHandler(handler)

    return logger
