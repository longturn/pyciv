# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.4"

import configparser
import logging
import os
import re
import sys
from warnings import warn

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode

sys.path.append("../")
from freeciv.rules import Ruleset

logging.basicConfig(level=logging.INFO)


def make_slug(name):
    name = unidecode(name).lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub("[^a-z0-9_]", "", name)
    return name

def show_item(item):
    print(item)

def list_to_bullet(named_list):
    """
    Custom jinja2 filter function to break a list of values and turn it into an rst bulleted list.
    """
    return_string = ""
    for item in named_list:
        return_string += "* " + str(item) + "\n  "

    return(return_string)

def vector_to_table(vector):
    """
    Custom jinja2 filter funtion to break out a multi-layered list and turn it into an rst table.
    """

    return(table)

env = Environment(
    loader=FileSystemLoader('./templates/'),
)
env.filters["make_slug"] = make_slug
env.filters["show_item"] = show_item
env.filters["list_to_bullet"] = list_to_bullet


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

    # Write out the top level ruleset index for all the given rulesets
    #  Due to the sheer size of the content, the base game data is written
    #  out to multiple files to make reading much easier.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/" % ruleset, exist_ok=True
    )
    template = env.get_template("index-game.rst")
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
            )
        )
    #TODO: See if we can do a check if there is a long description and don't write a file out if there isn't one
    template = env.get_template("description.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/description.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                about=about,
            )
        )
    template = env.get_template("game-parms.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/game-parms.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                civ_style=civ_style,
            )
        )
    template = env.get_template("plague.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/plague.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                illness=illness,
            )
        )
    template = env.get_template("incite-cost.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/incite-cost.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                incite_cost=incite_cost,
            )
        )
    template = env.get_template("unit-rules.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/unit-rules.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                combat_rules=combat_rules,
                auto_attack=auto_attack,
                actions=actions,
            )
        )
    template = env.get_template("borders.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/borders.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                borders=borders,
            )
        )
    template = env.get_template("research.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/research.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                research=research,
            )
        )
    template = env.get_template("culture.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/culture.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                culture=culture,
            )
        )
    template = env.get_template("calendar.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/calendar.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                calendar=calendar,
            )
        )
    template = env.get_template("city.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/city.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                parameters=city_parameters,
                citizens=citizens,
                missing_unit_upkeep = rules.cities.missing_unit_upkeep,
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


def main_func():
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

    #process_ruleset([file_locations.get("conf.fc21_aviation_path")], "aviation")

########################################
main_func()
