# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.6"

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

    return name


def list_to_uobullet(named_list):
    """
    Custom jinja2 filter function to break a list of values and turn it into an rst unordered
    bulleted list.
    """
    return_string = ""
    for item in named_list:
        return_string += "* " + str(item) + "\n  "

    return return_string


def list_to_obullet(named_list):
    """
    Custom jinja2 filter function to break a list of values and turn it into an rst ordered
    bulleted list.
    """
    return_string = ""
    for item in named_list:
        return_string += "#. " + str(item) + "\n  "

    return return_string


env = Environment(
    loader=FileSystemLoader("./templates/"),
)
env.filters["make_slug"] = make_slug
env.filters["clean_string"] = clean_string
env.filters["list_to_uobullet"] = list_to_uobullet
env.filters["list_to_obullet"] = list_to_obullet


def file_list(path):
    """
    Returns a sorted list of files given a path
    """

    file_list = []
    bad_file = -1
    entries = Path(path)
    for entry in entries.iterdir():
        file_list.append(entry.name)

    file_list.sort()
    if "index.rst" in file_list:
        bad_file = file_list.index("index.rst")
    if bad_file > 0:
        del file_list[bad_file]

    return file_list


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

    # Start with the top level game page index with information from the [about], [options]
    # [tileset], [soundset], and [musicset] sections.
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

    # If the game has a detailed description defined in the [about] section we have a
    # single page for that as they are often long.
    template = env.get_template("description.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/description.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                about=about,
            )
        )

    # Write out game parameters from the [civstyle] section
    template = env.get_template("game-parms.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/game-parms.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                civ_style=civ_style,
            )
        )

    # Write out the [illness] section to a page
    template = env.get_template("plague.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/plague.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                illness=illness,
            )
        )

    # Write out the city [incite_cost] section to its own page. It has a long math formula.
    template = env.get_template("incite-cost.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/incite-cost.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                incite_cost=incite_cost,
            )
        )

    # Write out the unit [combat_rules], [auto_attack], and [actions] sections to its own page.
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

    # Write out the national [borders] section to its own bage.
    template = env.get_template("borders.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/borders.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                borders=borders,
            )
        )

    # Write out the [research] section to its own page.
    template = env.get_template("research.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/research.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                research=research,
            )
        )

    # Write out the [culture] victory section to its own page.
    template = env.get_template("culture.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/culture.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                culture=culture,
            )
        )

    # Write out the game [calendar] section to its own page.
    template = env.get_template("calendar.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/calendar.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                calendar=calendar,
            )
        )

    # Write out the [parameters], [citizens] and [missing_unit_upkeep] sections from city.ruleset
    # to its own page.
    template = env.get_template("city.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/city.rst" % ruleset, "w"
    ) as out:
        out.write(
            template.render(
                parameters=city_parameters,
                citizens=citizens,
                missing_unit_upkeep=rules.cities.missing_unit_upkeep,
            )
        )

    # Get all the buildings
    all_buildings = rules.buildings.buildings

    # Create a directory to hold the building files.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/buildings/" % ruleset,
        exist_ok=True,
    )

    # Write a file for each building in the list of all of the buildings
    # FIXME: Figure out a way to use graphic_alt if main graphic isn't available.
    template = env.get_template("building.rst")
    for building in all_buildings.values():
        with open(
            file_locations.get("conf.fc21_rst_output")
            + "/%s/buildings/%s.rst" % (ruleset, make_slug(building.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    building=building,
                )
            )

    # Build a list of all the building files created above and then populate an index page.
    building_list = file_list(
        file_locations.get("conf.fc21_rst_output") + "/%s/buildings/" % ruleset
    )
    template = env.get_template("building-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output")
        + "/%s/buildings/index.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                building_list=building_list,
            )
        )

    # Get unit details
    all_unit_classes = rules.units.unit_classes
    all_unit_types = rules.units.unit_types

    # Create a directory to house all the unit-class pages.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/unit-classes/" % ruleset,
        exist_ok=True,
    )

    # Write out all of the unit class details.
    template = env.get_template("unit-class.rst")
    for unit_class in all_unit_classes.values():
        units_in_class = list(
            filter(lambda ut: (ut.uclass == unit_class.name), all_unit_types.values())
        )
        with open(
            file_locations.get("conf.fc21_rst_output")
            + "/%s/unit-classes/%s.rst" % (ruleset, make_slug(unit_class.name)),
            "w",
        ) as out:
            out.write(
                template.render(unit_class=unit_class, units_in_class=units_in_class)
            )

    # Build a list of all the unit class files created above and then populate an index page.
    unit_class_list = file_list(
        file_locations.get("conf.fc21_rst_output") + "/%s/unit-classes/" % ruleset
    )
    template = env.get_template("unit-class-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output")
        + "/%s/unit-classes/index.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                unit_class_list=unit_class_list,
            )
        )

    # Create a directory to house all the units pages.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/units/" % ruleset,
        exist_ok=True,
    )

    # Write out all of the unit type details.
    template = env.get_template("unit-type.rst")
    for unit_type in all_unit_types.values():
        obsolete = list(
            filter(
                lambda ut: (ut.obsolete_by == unit_type.name), all_unit_types.values()
            )
        )
        with open(
            file_locations.get("conf.fc21_rst_output")
            + "/%s/units/%s.rst" % (ruleset, make_slug(unit_type.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    unit_type=unit_type,
                    obsolete=obsolete,
                )
            )

    # Build a list of all the unit files created above and then populate an index page.
    # FIXME:figure out a way to use graphic_alt when the main graphic isn't available.
    unit_type_list = file_list(
        file_locations.get("conf.fc21_rst_output") + "/%s/units/" % ruleset
    )
    template = env.get_template("unit-type-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/units/index.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                unit_type_list=unit_type_list,
            )
        )

    # Get all the technology advances
    all_advances = rules.techs.advances

    # Create a directory to house all the tech advance pages.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances/" % ruleset,
        exist_ok=True,
    )

    # Write out all of the tech advance details.
    template = env.get_template("advance.rst")
    for advance in all_advances.values():
        required_by = list(
            filter(lambda adv: advance in adv.reqs, all_advances.values())
        )
        hard_required_by = list(
            filter(lambda adv: advance == adv.root_req, all_advances.values())
        )
        required_by_units = list(
            filter(lambda ut: (advance in ut.tech_req), all_unit_types.values())
        )

        with open(
            file_locations.get("conf.fc21_rst_output")
            + "/%s/advances/%s.rst" % (ruleset, make_slug(advance.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    advance=advance,
                    required_by=required_by,
                    hard_required_by=hard_required_by,
                    required_by_units=required_by_units,
                )
            )

    # Build a list of all the tech advance files created above and then populate an index page.
    advances_list = file_list(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances/" % ruleset
    )
    template = env.get_template("advance-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances/index.rst" % ruleset,
        "w",
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
    # rulesets.append('alien')
    rulesets.append("civ1")
    # rulesets.append('civ2')
    # rulesets.append('civ2civ3')
    # rulesets.append('classic')
    # rulesets.append('experimental')
    # rulesets.append('granularity')
    # rulesets.append('multiplayer')
    # rulesets.append('royale')
    # rulesets.append('sandbox')
    os.makedirs(file_locations.get("conf.fc21_rst_output") + "/", exist_ok=True)
    template = env.get_template("index.rst")
    with open(file_locations.get("conf.fc21_rst_output") + "/index.rst", "w") as out:
        out.write(template.render(rulesets=rulesets))

    # process all the shipped rulesets
    for ruleset in (
        # "alien",
        # "civ1",
        # "civ2",
        # "civ2civ3",
        # "classic",
        "experimental",
        # "granularity",
        # "multiplayer",
        # "royale",
        # "sandbox",
    ):
        process_ruleset([file_locations.get("conf.fc21_datadir_path")], ruleset)

    # process_ruleset([file_locations.get("conf.fc21_aviation_path")], "aviation")


########################################
main_func()
