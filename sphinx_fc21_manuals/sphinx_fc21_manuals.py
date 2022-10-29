# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.2"

import sys
import os
import logging
import configparser

from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append("../")
import freeciv.secfile as sf
import freeciv.game as game

logging.basicConfig(level=logging.INFO)

def make_slug(name):
    name = unidecode(name).lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub("[^a-z0-9_]", "", name)
    return name

#FIXME: Adding this breaks the ability to read the ruleset files
env = Environment(
    loader=PackageLoader("sphinx_fc21_manuals", "templates"),
    #autoescape=select_autoescape(["html", "xml"]),
)
#env.filters["make_slug"] = make_slug


def as_list(value):
    if type(value) == list:
        return value
    elif value == "":
        return []
    else:
        return [value]


def read_sections(section_class, sections):
    result = []
    for section in sections:
        if section_class._section_regex.match(section.name):
            logging.info(f'Processing section "%s"', section.name)
            fields = list(
                filter(lambda name: not name.startswith("_"), dir(section_class))
            )
            default_values = {name: getattr(section_class, name) for name in fields}
            annotations = section_class.__annotations__

            dictionnary = {}

            for name, value in section.items():
                if (
                    hasattr(section_class, "_rewrite_rules")
                    and name in section_class._rewrite_rules
                ):
                    name = section_class._rewrite_rules[name]

                if not name in fields and not name in annotations:
                    raise TypeError(
                        f'Type {section_class.__name__} has no field called "{name}"'
                    )

                if name in annotations and type(annotations[name]) == type:
                    if annotations[name] == list:
                        dictionnary[name] = as_list(value)
                        continue
                    elif annotations[name] == set:
                        dictionnary[name] = set(as_list(value))
                        continue

                dictionnary[name] = value

            result.append(section_class(**dictionnary))
    return result


def read_section(section_class, sections):
    all_results = list(read_sections(section_class, sections))
    if not all_results:
        raise ValueError(
            f'No section matching "{section_class._section_regex}" was found'
        )
    if len(all_results) > 1:
        raise ValueError(
            f'Several sections matching "{section_class._section_regex}" were found'
        )
    return all_results[0]


def load(name, path):
    logging.info("Reading %s..." % name)
    return sf.SpecParser(name, path).get_all()


def process_ruleset(path, ruleset):
    game_sections = load(f"{ruleset}/game.ruleset", path)

    # Get all the base game data
    game.DataFileHeader = read_section(game.DataFileHeader, game_sections)
    game.AboutData = read_section(game.AboutData, game_sections)
    game.OptionsData = read_section(game.OptionsData, game_sections)
    game.TilesetData = read_section(game.TilesetData, game_sections)
    game.SoundsetData = read_section(game.SoundsetData, game_sections)
    game.MusicsetData = read_section(game.MusicsetData, game_sections)
    game.CivStyleData = read_section(game.CivStyleData, game_sections)
    game.IllnessData = read_section(game.IllnessData, game_sections)
    game.InciteCostData = read_section(game.InciteCostData, game_sections)
    game.CombatRulesData = read_section(game.CombatRulesData, game_sections)
    #FIXME: The if_attacker table isn't working in game.py
    #game.AutoAttackData = read_section(game.AutoAttackData, game_sections)
    #FIXME: The attribute list has poison_empties_food_stock, but typeguard doesn't like it
    #game.ActionsData = read_section(game.ActionsData, game_sections)
    game.BordersData = read_section(game.BordersData, game_sections)
    game.ResearchData = read_section(game.ResearchData, game_sections)
    game.CultureData = read_section(game.CultureData, game_sections)
    #FIXME: The attribute list has fragment_name0, but typeguard doesn't like it
    #game.CalendarData = read_section(game.CalendarData, game_sections)


    logging.info(f"Writing manual for {ruleset}...")

    os.makedirs(file_locations.get("conf.fc21_rst_output")+"/%s/" % ruleset, exist_ok=True)
    #template = env.get_template("index.rst")


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
    print(file_locations.get("conf.fc21_datadir_path"))
    process_ruleset([file_locations.get("conf.fc21_datadir_path")], "civ1")

main()
