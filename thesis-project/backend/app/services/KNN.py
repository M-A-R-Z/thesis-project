from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier




class KNN:
    def __init__(self, sample_answers, dataset_list, strand_list):
        self.sample_answers = sample_answers
        self.dataset_list = dataset_list
        self.strand_list = strand_list

    def start_algorithm(self):
       
        knn = KNeighborsClassifier(n_neighbors= self.calculate_k())
        knn.fit(self.dataset_list, self.strand_list)
        results = self.predict(knn)
        return results
         

        
        

    def calculate_k(self):
        model = KNeighborsClassifier()
        param_grid = {'n_neighbors': [x for x in range(5, 11)]}
        param_grid = {'n_neighbors': [x for x in range(5, 11)]}
        grid_search = GridSearchCV(model, param_grid, cv=5)
        grid_search.fit(self.dataset_list, self.strand_list)
        k = grid_search.best_params_['n_neighbors']
        print(f"K is {k}")
        print("Best Accuracy:", grid_search.best_score_)
        return k


    def calculate_distance(self, knn):
        distances, indices = knn.kneighbors(self.sample_answers)
        print(distances)
        print(indices)
        return indices[0], distances[0]
         
    
    def predict(self, knn):
        indices, distances = self.calculate_distance(knn)
        nearest_neighbors = []
        k = len(indices)
        for i in range(k):            
            nearest_neighbors.append(self.strand_list[indices[i]])
        print(f"Nearest Neighbors: {nearest_neighbors}")
        total_stem = nearest_neighbors.count("STEM")
        total_humss = nearest_neighbors.count("HUMSS")
        total_abm = nearest_neighbors.count("ABM")
        strand_votes = {"stem_score": total_stem, "humss_score": total_humss, "abm_score": total_abm}
        vote_score = [total_stem, total_humss, total_abm]
        print(f"Votes: {strand_votes}")
        if vote_score.count(max(vote_score)) > 1:
            strand_votes["tie"] = True
            strand_votes["tie_strands"] = {}
            recommendation = self.tie_breaker(strand_votes, nearest_neighbors, distances, max(vote_score))
            
            
        else:
            strand_votes["tie"] = False           
            strand_votes["tie_strands"] = None
            recommendation = max(["stem_score", "humss_score", "abm_score"], key=strand_votes.get)
            
            print(f"Recommendation: {recommendation}")

        fixed_recommendation = self.fix_recommendation(recommendation)
        print(f"Recommendation: {fixed_recommendation}")
        strand_votes["recommendation"] = fixed_recommendation  
        strand_votes["neighbors"] = []
        strand_votes["k"] = k
        for i in range(k):
            strand_votes["neighbors"].append({})
            strand_votes["neighbors"][i]["neighbor_index"] = int(indices[i] + 1)
            strand_votes["neighbors"][i]["strand"] = nearest_neighbors[i]
            strand_votes["neighbors"][i]["distance"] = float(distances[i])
        

        return strand_votes


    def tie_breaker(self, strand_votes, nearest_neighbors, distances, tie_score):
        tied_strands = {}
        
        # Initialize weights for tied strands
        for key in strand_votes:
            if strand_votes[key] == tie_score:
                if key == "stem_score":
                    tied_strands["stem_weight"] = 0
                elif key == "humss_score":
                    tied_strands["humss_weight"] = 0
                elif key == "abm_score":
                    tied_strands["abm_weight"] = 0

        print(f"Tie between: {tied_strands}")

        # Calculate weighted distances for tied strands
        for i in range(len(nearest_neighbors)):
            convert_to_weighted = float(1 / distances[i])
            
            if nearest_neighbors[i] == "STEM" and "stem_weight" in tied_strands:
                tied_strands["stem_weight"] += convert_to_weighted
            elif nearest_neighbors[i] == "HUMSS" and "humss_weight" in tied_strands:
                tied_strands["humss_weight"] += convert_to_weighted
            elif nearest_neighbors[i] == "ABM" and "abm_weight" in tied_strands:
                tied_strands["abm_weight"] += convert_to_weighted

        # Determine the final recommendation based on weighted distances
        recommendation = max(tied_strands, key=tied_strands.get)
        if recommendation == "stem_weight":
            recommendation = "stem_score"
        elif recommendation == "humss_weight": 
            recommendation = "humss_score"
        elif recommendation == "abm_weight":
            recommendation = "abm_score"
        print(f"Final Recommendation: {recommendation}")
        
        strand_votes["tie"] = True
        strand_votes["tie_strands"] = tied_strands
        return recommendation
    
    def fix_recommendation(self, recommendation):
        if recommendation == "stem_weight" or recommendation == "stem_score":
            return "STEM"
        elif recommendation == "hummss_weight" or recommendation == "humss_score":
            return "HUMSS"
        elif recommendation == "abm_weight" or recommendation == "abm_score":
            return "ABM"
  
  



        
        
