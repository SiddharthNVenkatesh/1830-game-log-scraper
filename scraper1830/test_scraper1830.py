from scraper1830 import Scraper1830
import pytest


@pytest.fixture()
def myfixture():
    scraper = Scraper1830("60001")
    scraper.get_player_history()
    yield scraper


def test_scraper(myfixture):
    # test the class on game number 60001. test comparisons are obtained by looking at the self.log json directly.

    scraper = myfixture

    assert scraper.id == "60001"
    assert scraper.api == "https://18xx.games/api/game/60001"
    assert scraper.get_player_dict()[1903] == "tango sucka"

    print(scraper.get_initial_player_order())

    print(scraper.get_priority())

    # assert scraper.get_priority() ==  'lilyh'

    assert scraper.get_private_auction() == {
        "DH": ("lilyh", 100),
        "CS": ("JoonGloom", 45),
        "MH": ("The Beerguard", 155),
        "CA": ("MiroungaExpress", 200),
        "SV": ("JoonGloom", 20),
        "BO": ("tango sucka", 220),
    }

    print(scraper.get_remaining_cash())

    assert scraper.log["result"]["JoonGloom"] == 1524

    print(scraper.get_player_history())

    print(scraper.player_history_table())
