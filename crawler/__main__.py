import typer

from crawler.crawlers import BareMetalCrawler, CrawlerRunner, HostgatorCrawler
from crawler.outputters import CSVOutputter, JSONOutputter, StdoutOutputter

VULTR_URL = "https://www.vultr.com/products/bare-metal/#pricing"
HOSTGATOR_URL = "https://www.hostgator.com/vps-hosting"


def main(
    stdout: bool = typer.Option(False, "--print", help="Show results in stdout"),
    save_json: typer.FileTextWrite = typer.Option(
        None, help="Write results in a JSON file"
    ),
    save_csv: typer.FileTextWrite = typer.Option(
        None, help="Write results in a csv file"
    ),
) -> None:
    outputters = []

    if stdout is True:
        title = f"Pages: {VULTR_URL}, {HOSTGATOR_URL}"
        outputters.append(StdoutOutputter(title))

    if save_json is not None:
        outputters.append(JSONOutputter(save_json))

    if save_csv is not None:
        outputters.append(CSVOutputter(save_csv))

    crawlers = [BareMetalCrawler(VULTR_URL), HostgatorCrawler(HOSTGATOR_URL)]
    crawler = CrawlerRunner(crawlers, outputters)
    crawler.run()


if __name__ == "__main__":
    typer.run(main)
