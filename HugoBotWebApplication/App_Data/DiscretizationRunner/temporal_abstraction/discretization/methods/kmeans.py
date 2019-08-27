from sklearn.cluster import KMeans as ImportedKMeans

from temporal_abstraction.discretization.decorators import prop_vals_only
from temporal_abstraction.discretization.unsupervised import Unsupervised


class KMeans(Unsupervised):

    @staticmethod
    @prop_vals_only
    def kmeans_adapter(prop_values, nb_bins, nb_jobs=1):
        """
        :param: int, nb_jobs - number of parallel jobs for the calculation ('auto' for nb_bins)
        """
        if nb_jobs == 'auto':
            nb_jobs = nb_bins

        kmeans = ImportedKMeans(n_clusters=nb_bins, n_jobs=nb_jobs).fit(prop_values.values.reshape(-1, 1))

        centroids = sorted([b[0] for b in kmeans.cluster_centers_], reverse=False)

        # we set as cutpoints the average between each 2 centroids created by KMeans
        cutpoints = [(c1 + c2) / 2 for c1, c2 in zip(centroids, centroids[1:])]
        return cutpoints

    def _generate_cutpoints(self, prop_df):
        return KMeans.kmeans_adapter(prop_df, self._nb_bins)
