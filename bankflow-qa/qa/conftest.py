from decimal import Decimal
from urllib.parse import urlparse

import pytest
import requests


def pytest_addoption(parser):
    parser.addoption('--base-url',default='http://127.0.0.1:8087/parabank')


@pytest.fixture
def bank(pytestconfig):
    base=pytestconfig.getoption('--base-url').rstrip('/')
    if urlparse(base).hostname not in {'127.0.0.1','localhost'}:
        pytest.fail('BankFlow resets demo data. Only local clones are supported.')
    session=requests.Session()
    session.headers['Accept']='application/json'
    class Bank:
        def request(self,method,path,**kwargs):
            return session.request(method,base+'/services/bank'+path,timeout=25,**kwargs)
        def get(self,path,**kwargs):
            return self.request('GET',path,**kwargs)
        def post(self,path,**kwargs):
            return self.request('POST',path,**kwargs)
        def balance(self,account):
            response=self.get(f'/accounts/{account}')
            assert response.status_code==200,response.text
            return Decimal(str(response.json(parse_float=Decimal)['balance']))
        def transfer(self,amount,source=12567,target=12789):
            return self.post('/transfer',params={'fromAccountId':source,'toAccountId':target,'amount':amount})
        def transactions(self,account):
            response=self.get(f'/accounts/{account}/transactions')
            assert response.status_code==200,response.text
            return response.json(parse_float=Decimal)
    api=Bank()
    reset=api.post('/initializeDB')
    assert reset.status_code in {200,204},reset.text
    try:
        yield api
    finally:
        session.close()
