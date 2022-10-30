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
import freeciv.game as game
import freeciv.secfile as sf
from freeciv.secfile.loader import read_section, read_sections

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


def load(name, path):
    logging.info("Reading %s..." % name)
    return sf.SpecParser(name, path).get_all()


def process_ruleset(path, ruleset):
    game_sections = load(f"{ruleset}/game.ruleset", path)

    # Get all the base game data
    data_file_header = read_section(game.DataFileHeader, game_sections)
    about = read_section(game.AboutData, game_sections)
    options = read_section(game.OptionsData, game_sections)
    tileset = read_section(game.TilesetData, game_sections)
    soundset = read_section(game.SoundsetData, game_sections)
    musicset = read_section(game.MusicsetData, game_sections)
    civ_style = read_section(game.CivStyleData, game_sections)
    illness = read_section(game.IllnessData, game_sections)
    incite_cost = read_section(game.InciteCostData, game_sections)
    combat_rules = read_section(game.CombatRulesData, game_sections)
    auto_attack = read_section(game.AutoAttackData, game_sections)
    actions = read_section(game.ActionsData, game_sections)
    borders = read_section(game.BordersData, game_sections)
    research = read_section(game.ResearchData, game_sections)
    culture = read_section(game.CultureData, game_sections)
    calendar = read_section(game.CalendarData, game_sections)
    settings = read_section(game.Settings, game_sections)

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
