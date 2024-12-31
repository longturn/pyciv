# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Louis Moureaux <m_louis30@yahoo.com>

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image
from typeguard import typechecked

from .secfile.loader import read_section, read_sections, section
from .secfile.parser import SpecParser

__all__ = [
    "FileData",
    "ExtraData",
    "GridData",
    "TileData",
    "TilespecData",
    "Tileset",
    "Sprite",
    "SpriteData",
]


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
class TileData:
    row: int
    column: int
    tag: list[str]

    option: set[str] = field(default_factory=set)

    hot_x: int = 0
    hot_y: int = 0


@section("grid_.+")
@typechecked
@dataclass
class GridData:
    dx: int
    dy: int

    tiles: list[TileData]

    x_top_left: int = 0
    y_top_left: int = 1

    pixel_border: int = 0


@typechecked
@dataclass
class SpriteData:
    tag: list[str]
    file: str

    option: set[str] = field(default_factory=set)


@section("extra")
@typechecked
@dataclass
class ExtraData:
    sprites: list[SpriteData]


class Sprite:
    """
    Allows loading sprites from a tileset.
    """

    location: SpriteData | tuple[FileData, GridData, TileData]

    def __init__(self, location: SpriteData | tuple[FileData, GridData, TileData]):
        self.location = location

    @property
    def filename(self) -> str:
        """
        Returns the name of the image file to load this sprite from, without extension.
        """
        if isinstance(self.location, SpriteData):
            return self.location.file
        return self.location[0].gfx

    def locate(self, path, extension=".png") -> Path:
        """
        Finds an image file to load this sprite from.
        """
        filename = self.filename + extension
        for location in path:
            full_path = Path(location) / filename
            if full_path.exists():
                return full_path

        raise ValueError(f'Could not find a file called "{filename}"')

    def load(self, path, extension=".png") -> Image:
        """
        Loads a sprite.
        """
        image = Image.open(self.locate(path, extension))
        if isinstance(self.location, SpriteData):
            return image

        # Crop the sprite from the grid
        _, grid, tile = self.location

        x = grid.x_top_left + (grid.dx + grid.pixel_border) * tile.column
        y = grid.y_top_left + (grid.dy + grid.pixel_border) * tile.row

        return image.crop((x, y, x + grid.dx, y + grid.dy))


class Tileset:
    """
    Represents a Freeciv tileset.
    """

    name: str
    tilespec: TilespecData
    grids: list[GridData]
    extras: list[ExtraData]

    sprite: dict[str, Sprite]

    def __init__(self, name: str, path: str, options: set[str] = set()):
        """
        Reads the tileset called `name` under the data `path`.
        """

        self.name = name

        sections = SpecParser.load(f"{name}.tilespec", path)
        self.tilespec = read_section(TilespecData, sections)

        self.grids = []
        self.extras = []
        self.sprites = {}

        for spec in self.tilespec.files:
            sections = SpecParser.load(spec, path)

            file_data = read_section(FileData, sections, missing_ok=True)

            grids = read_sections(GridData, sections)
            self.grids += grids

            for grid in grids:
                for tile in grid.tiles:
                    # Only load sprites for enabled options
                    if not tile.option.issubset(options):
                        continue

                    for tag in tile.tag:
                        self.sprites[tag] = Sprite((file_data, grid, tile))

            extra = read_section(ExtraData, sections, missing_ok=True)
            if extra:
                self.extras.append(extra)

                for sprite_data in extra.sprites:
                    for tag in sprite_data.tag:
                        self.sprites[tag] = Sprite(sprite_data)
