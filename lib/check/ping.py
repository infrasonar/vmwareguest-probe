import logging
from icmplib import async_vcenterguest
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, NoCountException


async def check_vcenterguest(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    ...
