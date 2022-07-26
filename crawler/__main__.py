import typer

from crawler.crawler import BareMetalCrawler

VULTR_URL = "https://www.vultr.com/products/bare-metal/#pricing"


def main(stdout: bool = typer.Option(False, "--print", help="Show results in stdout")):
    crawler = BareMetalCrawler(VULTR_URL)

    if stdout is True:
        crawler.show_results()


if __name__ == "__main__":
    typer.run(main)
