import logging
import ssl
from collections import defaultdict
from datetime import datetime, timedelta
from pyVmomi import vim, vmodl  # type: ignore
from pyVim import connect

from .asset_cache import AssetCache

MAX_CONN_AGE = 900


def get_data(ip4, username, password, instance_uuid, asset_name, interval):
    conn = _get_conn(ip4, username, password)
    content = conn.RetrieveContent()
    content_time = conn.CurrentTime()

    search_index = content.searchIndex
    assert search_index is not None

    instances = search_index.FindAllByUuid(None, instance_uuid, True, True)
    assert len(instances), 'no vms found for the given instance uuid'
    assert len(instances) == 1, \
        'more than one vm found for the given instance uuid'
    instance = instances[0]

    perf_manager = content.perfManager
    assert perf_manager is not None

    counters_lk = {c.key: c for c in perf_manager.perfCounter}
    available = \
        perf_manager.QueryAvailablePerfMetric(entity=instance)  # type: ignore

    metrics = (('cpu', 'ready'), ('disk', 'busResets'))
    metric_id = [
        vim.PerformanceManager.MetricId(counterId=m.counterId,
                                        instance=m.instance)
        for m in available
        if m.counterId in counters_lk and (
            counters_lk[m.counterId].groupInfo.key,
            counters_lk[m.counterId].nameInfo.key) in metrics
    ]
    if len(metric_id) == 0:
        return instance, None

    end_time = content_time
    start_time = content_time - timedelta(seconds=interval + 1)
    spec = vim.PerformanceManager.QuerySpec(intervalId=20,
                                            entity=instance,
                                            metricId=metric_id,
                                            startTime=start_time,
                                            endTime=end_time)
    counters = defaultdict(dict)
    for stat in perf_manager.QueryStats(querySpec=[spec]):
        for val in stat.value:  # type: ignore
            counter = counters_lk[val.id.counterId]
            path = counter.groupInfo.key, counter.nameInfo.key
            counters[path][val.id.instance] = val.value
    return instance, counters


def drop_connnection(host):
    conn, _ = AssetCache.get_value((host, 'connection'))
    if conn:
        AssetCache.drop((host, 'connection'))
        conn._stub.DropConnections()


def _get_conn(host, username, password):
    conn, expired = AssetCache.get_value((host, 'connection'))
    if conn:
        if expired:
            conn._stub.DropConnections()
        else:
            return conn

    conn = _get_connection(host, username, password)
    if not conn:
        raise ConnectionError('unable to connect')
    AssetCache.set_value((host, 'connection'), conn, MAX_CONN_AGE)
    return conn


def _get_connection(host, username, password):
    logging.info(f'Connecting to {host}')
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    return connect.SmartConnect(
        host=host,
        user=username,
        pwd=password,
        sslContext=context,
        connectionPoolTimeout=10)
