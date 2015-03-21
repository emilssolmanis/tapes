from flask import Flask
from tapes.registry import Registry

app = Flask(__name__)
registry = Registry()
timer = registry.timer('my.timer')


@app.route('/')
def hello():
    with timer.time():
        return 'finished'


if __name__ == '__main__':
    app.run(port=8888)
