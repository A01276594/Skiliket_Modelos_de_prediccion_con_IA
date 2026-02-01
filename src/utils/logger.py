import logging
from rich.logging import RichHandler
from typing import Any
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("app_logger")
log.setLevel(logging.INFO)
log.propagate = False 
log.handlers.clear()
rich_handler = RichHandler(
    markup=True,          
    rich_tracebacks=True, 
    show_time=True,
    show_level=False,     
    show_path=False
)
formatter = logging.Formatter("%(message)s", datefmt="[%X]")
rich_handler.setFormatter(formatter)
log.addHandler(rich_handler)

class Logger:
    @staticmethod
    def info(message: Any) -> None:
        log.info(f"{message}") 

    @staticmethod
    def warning(message: Any) -> None:
        log.warning(f"[bold yellow]{message}[/]")

    @staticmethod
    def error(message: Any) -> None:
        log.error(f"[bold red]{message}[/]")

    @staticmethod
    def critical(message: Any) -> None:
        log.critical(f"[bold red on white]{message}[/]")