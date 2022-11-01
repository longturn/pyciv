# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.3"

import configparser
import logging
import os
import re
import sys
from warnings import warn

from jinja2 import Environment, PackageLoader, select_autoescape

#from markdown import markdown

sys.path.append("../")
from freeciv.rules import Ruleset

logging.basicConfig(level=logging.INFO)


def make_slug(name):
    name = unidecode(name).lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub("[^a-z0-9_]", "", name)
    return name


env = Environment(
    loader=PackageLoader("sphinx_fc21_manuals", "templates"),
)
env.filters["make_slug"] = make_slug


def process_ruleset(path, ruleset):
    rules = Ruleset(ruleset, path)

    # Get all the base game data
    data_file_header = rules.game.data_file_header
    about = rules.game.about
    options = rules.game.options
    tileset = rules.game.tileset
    soundset = rules.game.soundset
    musicset = rules.game.musicset
    civ_style = rules.game.civ_style
    illness = rules.game.illness
    incite_cost = rules.game.incite_cost
    combat_rules = rules.game.combat_rules
    auto_attack = rules.game.auto_attack
    actions = rules.game.actions
    borders = rules.game.borders
    research = rules.game.research
    culture = rules.game.culture
    calendar = rules.game.calendar
    settings = rules.game.settings

    # Get the city settings
    city_parameters = rules.cities.parameters
    citizens = rules.cities.citizens
    missing_unit_upkeep = rules.cities.missing_unit_upkeep

    logging.info(f"Writing manual for {ruleset}...")

    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/" % ruleset, exist_ok=True
    )
    template = env.get_template("index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/index.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                about=about,
                options=options,
                tileset=tileset,
                soundset=soundset,
                musicset=musicset,
                civ_style=civ_style,
                illness=illness,
                incite_cost=incite_cost,
                combat_rules=combat_rules,
                auto_attack=auto_attack,
                actions=actions,
                borders=borders,
                research=research,
                culture=culture,
                calendar=calendar,
                settings=settings,
            )
        )


def get_config(conf, section):
    """
    Get all the variables from a given conf file. Return a dictionary of items.
    """

    config = configparser.ConfigParser()
    config.read(conf)
    options_dict = dict(config[section])

    return options_dict


# global variable
file_locations = get_config("conf.ini", "MAIN")


def main():
    """
    Main function for sphinx_fc21_manuals
    """

    print(f"Welcome to {sys.argv[0]} v{__version__}\n")

    for ruleset in (
        "civ1",
        "civ2",
        "civ2civ3",
        "classic",
        "experimental",
        "granularity",
        "multiplayer",
        "royale",
        "sandbox",
    ):
        process_ruleset([file_locations.get("conf.fc21_datadir_path")], ruleset)


main()
