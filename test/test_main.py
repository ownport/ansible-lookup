
import json


def test_json_param():

    assert json.loads("[1, 2, 3]") == [1,2,3]
    assert json.loads('{"k":"v"}') == {'k':'v'}
