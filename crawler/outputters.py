import json

from rich.console import Console
from rich.table import Table
from typer import FileTextWrite


class StdoutOutputter:
    def __init__(self, table_title: str):
        self.table_title = table_title

    def generate_output(self, field_names: list[list[str]], results: list[str]) -> None:
        table = Table(title=self.table_title, show_lines=True)

        for field_name in field_names:
            table.add_column(field_name)

        for result in results:
            table.add_row(*result)

        console = Console()
        console.print(table)


class JSONOutputter:
    def __init__(self, file: FileTextWrite):
        self.file = file

    def generate_output(self, field_names: list[list[str]], results: list[str]) -> None:
        results_dicts = [dict(zip(field_names, result)) for result in results]
        self.file.write(f"{json.dumps(results_dicts)}\n")
