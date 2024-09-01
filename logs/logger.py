import datetime
import logging
from pathlib import Path


class Logger:
    format = (
        "[%(levelname)s] %(asctime)s | "
        "PID:%(process)d - %(threadName)s | "
        "%(filename)s - %(funcName)s | "
        "EVENT:%(message)s"
    )

    @staticmethod
    def make_log_dir(dir_path: str):
        log_dir = Path(dir_path)

        log_dir.mkdir(parents=True, exist_ok=True)

        return log_dir

    @staticmethod
    def setup_file_handler(dir_path: str, level=logging.DEBUG):
        log_dir = Logger.make_log_dir(dir_path)

        t_stamp = datetime.datetime.now().strftime("%m%d%y_%H%M")

        filename = log_dir / f"{t_stamp}.log"

        f_handler = logging.FileHandler(filename)
        f_handler.setLevel(level=level)

        return f_handler

    @staticmethod
    def setup_formatter():
        return logging.Formatter(Logger.format, "%H:%M:%S")

    @staticmethod
    def setup_log(log_level=logging.INFO, local_dir: str = None):
        handlers = []

        if local_dir:
            handlers.append(Logger.setup_file_handler(local_dir))

        log_format = Logger.setup_formatter()

        for handler in handlers:
            handler.setFormatter(log_format)

        logging.basicConfig(handlers=handlers, level=log_level)
