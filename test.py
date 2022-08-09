import logging
import os
import re
from warnings import warn

from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import markdown
from unidecode import unidecode

import freeciv.rulesett as rs
import freeciv.secfile as sf
from freeciv.buildings import Building
from freeciv.effects import Effect
from freeciv.science import Advance
from freeciv.units import UnitClass, UnitType, load_veteran_levels

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
            logging.debug(f'Processing section "%s"', section.name)
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
                    # if type(value) != annotations[name]:
                    # raise TypeError(f'Expected {annotations[name].__name__} for {section_class.__name__}.{name}, got {type(value).__name__}')

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
    about = read_section(rs.AboutData, game_sections)

    tech_sections = load(f"{ruleset}/techs.ruleset", path)

    all_advances = {
        advance.name: advance for advance in read_sections(Advance, tech_sections)
    }

    def find_requirement(advance, name, all_advances):
        if name is None:
            return None
        elif name in all_advances:
            return all_advances[name]
        else:
            raise ValueError(
                'Advance "%s" references unknown advance "%s"' % (advance.name, name)
            )

    for advance in all_advances.values():
        advance.req1 = find_requirement(advance, advance.req1, all_advances)
        advance.req2 = find_requirement(advance, advance.req2, all_advances)
        advance.root_req = find_requirement(advance, advance.root_req, all_advances)
        # TODO Check for loops

    units_sections = load(f"{ruleset}/units.ruleset", path)

    all_unit_classes = {
        unit_class.name: unit_class
        for unit_class in read_sections(UnitClass, units_sections)
    }
    all_unit_types = {
        unit_type.name: unit_type
        for unit_type in read_sections(UnitType, units_sections)
    }

    veteran_system = None
    for section in units_sections:
        if section.name == "veteran_system":
            veteran_system = load_veteran_levels(**section)
    if veteran_system is None:
        raise ValueError("The [veteran_system] section could not be found")

    for unit_type in all_unit_types.values():
        if unit_type.uclass in all_unit_classes:
            unit_type.uclass = all_unit_classes[unit_type.uclass]
        else:
            raise ValueError(
                'Unit type "%s" references unknown unit class "%s"'
                % (unit_type.name, unit_type.uclass)
            )

        if unit_type.obsolete_by in all_unit_types:
            unit_type.obsolete_by = all_unit_types[unit_type.obsolete_by]
        elif not unit_type.obsolete_by is None:
            raise ValueError(
                'Unit type "%s" references unknown unit type "%s"'
                % (unit_type.name, unit_type.obsolete_by)
            )

        all_targets = []
        for target in unit_type.targets:
            if target in all_unit_classes:
                all_targets.append(all_unit_classes[target])
            else:
                raise ValueError(
                    'Unit type "%s" references unknown target "%s"'
                    % (unit_type.name, target)
                )
        unit_type.targets = all_targets

        reqs = set()
        for req in unit_type.tech_req:
            if req in all_advances:
                reqs.add(all_advances[req])
            else:
                raise ValueError(
                    'Unit type "%s" references unknown advance "%s"'
                    % (unit_type.name, req.name)
                )
        unit_type.tech_req = reqs

        cargo = set()
        if unit_type.cargo:
            for name in unit_type.cargo:
                if name in all_unit_classes:
                    cargo.add(all_unit_classes[name])
                else:
                    raise ValueError(
                        'Unit type "%s" references unknown unit class "%s"'
                        % (unit_type.name, name)
                    )
        unit_type.cargo = cargo

        if unit_type.veteran_levels is None:
            unit_type.veteran_levels = veteran_system

    buildings_sections = load(f"{ruleset}/buildings.ruleset", path)
    all_buildings = {
        building.name: building
        for building in read_sections(Building, buildings_sections)
    }

    effects_sections = load(f"{ruleset}/effects.ruleset", path)
    effects = read_sections(Effect, effects_sections)
    effects.sort(key=lambda e: e.type or "")

    # TODO Validation, linking...

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
