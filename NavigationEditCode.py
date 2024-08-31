import pandas as pd

def navigation_plot(pre_path,layout):
    #Layout is the stats layout where the graph is present for the plot
    #pre_path contains the path for the preprocessed data

    #PreProcessing
    dataframe_new = pd.read_csv(pre_path)

    grouped  = dataframe_new.groupby("Device_id")
    x = []
    y = []
    labels = []
    for name,group in grouped:
        labels.append(name)
        x.append(group['X_GPS'].values[0])
        y.append(group['Y_GPS'].values[0])
    layout.canvas.ax.clear()
    layout.canvas.ax.scatter(x,y)
    for i in range(0,len(x)):
        layout.canvas.ax.annotate(labels[i], (x[i], y[i]))

    layout.canvas.ax.legend()
    layout.canvas.ax.axis([0,650,0,700])
    layout.canvas.draw()
