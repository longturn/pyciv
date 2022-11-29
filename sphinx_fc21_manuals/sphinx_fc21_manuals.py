# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>
# SPDX-FileCopyrightText: 2022 Louis Moureaux <m_louis30@yahoo.com>

# Version string, the build counter goes up by one at each commit.
__version__ = "0.0.18"

import argparse
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

# Setup command line argument parsing, variables are global.
parser = argparse.ArgumentParser(
    description="Process a Freeciv21 Ruleset and write out Sphinx reStructured Text help files."
)
parser.add_argument(
    "-r", "--ruleset_dir", help="Path to a ruleset serv file directory."
)
parser.add_argument("-t", "--target_dir", help="Path for output directory.")
parser.add_argument(
    "-n", "--name", help="Name of the ruleset to parse.", default="None"
)

args = parser.parse_args()


def make_slug(name):
    name = unidecode(name).lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub("[^a-z0-9_]", "", name)

    return name


def clean_string(name):
    """
    Custom jinja2 filter used to cleanup malformatted strings in the templates. We often
    get malformed strings from the helptext sections of the rulesets as they are not
    written with rst in mind.
    """
    name = name.replace("\n", "")
    name = name.replace(".", ". ")
    name = name.replace("*", "\n\n*")
    name = name.replace(":", ": ")
    name = name.replace("%s", "")

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


def action_enabler_check(unitFlags, unitRoles, unitClass, aeItem):
    """
    Custom jinja function to determine if a specific action enabler is for a given unit
    """

    # Test 1: Check to see if the UnitFlag value in the requirement vector name field is in the set
    #   from unitFlags. The value of the present field in the requirement vector must also be True.
    # Test 2: Check to see if the UnitType value in the requirement vector name field is in the set
    #   from unitRoles. The value of the present field in the requirement vector must also be True.
    # Test 3: Check to see if the UnitClassFlag value in the requirement vector name field is in the
    #   set from unitClassFlags. The value of the present field in the requirement vector must also
    #   be True.
    # Test 4: Check to see if UnitFlag, UnitType and UnitClassFlag is NOT in the requirement vector.
    #   If so. then return True as the action enabler is for every unit. We use the counter variable
    #   to help here.

    counter = 0
    for req in aeItem.actor_reqs:
        if req.type == "UnitFlag":
            counter += 1
            if req.present and req.name in unitFlags:
                return True
            elif not req.present and req.name in unitFlags:
                return False
        if req.type == "UnitType":
            counter += 1
            if req.present and req.name in unitRoles:
                return True
            elif not req.present and req.name in unitRoles:
                return False
        if req.type == "UnitClassFlag":
            counter += 1
            if req.present and req.name in unitClass.flags:
                return True
            elif not req.present and req.name in unitClass.flags:
                return False

    # The culmination of Test 4. If none of the others are found in the full set of reqs, then the action
    #   is for all units.
    if counter == 0:
        return True

    return False


def image_file_exists():
    """
    Custom jinja function to determine if a file exists on the filesystem, such as an image file.
    Used to cleanup rst image tags that point to locations that do not have an appropriate image
    file.
    """

    return False


# Jinja2 Environment
env = Environment(
    loader=FileSystemLoader("./templates/"),
)
env.filters["make_slug"] = make_slug
env.filters["clean_string"] = clean_string
env.filters["list_to_uobullet"] = list_to_uobullet
env.filters["list_to_obullet"] = list_to_obullet
env.globals["action_enabler_check"] = action_enabler_check
env.globals["image_file_exists"] = image_file_exists


