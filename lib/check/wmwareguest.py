import logging
from icmplib import async_wmwareguest
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, NoCountException


async def check_wmwareguest(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    ...
