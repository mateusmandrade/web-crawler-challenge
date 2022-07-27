import csv
import json

from rich.console import Console
from rich.table import Table
from typer import FileTextWrite


class Outputter:
    """
    Class output interface
    """

    def generate_output(self, field_names: list[str], results: list[list[str]]) -> None:
        """
        Method template to generate output

        :param field_names: list with field names
        :param results: list of separated results
        """
        raise NotImplementedError


class StdoutOutputter(Outputter):
    """
    Class to show results in stdout output

    :param table_tile: table title
    """

    def __init__(self, table_title: str):
        self.table_title = table_title

    def generate_output(self, field_names: list[str], results: list[list[str]]) -> None:
        """
        Generate output in stdout

        :param field_names: list with field names
        :param results: list of separated results
        """
        table = Table(title=self.table_title, show_lines=True)

        for field_name in field_names:
            table.add_column(field_name)

        for result in results:
            table.add_row(*result)

        console = Console()
        console.print(table)


class FileOutputter(Outputter):
    """
    Base class to provide result output to a file

    :param file: File to write output
    """

    def __init__(self, file: FileTextWrite):
        self.file = file

    def _get_results_dicts(
        self, field_names: list[str], results: list[list[str]]
    ) -> list[dict[str, str]]:
        """
        Returns a structured dict with field and values to write in a file

        :param field_names: list with field names
        :param results: list of separated results
        """
        results_dicts = [dict(zip(field_names, result)) for result in results]
        return results_dicts


class JSONOutputter(FileOutputter):
    """
    Class to provide result output to a JSON file

    :param file: File to write output
    """

    def generate_output(self, field_names: list[list[str]], results: list[str]) -> None:
        """
        Generate output in JSON file format

        :param field_names: list with field names
        :param results: list of separated results
        """
        results_dicts = self._get_results_dicts(field_names, results)
        self.file.write(f"{json.dumps(results_dicts)}\n")


class CSVOutputter(FileOutputter):
    """
    Class to provide result output to a csv file

    :param file: File to write output
    """

    def generate_output(self, field_names: list[list[str]], results: list[str]) -> None:
        """
        Generate output in csv file format

        :param field_names: list with field names
        :param results: list of separated results
        """
        results_dicts = self._get_results_dicts(field_names, results)
        csv_writer = csv.DictWriter(self.file, fieldnames=field_names)
        csv_writer.writeheader()

        for result in results_dicts:
            csv_writer.writerow(result)
