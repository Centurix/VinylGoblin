#!/usr/bin/env python3
import os
import click
from typing import cast
from click._termui_impl import ProgressBar
import click.shell_completion
from discogs_client import Client, WantlistItem  # type: ignore
from discogs_client.exceptions import HTTPError
from vinyl_goblin.shops import shops
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIRECTORY = "results"


@click.command
@click.argument("DISCOGS_TOKEN", envvar="DISCOGS_TOKEN", type=str)
def main(discogs_token: str) -> None:
    with open(Path(SCRIPT_DIRECTORY, "banner.txt"), "r", encoding="utf-8") as banner:
        click.secho(banner.read(), fg="red", bold=True)

    click.secho(f"Fetching discogs wantlist using {discogs_token}...", fg="green", bold=True)
    client = Client(
        user_agent="VinylGoblin",
        user_token=discogs_token
    )
    try:
        wantlist = client.identity().wantlist

        click.secho(f"Found {len(wantlist)} releases in the wantlist", fg="bright_green")

        click.secho(f"Placing results in `{OUTPUT_DIRECTORY}`", fg="magenta", italic=True)
        os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

        for Shop in shops:
            with Shop() as shop:
                click.secho(f"Finding releases from {shop.shop_title}...", fg="cyan")
                with open(f"results/{shop.shop_name}_results.csv", "w") as results_handle:
                    with cast(ProgressBar[WantlistItem], click.progressbar(wantlist)) as bar:
                        for item in bar:
                            artist = item.release.artists[0].name
                            album = item.release.title
                            releases = shop.fetch_items_by_artist_and_album(artist, album)
                            for release in releases:
                                results_handle.write(f"{shop.shop_name}_records|{release.release}|{release.regular_price}|{release.sale_price}\n")

        click.secho("De-duplicating...")
        for entry in os.scandir(OUTPUT_DIRECTORY):
            if entry.name.endswith(".csv"):
                with open(entry.path, "r") as file_handle:
                    rows = file_handle.readlines()
                destination_rows = []
                for row in rows:
                    if row not in destination_rows:
                        destination_rows.append(row)
                destination_rows = sorted(destination_rows)
                with open(entry.path, "w") as out_handle:
                    out_handle.writelines(destination_rows)

        click.secho("Complete", fg="green")
    except HTTPError as httpe:
        click.secho(f"Error communicating with Discogs: {httpe}")


if __name__ == "__main__":
    main()
