import typer

from crawler.crawler import BareMetalCrawler
from crawler.outputters import JSONOutputter, StdoutOutputter

VULTR_URL = "https://www.vultr.com/products/bare-metal/#pricing"


def main(
    stdout: bool = typer.Option(False, "--print", help="Show results in stdout"),
    save_json: typer.FileTextWrite = typer.Option(
        None, help="Write results in a JSON file"
    ),
):
    outputs = []

    if stdout is True:
        outputs.append(StdoutOutputter(VULTR_URL))

    if save_json is not None:
        outputs.append(JSONOutputter(save_json))

    crawler = BareMetalCrawler(VULTR_URL, outputs)
    crawler.show_results()


if __name__ == "__main__":
    typer.run(main)
