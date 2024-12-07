#!/usr/bin/env python3
import click
from typing import cast
from click._termui_impl import ProgressBar
from discogs_client import Client, WantlistItem  # type: ignore
from vinyl_goblin.shops import shops
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


@click.command
@click.argument("DISCOGS_TOKEN", envvar="DISCOGS_TOKEN", type=str)
def main(discogs_token: str) -> None:
    with open(Path("src", "vinyl_goblin", "banner.txt"), "r") as banner:
        click.secho(banner.read(), fg="red", bold=True)

    click.secho("Fetching discogs wantlist...", fg="green", bold=True)
    client = Client(
        user_agent="VinylGoblin",
        user_token=discogs_token
    )
    wantlist = client.identity().wantlist
    click.secho(f"Found {len(wantlist)} releases in the wantlist", fg="bright_green")

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

    click.secho("Complete", fg="green")

if __name__ == "__main__":
    main()