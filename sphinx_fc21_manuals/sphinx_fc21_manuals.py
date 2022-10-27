# sphinx_fc21_manuals.py
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 James Robertson <jwrober@gmail.com>

# Version string
__version__ = "0.1"

import sys
import logging
import configparser

logging.basicConfig(level=logging.INFO)


def get_config(conf, section):
    """
    Get all the variables from a given conf file
    """

    config = configparser.ConfigParser()
    config.read(conf)

    # TODO: Convert this to a loop of some kind to "find" the variables and set them
    #  Don't forget to handle comma separated list and turn into a list or a tuple
    if config.has_option(section, "fc21_datadir_path"):
        fc21_datadir_path = config[section]["fc21_datadir_path"]
        logging.debug(f"fc21_datadir_path: %s", fc21_datadir_path)
    if config.has_option(section, "fc21_rst_output"):
        fc21_rst_output = config[section]["fc21_rst_output"]
        logging.debug(f"fc21_rst_output: %s", fc21_rst_output)
    if config.has_option(section, "fc21_rulesets"):
        fc21_rulesets = config[section]["fc21_rulesets"]
        fc21_rulesets = tuple(fc21_rulesets.split(","))
        logging.debug(f"fc21_rulesets: %s", fc21_rulesets)


def main():
    """
    Main function for sphinx_fc21_manuals
    """

    print(f"Welcome to {sys.argv[0]} v{__version__}")
    get_config("conf.ini", "MAIN")


main()
