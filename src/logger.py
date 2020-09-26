from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_path = Path("/tmp/logs")
log_path.mkdir(parents=True, exist_ok=True)


file_handler = logging.FileHandler(log_path / "watt-time.log")
file_format = logging.Formatter(
    "%(levelname)s %(asctime)s @%(process)s %(funcName)s:%(lineno)d - %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

stdout_handler = logging.StreamHandler()
stdout_format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")
stdout_handler.setFormatter(stdout_format)
logger.addHandler(stdout_handler)
