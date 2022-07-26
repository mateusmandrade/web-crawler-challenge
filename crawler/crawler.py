import requests
from lxml import html
from rich.console import Console
from rich.table import Table


class BareMetalCrawler:
    field_names = (
        "MACHINE NAME",
        "PRICE [$/mo]",
        "STORAGE / SSD DISK",
        "CPU/CVPU",
        "MEMORY",
        "BANDWIDTH / TRANSFER",
    )

    def __init__(self, url: str) -> None:
        self.url = url

    def _get_xpath_list(self, query: str) -> list:
        response = requests.get(self.url)
        tree = html.fromstring(response.content)

        return tree.xpath(query)

    def _get_specifications(self) -> list[list[str]]:
        xpath_query = '//h3[@class="package__title h6"] | //span[@class="price__value"]//b | //li[@class="package__list-item"]'
        xpath_list = self._get_xpath_list(xpath_query)
        infos = list(
            filter(
                lambda x: not x.endswith("Network"),
                (
                    node.text_content().replace("\t", "").replace("\n", " ").strip()
                    for node in xpath_list
                ),
            )
        )
        specifications = []
        step_len = 0

        while step_len < len(infos):
            specification = [
                infos[step_len],
                infos[step_len + 1],
            ]

            if "NVMe" in infos[step_len + 3]:
                specification.append(
                    "\n".join((infos[step_len + 2], infos[step_len + 3]))
                )
                step_len += 1
            else:
                specification.append(infos[step_len + 2])

            if "Intel" in infos[step_len + 3]:
                specification.append(
                    "\n".join((infos[step_len + 3], infos[step_len + 4]))
                )
                step_len += 1
            else:
                specification.append(infos[step_len + 3])

            specification.append(infos[step_len + 4])
            specification.append(infos[step_len + 5])

            specifications.append(specification)
            step_len += len(self.field_names)

        return specifications

    def show_results(self) -> None:
        machines_specifications = self._get_specifications()
        table = Table(title=f"Page: {self.url}", show_lines=True)

        for field_name in self.field_names:
            table.add_column(field_name)

        for specifications in machines_specifications:
            table.add_row(*specifications)

        console = Console()
        console.print(table)
