import asyncio
import logging
from http.client import BadStatusLine
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from pyVmomi import vim  # type: ignore
from typing import List, Tuple

from .vmwareconn import get_data, drop_connnection

DEFAULT_INTERVAL = 300


async def vmwarequery(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> list:
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        msg = 'missing credentails in local config'
        raise CheckException(msg)
    hypervisor = check_config.get('hypervisor')
    if hypervisor is None:
        msg = 'missing hypervisor in collector configuration'
        raise CheckException(msg)
    interval = check_config.get('_interval', DEFAULT_INTERVAL)
    instance_uuid = check_config.get('instance_uuid')
    if instance_uuid is None:
        msg = 'missing instance uuid in collector configuration'
        raise CheckException(msg)

    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            get_data,
            hypervisor,
            username,
            password,
            instance_uuid,
            asset.name,
            interval,
        )
    except CheckException:
        raise
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        msg = 'invalid login or not authenticated'
        raise CheckException(msg)
    except vim.fault.HostConnectFault:
        msg = 'failed to connect'
        raise CheckException(msg)
    except (IOError,
            BadStatusLine,
            ConnectionError) as e:
        msg = str(e) or e.__class__.__name__
        drop_connnection(hypervisor)
        raise CheckException(msg)
    except AssertionError as e:
        msg = str(e)
        raise CheckException(msg)
    except Exception as e:
        msg = str(e) or e.__class__.__name__
        logging.exception(msg)
        raise CheckException(msg)
    else:
        return result
