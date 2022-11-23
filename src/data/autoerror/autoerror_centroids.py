import numpy as np
from skimage import measure
import glob
import os.path
import pickle
import pandas as pd

# Given a matrix of integers, each different integer value corresponding
# to a different label, this function calculates the centroid (i.e. center of mass)
# of all points corresponding to the specific label

def find_centroid(matrix, label):

    centroid = np.zeros(2)
    counter = 0

    # Cycle over all entries, adding to the centroid if we match the label.

    for i in range(0, matrix.shape[0]-1):
        for j in range(0, matrix.shape[1]-1):
            if matrix[i , j] == label:
                centroid += np.array([i, j])
                counter += 1

    return centroid / counter, counter


# Given a matrix loaded from the BHM, this function will calculate
# a corresponding matrix of integers, where each integer corresponds
# to a label, after the segmention.
#
# We also return a list of centroids

def get_labels_and_centroids(bhm):

    # Identify the points that corresponds to a height more than three times the average

    elevated_points = bhm > 3 * bhm.mean()

    # Use scikit-image to create clusters out of them, according to connectivity

    label_matrix = measure.label(elevated_points)

    # Create a list of unique labels, with their counts

    unique, counts = np.unique(label_matrix, return_counts=True)

    # Remove the component with most pixels (will be the background), and the components with less than 1300 pixels

    zipped = list(zip(unique, counts))
    zipped.sort(key=lambda x: -x[1])
    zipped.pop(0)

    ok_labels = list(map(lambda x: x[0], filter(lambda x: x[1] > 1300, zipped)))

    # Select from label_matrix only the 'ok' labels, setting the other ones to 0

    ok_label_matrix = label_matrix

    for i in range(0, 500):
        for j in range (0, 500):
            if ok_label_matrix[i, j] not in ok_labels:
                ok_label_matrix[i, j] = 0

    # TODO: the loop above can be replaced by a single call to vectorize, something like
    # vfunc = np.vectorize(lambda x: 0 if x not in ok_labels else x)
    # label_matrix = vfunc(label_matrix)

    # Find the centroids corresponding to the 'surviving' components

    centroids = []

    for label in ok_labels:

        centroid, counter = find_centroid(ok_label_matrix, label)
        centroids.append(centroid)

    return ok_label_matrix, centroids

# This function calculates the error centroid by centroid

def error_on_centroids(ground_truth, prediction, min=0, max=99999):

    # z1 corresponds to the BHM, z2 corresponds to the model prediction. Note the scaling factors.

    z1 = np.flipud(np.load(ground_truth, allow_pickle=True))
    z2 = 50 * np.flipud(np.load(prediction, allow_pickle=True))

    _, centroids = get_labels_and_centroids(z1)

    average = 0
    counter = 0
    all_errors = []

    # For all centroids, we calculate the error and we update the counters.

    for centroid in centroids:

        (xcoord, ycoord) = (int(centroid[0]), int(centroid[1]))

        # The coordinates need to be flipped
        (xcoord, ycoord) = (ycoord, xcoord)

        # If the centroid is not within the specified range, we do not count it

        height = z1[xcoord, ycoord]
        if height < min or height > max:
            continue

        this_average = abs(z1[xcoord, ycoord]-z2[xcoord, ycoord])/z1.mean()

        average += this_average
        counter += 1

        all_errors.append({'error': this_average, 'height': height})

    # Finally we return the average error, the average height, and the histogram with all errors.

    return (average / counter, z1.mean(), all_errors) if counter > 0 else (0, 0, [])

# This function calcolates the error building by building

def error_on_segments(ground_truth, prediction):

    # z1 corresponds to the BHM, z2 corresponds to the model prediction. Note the scaling factors.

    z1 = np.flipud(np.load(ground_truth, allow_pickle=True))
    z2 = 50 * np.flipud(np.load(prediction, allow_pickle=True))

    # zerror is a matrix containing the relative error, pixel by pixel

    zerror = abs(z1 - z2) / z1.mean()

    label_matrix, centroids = get_labels_and_centroids(z1)

    unique_labels = np.unique(label_matrix)

    average = 0
    counter = 0
    all_errors = []

    # We iterate over all labels, and we update the running average

    for label in unique_labels:

        if label == 0:
            continue

        vfunc = np.vectorize(lambda x: 1 if x == label else 0)
        mask = vfunc(label_matrix).transpose()

        this_error = np.multiply(mask, zerror).sum() / mask.sum()

        average += this_error # Error calculated on all the pixels of the current building
        counter += 1 # Numbers of pixels in the current building

        height = np.multiply(mask, z1).sum() / mask.sum()
        all_errors.append({'error': this_error, 'height': 0})

    # Finally we return the average error, the average height, and the histogram with all errors.

    return average / counter, z1.mean(), all_errors




