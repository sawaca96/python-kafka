from typing import Dict, Any, List
from uuid import uuid4

from trading import db
from trading.utils import fetch_all
from trading.models import Order, Account


async def create_account(account: Dict[str, Any]) -> Account:
    account_id = uuid4()
    cash = account["start_cash"]
    account = await Account.create(
        id=account_id,
        cash=cash,
        **account,
    )
    return account.to_dict()


async def fetch_accounts() -> List[Dict[str, Any]]:
    query = db.select([Account])
    accounts = await fetch_all(query)
    return accounts.to_dict()


async def create_order(order: Dict[str, Any]) -> Order:
    order_id = uuid4()
    order = await Order.create(id=order_id, unfilled=order.quantity, **order)
    return Order.to_dict()


async def fetch_order() -> List[Dict[str, Any]]:
    query = db.select([Order])
    orders = await fetch_all(query)
    return order.to_dict()
