from sklearn.cluster import KMeans as ImportedKMeans

from discretization.decorators import prop_vals_only
from discretization.unsupervised import Unsupervised


class KMeans(Unsupervised):

    @staticmethod
    @prop_vals_only
    def kmeans_adapter(prop_values, nb_bins, nb_jobs=1, *args, **kwargs):
        """
        :param: nb_jobs - number of parallel jobs for the calculation ('auto' for nb_bins)
        """
        if nb_jobs == 'auto':
            nb_jobs = nb_bins

        kmeans = ImportedKMeans(n_clusters=nb_bins, n_jobs=nb_jobs).fit(prop_values.values.reshape(-1, 1))  # TODO: check if dask has reshape

        centroids = sorted([b[0] for b in kmeans.cluster_centers_], reverse=False)
        cutpoints = [(c1 + c2) / 2 for c1, c2 in zip(centroids, centroids[1:])]
        return cutpoints

    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return KMeans.kmeans_adapter(prop_df, nb_bins, *args, **kwargs)
