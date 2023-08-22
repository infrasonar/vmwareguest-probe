from libprobe.probe import Probe
from lib.check.vmwareguest import check_vmwareguest
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'vmwareguest': check_vmwareguest
    }

    probe = Probe("vmwareguest", version, checks)

    probe.start()
