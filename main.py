import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from movie_rating_object import MovieRatingObject
from scipy import spatial


class Similarity:
    matrix = None
    movie_rating = MovieRatingObject()

    def get_similarity(self):
        self.get_data()
        self.make_matrix()
        self.get_cosine()

    def get_data(self):
        with open('movie-ratings.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                self.movie_rating.users.append(int(row[0]))
                self.movie_rating.movies.append(int(row[1]))
                self.movie_rating.ratings.append(float(row[2]))

                line_count += 1
                if line_count > 10000:
                    break

    def make_matrix(self):
        self.matrix = np.zeros((self.movie_rating.get_amount_users(), self.movie_rating.get_max_movies()))
        for i in range(self.movie_rating.get_len_users()):
            self.matrix[self.movie_rating.users[i]][self.movie_rating.movies[i]] = self.movie_rating.ratings[i]
        np.set_printoptions(threshold=np.inf)

    def get_cosine(self):
        result_dict = {}
        # self.matrix = self.matrix.transpose()

        for i in range(0, 4):
            top_5 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            for j in range(0, len(self.matrix)):
                if i != j:
                    result = 1 - spatial.distance.cosine(self.matrix[i], self.matrix[j])
                    top_5.append([j, result])
                    top_5.sort(key=lambda x: x[1])
                    top_5 = top_5[1:]
            result_dict[i] = top_5
        print(result_dict)


if __name__ == '__main__':
    sim = Similarity()
    sim.get_similarity()
