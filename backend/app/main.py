import asyncio

from rich.panel import Panel
from agent.chat import run
from rich.text import Text
from config import CONSOLE

if __name__ == "__main__":
    console = CONSOLE

    # Display Claude Code CLI inspired agent header and logo
    logo_panel = Panel(
        Text("🤖 Leads Generation Agent", style="bold cyan"),
        subtitle="[dim]AI-Powered Map Scraping & Prospecting Tool[/dim]",
        style="blue",
        expand=False,
    )
    console.print()
    console.print(logo_panel)
    console.print()

    # starting the agent
    asyncio.run(run())