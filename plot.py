import matplotlib.pyplot as plt
import numpy as np

def makePlot(data):
    index = 1
    labels = []
    values = []
    for row in data:
        values.append(row[1])
        labels.append(str(index))
        index += 1
    fig_url = 'plot.png'
    y = np.array(values)
    plt.pie(y)
    plt.savefig(fig_url, bbox_inches="tight", dpi=800)
    return fig_url