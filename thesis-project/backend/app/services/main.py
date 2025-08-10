from SupaBaseConnector import SupaBaseConnector
from KNN import KNN
from flask import Flask, jsonify, request
from flask_cors import CORS


sample_answers = {"STEM:": 40, "HUMSS": 25, "ABM": 32}
tie_sample_answers = {"STEM:": 31, "HUMSS": 31, "ABM": 31}
dataset_list = []
strand_list = []

sql = SupaBaseConnector()
app = Flask(__name__)
CORS(app)

def run_algorithm(user_dataset):
    clear_table() #<-----REMOVE THIS IN THE FUTURE
    dataset_list = []
    strand_list = []
    dataset_values = []
    sql.select_initial_data()
    datasets = sql.fetch_data() #<-----Dictionaries within a list
    print(datasets)

    for i in range(len(datasets)): #<-----compile all dataset and classifier to list
        values = list(datasets[i].values())
        dataset_values = values[1:4]
        dataset_list.append(dataset_values)
        strand_list.append(values[-1])

    predict_dataset = list(user_dataset.values())
    predict_dataset = [predict_dataset]  # Convert to 2D array for prediction
    algorithm = KNN(predict_dataset, dataset_list, strand_list)
    results = algorithm.start_algorithm()
    print(results)
    return results

def clear_table(): #<-----REMOVE THIS IN THE FUTURE
    
    sql.wipe_data_of_table("neighbors")
    sql.wipe_data_of_table("tie_table")  
    sql.wipe_data_of_table("results")


def merge_strand_answers(answers): 
    strand_scores = {"STEM": 0, "HUMSS": 0, "ABM":0}
    for i in range(len(answers)):

    
        if i % 3 == 0:
            strand_scores["STEM"] += answers[i]
        elif i % 3 == 1:
            strand_scores["HUMSS"] += answers[i]
        else:
            strand_scores["ABM"] += answers[i]
    print(strand_scores)
    return strand_scores

reults_data = run_algorithm(sample_answers)
print("---------------------------------------------------------")
reults_data = run_algorithm(tie_sample_answers)

@app.route("/Assessment")
def get_questions():
    response = sql.select_questions()
    return jsonify(response)

@app.route('/submit', methods=['POST'])
def submit_answers():
    data = request.get_json()
    answers = data.get('answers', [])
    print(f"Test {answers}")
    user_dataset = merge_strand_answers(answers) 
    results_data = run_algorithm(user_dataset)

    results_table = results_data.copy()
    del results_table["neighbors"]
    del results_table["tie_strands"]
    results_response = sql.supabase_insert("results", results_table)
    print(f"Results: {results_table}")
    print(results_response)
    id = results_response["id"]
    print(type(id))

    for i in range(len(results_data["neighbors"])):

        neighbors_table = results_data["neighbors"][i]   
        neighbors_table["results_id"] = id
        print(f"Neighbors: {neighbors_table}")
        neighbors_response = sql.supabase_insert("neighbors", neighbors_table)
        print(neighbors_response)
    if results_data["tie_strands"]:
        tie_strands_table = results_data["tie_strands"]
        tie_strands_table["results_id"] = id
        print(f"Tie Strands: {tie_strands_table}")

        tie_response = sql.supabase_insert("tie_table", tie_strands_table)
        print(tie_response)
    print(f"Results Full: {results_data}")
    return jsonify(results_data)

@app.route("/statistics")
def get_neighbors():
    neighbors = sql.select_neighbors()
    
    # Fetch the latest result with scores
    results = sql.select_latest_results()  # You'll implement this
    if results:
        latest_result = results[0]  # Assuming results are sorted by latest first
        response = {
            "stem_score": latest_result["stem_score"],
            "humss_score": latest_result["humss_score"],
            "abm_score": latest_result["abm_score"],
            "neighbors": neighbors
        }
    else:
        response = {
            "stem_score": 0,
            "humss_score": 0,
            "abm_score": 0,
            "neighbors": neighbors
        }

    return jsonify(response)


if __name__ == '__main__':
    
    app.run(debug=True)