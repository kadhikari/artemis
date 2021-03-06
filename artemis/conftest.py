"""
py test discover this file by default

Used to run some stuff at global scope
"""
import logging
import pytest
from artemis import utils
from artemis.configuration_manager import config


def pytest_addoption(parser):
    """
    We add a pytest option to
    * skip the cities integration
    * skip the data integration (if it has been done before, it can save some time)
    """
    parser.addoption("--skip_cities", action="store_true", help="skip cities loading")
    parser.addoption("--skip_bina", action="store_true", help="skip binarization")


@pytest.fixture(scope="session", autouse=True)
def load_cities(request):
    """
    Before running the tests we want to load cities
    """
    log = logging.getLogger(__name__)
    if request.config.getvalue("skip_cities"):
        log.info("skiping cities loading")
        return

    log.info("loading cities database")

    utils.launch_exec('cities -i {input} --connection-string'
                      .format(input=config['CITIES_INPUT_FILE']),
                      additional_args=[config['CITIES_DB']])

    log.info("cities database loaded")
