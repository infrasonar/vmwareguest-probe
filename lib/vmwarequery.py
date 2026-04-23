import asyncio
import logging
from http.client import BadStatusLine
from libprobe.exceptions import CheckException, IgnoreResultException
from pyVmomi import vim

from .vmwareconn import get_data, drop_connnection

DEFAULT_INTERVAL = 300


async def vmwarequery(
        local_config: dict,
        config: dict) -> tuple[vim.ManagedEntity,
                               dict | None,
                               list[dict] | None]:
    username = local_config.get('username')
    password = local_config.get('password')
    if None in (username, password):
        msg = 'missing credentials in local config'
        logging.error(msg)
        raise IgnoreResultException
    hypervisor = config.get('hypervisor')
    if hypervisor is None:
        msg = 'missing hypervisor in collector configuration'
        logging.error(msg)
        raise IgnoreResultException
    interval = config.get('_interval', DEFAULT_INTERVAL)
    instance_uuid = config.get('instance_uuid')
    if instance_uuid is None:
        msg = 'missing instance uuid in collector configuration'
        logging.error(msg)
        raise IgnoreResultException

    try:
        result = await asyncio.get_running_loop().run_in_executor(
            None,
            get_data,
            hypervisor,
            username,
            password,
            instance_uuid,
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


# NOTE type ignore
# pymomi typing does't tell about Exception base types