# The directory for the data
pairs="pairs_17"
short_path="~/data/UNICEF_data/tim_maxar_bhm_final_pairs/"+pairs+"/"
path=os.path.expanduser(short_path)


# The directory with the ground truth (BHM) files
bhm_directory = 'sliced_bhm'


# The directories with the prediction files.
# Make sure that the directories are somehow 'compatible' (e.g. different pairs id, but same number of epochs),
# as it wouldn't make much sense to calculate an average error over different epochs.

prediction_directories = ['train_maxar_sliced_prediction_17only_epoch3',
                            'train_maxar_sliced_prediction_17only_epoch20',
                            'train_maxar_sliced_prediction_17only_epoch50',
                            'train_maxar_sliced_prediction_pair16_17_epoch50']
df=pd.DataFrame({"prediction_dir":prediction_directories})
df['pairs']=df.prediction_dir
df["abs_error"]=df.prediction_dir
df["all_error"]=df.prediction_dir
df["all_heights"]=df.prediction_dir
pairs = []
#for directory in prediction_directories: #use if do not want to distinguish between directories
for index,row in df.iterrows(): #iuse if want to dicsinguish between directories
    directory=row.prediction_dir
    print(directory)
    for name in glob.glob(path+directory + '/*.npy'):
        bhm_name = name.replace(directory, bhm_directory).replace('maxar-', 'bhm-')
        pairs.append({'prediction': name, 'bhm': bhm_name})
    row.pairs=pairs

  


# We load the files and calculate cumulative statistics using error_on_centroid()

absolute_error = 0
counter = 0
histogram = []

for index,row in df.iterrows():
    print(index)
    absolute_error = 0
    counter = 0
    histogram = []
    for pair in row.pairs:

        if not os.path.exists(pair['bhm']):
            continue

        if not os.path.exists(pair['prediction']):
            continue

        #print('Loading {} (BHM) and {} (prediction)'.format(pair['bhm'], pair['prediction']))

        error, mean, all_errors = error_on_centroids(pair['bhm'], pair['prediction'])

        absolute_error += error * mean
        counter += 1
        histogram.extend(all_errors)

    absolute_error /= counter
    print(row.prediction_dir)
    with open(path+"prediction_error/"+str(row.prediction_dir)+"_centroids.histogram", "wb") as fp:
        pickle.dump(histogram, fp)
        fp.close()
    row.abs_error=absolute_error
    row.all_error=list(map(lambda x: x['error'], histogram))
    row.all_heights=list(map(lambda x: x['height'], histogram))

error_csv=path+"prediction_error/"+"centroid_error.csv"
if os.path.isfile(error_csv)==False:
        df[["prediction_dir","abs_error","all_error"]].to_csv(error_csv)
        print(error_csv+" created")
# Here one could plot the histograms
# Something like
# import seaborn as sns
# sns.boxplot()
# or also
# sns.violinplot(data=histogram, palette="muted", split=True, cut=0)
# and then saving it to a file? What's the command?

# Now we do the same, but with error_on_segments()

""" absolute_error = 0
counter = 0
histogram = []

for pair in pairs:

    if not os.path.exists(pair['bhm']):
        continue

    if not os.path.exists(pair['prediction']):
        continue

    print('Loading {} (BHM) and {} (prediction)'.format(pair['bhm'], pair['prediction']))

    error, mean, all_errors = error_on_segments(pair['bhm'], pair['prediction'])

    absolute_error += error * mean
    counter += 1
    histogram.extend(all_errors)

absolute_error /= counter

print('Absolute error (in meters) calculated over {} files, segment-by-segment: {}'.format(counter, absolute_error))

with open(str(df.prediction_dir[0])+"segments.histogram", "wb") as fp:
    pickle.dump(histogram, fp)
 """
# Also here, one could save the histogram!

# Finally, one can define maybe 3 or 4 classes of buildings, by height. And evaluate the errors (also with histograms), class by class.
