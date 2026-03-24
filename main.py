from libprobe.probe import Probe
from lib.check.vmwareguest import CheckVMwareGuest
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckVMwareGuest,
    )

    probe = Probe("vmwareguest", version, checks)

    probe.start()
