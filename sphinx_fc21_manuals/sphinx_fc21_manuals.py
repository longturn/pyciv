# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>
# SPDX-FileCopyrightText: 2022 Louis Moureaux <m_louis30@yahoo.com>

# Version string
__version__ = "0.8"

import configparser
import logging
import os
import re
import sys
from pathlib import Path
from warnings import warn

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode

# FIXME: There is probably a better way to do this
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
    name = name.replace(":", ": ")

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


def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


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

    # Get all the effects
    all_effects = rules.effects
    all_effects.sort(key=lambda e: e.type or "")

    # all_tech_effects = []
    # all_building_effects = []
    # for effect in all_effects:
    #    for i in range(len(effect.reqs)):
    #        if i == 0: pass
    #        match effect.reqs[i].type:
    #            case "Tech":
    #                all_tech_effects.append(effect)
    #            case "Building":
    #                all_building_effects.append(effect)

    # print(all_building_effects)

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
    building_list = []
    template = env.get_template("building.rst")
    for building in all_buildings.values():
        building_list.append(building.name)
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
    template = env.get_template("building-index.rst")
    building_list.sort()
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/buildings.rst" % ruleset,
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

    # Create a directory to house all the unit-type and unit-class pages.
    os.makedirs(
        file_locations.get("conf.fc21_rst_output") + "/%s/units/" % ruleset,
        exist_ok=True,
    )

    # Write out all of the unit class details.
    unit_class_list = []
    template = env.get_template("unit-class.rst")
    for unit_class in all_unit_classes.values():
        unit_class_list.append(unit_class.name)
        units_in_class = filter(
            lambda ut: ut.uclass == unit_class, all_unit_types.values()
        )
        with open(
            file_locations.get("conf.fc21_rst_output")
            + "/%s/units/%s.rst" % (ruleset, make_slug(unit_class.name)),
            "w",
        ) as out:
            out.write(
                template.render(unit_class=unit_class, units_in_class=units_in_class)
            )

    # Build a list of all the unit class files created above and then populate an index page.
    unit_class_list.sort()
    template = env.get_template("unit-class-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/unit-classes.rst" % ruleset,
        "w",
    ) as out:
        out.write(
            template.render(
                unit_class_list=unit_class_list,
            )
        )

    # Write out all of the unit type details.
    unit_type_list = []
    template = env.get_template("unit-type.rst")
    for unit_type in all_unit_types.values():
        unit_type_list.append(unit_type.name)
        obsolete = list(
            filter(lambda ut: (ut.obsolete_by == unit_type), all_unit_types.values())
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
    unit_type_list.sort()
    template = env.get_template("unit-type-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/unit-types.rst" % ruleset,
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

    advances_list = []
    for advance in all_advances.values():
        advances_list.append(advance.name)
        required_by = list(
            filter(lambda adv: (advance in adv.reqs), all_advances.values())
        )
        hard_required_by = list(
            filter(lambda adv: (advance == adv.root_req), all_advances.values())
        )
        required_by_units = list(
            filter(lambda ut: (advance in ut.tech_req), all_unit_types.values())
        )
        all_advances_buildings = [
            building
            for building in all_buildings.values()
            if advance.name in building.required_techs()
        ]

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
                    all_advances_buildings=all_advances_buildings,
                )
            )

    # Build a list of all the tech advance files created above and then populate an index page.
    advances_list.sort()
    template = env.get_template("advance-index.rst")
    with open(
        file_locations.get("conf.fc21_rst_output") + "/%s/advances.rst" % ruleset,
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
    # rulesets.append('aviation')
    os.makedirs(file_locations.get("conf.fc21_rst_output") + "/", exist_ok=True)
    template = env.get_template("index.rst")
    with open(file_locations.get("conf.fc21_rst_output") + "/index.rst", "w") as out:
        out.write(template.render(rulesets=rulesets))

    # process all the shipped rulesets
    for ruleset in (
        # "alien",
        "civ1",
        # "civ2",
        # "civ2civ3",
        # "classic",
        # "experimental",
        # "granularity",
        # "multiplayer",
        # "royale",
        # "sandbox",
    ):
        process_ruleset([file_locations.get("conf.fc21_datadir_path")], ruleset)

    # process_ruleset([file_locations.get("conf.fc21_aviation_path")], "aviation")


########################################
main_func()
