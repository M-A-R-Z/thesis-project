from SupaBaseConnector import SupaBaseConnector
from KNN_scratch import KNN_scratch



sample_answers = [[40, 24, 30], [39, 14, 19],[27, 32, 45],[11, 28, 17],[33, 49, 12],[24, 26, 48],[13, 30, 44],[38, 22, 41],[47, 18, 23],[21, 12, 46]]
dataset_list = []
strand_list = []
dataset_values = []
sql = SupaBaseConnector()


sql.select_initial_data()
datasets = sql.fetch_data() #<-----Dictionaries within a list


for i in range(len(datasets)): #<-----compile all dataset and classifier to list
    values = list(datasets[i].values())
    dataset_values = values[1:4]
    dataset_list.append(dataset_values)
    strand_list.append(values[-1])


algorithm = KNN_scratch(sample_answers, dataset_list, strand_list)
algorithm.predict()