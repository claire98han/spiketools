"""Tests for spiketools.spatial.checks"""

import numpy as np

from pytest import raises

from spiketools.spatial.checks import *

###################################################################################################
###################################################################################################

def test_check_position():

    position1 = np.array([1, 2, 3])
    position2 = np.array([[1, 2, 3], [1, 2, 3]])
    position3 = np.array([[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]]])

    check_position(position1)
    check_position(position2)
    with raises(AssertionError):
        check_position(position3)

def test_check_spatial_bins():

    bins_int = 12
    bins_1d = [12]
    bins_2d = [5, 10]

    position = np.array([[1, 2, 3], [4, 5, 6]])

    out1d1 = check_spatial_bins(bins_int)
    out1d2 = check_spatial_bins(bins_1d)
    assert out1d1 == out1d2 == bins_1d

    bins = check_spatial_bins(bins_2d, position)
    assert bins == bins_2d

    with raises(AssertionError):
        check_spatial_bins([1.2, 2.3])
    with raises(AssertionError):
        check_spatial_bins([1, 2, 3])
    with raises(AssertionError):
        check_spatial_bins(bins_1d, position)
