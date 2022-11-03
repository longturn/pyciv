# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.5"

import configparser
import logging
import os
import re
import sys
from warnings import warn
from pathlib import Path

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

def clean_string(name):
    name = name.replace("\n", "")
    name = name.replace(".", ". ")
    name = name.replace("*", "\n\n*")

    return(name)

def list_to_uobullet(named_list):
    """
    Custom jinja2 filter function to break a list of values and turn it into an rst unordered
    bulleted list.
    """
    return_string = ""
    for item in named_list:
        return_string += "* " + str(item) + "\n  "

    return(return_string)


def list_to_obullet(named_list):
    """
    Custom jinja2 filter function to break a list of values and turn it into an rst ordered
    bulleted list.
    """
    return_string = ""
    for item in named_list:
        return_string += "#. " + str(item) + "\n  "

    return(return_string)

def vector_to_table(vector):
    """
    Custom jinja2 filter funtion to break out a multi-layered list and turn it into an rst table.
    """
    #return_table = ""
    #for req in vector:
    #    return_table +=

    return(return_table)

env = Environment(
    loader=FileSystemLoader('./templates/'),
)
env.filters["make_slug"] = make_slug
env.filters["clean_string"] = clean_string
env.filters["list_to_uobullet"] = list_to_uobullet
env.filters["list_to_obullet"] = list_to_obullet
#env.filters["vector_to_table"] = vector_to_table

def file_list(path):
    """
    Returns a sorted list of files given a path
    """

    file_list = []
    bad_file = 0
    entries = Path(path)
    for entry in entries.iterdir():
        file_list.append(entry.name)

    file_list.sort()
    if ['index.rst'] in file_list:
        bad_file = file_list.index("index.rst")
    if bad_file > 0:
        del file_list[bad_file]

    return(file_list)

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

    # Get all the buildings
    all_buildings = rules.buildings.buildings

    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/buildings/" % ruleset, exist_ok=True
    )
    template = env.get_template("building.rst")

    for building in all_buildings.values():
        with open(
            file_locations.get("conf.fc21_rst_output") + "/%s/buildings/%s.rst" % (ruleset, make_slug(building.name)), "w"
        ) as out:
            out.write(
                template.render(
                    building=building,
                )
            )

    building_list = file_list(file_locations.get("conf.fc21_rst_output") + "/%s/buildings/" % ruleset)
    template = env.get_template("building-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/buildings/index.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                building_list=building_list,
        )
    )

    # Get unit details
    all_unit_classes = rules.units.unit_classes
    all_unit_types = rules.units.unit_types
    all_buildings = rules.buildings.buildings

    # Get all the technology advances
    all_advances = rules.techs.advances
    for advance in all_advances.values():
        required_by = list(
            filter(lambda adv: advance in adv.reqs, all_advances.values())
        )
        hard_required_by = list(
            filter(lambda adv: advance == adv.root_req, all_advances.values())
        )
        required_by_units = list(
            filter(lambda ut: advance in ut.tech_req, all_unit_types.values())
        )

    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances/" % ruleset, exist_ok=True
    )
    template = env.get_template("advance.rst")

    for advance in all_advances.values():
        with open(
            file_locations.get("conf.fc21_rst_output") + "/%s/advances/%s.rst" % (ruleset, make_slug(advance.name)), "w"
        ) as out:
            out.write(
                template.render(
                    advance=advance,
                    required_by=required_by,
                    hard_required_by=hard_required_by,
                    required_by_units=required_by_units,
                )
            )

    advances_list = file_list(file_locations.get("conf.fc21_rst_output") + "/%s/advances/" % ruleset)
    template = env.get_template("advance-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances/index.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                advances_list=advances_list,
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

    # Write top level index.rst
    rulesets = []
    rulesets.append('civ1')
    rulesets.append('civ2')
    rulesets.append('civ2civ3')
    rulesets.append('classic')
    rulesets.append('experimental')
    #rulesets.append('granularity')
    rulesets.append('multiplayer')
    rulesets.append('royale')
    rulesets.append('sandbox')
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/", exist_ok=True
    )
    template = env.get_template("index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/index.rst", "w"
    ) as out:
        out.write(
            template.render(
                rulesets=rulesets
        )
    )

    # process all the shipped rulesets
    for ruleset in (
        "civ1",
        "civ2",
        "civ2civ3",
        "classic",
        "experimental",
        #"granularity",
        "multiplayer",
        "royale",
        "sandbox",
    ):
        process_ruleset([file_locations.get("conf.fc21_datadir_path")], ruleset)

    #process_ruleset([file_locations.get("conf.fc21_aviation_path")], "aviation")

########################################
main_func()
