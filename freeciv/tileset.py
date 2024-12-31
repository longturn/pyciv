# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Louis Moureaux <m_louis30@yahoo.com>

from dataclasses import dataclass, field

from typeguard import typechecked

from .secfile.loader import read_section, read_sections, section
from .secfile.parser import SpecParser

__all__ = ["FileData", "Grid", "Tile", "TilespecData", "Tileset", "Sprite"]


@section("tilespec")
@typechecked
@dataclass
class TilespecData:
    options: str
    name: str
    priority: int

    summary: str

    normal_tile_width: int
    normal_tile_height: int
    small_tile_width: int
    small_tile_height: int

    type: str
    is_hex: bool

    fog_style: str
    darkness_style: str

    unit_flag_offset_x: int
    unit_flag_offset_y: int
    city_flag_offset_x: int
    city_flag_offset_y: int
    occupied_offset_x: int
    occupied_offset_y: int

    unit_offset_x: int
    unit_offset_y: int

    replaced_hue: int

    activity_offset_x: int
    activity_offset_y: int

    select_offset_x: int
    select_offset_y: int

    city_offset_x: int
    city_offset_y: int

    city_size_offset_x: int
    city_size_offset_y: int

    citybar_offset_y: int

    tilelabel_offset_y: int

    files: list[str]

    version: str = ""

    preferred_scale: int = 100

    select_step_ms: int = 100

    unit_upkeep_offset_y: int = 0

    unit_upkeep_small_offset_y: int = 0

    unit_default_orientation: str = "s"

    layer_order: list[str] = field(
        default_factory=lambda: [
            "Background",
            "Terrain1",
            "Darkness",
            "Terrain2",
            "Terrain3",
            "Water",
            "Roads",
            "Special1",
            "Grid1",
            "City1",
            "Special2",
            "Fog",
            "Unit",
            "Special3",
            "BaseFlags",
            "City2",
            "Grid2",
            "Overlays",
            "TileLabel",
            "CityBar",
            "FocusUnit",
            "Goto",
            "WorkerTask",
            "Editor",
            "InfraWork",
        ]
    )


@section("file")
@typechecked
@dataclass
class FileData:
    gfx: str


@typechecked
@dataclass
class Tile:
    row: int
    column: int
    tag: list[str]

    option: set[str] = field(default_factory=set)

    hot_x: int = 0
    hot_y: int = 0


@section("grid_.+")
@typechecked
@dataclass
class Grid:
    dx: int
    dy: int

    tiles: list[Tile]

    x_top_left: int = 0
    y_top_left: int = 1

    pixel_border: int = 0


@dataclass
class Sprite:
    image: FileData
    grid: Grid
    tile: Tile


class Tileset:
    """
    Represents a Freeciv tileset.
    """

    name: str
    tilespec: TilespecData
    grids: list[Grid]
    sprite: dict[str, Sprite]

    def __init__(self, name: str, path: str):
        """
        Reads the tileset called `name` under the data `path`.
        """

        self.name = name

        sections = SpecParser.load(f"{name}.tilespec", path)
        self.tilespec = read_section(TilespecData, sections)

        self.grids = []
        self.sprites = {}

        for spec in self.tilespec.files:
            sections = SpecParser.load(spec, path)
            file_data = read_section(FileData, sections, missing_ok=True)
            grids = read_sections(Grid, sections)

            self.grids.append(grids)
            for grid in grids:
                for tile in grid.tiles:
                    for tag in tile.tag:
                        self.sprites[tag] = Sprite(file_data, grid, tile)
