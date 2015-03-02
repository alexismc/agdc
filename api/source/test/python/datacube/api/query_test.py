#!/usr/bin/env python

# ===============================================================================
# Copyright (c)  2014 Geoscience Australia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither Geoscience Australia nor the names of its contributors may be
#       used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ===============================================================================


__author__ = "Simon Oldfield"


from datacube.api.model import DatasetType, Tile, Cell, Satellite
from datacube.api.query import list_tiles, list_tiles_wkt, list_tiles_to_file, list_tiles_between_dates, list_cells, \
    list_cells_to_file, list_tiles_dtm
import logging
import os
from datacube.config import Config
import csv
from datetime import datetime, date


_log = logging.getLogger()


def main():
    logging.basicConfig(level=logging.INFO)

    config = Config(os.path.expanduser("~/.datacube/config"))
    _log.debug(config.to_str())

    # find_missing_wofs_tiles(config)

    # do_list_tiles_by_xy_single(config)
    # do_list_cells_by_xy_single(config)

    # do_list_tiles_dtm_by_xy_single(config)

    # do_list_tiles_by_xy_multiple(config)
    # do_list_cells_by_xy_multiple(config)

    # do_list_tiles_by_shape_wkt(config)

    # do_list_tiles_by_xy_single_date_range(config)

    # do_list_tiles_by_xy_single_csv(config)
    # do_list_cells_by_xy_single_csv(config)

    # These are my test cells

    do_list_dataset_paths(config, x=[120], y=[-20], satellites=[Satellite.LS5, Satellite.LS7, Satellite.LS8], dataset_types=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED, DatasetType.DEM_SMOOTHED, DatasetType.DSM])
    do_list_dataset_paths(config, x=[123], y=[-25], satellites=[Satellite.LS5, Satellite.LS7, Satellite.LS8], dataset_types=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED, DatasetType.DEM_SMOOTHED, DatasetType.DSM])
    do_list_dataset_paths(config, x=[135], y=[-18], satellites=[Satellite.LS5, Satellite.LS7, Satellite.LS8], dataset_types=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED, DatasetType.DEM_SMOOTHED, DatasetType.DSM])
    # do_list_dataset_paths(config, x=[142], y=[-22], satellites=[Satellite.LS5, Satellite.LS7, Satellite.LS8], dataset_types=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED, DatasetType.DEM_SMOOTHED, DatasetType.DSM])
    # do_list_dataset_paths(config, x=[146], y=[-34], satellites=[Satellite.LS5, Satellite.LS7, Satellite.LS8], dataset_types=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED, DatasetType.DEM_SMOOTHED, DatasetType.DSM])


