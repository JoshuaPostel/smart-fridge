from pathlib import Path
import logging

log_path = Path(__file__).resolve().parent.parent / "output"
log_path.mkdir(parents=True, exist_ok=True)

logging.captureWarnings(True)


class FilterOnSubstring(logging.Filter):
    def __init__(self, substring):
        self.substring = substring

    def filter(self, record):
        return self.substring not in record.getMessage()


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "short": {"format": "%(asctime)s %(levelname)s: %(message)s"},
        "verbose": {
            "format": "%(levelname)s %(asctime)s @%(process)s %(funcName)s:%(lineno)d - %(message)s"
        },
    },
    "filters": {
        "LinAlgWarnings": {"()": FilterOnSubstring, "substring": "LinAlgWarning"},
        "OptimizeWarnings": {"()": FilterOnSubstring, "substring": "OptimizeWarning"},
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "short",
            "filters": ["LinAlgWarnings", "OptimizeWarnings"],
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": log_path / "fridge.log",
            "mode": "w",
        },
    },
    "loggers": {"": {"handlers": ["stderr", "file"], "level": "INFO"}},
}
