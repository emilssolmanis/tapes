from time import sleep
from flask import Flask
from tapes.distributed.registry import DistributedRegistry, RegistryAggregator

app = Flask(__name__)

registry = DistributedRegistry()
registry.connect()
timer = registry.timer('my.timer')


@app.route('/')
def hello():
    with timer.time():
        return 'finished'


if __name__ == '__main__':
    def _report(_registry):
        while True:
            sleep(100)

    RegistryAggregator(_report).start()

    app.run(port=8888)
