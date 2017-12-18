from tradingbot.third_party import third_party


def test_thirdparty():
    assert third_party.get_config_dir().split('/')[-1] == 'configs'
