import asyncio
import logging
from http.client import BadStatusLine
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreCheckException, \
    IgnoreResultException
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
        logging.error(f'missing credentails for {asset}')
        raise IgnoreResultException
    hypervisor = check_config.get('hypervisor')
    if hypervisor is None:
        logging.error(f'missing hypervisor for {asset}')
        raise IgnoreResultException
    interval = check_config.get('_interval', DEFAULT_INTERVAL)
    instance_uuid = check_config.get('uuid')
    
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
    except (CheckException,
            IgnoreCheckException,
            IgnoreResultException):
        raise
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        raise IgnoreResultException
    except vim.fault.HostConnectFault:
        msg = 'Failed to connect.'
        raise CheckException(msg)
    except (IOError,
            BadStatusLine,
            ConnectionError) as e:
        msg = str(e) or e.__class__.__name__
        drop_connnection(hypervisor)
        raise CheckException(msg)
    except Exception as e:
        msg = str(e) or e.__class__.__name__
        logging.exception(msg)
        raise CheckException(msg)
    else:
        return result
