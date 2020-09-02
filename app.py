import os
import signal
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test-frontwheels')
def test_front_wheels():
    res= os.system("picar front-wheel-test")
    return res

@app.route('/test-rear-wheels')
def test_rear_wheels():
    res = os.system("picar rear-wheel-test")
    return res


@app.route('/stop-services/<process_string>')
def stop_services(process_string=None):
    kill_process(process_string)
    return f"Successfully stopped {process_string}"


def get_pid(process_name):
    import os
    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]


def check_process_ids(name):
    output = []
    cmd = "ps -aef | grep -i '%s' | grep -v 'grep' | awk '{ print $2 }' > /tmp/out"
    os.system(cmd % name)
    with open('/tmp/out', 'r') as f:
        line = f.readline()
        while line:
            output.append(line.strip())
            line = f.readline()
            if line.strip():
                output.append(line.strip())

    return output


def kill_process(process_string):
    process_ids = check_process_ids(process_string)
    for pid in process_ids:
        os.kill(int(pid), signal.SIGTERM)


if __name__ == '__main__':
    app.run()
