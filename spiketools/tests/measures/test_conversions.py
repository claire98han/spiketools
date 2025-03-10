"""Tests for spiketools.measures.conversions"""

import numpy as np

from pytest import raises

from spiketools.measures.spikes import compute_isis

from spiketools.measures.conversions import *

###################################################################################################
###################################################################################################

def test_convert_times_to_train(tspikes):

    spike_train = convert_times_to_train(tspikes)
    assert isinstance(spike_train, np.ndarray)
    assert spike_train.shape[-1] > tspikes.shape[-1]
    assert sum(spike_train) == tspikes.shape[-1]

    # Check the error with times / sampling rate mismatch
    spikes = np.array([0.1000, 0.1500, 0.1505, 0.2000])
    with raises(ValueError):
        convert_times_to_train(spikes, fs=1000)

def test_convert_train_to_times():

    train = np.zeros(100)
    spike_inds = np.array([12, 24, 36, 45, 76, 79, 90])
    np.put(train, spike_inds, 1)
    expected = (spike_inds / 1000) + 0.001

    # Check spike train for sampling rate of 1000
    spikes = convert_train_to_times(train, fs=1000)
    assert isinstance(spikes, np.ndarray)
    assert spikes.shape[-1] == spike_inds.shape[-1]
    assert np.array_equal(spikes, expected)

    # Check different sampling rate
    spikes = convert_train_to_times(train, fs=500)
    assert isinstance(spikes, np.ndarray)
    assert spikes.shape[-1] == spike_inds.shape[-1]
    assert np.array_equal(spikes, expected * 2)

def test_convert_isis_to_times(tspikes):

    isis = compute_isis(tspikes)

    spikes1 = convert_isis_to_times(isis)
    assert spikes1.shape[-1] == tspikes.shape[-1]

    spikes2 = convert_isis_to_times(isis, offset=2.)
    assert spikes2[0] == 2.

    spikes3 = convert_isis_to_times(isis, add_offset=False)
    assert len(spikes3) == len(isis)

    spikes4 = convert_isis_to_times(isis, offset=tspikes[0])
    assert np.array_equal(spikes4, tspikes)

def test_convert_times_to_rates(tspikes):

    # Using precomputed bin definition
    bins = np.arange(0, 10, 1)
    rates = convert_times_to_rates(tspikes, bins)
    assert isinstance(rates, np.ndarray)
    assert len(rates) == len(bins) - 1

    # Passing in bin width, with smoothing
    rates = convert_times_to_rates(tspikes, 0.5, time_range=[0, 8.5], smooth=0.5)
    assert isinstance(rates, np.ndarray)

    # Check bins with different sizes
    spikes = np.array([0.25, 0.5, 0.75, 1.25, 1.75, 2.25, 2.5, 2.75])
    tbins = np.array([0, 1, 1.5, 2, 3])
    rates = convert_times_to_rates(spikes, tbins)
    assert isinstance(rates, np.ndarray)
    assert np.array_equal(rates, np.array([3., 2., 2., 3.]))
