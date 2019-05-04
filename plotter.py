import matplotlib.pyplot as plt

class DynamicPlot():
    def __init__(self, xlabel, ylabel, mins=None):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.minimums = mins

        print("(", self.xlabel, self.ylabel, self.minimums, ")")

        self.on_launch()

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.lines, = self.ax.plot([],[], 'r.-')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        if self.minimums is not None:
            self.ax.set_xlim(self.minimums[0], self.minimums[1])
        #Other stuff
        self.ax.grid()
        self.figure.show()
        self.figure.canvas.draw()

    def update(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def update_multi(self, ts, minp, maxp, medp):
        self.ax.plot(ts, minp, 'g-')
        self.ax.plot(ts, maxp, 'g-')
        self.ax.plot(ts, medp, 'r-')
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()