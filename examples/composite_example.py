'''Example for trading with human readable numbers

Usage: python -m examples.composite_example
'''
import asyncio
import logging
from random import randrange
from dydx4.chain.aerial.wallet import LocalWallet
from dydx4.clients import CompositeClient, Subaccount
from dydx4.clients.constants import BECH32_PREFIX, Network

from dydx4.clients.helpers.chain_helpers import (
    OrderType, 
    OrderSide, 
    OrderTimeInForce, 
    OrderExecution,
)
from examples.utils import loadJson

from tests.constants import DYDX_TEST_MNEMONIC


async def main() -> None:
    wallet = LocalWallet.from_mnemonic(DYDX_TEST_MNEMONIC, BECH32_PREFIX)
    network = Network.staging()
    client = CompositeClient(
        network,
    )
    subaccount = Subaccount(wallet, 0)
    ordersParams = loadJson('human_readable_orders.json')
    for orderParams in ordersParams:
        type = OrderType[orderParams["type"]]
        side = OrderSide[orderParams["side"]]
        time_in_force_string = orderParams.get("timeInForce", "GTT")
        time_in_force = OrderTimeInForce[time_in_force_string]
        price = orderParams.get("price", 1350)
        time_in_force_seconds = 60 if time_in_force == OrderTimeInForce.GTT else 0
        post_only = orderParams.get("postOnly", False)
        try:
            tx = client.place_order(
                subaccount,
                market='ETH-USD',
                type=type,
                side=side,
                price=price,
                size=0.01,
                client_id=randrange(0, 100000000),
                time_in_force=time_in_force,
                good_til_time_in_seconds=time_in_force_seconds,
                execution=OrderExecution.DEFAULT,
                post_only=post_only,
                reduce_only=False
            )
            print('**Order Tx**')
            print(tx)
        except Exception as error:
            print('**Order Failed**')
            print(str(error))

        await asyncio.sleep(5)  # wait for placeOrder to complete

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
