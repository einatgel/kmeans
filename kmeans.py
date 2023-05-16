import sys
import math
import os

MAX_ITER = 1000
DEFAULT_ITER = 200
DEFAULT_EPSILON = 0.001

class Invalid_args(Exception):
    pass

class Kmean_group:
    def __init__(self, vector):
        self.rep = vector
        self.members = []

    def calculate_eclidean_dis_with_rep(self, x):
        return self.calculate_eclidean_dis(x, self.rep)
    
    def calculate_eclidean_dis(self, x, centroid):
        distance = 0
        for cor in range(len(centroid)):
            distance += math.pow((centroid[cor] - x[cor]), 2)
        return math.sqrt(distance)

    def add_member(self, vector):
        self.members.append(vector)

    def update_rep_and_check_accuracy(self):
        prev_rep = self.rep
        new_centroid = []
        for cor in range(len(self.rep)):
            sum_cor = 0
            for member in self.members:
                sum_cor += member[cor]
            if len(self.members) == 0:
                new_centroid.append(0)
            else:
                new_centroid.append(sum_cor/ len(self.members))
        self.rep = new_centroid
        return self.calculate_eclidean_dis(self.rep, prev_rep) < DEFAULT_EPSILON
    
    def clear_members_list(self):
        self.members = []
    
    def print_centroid(self):
        string = ""
        for cor in self.rep:
            string += "{:.4f}".format(cor) + ","
        string = string[:-1]
        print(string)

def parse_input():
    k = sys.argv[1]
    if len(sys.argv) == 3:
        file_name  = sys.argv[2]
        iter = DEFAULT_ITER
    else :
        iter = sys.argv[2]
        file_name = sys.argv[3]
        try: 
            iter = int(iter)
        except ValueError:
            raise Invalid_args("Invalid maximum iteration!")
        if iter < 1 or iter > MAX_ITER :
            raise Invalid_args("Invalid maximum iteration!")

    directory = os.getcwd()
    file_path = directory + "/" + file_name
    datapoints = []
    with open(file_path, 'r') as f: 
        datapoints = f.read().split("\n")[:-1]
        format_datapoints = []
        for datapoint in datapoints:
            vector = []
            for cor in datapoint.split(","):
                vector.append(float(cor))
            format_datapoints.append(vector)
        datapoints_amount = len(datapoints)
    try: 
        k = int(k)
    except ValueError:
        raise Invalid_args("Invalid number of clusters!")
    if k < 1 or k > datapoints_amount :
        raise Invalid_args("Invalid number of clusters!")
    
    return iter, k, format_datapoints

def initilize(k, datapoints):
    k_means = []
    for i in range(k):
        vector = datapoints[i]
        k_means.append(Kmean_group(vector))
    return k_means

def update_and_check_centroids_accuracy(k_means):
    to_continue_iter = False
    for i in k_means:
        if not i.update_rep_and_check_accuracy():
            to_continue_iter = True
        i.clear_members_list()
    return to_continue_iter

def calculate_kmeans(iter, k , datapoints):
    k_means = initilize(k, datapoints)
    current_iter = 0
    to_continue_iter = True

    while (current_iter < iter and to_continue_iter):
        for i in range(len(datapoints)):
            vector = datapoints[i]
            relevant_k_mean_group = False
            min_dis = False
            for j in range(k):
                temp_cal = k_means[j].calculate_eclidean_dis_with_rep(vector)
                if relevant_k_mean_group is False or temp_cal < min_dis:
                    min_dis = temp_cal
                    relevant_k_mean_group = k_means[j]
            relevant_k_mean_group.add_member(vector)
        to_continue_iter = update_and_check_centroids_accuracy(k_means)
        current_iter += 1
    return k_means

def print_k_centroid(k_means):
    for cluster in k_means:
        cluster.print_centroid()

def main():
    try:
        iter, k, datapoints = parse_input()
        k_means = calculate_kmeans(iter, k , datapoints)
        print_k_centroid(k_means)
    except Invalid_args:
        raise
    except: 
        raise RuntimeError("An Error Has Occurred")

if __name__ == "__main__":
    main()


    


        



