import pickle
import seaborn as sns

file = open('centroids.histogram','rb')
saved_histogram_data = pickle.load(file)

errors = list(map(lambda x: x['error'], saved_histogram_data))

sns.set_style("whitegrid")
my_boxplot = sns.boxplot(data=errors)
my_boxplot.set(ylim=(-0.1, 2.5))
fig = my_boxplot.get_figure()
fig.savefig("boxplot0.png")
