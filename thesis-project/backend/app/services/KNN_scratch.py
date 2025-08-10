from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier


class KNN_scratch:
    def __init__(self, sample_answers, dataset_list, strand_list):
        self.sample_answers = sample_answers
        self.dataset_list = dataset_list
        self.strand_list = strand_list

    def predict(self):
        strand = []
        knn = KNeighborsClassifier(n_neighbors=10)
        knn.fit(self.dataset_list, self.strand_list)
        self.calculate_distance(knn)
        
        recommendation = knn.predict(self.sample_answers)
        print(recommendation)
        strand.append(recommendation[0])

    def calculate_distance(self, knn):
        distances, indices = knn.kneighbors(self.sample_answers)
        print(distances)
        print(indices)


