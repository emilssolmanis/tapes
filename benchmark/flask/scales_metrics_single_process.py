from greplin import scales
from flask import Flask


STATS = scales.collection('/web', scales.PmfStat('latency'))

app = Flask(__name__)


@app.route('/')
def hello():
    with STATS.latency.time():
        return 'finished'


if __name__ == '__main__':
    app.run(port=8888)
