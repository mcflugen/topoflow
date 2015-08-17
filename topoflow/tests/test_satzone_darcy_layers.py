#!/usr/bin/env python
#
# Tests the SatZoneDarcyLayers TopoFlow component.
#
# site_prefix = 'Treynor'
# case_prefix = 'June_20_67'
#
# Required input files:
# - June_20_67_satzone_darcy_layers.cfg
# - Treynor.rti
# - Treynor_DEM.rtg

from shutil import rmtree
from os import makedirs, listdir
from os.path import join, dirname, exists
from nose.tools import assert_is_instance, assert_is_not_none
from numpy.testing import assert_almost_equal
from topoflow.components.satzone_darcy_layers import satzone_component as Model
from . import input_dir, output_dir


cfg_file = join(input_dir, 'June_20_67_satzone_darcy_layers.cfg')
time_factor = 5.0


def setup_module():
    global comp
    comp = Model()
    if exists(output_dir) is False:
        makedirs(output_dir)


def teardown_module():
    parent_dir = dirname(output_dir)
    if exists(parent_dir):
        rmtree(parent_dir)


def test_is_instance():
    assert_is_instance(comp, Model)


def test_irf():
    comp.initialize(cfg_file)
    comp.update()
    comp.finalize()


def test_has_output():
    assert_is_not_none(listdir(output_dir))


def test_update_until():
    time_step = comp.get_time_step()
    until_time = time_step * time_factor

    comp.initialize(cfg_file)
    comp.update_until(until_time)
    end_time = comp.get_current_time()
    comp.finalize()
    assert_almost_equal(end_time, until_time)
