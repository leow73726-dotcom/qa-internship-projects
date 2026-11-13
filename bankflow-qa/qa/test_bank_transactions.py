from decimal import Decimal

import pytest


def test_demo_login_and_account_contract(bank):
    customer=bank.get('/login/john/demo')
    assert customer.status_code==200,customer.text
    assert customer.json()['id']==12212
    accounts=bank.get('/customers/12212/accounts')
    assert accounts.status_code==200
    assert len(accounts.json())>=2
    assert all(account['customerId']==12212 for account in accounts.json())


@pytest.mark.parametrize('amount',['0.01','1','12.34','100'])
def test_transfer_conserves_total_and_changes_both_balances(bank,amount):
    before=[bank.balance(12567),bank.balance(12789)]
    response=bank.transfer(amount)
    assert response.status_code==200,response.text
    after=[bank.balance(12567),bank.balance(12789)]
    assert after==[before[0]-Decimal(amount),before[1]+Decimal(amount)]
    assert sum(before)==sum(after)


def test_transfer_creates_matching_debit_and_credit_entries(bank):
    before_a={row['id'] for row in bank.transactions(12567)}
    before_b={row['id'] for row in bank.transactions(12789)}
    assert bank.transfer('10.25').status_code==200
    new_a=[row for row in bank.transactions(12567) if row['id'] not in before_a]
    new_b=[row for row in bank.transactions(12789) if row['id'] not in before_b]
    assert len(new_a)==len(new_b)==1
    assert new_a[0]['type']=='Debit' and new_b[0]['type']=='Credit'
    assert Decimal(str(new_a[0]['amount']))==Decimal('10.25')
    assert Decimal(str(new_b[0]['amount']))==Decimal('10.25')


def test_decimal_deposits_are_exact(bank):
    before=bank.balance(12900)
    for amount in ['0.10','0.20']:
        assert bank.post('/deposit',params={'accountId':12900,'amount':amount}).status_code==200
    assert bank.balance(12900)==before+Decimal('0.30')


def test_withdraw_changes_balance_by_exact_amount(bank):
    before=bank.balance(12567)
    assert bank.post('/withdraw',params={'accountId':12567,'amount':'10.01'}).status_code==200
    assert bank.balance(12567)==before-Decimal('10.01')


@pytest.mark.parametrize('amount',['0','-1','0.001'])
def test_transfer_policy_rejects_invalid_amount_without_writes(bank,amount):
    before=[bank.balance(12567),bank.balance(12789)]
    transactions=len(bank.transactions(12567))
    response=bank.transfer(amount)
    assert response.status_code==400,response.text
    assert [bank.balance(12567),bank.balance(12789)]==before
    assert len(bank.transactions(12567))==transactions


def test_same_account_transfer_is_rejected(bank):
    before=bank.balance(12567)
    assert bank.transfer('1',target=12567).status_code==400
    assert bank.balance(12567)==before


def test_missing_amount_is_rejected(bank):
    before=bank.balance(12567)
    response=bank.post('/transfer',params={'fromAccountId':12567,'toAccountId':12789})
    assert response.status_code==400,response.text
    assert bank.balance(12567)==before


def test_failed_destination_rolls_back_debit_and_ledger(bank):
    before=bank.balance(12567)
    entries=len(bank.transactions(12567))
    response=bank.transfer('10',target=2147483647)
    assert response.status_code>=400
    assert bank.balance(12567)==before
    assert len(bank.transactions(12567))==entries


def test_transaction_amount_filter(bank):
    assert bank.transfer('12.34').status_code==200
    response=bank.get('/accounts/12567/transactions/amount/12.34')
    assert response.status_code==200,response.text
    assert response.json()
    assert all(Decimal(str(row['amount']))==Decimal('12.34') for row in response.json())
