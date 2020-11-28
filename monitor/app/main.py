from flask import Flask
import psutil

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
                'I/O': self.disk_io()
            }
        }

    def cpu_load_avg(self):
        return psutil.getloadavg()

    def mem_virtual(self):
        raw = psutil.virtual_memory()
        return self._memory(raw.total, raw.available)

    def mem_swap(self):
        raw = psutil.swap_memory()
        return self._memory(raw.total, raw.free)

    def _memory(self, total, available):
        return {
            'total': total,
            'available': available,
            'usage ratio': 1 - available/total
        }

    def disk_io(self):
        raw = psutil.disk_io_counters(perdisk=False)
        return {
            'read bytes': raw.read_bytes,
            'write bytes': raw.write_bytes
        }


@app.route('/')
def snapshot():
    snap = SystemMetrics()
    return snap.report()
