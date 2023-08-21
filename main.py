from libprobe.probe import Probe
from lib.check.vcenterguest import check_vcenterguest
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'vcenterguest': check_vcenterguest
    }

    probe = Probe("vcenterguest", version, checks)

    probe.start()
