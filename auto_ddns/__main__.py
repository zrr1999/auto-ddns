from __future__ import annotations

import json
import time
from pathlib import Path

import typer
from loguru import logger
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler
from rich.style import Style

from auto_ddns.utils import create_setter_by_str

app = typer.Typer()


def init_logger(log_level: str):
    handler = RichHandler(console=Console(style=Style()), highlighter=NullHighlighter(), markup=True)
    logger.remove()
    logger.add(handler, format="{message}", level=log_level)


@app.command()
def update(path: Path = Path("~/.config/autoconfig/auto-ddns.json"), setter: str = "dnspod", log_level: str = "INFO"):
    init_logger(log_level)
    logger.info(f"Loading config from [bold purple]{path}[/]")
    with open(path.expanduser()) as f:
        config = json.load(f)
    setter_obj = create_setter_by_str(config, setter)
    setter_obj.update_dns()


@app.command()
def daemon(path: Path = Path("~/.config/autoconfig/auto-ddns.json"), setter: str = "dnspod", log_level: str = "INFO"):
    init_logger(log_level)
    logger.info(f"Loading config from [bold purple]{path}[/]")
    with open(path.expanduser()) as f:
        config = json.load(f)
    setter_obj = create_setter_by_str(config, setter)
    while True:
        setter_obj.update_dns()
        interval = 300
        logger.info(f"Sleeping for {interval} seconds")
        time.sleep(interval)


if __name__ == "__main__":
    app()
