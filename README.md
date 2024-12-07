# Vinyl Goblin
Reads your Discogs wantlist and then finds each release in almost every Brisbane record
store. It then saves the results in text files that can be searched using a text editor like
VS Code or whatever.

## Shops supported:

* Blackened Records (Metal)
* Catalog Music
* Dutch Vinyl (Both Brisbane and Melbourne stores)
* Glitter Records
* Jet Black Cat Records
* Monster Robot (EDM, lots of 12" EPs)
* Record Exchange (Online only)
* Relove Oxley
* Rockaway Records
* Rocking Horse Records
* Sonic Sherpa
* Spin and Groove Records
* Stash Records
* Waxx Lyrical

Retro World Collective is not here because they don't have an online store

Butter Beats only lists less than 30 records on their online store at any time

JB Hi Fi is not here because it's honestly too hard for very little reward on over priced records

echo & bounce are not here because there is no non-graphql direct search for releases

# Installation
This uses [PDM](https://pdm-project.org/en/latest/) for its dependency management and virtual environments. If you don't want to install that, you
can install the dependencies listed in the `pyproject.toml` file to get things running.

To install using PDM though, change to the project directory and run:

`pdm install`

Everything will be installed.

It states that it runs on Python 3.13, but there's nothing really stopping it running on earlier versions.

# Running
First, you will need to create an app in your discogs account. You can find that [here](https://www.discogs.com/settings/developers)

The application name needs to be `VinylGoblin` for this to work.

Then you need to generate a new access token.

Rename or copy the `env.example` to `.env` and put the access token in the file.

Then, to run the searching session:

`python src/vinyl_goblin`

And it will start finding your wantlist.

IT TAKES A LONG TIME. LIKE HOURS.

It also gives you a progress bar for each store. Once they're all done, you'll get a bunch of text files in the results directory.
These can be searched and will give you the shop and price.

# Notes
Some shops are more straight forward to scrape than others. This uses a mix of requests/selenium and Beautiful Soup to get things found.

# Restricting the number of shops to use
In the `src/vinyl_goblin/shops/__init__.py` file there is a `shops` list. Comment out the lines you don't want and it won't search them.

# Adding shops
It's fairly straight forward. Copy an existing shop file in the `src/vinyl_goblin/shops` directory and rename it to the one you want to scrape from. You'll need to figure out how the shop searches for records with the URL, most have some path like `/search?artist+blah+blah`. You'll see where that goes in the code. Then once you have a search result page you'll need to figure out how to identify each release on the page, usually <li> elements with stuff in them. Then find the title and price. Good luck. You can ask questions and submit bugs in the repo.

If you're submitting changes, it'll need to have correct types and also linting passed over it. If you installed using PDM, you can do:

`pdm run all`

And it'll run all the checks you need. Make a fork, create a branch, push it and create a PR and hopefully it'll get accepted.

In the future I might get around to making tests. Then you'll have to do them as well.

