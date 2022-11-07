# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2022 Louis Moureaux <m_louis30@yahoo.com>

from typing import get_args, get_type_hints

from .buildings import BuildingsSettings
from .cities import CitySettings
from .effects import Effect, EffectsSettings
from .game import GameSettings
from .science import Advance, ScienceSettings
from .secfile import SpecParser
from .units import UnitClass, UnitsSettings, UnitType, load_veteran_levels

__all__ = ["Ruleset"]


class Ruleset:
    """
    Represents a Freeciv ruleset.
    """

    buildings: BuildingsSettings
    effects: list[Effect]
    game: GameSettings
    techs: ScienceSettings
    units: UnitsSettings

    def __init__(self, name, path):
        """
        Reads the ruleset called `name` under the data `path`.
        """

        sections = SpecParser.load(f"{name}/buildings.ruleset", path)
        self.buildings = BuildingsSettings(sections)

        sections = SpecParser.load(f"{name}/cities.ruleset", path)
        self.cities = CitySettings(sections)

        sections = SpecParser.load(f"{name}/effects.ruleset", path)
        self.effects = EffectsSettings(sections)

        sections = SpecParser.load(f"{name}/game.ruleset", path)
        self.game = GameSettings(sections)

        sections = SpecParser.load(f"{name}/techs.ruleset", path)
        self.techs = ScienceSettings(sections)

        sections = SpecParser.load(f"{name}/units.ruleset", path)
        self.units = UnitsSettings(sections)

        # Replace NamedReference
        self._collections = {
            "Advance": self.techs.advances,
            "Building": self.buildings.buildings,
            "UnitClass": self.units.unit_classes,
            "UnitType": self.units.unit_types,
        }
        # FIXME This seems to be doing quite a bit of extra work.
        self._link(self)

    def _handle(self, obj, hint):
        """
        Returns the replacement of obj according to any NamedReference
        present in the type hint.
        """

        if type(obj) in (list, set, tuple):
            # Handle each item in the container
            (arg,) = get_args(hint)
            return type(obj)(self._handle(x, arg) for x in obj)

        if not hasattr(hint, "wrapped"):
            self._link(obj)
            return obj

        objname = obj

        if objname in (None, "None", "-", ""):
            return None

        if not hint.wrapped in self._collections:
            warn(f"Cannot replace NamedReference({hint.wrapped})")
            return None

        if not objname in self._collections[hint.wrapped]:
            warn(f"Cannot find a {hint.wrapped} called {objname}")
            return None

        return self._collections[hint.wrapped][objname]

    def _link(self, obj):
        """
        Replaces all NamedReference in obj with the appropriate objects from
        _collections.
        """

        if type(obj) in (bool, float, int, str):
            pass
        elif type(obj) == dict:
            for val in obj.values():
                self._link(val)
        elif type(obj) in (list, set, tuple):
            for val in obj:
                self._link(val)
        else:
            hints = get_type_hints(type(obj))
            if hints:
                for propname, hint in hints.items():
                    prop = getattr(obj, propname)
                    setattr(obj, propname, self._handle(prop, hint))
            elif hasattr(obj, "__dict__"):
                for propname in vars(obj):
                    self._link(getattr(obj, propname))
