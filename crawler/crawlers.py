import requests
from lxml import html

from crawler.outputters import Outputter


class BaseCrawler:
    """
    Crawler base class
    """

    def __init__(self, url: str) -> None:
        self.url = url

    def get_results(self) -> list[list[str]]:
        """
        Method template to get crawler results
        """
        raise NotImplementedError

    def get_xpath_list(self, query: str, remove_patterns: list | None) -> list[str]:
        """
        Get xpath tree of a given page

        :param query: XPath query
        """
        response = requests.get(self.url)
        tree = html.fromstring(response.content)

        xpath_list = [item.text_content() for item in tree.xpath(query)]

        if remove_patterns is not None:
            for index in range(len(xpath_list)):
                for pattern in remove_patterns:
                    xpath_list[index] = xpath_list[index].replace(pattern, "")

        return xpath_list


class BareMetalCrawler(BaseCrawler):
    """
    Class to crawl bare metal machines page

    :param url: page URL
    :outputters: output instance to show results
    """

    field_names = (
        "MACHINE NAME",
        "PRICE [$/mo]",
        "STORAGE / SSD DISK",
        "CPU/CVPU",
        "MEMORY",
        "BANDWIDTH / TRANSFER",
    )

    def get_results(self) -> list[dict[str, str]]:
        """
        Returns machine specifications from bare metal page
        """
        xpath_query = '//h3[@class="package__title h6"] | //span[@class="price__value"]//b | //li[@class="package__list-item"]'
        xpath_list = self.get_xpath_list(xpath_query, remove_patterns=["\t"])
        infos = list(
            filter(
                lambda x: not x.endswith("Network"),
                (node.replace("\n", " ").strip() for node in xpath_list),
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
                    " / ".join((infos[step_len + 2], infos[step_len + 3]))
                )
                step_len += 1
            else:
                specification.append(infos[step_len + 2])

            if "Intel" in infos[step_len + 3]:
                specification.append(
                    " / ".join((infos[step_len + 3], infos[step_len + 4]))
                )
                step_len += 1
            else:
                specification.append(infos[step_len + 3])

            specification.append(infos[step_len + 4])
            specification.append(infos[step_len + 5])

            specifications.append(dict(zip(self.field_names, specification)))
            step_len += len(self.field_names)

        return specifications


class HostgatorCrawler(BaseCrawler):
    field_names = (
        "MACHINE NAME",
        "MEMORY",
        "CPU/CVPU",
        "STORAGE / SSD DISK",
        "BANDWIDTH / TRANSFER",
        "PRICE [$/mo]",
    )

    def get_results(self) -> list[dict[str, str]]:
        """
        Returns machine specifications from Hostgator VPS page
        """
        xpath_query = '//h3[@class="pricing-card-title"] | //li[@class="pricing-card-list-items"] | //p[@class="pricing-card-price"]'
        infos = self.get_xpath_list(xpath_query, remove_patterns=["\xa0", "/mo*"])
        step = slice(0, len(infos), len(self.field_names))
        results = []

        for start, end in zip(
            range(0, step.stop, step.step), range(step.step, step.stop + 1, step.step)
        ):
            results.append(dict(zip(self.field_names, infos[start:end])))

        return results


class CrawlerRunner:
    """
    Class to run crawlers and generate outputs

    :param crawlers: List of crawler instances
    :param outputters: List of outputter instances
    """

    def __init__(self, crawlers: list[BaseCrawler], outputters: list[Outputter]):
        self.crawlers = crawlers
        self.outputters = outputters

    def run(self) -> None:
        """
        Get crawler results and generate outputs
        """
        results = []

        for crawler in self.crawlers:
            results.extend(crawler.get_results())

        field_names = list(next(result.keys() for result in results))

        for output in self.outputters:
            output.generate_output(results, field_names=field_names)
