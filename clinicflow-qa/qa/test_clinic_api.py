from datetime import date

import pytest


def test_health_and_openapi(api):
    assert api.get('/actuator/health').json()['status']=='UP'
    paths=api.get('/v3/api-docs').json()['paths']
    assert '/api/owners' in paths


def test_owner_create_read_update_delete(api,owner_factory):
    owner=owner_factory()
    path=f"/api/owners/{owner['id']}"
    assert api.get(path).json()['telephone']=='1234567890'
    body={key:owner[key] for key in ['firstName','lastName','address','city','telephone']}
    body['city']='Updated City'
    assert api.put(path,json=body).status_code==204
    assert api.get(path).json()['city']=='Updated City'
    assert api.delete(path).status_code==204
    assert api.get(path).status_code==404


@pytest.mark.parametrize('telephone',['123456789','12345678901','abcdefghij','',None])
def test_invalid_phone_is_not_persisted(api,telephone):
    body={'firstName':'Phone','lastName':'Invalid','address':'Test','city':'Test','telephone':telephone}
    assert api.post('/api/owners',json=body).status_code==400
    response=api.get('/api/owners',params={'lastName':'Invalid'})
    assert response.status_code==404 or all(row['firstName']!='Phone' for row in response.json())


@pytest.mark.parametrize('first_name',['', '   ', 'a'*31, 'Test1'])
def test_invalid_name(api,first_name):
    body={'firstName':first_name,'lastName':'Boundary','address':'Test','city':'Test','telephone':'1234567890'}
    assert api.post('/api/owners',json=body).status_code==400


@pytest.mark.parametrize('first_name',['A','a'*30,'测试'])
def test_valid_name_boundaries(owner_factory,first_name):
    assert owner_factory(firstName=first_name)['firstName']==first_name


def test_owner_pet_visit_business_flow(api,owner_factory):
    owner=owner_factory()
    owner_id=owner['id']
    pet_type=api.get('/api/pettypes').json()[0]
    pet_payload={'name':'QA pet','birthDate':'2020-01-01','type':pet_type}
    response=api.post(f'/api/owners/{owner_id}/pets',json=pet_payload)
    assert response.status_code==201,response.text
    pet=response.json()
    assert pet['ownerId']==owner_id
    assert api.get(f"/api/owners/{owner_id}/pets/{pet['id']}").status_code==200
    response=api.post(f"/api/owners/{owner_id}/pets/{pet['id']}/visits",json={'date':date.today().isoformat(),'description':'QA checkup'})
    assert response.status_code==201,response.text
    visit=response.json()
    assert visit['petId']==pet['id']
    assert any(row['id']==visit['id'] for row in api.get(f"/api/pets/{pet['id']}").json()['visits'])


def test_nested_pet_cannot_be_read_through_different_owner(api,owner_factory):
    a,b=owner_factory(),owner_factory()
    pet_type=api.get('/api/pettypes').json()[0]
    response=api.post(f"/api/owners/{a['id']}/pets",json={'name':'Owned Pet','birthDate':'2020-01-01','type':pet_type})
    pet=response.json()
    assert api.get(f"/api/owners/{b['id']}/pets/{pet['id']}").status_code==404


@pytest.mark.parametrize('operation',['update','visit'])
def test_nested_pet_write_requires_matching_owner(api,owner_factory,operation):
    a,b=owner_factory(),owner_factory()
    pet_type=api.get('/api/pettypes').json()[0]
    payload={'name':'Original Pet','birthDate':'2020-01-01','type':pet_type}
    pet=api.post(f"/api/owners/{a['id']}/pets",json=payload).json()
    path=f"/api/owners/{b['id']}/pets/{pet['id']}"
    if operation=='update':
        response=api.put(path,json={**payload,'name':'Wrong owner edit'})
    else:
        response=api.post(path+'/visits',json={'date':date.today().isoformat(),'description':'Wrong owner visit'})
    assert response.status_code==404,response.text
    current=api.get(f"/api/pets/{pet['id']}").json()
    assert current['name']=='Original Pet'
    assert current['visits']==[]


@pytest.mark.parametrize('path',['/api/owners/2147483647','/api/pets/2147483647','/api/visits/2147483647'])
def test_missing_resource(api,path):
    assert api.get(path).status_code==404


@pytest.mark.parametrize('query',[{'page':-1},{'size':0}])
def test_page_boundaries(api,query):
    assert api.get('/api/v2/owners',params=query).status_code==400
