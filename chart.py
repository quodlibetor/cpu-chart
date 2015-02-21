import os
import time

import pygal


def label(time):
    return "%ss" % time


def chart(data):
    line_chart = pygal.Line()
    line_chart.title = 'CPU Usage History in %'
    line_chart.x_labels = map(label, list(range(-10, 0)))
    data = [d * 100 for d in data]  # convert each point to percent
    line_chart.add("User", data)
    line_chart.render_to_file("chart.svg")
    os.rename("chart.svg", "the_chart.svg")


def get_cpu():
    with open("/proc/stat") as stat_fh:
        raw_data = stat_fh.readline()

    name, *stats = raw_data.split()
    assert name == 'cpu'
    stats = [int(stat) for stat in stats]

    user, total = stats[0], sum(stats)

    return (user, total)


def loop():
    user, total = get_cpu()
    history = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    while 1:
        time.sleep(1)
        new_user, new_total = get_cpu()

        avg = (new_user - user) / (new_total - total)
        history.append(avg)
        history = history[-10:]  # just the most recent ten values

        chart(history)


if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        print("Caught quit, shutting down...")
