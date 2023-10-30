from ..util import connect_network, try_until_runs
import pytest


def test_connect_network():
    wlan = connect_network()
    isinstance(wlan, network.WLAN)