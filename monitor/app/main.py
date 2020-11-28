from flask import Flask
import psutil
import time
import datetime

conf = {
    'version': '0.1.0',
    'name': 'autoshut:monitor'
}
app = Flask(conf['name'])


@app.route('/about')
def about():
    return {
        'name': conf['name'],
        'version': conf['version']
    }


class SystemMetrics:
    def __init__(self):
        self._inittime = datetime.datetime.now()
        self._disk_io_init = self._disk_io_snap()
        self._net_io_init = self._net_io_snap()

    def report(self):
        return {
            'cpu': {
                'load avg': self.cpu_load_avg()
            },
            'mem': {
                'virt': self.mem_virtual(),
                'swap': self.mem_swap()
            },
            'disk': {
                'IO': self.disk_io(self._disk_io_init, self._inittime)
            },
            'net': {
                'IO': self.net_io(self._net_io_init, self._inittime)
            }
        }

    def _unit(value, unit):
        return { 'value': value, 'unit': unit }
    def _b(value):
        return SystemMetrics._unit(value, 'b')
    def _B(value):
        return SystemMetrics._unit(value, 'B')
    def _bps(value):
        return SystemMetrics._unit(value, 'b/s')
    def _Bps(value):
        return SystemMetrics._unit(value, 'B/s')
    def _points(value):
        return SystemMetrics._unit(value, 'points')
    def _percent(value):
        return SystemMetrics._unit(value, '%')

    # CPU
    def cpu_load_avg(self):
        return [ SystemMetrics._points(load) for load in psutil.getloadavg() ]

    # MEM
    def _memory(self, total, available):
        return {
            'total': SystemMetrics._B(total),
            'available': SystemMetrics._B(available),
            'usage ratio': SystemMetrics._percent(1 - available/total)
        }

    def mem_virtual(self):
        raw = psutil.virtual_memory()
        return self._memory(raw.total, raw.available)

    def mem_swap(self):
        raw = psutil.swap_memory()
        return self._memory(raw.total, raw.free)


    # IO
    def _io(self, r, w):
        return {
            'read': r,
            'write': w
        }

    def _io_diff(self, oldsnap, newsnap, snaptime):
        timediff = (datetime.datetime.now() - snaptime).total_seconds()
        return { key: SystemMetrics._Bps((newsnap[key]['value'] - oldsnap[key]['value']) / timediff) for key in newsnap }

    # DISK
    def _disk_io_snap(self):
        raw = psutil.disk_io_counters(perdisk=False)
        return self._io(SystemMetrics._B(raw.read_bytes), SystemMetrics._B(raw.write_bytes))

    def disk_io(self, oldsnap, snaptime):
        newsnap = self._disk_io_snap()
        return self._io_diff(oldsnap, newsnap, snaptime)

    # NET
    def _net_io_snap(self):
        raw = psutil.net_io_counters(pernic=False)
        return self._io(SystemMetrics._B(raw.bytes_recv), SystemMetrics._B(raw.bytes_sent))

    def net_io(self, oldsnap, snaptime):
        newsnap = self._net_io_snap()
        return self._io_diff(oldsnap, newsnap, snaptime)



@app.route('/')
def snapshot():
    snap = SystemMetrics()
    time.sleep(1)
    return snap.report()
