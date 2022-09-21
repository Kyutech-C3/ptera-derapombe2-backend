import pytest
from .fixtures import client, use_test_db_fixture

@pytest.mark.usefixtures('use_test_db_fixture')
class TestItem:
	def test_hoge(_):
		pass
