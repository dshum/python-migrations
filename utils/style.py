from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "success": "green",
    "info": "blue",
    "warn": "yellow",
    "error": "white on red"
})

console = Console(theme=theme)
