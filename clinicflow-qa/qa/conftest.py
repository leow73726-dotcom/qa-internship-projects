from urllib.parse import urlparse
import uuid

import pytest
import requests


def pytest_addoption(parser):
    parser.addoption('--base-url',default='http://127.0.0.1:9966/petclinic')


@pytest.fixture
def api(pytestconfig):
    base=pytestconfig.getoption('--base-url').rstrip('/')
    if urlparse(base).hostname not in {'127.0.0.1','localhost'}:
        pytest.fail('Use a local clone; this suite creates and deletes demo records.')
    session=requests.Session()
    class Client:
        def request(self,method,path,**kwargs):
            return session.request(method,base+path,timeout=15,**kwargs)
        def get(self,path,**kwargs):
            return self.request('GET',path,**kwargs)
        def post(self,path,**kwargs):
            return self.request('POST',path,**kwargs)
        def put(self,path,**kwargs):
            return self.request('PUT',path,**kwargs)
        def delete(self,path,**kwargs):
            return self.request('DELETE',path,**kwargs)
    try:
        yield Client()
    finally:
        session.close()


@pytest.fixture
def owner_factory(api):
    ids=[]
    def create(**changes):
        suffix=uuid.uuid4().hex[:10].translate(str.maketrans('0123456789','ghijklmnop'))
        body={'firstName':'Test','lastName':'QA'+suffix,'address':'1 Test Street','city':'Test City','telephone':'1234567890',**changes}
        response=api.post('/api/owners',json=body)
        assert response.status_code==201,response.text
        owner=response.json()
        ids.append(owner['id'])
        return owner
    yield create
    for owner_id in reversed(ids):
        response=api.delete(f'/api/owners/{owner_id}')
        assert response.status_code in {204,404},response.text
