from uuid import uuid4

from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from trading.schema import Account, Order
from trading import service, order_producer
from trading.broker import Broker


router = APIRouter()


@router.get("/account", status_code=HTTP_200_OK)
async def fetch_account():
    data = await service.fetch_accounts()
    return data


@router.post("/account", status_code=HTTP_201_CREATED)
async def create_account(account: Account):
    account = account.dict()
    data = await service.create_account(account)
    return data


@router.get("/order", status_code=HTTP_200_OK)
async def fetch_order():
    data = await service.fetch_order()
    return data


@router.post("/order", status_code=HTTP_201_CREATED)
async def create_order(order: Order):
    order = order.dict()
    order["id"] = uuid4()
    await order_producer.produce(order)
    return {"message": "success"}


@router.delete("/order/{order_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    # name = "real:005930"
    # feed = await Broker.get(name)
    # feed.destroy()
    await service.delete_order(order_id)
