from libprobe.probe import Probe
from lib.check.wmwareguest import check_wmwareguest
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'wmwareguest': check_wmwareguest
    }

    probe = Probe("wmwareguest", version, checks)

    probe.start()
