import argparse
import logging


def setup_logging():
    parser = argparse.ArgumentParser(description="Galaga Clone")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging level (default: INFO)",
    )
    args, _ = parser.parse_known_args()

    level = getattr(logging, args.log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    file_handler = logging.FileHandler("game.log", mode="w")
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[file_handler])


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