def process_ruleset(path, ruleset):
    """
    This is a long function that effectively instantiates all of the objects of a Freeciv
    ruleset including:

      * Game parameters [game.ruleset]
      * City parameters [cities.ruleset]
      * Buildings [buildings.ruleset], also known as City Improvements
      * Forms of government [government.ruleset]
      * Technological advances [techs.ruleset]
      * Unit information [units.ruleset], including unit classes and unit types along with the varying
        actions from [game.ruleset]

    We leverage Jinja2 templates to make processing similar object instances (e.g. a single unit
    type such as Phalanx) in its own page. See the templates directory.

    As of v0.18 (Nov 2022), the following game objects have not been processed and enabled here:

      * All the effects from [effects.ruleset], [nation_intelligence_effects.ruleset], and
        [ai_effects.ruleset] among the common list. Effects can easily be added to a single gigantic
        page, but that makes undertstanding them more difficult. It is best to document them in the
        same page as the target (e.g. A Great Wonder's effects on the page for the Great Wonder).
      * Nations. Some rulesets have unique Nations defined and many rulesets leverage a common
        set of Nations. Custom code will been to be written to handle both scenarios.
      * Terrain from [terrain.ruleset]. Right now the ruleset specfile parser does not handle
        tileset specifics. Escpecially sprites contained in a single file as opposed to being
        separate files. Also need to determine if we are going to go with hex tiles or square tiles
        for our documentation.
      * Styles from [styles.ruleset]. It is to be determined if this is something we need to document.
    """

    # Instantiate the top level class
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
    action_enablers = rules.game.action_enablers
    borders = rules.game.borders
    research = rules.game.research
    culture = rules.game.culture
    calendar = rules.game.calendar
    settings = rules.game.settings

    # Get the city settings
    city_parameters = rules.cities.parameters
    citizens = rules.cities.citizens
    missing_unit_upkeep = rules.cities.missing_unit_upkeep

    # Get government settings
    gov_parms = rules.governments.government_parms
    all_governments = rules.governments.governments

    logging.info(f"Writing manual for {ruleset}...")

    # Write out the top level ruleset index for all the given rulesets
    #  Due to the sheer size of the content, the base game data is written
    #  out to multiple files to make reading much easier.
    os.makedirs(args.target_dir + "/%s/" % ruleset, exist_ok=True)

    # Start with the top level game page index with information from the [about], [options]
    # [tileset], [soundset], and [musicset] sections in game.ruleset. Also includes the
    # [government] section from governments.ruleset.
    template = env.get_template("index-game.rst")
    with open(args.target_dir + "/%s/index.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                about=about,
                options=options,
                tileset=tileset,
                soundset=soundset,
                musicset=musicset,
                gov_parms=gov_parms,
            )
        )

    # If the game has a detailed description defined in the [about] section we have a
    # single page for that as they are often long.
    template = env.get_template("description.rst")
    with open(args.target_dir + "/%s/description.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                about=about,
            )
        )

    # Write out game parameters from the [civstyle] section in game.ruleset.
    template = env.get_template("game-parms.rst")
    with open(args.target_dir + "/%s/game-parms.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                civ_style=civ_style,
            )
        )

    # Write out the [illness] section to a page from game.ruleset.
    template = env.get_template("plague.rst")
    with open(args.target_dir + "/%s/plague.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                illness=illness,
            )
        )

    # Write out the city [incite_cost] section to its own page from game.ruleset.
    # It has a long math formula.
    template = env.get_template("incite-cost.rst")
    with open(args.target_dir + "/%s/incite-cost.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                incite_cost=incite_cost,
            )
        )

    # Write out the unit [combat_rules], [auto_attack], and [actions] sections to its own page
    # from game.ruleset.
    template = env.get_template("unit-rules.rst")
    with open(args.target_dir + "/%s/unit-rules.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                combat_rules=combat_rules,
                auto_attack=auto_attack,
                actions=actions,
            )
        )

    # Write out the national [borders] section to its own bage from game.ruleset.
    template = env.get_template("borders.rst")
    with open(args.target_dir + "/%s/borders.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                borders=borders,
            )
        )

    # Write out the [research] section to its own page from game.ruleset.
    template = env.get_template("research.rst")
    with open(args.target_dir + "/%s/research.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                research=research,
            )
        )

    # Write out the [culture] victory section to its own page from game.ruleset.
    template = env.get_template("culture.rst")
    with open(args.target_dir + "/%s/culture.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                culture=culture,
            )
        )

    # Write out the game [calendar] section to its own page from game.ruleset.
    template = env.get_template("calendar.rst")
    with open(args.target_dir + "/%s/calendar.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                calendar=calendar,
            )
        )

    # Write out the [parameters], [citizens] and [missing_unit_upkeep] sections from city.ruleset
    # to its own page.
    template = env.get_template("city.rst")
    with open(args.target_dir + "/%s/city.rst" % ruleset, "w") as out:
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
    os.makedirs(args.target_dir + "/%s/buildings/" % ruleset, exist_ok=True)

    # Write a file for each building in the list of all of the buildings
    building_list = []
    template = env.get_template("building.rst")
    for building in all_buildings.values():
        building_list.append(building.name)
        with open(
            args.target_dir
            + "/%s/buildings/%s.rst" % (ruleset, make_slug(building.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    building=building,
                )
            )

    # Using a list of all the building files created above and then populate an index page.
    template = env.get_template("building-index.rst")
    building_list.sort()
    with open(args.target_dir + "/%s/buildings.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                building_list=building_list,
            )
        )

    # Get unit details
    all_unit_classes = rules.units.unit_classes
    all_unit_types = rules.units.unit_types

    # Create a directory to house all the unit-type and unit-class pages.
    os.makedirs(args.target_dir + "/%s/units/" % ruleset, exist_ok=True)

    # Write out all of the unit class details.
    unit_class_list = []
    template = env.get_template("unit-class.rst")
    for unit_class in all_unit_classes.values():
        unit_class_list.append(unit_class.name)
        units_in_class = filter(
            lambda ut: ut.uclass == unit_class, all_unit_types.values()
        )
        with open(
            args.target_dir
            + "/%s/units/%s.rst" % (ruleset, "class_" + make_slug(unit_class.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    unit_class=unit_class,
                    units_in_class=units_in_class,
                )
            )

    # Using a list of all the unit class files created above and then populate an index page.
    unit_class_list.sort()
    template = env.get_template("unit-class-index.rst")
    with open(args.target_dir + "/%s/unit-classes.rst" % ruleset, "w") as out:
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
            args.target_dir + "/%s/units/%s.rst" % (ruleset, make_slug(unit_type.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    unit_type=unit_type,
                    obsolete=obsolete,
                    action_enablers=action_enablers,
                )
            )

    # Build a list of all the unit files created above and then populate an index page.
    unit_type_list.sort()
    template = env.get_template("unit-type-index.rst")
    with open(args.target_dir + "/%s/unit-types.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                unit_type_list=unit_type_list,
            )
        )

    # Get all the technology advances
    all_advances = rules.techs.advances

    # Create a directory to house all the tech advance pages.
    os.makedirs(args.target_dir + "/%s/advances/" % ruleset, exist_ok=True)

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
            args.target_dir
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

    # Using a list of all the tech advance files created above and then populate an index page.
    advances_list.sort()
    template = env.get_template("advance-index.rst")
    with open(args.target_dir + "/%s/advances.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                advances_list=advances_list,
            )
        )

    # Create a directory to house all the government pages.
    os.makedirs(args.target_dir + "/%s/governments/" % ruleset, exist_ok=True)

    # Write out all of the tech advance details. Note that we gathered all of the government
    #  details much earlier for use in the top level game information.
    template = env.get_template("government.rst")

    governments_list = []
    for government in all_governments.values():
        governments_list.append(government.name)
        with open(
            args.target_dir
            + "/%s/governments/%s.rst" % (ruleset, make_slug(government.name)),
            "w",
        ) as out:
            out.write(
                template.render(
                    government=government,
                )
            )

    # Using a list of all the government files created above and then populate an index page.
    governments_list.sort()
    template = env.get_template("government-index.rst")
    with open(args.target_dir + "/%s/governments.rst" % ruleset, "w") as out:
        out.write(
            template.render(
                governments_list=governments_list,
            )
        )


def main():
    """
    Main function for sphinx_fc21_manuals
    """

    print(f"Welcome to {sys.argv[0]} v{__version__}\n")

    # If we don't pass a single ruleset name, assume you want to process all this shipped
    #  rulesets.
    if args.name == "None":
        # process all the shipped rulesets
        for ruleset in (
            "alien",
            "civ1",
            "civ2",
            "civ2civ3",
            "classic",
            "experimental",
            # "granularity",
            "multiplayer",
            "royale",
            "sandbox",
        ):
            process_ruleset([args.ruleset_dir], ruleset)
    else:
        process_ruleset([args.ruleset_dir], args.name)


########################################
# We made it, now run it!
main()
