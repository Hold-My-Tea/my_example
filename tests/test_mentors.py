import pytest
import requests
from helpers import test_data as td
class TestAcc:
    @pytest.parametrize('type, data', [
        ('ipmi', td.ipmi),
        ('snmpv2c', {}),
        ('snmpv3', td.snmpv3),
        ('snmpv3', td.snmpv3_noauth),
        ('snmpv3', td.snmpv3_noprv),
        ('snmpv3', td.snmpv3_prv),
    ])
    def test_accounts_v2(self, type, data):
        basic_request = {
            'name': 'test_user',
            'type': type,
            'data': data
        }
        response = requests.post(json=basic_request)
        assert response