def do_list_dataset_paths(config,
                          x=range(110, 155 + 1), y=range(-55, -10 + 1),
                          acq_min=date(1980, 1, 1), acq_max=date(2020, 12, 31),
                          satellites=list(Satellite),
                          dataset_types=list(DatasetType)):
    tiles = list_tiles(x=x, y=y,
                       acq_min=acq_min, acq_max=acq_max, satellites=satellites,
                       datasets=dataset_types,
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        for dataset_type in dataset_types:
            if dataset_type in tile.datasets:
                print tile.datasets[dataset_type].path


def find_missing_wofs_tiles(config):
    _log.info("Finding missing WOFS water extent tiles...")
    tiles = list_tiles(x=range(110, 155+1), y=range(-55, -10+1),
                       acq_min=date(1980, 1, 1), acq_max=date(2020, 12, 31), satellites=[Satellite.LS5, Satellite.LS7],
                       #acq_min=date(2013, 1, 1), acq_max=date(2013, 12, 31), satellites=[Satellite.LS8],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25, DatasetType.WATER],
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        if DatasetType.WATER not in tile.datasets:
            _log.info("No WOFS extent found for xy = %s acq date = [%s] NBAR = [%s]", tile.xy, tile.end_datetime, tile.datasets[DatasetType.ARG25].path)


def do_list_tiles_by_xy_single(config):
    _log.info("Testing list_tiles...")
    tiles = list_tiles(x=[123], y=[-25],
                       acq_min=date(2005, 1, 1), acq_max=date(2005, 12, 31), satellites=[Satellite.LS5, Satellite.LS7],
                       #acq_min=date(2013, 1, 1), acq_max=date(2013, 12, 31), satellites=[Satellite.LS8],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        _log.info("Found tile xy = %s acq date = [%s] NBAR = [%s]", tile.xy, tile.end_datetime, tile.datasets[DatasetType.ARG25].path)
        _log.info("Found tile xy = %s acq date = [%s] WOFS = [%s]", tile.xy, tile.end_datetime,
                  DatasetType.WATER in tile.datasets and tile.datasets[DatasetType.WATER].path or "---")


def do_list_tiles_dtm_by_xy_single(config):
    _log.info("Testing list_tiles_dtm...")
    tiles = list_tiles_dtm(x=[123], y=[-25],
                           datasets=[DatasetType.DSM, DatasetType.DEM, DatasetType.DEM_HYDROLOGICALLY_ENFORCED,
                                     DatasetType.DEM_SMOOTHED],
                           database=config.get_db_database(), user=config.get_db_username(),
                           password=config.get_db_password(),
                           host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        _log.info("Found tile xy = %s acq date = [%s] DSM = [%s]", tile.xy, tile.end_datetime, tile.datasets[DatasetType.DSM].path)


def do_list_cells_by_xy_single(config):
    cells = list_cells(x=[123], y=[-25], years=[2002], satellites=["LS7"],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for cell in cells:
        _log.debug("Found cell xy = %s", cell.xy)


def do_list_tiles_by_xy_multiple(config):
    tiles = list_tiles(x=[124, 125], y=[-25, -24], years=[2002], satellites=["LS7"],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        _log.debug("Found tile xy = %s acq date = [%s]", tile.xy, tile.end_datetime)


def do_list_cells_by_xy_multiple(config):
    cells = list_cells(x=[124, 125], y=[-25, -24], years=[2002], satellites=["LS7"],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    for cell in cells:
        _log.debug("Found cell xy = %s", cell.xy)


def do_list_tiles_by_shape_wkt(config):
    tiles = list_tiles_wkt(wkt="POLYGON((123.5 -24,124.5 -23.5,125.5 -24,124.5 -24.5,123.5 -24))", years=[2002],
                           satellites=["LS7"],
                           datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                           database=config.get_db_database(), user=config.get_db_username(),
                           password=config.get_db_password(),
                           host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        _log.debug("Found tile xy = %s acq date = [%s]", tile.xy, tile.end_datetime)


def do_list_tiles_by_xy_single_date_range(config):
    tiles = list_tiles_between_dates(x=[149], y=[-29], satellites=["LS5", "LS7"],
                                     start_dt=datetime(2001, 1, 1), stop_dt=datetime(2001, 1, 31),
                                     # start_dt=datetime(2004, 7, 1), stop_dt=datetime(2004, 7, 31),
                                     datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                                     database=config.get_db_database(), user=config.get_db_username(),
                                     password=config.get_db_password(),
                                     host=config.get_db_host(), port=config.get_db_port())

    for tile in tiles:
        _log.debug("Found tile xy = %s acq date = [%s]", tile.xy, tile.end_datetime)


# Records DB -> CSV -> model classes

def do_list_tiles_by_xy_single_csv(config):

    filename = "/tmp/tiles.csv"

    list_tiles_to_file(x=[123], y=[-25], years=[2002], satellites=["LS7"],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       filename=filename,
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    tiles = []

    with open(filename, "rb") as f:
        reader = csv.DictReader(f)
        for record in reader:
            _log.debug("Found CSV record [%s]", record)
            tiles.append(Tile.from_csv_record(record))

    for tile in tiles:
        _log.debug("Found tile xy = %s acq date = [%s] NBAR = %s", tile.xy, tile.end_datetime, tile.datasets[DatasetType.ARG25].path)


def do_list_cells_by_xy_single_csv(config):

    filename = "/tmp/cells.csv"

    list_cells_to_file(x=[123], y=[-25], years=[2002], satellites=["LS7"],
                       datasets=[DatasetType.ARG25, DatasetType.PQ25, DatasetType.FC25],
                       filename=filename,
                       database=config.get_db_database(), user=config.get_db_username(),
                       password=config.get_db_password(),
                       host=config.get_db_host(), port=config.get_db_port())

    cells = []

    with open(filename, "rb") as f:
        reader = csv.DictReader(f)
        for record in reader:
            _log.debug("Found CSV record [%s]", record)
            cells.append(Cell.from_csv_record(record))

    for cell in cells:
        _log.debug("Found cell xy = %s", cell.xy)


if __name__ == "__main__":
    main()
