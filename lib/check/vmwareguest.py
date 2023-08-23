from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IncompleteResultException
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
from ..vmwarequery import vmwarequery


def on_guest_info(obj):
    # vim.vm.GuestInfo
    return {
        'appHeartbeatStatus': obj.appHeartbeatStatus,  # str
        'appState': obj.appState,  # str
        'guestFamily': obj.guestFamily,  # str
        'guestFullName': obj.guestFullName,  # str
        'guestId': obj.guestId,  # str
        'guestKernelCrashed': obj.guestKernelCrashed,  # bool
        'guestOperationsReady': obj.guestOperationsReady,  # bool
        'guestState': obj.guestState,  # str
        'guestStateChangeSupported': obj.guestStateChangeSupported,  # bool
        'hostName': obj.hostName,  # str
        'interactiveGuestOperationsReady':
            obj.interactiveGuestOperationsReady,  # bool
        'ipAddress': obj.ipAddress,  # str
        'toolsInstallType': obj.toolsInstallType,  # str/null
        'toolsRunningStatus': obj.toolsRunningStatus,  # str
        'toolsStatus': obj.toolsStatus,  # str
        'toolsVersion': obj.toolsVersion,  # str
        'toolsVersionStatus': obj.toolsVersionStatus,  # str
        'toolsVersionStatus2': obj.toolsVersionStatus2,  # str
    }


def on_runtime_info(obj):
    # vim.vm.RuntimeInfo
    return {
        'bootTime': datetime_to_timestamp(obj.bootTime),  # int/null
        'cleanPowerOff': obj.cleanPowerOff,  # bool
        'connectionState': obj.connectionState,  # str
        'consolidationNeeded': obj.consolidationNeeded,  # str
        'cryptoState': obj.cryptoState,  # str/null
        'faultToleranceState': obj.faultToleranceState,  # str
        'instantCloneFrozen': obj.instantCloneFrozen,  # bool/null
        'maxCpuUsage': obj.maxCpuUsage,  # int
        'maxMemoryUsage': obj.maxMemoryUsage,  # int
        'memoryOverhead': obj.memoryOverhead,  # int
        'minRequiredEVCModeKey': obj.minRequiredEVCModeKey,  # str
        'needSecondaryReason': obj.needSecondaryReason,  # str/null
        'numMksConnections': obj.numMksConnections,  # int
        'onlineStandby': obj.onlineStandby,  # bool
        'paused': obj.paused,  # bool
        'powerState': obj.powerState,  # str
        'quiescedForkParent': obj.quiescedForkParent,  # bool/null
        'recordReplayState': obj.recordReplayState,  # str
        'snapshotInBackground': obj.snapshotInBackground,  # bool
        'suspendInterval': obj.suspendInterval,  # int
        'suspendTime': datetime_to_timestamp(obj.suspendTime),
        'toolsInstallerMounted': obj.toolsInstallerMounted,  # bool
        'vFlashCacheAllocation': obj.vFlashCacheAllocation,  # int
    }


def on_virtual_hardware(obj):
    # vim.vm.VirtualHardware
    return {
        'memoryMB': obj.memoryMB,
        'numCPU': obj.numCPU,
        'numCoresPerSocket': obj.numCoresPerSocket,
        'virtualICH7MPresent': obj.virtualICH7MPresent,
        'virtualSMCPresent': obj.virtualSMCPresent,
    }


def on_config_info(obj):
    # vim.vm.ConfigInfo
    return {
        **on_virtual_hardware(obj.hardware),
        'alternateGuestName': obj.alternateGuestName,  # str
        'annotation': obj.annotation,  # str
        'changeTrackingEnabled': obj.changeTrackingEnabled,  # bool
        'changeVersion': obj.changeVersion,  # str
        'createDate': datetime_to_timestamp(obj.createDate),  # int/null
        'cpuHotAddEnabled': obj.cpuHotAddEnabled,  # bool
        'cpuHotRemoveEnabled': obj.cpuHotRemoveEnabled,  # bool
        'firmware': obj.firmware,  # str
        'guestAutoLockEnabled': obj.guestAutoLockEnabled,  # bool
        'guestFullNameConfig': obj.guestFullName,  # str
        'guestIdConfig': obj.guestId,  # str
        'hotPlugMemoryIncrementSize': obj.hotPlugMemoryIncrementSize,  # str
        'hotPlugMemoryLimit': obj.hotPlugMemoryLimit,  # str
        'instanceUuid': obj.instanceUuid,  # str
        'locationId': obj.locationId,  # str
        'maxMksConnections': obj.maxMksConnections,  # int
        'memoryHotAddEnabled': obj.memoryHotAddEnabled,  # bool
        'memoryReservationLockedToMax':
            obj.memoryReservationLockedToMax,  # bool
        'messageBusTunnelEnabled': obj.messageBusTunnelEnabled,  # bool
        'migrateEncryption': obj.migrateEncryption,  # str
        'modified': datetime_to_timestamp(obj.modified),
        # 'name': obj.name,  # str
        'nestedHVEnabled': obj.nestedHVEnabled,  # bool
        'npivDesiredNodeWwns': obj.npivDesiredNodeWwns,  # int/null
        'npivDesiredPortWwns': obj.npivDesiredPortWwns,  # int/null
        'migrateEncryption': obj.migrateEncryption,  # str
        'npivOnNonRdmDisks': obj.npivOnNonRdmDisks,  # bool
        'npivTemporaryDisabled': obj.npivTemporaryDisabled,  # bool
        'npivWorldWideNameType': obj.npivWorldWideNameType,  # str
        'swapPlacement': obj.swapPlacement,  # str
        'swapStorageObjectId': obj.swapStorageObjectId,  # str
        'template': obj.template,  # bool
        'uuid': obj.uuid,  # str
        'vAssertsEnabled': obj.vAssertsEnabled,  # bool
        'vFlashCacheReservation': obj.vFlashCacheReservation,  # int
        'vPMCEnabled': obj.vPMCEnabled,  # bool
        'version': obj.version,  # str
        'vmStorageObjectId': obj.vmStorageObjectId,  # str
    }


