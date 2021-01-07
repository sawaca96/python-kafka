from typing import Dict, Any, List
from uuid import uuid4

from trading import db
from trading.utils import fetch_all
from trading.models import Order, Account, Position


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
    return accounts


async def create_order(order: Dict[str, Any]) -> Order:
    order = await Order.create(unfilled=order["quantity"], **order)
    return order.to_dict()


async def fetch_order() -> List[Dict[str, Any]]:
    query = db.select([Order])
    orders = await fetch_all(query)
    return orders


async def delete_order(order_id: str):
    query = Order.delete.where(Order.id == order_id)
    await query.gino.status()


async def create_position(account_id: str, position: Dict[str, Any]):
    position_id = uuid4()
    position = await Position.create(id=position_id, **position)
    return position.to_dict()