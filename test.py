import logging
import os
import re
from warnings import warn

from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import markdown
from unidecode import unidecode

from freeciv.rules import Ruleset

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


def make_slug(name):
    name = unidecode(name).lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub("[^a-z0-9_]", "", name)
    return name


env = Environment(
    loader=PackageLoader("freeciv", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
env.filters["make_slug"] = make_slug


def process_ruleset(path, ruleset):
    rules = Ruleset(ruleset, path)

    about = rules.game.about
    all_advances = rules.techs.advances
    all_unit_classes = rules.units.unit_classes
    all_unit_types = rules.units.unit_types
    all_buildings = rules.buildings.buildings

    effects = rules.effects
    effects.sort(key=lambda e: e.type or "")

    ############################################################################

    logging.info(f"Writing manual for {ruleset}...")

    os.makedirs("rules/%s/" % ruleset, exist_ok=True)
    template = env.get_template("index.html")
    with open("rules/%s/index.html" % ruleset, "w") as out:
        out.write(
            template.render(
                about=about,
                html_summary=markdown(about.summary),
                html_description=markdown(about.description),
            )
        )

    os.makedirs("rules/%s/tech" % ruleset, exist_ok=True)
    template = env.get_template("advance.html")

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
        with open(
            "rules/%s/tech/%s.html" % (ruleset, make_slug(advance.name)), "w"
        ) as out:
            out.write(
                template.render(
                    advance=advance,
                    required_by=required_by,
                    hard_required_by=hard_required_by,
                    required_by_units=required_by_units,
                    html_description=markdown(advance.helptext),
                )
            )

    template = env.get_template("tech_index.html")
    with open("rules/%s/tech/index.html" % ruleset, "w") as out:
        out.write(template.render(all_advances=all_advances.values()))

    os.makedirs("rules/%s/unit_class" % ruleset, exist_ok=True)
    template = env.get_template("unit_class.html")

    for unit_class in all_unit_classes.values():
        units_in_class = filter(
            lambda ut: ut.uclass == unit_class, all_unit_types.values()
        )
        with open(
            "rules/%s/unit_class/%s.html" % (ruleset, make_slug(unit_class.name)), "w"
        ) as out:
            out.write(
                template.render(unit_class=unit_class, units_in_class=units_in_class)
            )

    template = env.get_template("unit_class_index.html")
    with open("rules/%s/unit_class/index.html" % ruleset, "w") as out:
        out.write(template.render(all_unit_classes=all_unit_classes.values()))

    os.makedirs("rules/%s/unit" % ruleset, exist_ok=True)
    template = env.get_template("unit_type.html")

    for unit_type in all_unit_types.values():
        obsolete = list(
            filter(lambda ut: ut.obsolete_by == unit_type, all_unit_types.values())
        )
        with open(
            "rules/%s/unit/%s.html" % (ruleset, make_slug(unit_type.name)), "w"
        ) as out:
            out.write(
                template.render(
                    unit_type=unit_type,
                    obsolete=obsolete,
                    html_description=markdown(unit_type.helptext),
                )
            )

    template = env.get_template("unit_index.html")
    with open("rules/%s/unit/index.html" % ruleset, "w") as out:
        out.write(template.render(all_unit_types=all_unit_types.values()))

    os.makedirs("rules/%s/building" % ruleset, exist_ok=True)
    template = env.get_template("building.html")

    for building in all_buildings.values():
        with open(
            "rules/%s/building/%s.html" % (ruleset, make_slug(building.name)), "w"
        ) as out:
            out.write(
                template.render(
                    building=building, html_description=markdown(building.helptext)
                )
            )

    template = env.get_template("building_index.html")
    with open("rules/%s/building/index.html" % ruleset, "w") as out:
        out.write(template.render(all_buildings=all_buildings.values()))

    os.makedirs("rules/%s/effect" % ruleset, exist_ok=True)
    template = env.get_template("effects_index.html")
    with open("rules/%s/effect/index.html" % ruleset, "w") as out:
        out.write(template.render(effects=effects))


for ruleset in (
    "civ1",
    "civ2",
    "civ2civ3",
    "classic",
    "experimental",
    "multiplayer",
    "sandbox",
):
    process_ruleset(["/usr/share/freeciv"], ruleset)

for ruleset in (
    ("AU1", "augmented2"),
    "augmented2",
    "MP3_26",
    ("LT30", "lt30"),
    "LT31",
    "LT32",
    "LT33",
    "LT34",
    "LT35",
    "LT36",
    "LT37",
    "LT38",
    "LT39",
    "LT40",
    "LT41",  #'LT42', # Effects are broken
    "LT43",
    "LT44",
    "LT45",
    "LT46",
    "LT47",  #'LT48', # Has a syntax error
    "LT49",
    "LT50",
    "LT51",
    "LT52",
    "LT53",
    "LearningLT",
):
    if not type(ruleset) is tuple:
        ruleset = (ruleset, ruleset)
    process_ruleset(
        [f"/home/louis/freeciv/ltnet/games/{ruleset[0]}/data", "/usr/share/freeciv"],
        ruleset[1],
    )

# process_ruleset([f'/home/louis/freeciv/fc-aviation', '/usr/share/freeciv'],
#'aviation')