def on_quickstats(obj):
    # vim.vm.VirtualMachineQuickStats
    return {
        'activeMemory': obj.activeMemory,  # int/null
        'balloonedMemory': obj.balloonedMemory,  # int
        'compressedMemory': obj.compressedMemory,  # int
        'consumedOverheadMemory': obj.consumedOverheadMemory,  # int
        'grantedMemory': obj.grantedMemory,  # int
        'guestHeartbeatStatus': obj.guestHeartbeatStatus,  # str
        'guestMemoryUsage': obj.guestMemoryUsage,  # int
        'hostMemoryUsage': obj.hostMemoryUsage,  # int
        'overallCpuReadiness': obj.overallCpuReadiness,  # int/null
        'overallCpuUsage': obj.overallCpuUsage,  # int
        'privateMemory': obj.privateMemory,  # int
        'sharedMemory': obj.sharedMemory,  # int
        'swappedMemory': obj.swappedMemory,  # int
        'uptimeSeconds': obj.uptimeSeconds,  # int
    }


def on_virtual_disk_backing_info(obj):
    # vim.vm.device.VirtualDisk.FlatVer2BackingInfo
    return {
        'changeId': obj.changeId,  # str/null
        'contentId': obj.contentId,  # str/null
        'deltaDiskFormat': obj.deltaDiskFormat,  # str
        'deltaDiskFormatVariant': obj.deltaDiskFormatVariant,  # str
        'deltaGrainSize': obj.deltaGrainSize,  # int
        'digestEnabled': obj.digestEnabled,  # bool
        'diskMode': obj.diskMode,  # str
        'eagerlyScrub': obj.eagerlyScrub,  # bool/null
        'fileName': obj.fileName,  # str
        'sharing': obj.sharing,  # str
        'split': obj.split,  # bool
        'thinProvisioned': obj.thinProvisioned,  # bool
        'uuid': obj.uuid,  # str
        'writeThrough': obj.writeThrough,  # bool
    }


def on_virtual_disk(obj):
    # vim.vm.device.VirtualDisk
    return {
        **on_virtual_disk_backing_info(obj.backing),
        'capacityInBytes': obj.capacityInBytes,  # int
        'diskObjectId': obj.diskObjectId,  # str/null
        'nativeUnmanagedLinkedClone':
            obj.nativeUnmanagedLinkedClone,  # bool/null
    }


def on_snapshot_tree(obj):
    # vim.vm.SnapshotTree
    return {
        'backupManifest': obj.backupManifest,  # str
        'createTime': datetime_to_timestamp(obj.createTime),
        'description': obj.description,  # str
        'id': obj.id,  # int
        # 'name': obj.name,  # str
        'quiesced': obj.quiesced,  # xsd:boolean
        'replaySupported': obj.replaySupported,  # xsd:boolean
        'state': obj.state,  # str
    }


def snapshot_flat(snapshots, vm_name):
    for snapshot in snapshots:
        snapshot_dct = on_snapshot_tree(snapshot)
        snapshot_dct['name'] = f'{vm_name}/{snapshot.id}'
        snapshot_dct['snapshotName'] = snapshot.name
        snapshot_dct['snapshotId'] = snapshot.id
        snapshot_dct['vm'] = vm_name
        yield snapshot_dct
        for item in snapshot_flat(
                snapshot.childSnapshotList, vm_name):
            item['parentSnapshotName'] = snapshot.name
            item['parentSnapshotId'] = snapshot.id
            yield item


async def check_vmwareguest(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    vm, counters = await vmwarequery(
        asset,
        asset_config,
        check_config
    )

    virtual_disks = []
    snapshots = []

    info_dct = on_guest_info(vm.guest)
    info_dct.update(on_config_info(vm.config))
    info_dct.update(on_runtime_info(vm.runtime))
    info_dct.update(on_quickstats(vm.summary.quickStats))

    # vm.runtime.host is empty when vm is off
    info_dct['currentHypervisor'] = vm.runtime.host and vm.runtime.host.name
    info_dct['name'] = vm.name

    # aggregate performance metrics per guest
    if counters is not None:
        path = ('cpu', 'ready')
        total_name = ''
        values = counters[path].get(total_name)
        if values:
            info_dct['cpuReadiness'] = max(values) / 20_000 * 100
        # number of disk bus reset commands by the virtual machine
        # filter out negative values
        path = ('disk', 'busResets')
        info_dct['busResets'] = sum(
            sum(v for v in values if v > 0)
            for values in counters[path].values()
        )

    # SNAPSHOTS
    if vm.snapshot:
        snapshots.extend(
            snapshot_flat(
                vm['snapshot'].rootSnapshotList, vm['name']))

    for device in vm.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualDisk):
            disk_dct = on_virtual_disk(device)
            disk_dct['name'] = device.backing.fileName

            datastore = device.backing.datastore
            disk_dct['datastore'] = datastore.name
            disk_dct['label'] = device.deviceInfo.label
            virtual_disks.append(disk_dct)

    return {
        'guest': [info_dct],
        'snapshots': snapshots,
        'virtualDisks': virtual_disks,
    }
