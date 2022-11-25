import pickle
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

file = open('train_maxar_sliced_prediction_17only_epoch20centroids.histogram','rb')
saved_histogram_data = pickle.load(file)

errors = list(map(lambda x: x['error'], saved_histogram_data))

sns.set_style("whitegrid")
my_boxplot = sns.boxplot(data=errors)
my_boxplot.set(ylim=(-0.1, 2.5))
fig = my_boxplot.get_figure()
fig.savefig("boxplot0.png")

sns.set_style("whitegrid")
#my_hist = sns.histplot(data=errors)
#my_hist.set(ylim=(-0.1, 2.5))
#fig = my_boxplot.get_figure()
bins=np.arange(0,2.75,0.5)
hist, bin_edges = np.histogram(errors,bins) # make the histogram

fig,ax = plt.subplots()
# Set the ticks to the middle of the bars
ax.set_xticks([i for i,j in enumerate(hist)])

# Set the xticklabels to a string that tells us what the bin edges were
ax.set_xticklabels(['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])


# Plot the histogram heights against integers on the x axis
ax.bar(range(len(hist)),hist,width=1)

ax.set_title('Errors of all centroids')
ax.set_ylabel('value count')
ax.set_xlabel('absolute error (m)')
fig.savefig("centroids_histplot0.png")
