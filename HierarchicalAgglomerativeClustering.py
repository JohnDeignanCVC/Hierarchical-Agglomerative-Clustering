import random, math, sys, getopt

class Graph:
    def __init__(self):
        self.datapoints = []                    # datapoints in graph
        self.clusters = dict()                  # clusters of datapoints in graph
        self.avg_silhouette_coefficient = 0     # average silhouette coefficient of all datapoints in the graph
        
        # lambda function to check if two datapoints are the same        
        self.check_same_dp = lambda dp1, dp2: True if ((dp1.x == dp2.x) and (dp1.y == dp2.y) and (dp1.z == dp2.z)) else False
        # lambda function to calculate euclidean distance between two datapoints
        self.euc_distance = lambda dp1, dp2:  math.sqrt((abs(dp1.x-dp2.x)**2)+(abs(dp1.y-dp2.y)**2)+(abs(dp1.z-dp2.z)**2))
        # lambda function to check if clustering datapoints should continue
        self.cluster_continue = lambda k: True if len(set([dp.cluster for dp in self.datapoints])) > k else False

    def __str__(self):
        ret_string = (('-' * 65) +
                      '\n|' + '{:^15}'.format('CLUSTER') +
                      '|' + '{:^15}'.format('X') +
                      '|' + '{:^15}'.format('Y') +
                      '|' + '{:^15}'.format('Z') +
                      '|\n' + ('-' * 65) + '\n')
        ret_string += '\n'.join(('|' + '{:^15}'.format(str(dp.cluster)) +
                                 '|' + '{:^15}'.format(str(dp.x)) +
                                 '|' + '{:^15}'.format(str(dp.y)) +
                                 '|' + '{:^15}'.format(str(dp.z)) + '|') for dp in self.datapoints)
        ret_string += ('\n' + ('-' * 65))
        return ret_string

    def get_data(self, file):
        '''Gather DataPoints from specified .txt file

        Args:
            file (str): Path to file containing DataPoints
        '''
        with open(file) as f:
            data = f.readlines()
                        
        # initialize datapoints
        cluster = 1
        for line in data:
            line_split = line.strip().split(',')
            self.datapoints.append(DataPoint(float(line_split[0]), float(line_split[1]), float(line_split[2]), cluster))
            cluster += 1

    def remove_outliers(self, p, d):
        '''Remove outliers from Graph object

        Args:
            d (int/float): a euclidean distance used to identify neighbors of a DataPoint
            p (int): fraction of DataPoints that must lie outside of a distance (d) to be considered an outlier
        '''        
        min_inside_d = math.floor(len(self.datapoints)*p)       # minimum neighbor count
        max_outside_d = len(self.datapoints) - min_inside_d     # maximum points allowed outside of D

        # calculate amount of datapoints outside of a distance D for each datapoint
        no_outliers = True
        for dp1 in self.datapoints:
            for dp2 in self.datapoints:
                distance = self.euc_distance(dp1, dp2)
                dp1.neighbor_count += 1 if distance < d else 0
            num_outside_d = len(self.datapoints) - dp1.neighbor_count
            # if the amount of datapoints outside of a distance D exceeds the
            # maximum allowed amount, the datapoint is an outlier and is removed
            if num_outside_d > max_outside_d:
                no_outliers = False
                self.datapoints.remove(dp1)
                print('OUTLIER REMOVED: ' + str(dp1))
                
        # if no outliers were identified, state saying so
        if no_outliers:
            print('*'*50)
            print('{:^50}'.format('NO OUTLIERS FOUND'))
            print('*'*50)
            
        return self

    def merge_cluster(self, dp1, dp2):
        '''Merge two clusters
        
        Args:
                dp1 (DataPoint object): first datapoint involved in merge
                dp2 (DataPoint object): second datapoint involved in merge
        '''
        # do not merge unless the two points are in different clusters
        if not dp1.cluster == dp2.cluster:
            # gather all datapoints in dp1 cluster
            cluster1 = []
            [cluster1.append(dp) for dp in self.datapoints if dp.cluster == dp1.cluster]
            # gather all datapoints in dp2 cluster
            cluster2 = []
            [cluster2.append(dp) for dp in self.datapoints if dp.cluster == dp2.cluster]

            # merge dp2 cluster into dp1 cluster if dp1 contains more datapoints or the same amount
            if len(cluster1) >= len(cluster2):
                [dp.set_cluster(dp1.cluster) for dp in cluster2]
            # merge dp1 cluster into dp2 cluster if dp2 contains more datapoints
            elif len(cluster1) < len(cluster2):
                [dp.set_cluster(dp2.cluster) for dp in cluster1]

    def cluster(self, k):
        '''Assign cluster to each datapoint
        
        Args:
                k (int): number of clusters
        '''
        # calculate distance from datapoint to every other datapoint
        distances = dict()
        for dp1 in self.datapoints:
            for dp2 in self.datapoints:
                if not self.check_same_dp(dp1, dp2):
                    distance = self.euc_distance(dp1, dp2)
                    if distance not in distances:
                        distances[distance] = [[dp1, dp2]]
                    else:
                        distances[distance].append([dp1, dp2])
                
        # sort distances from shortest to longest and merge clusters
        # with shortest distance until cluster amount is satisfied
        continue_cluster = True
        for distance in sorted(distances):
            if continue_cluster:
                for pair in distances[distance]:
                    if self.cluster_continue(k):
                        self.merge_cluster(pair[0], pair[1])
                    else:
                        continue_cluster = False
                        break
            else:
                break

    def final_clusters(self):
        '''Assign final graph clusters'''
        [self.clusters.setdefault(dp.cluster, []).append(dp) for dp in self.datapoints]

    def reassign_clusters(self):
        '''For readability, reassign cluster values starting from 1'''
        new_clusters = dict()
        cluster_num = 1
        for cluster in self.clusters:
            new_clusters[cluster_num] = [dp for dp in self.clusters[cluster]]
            for dp in new_clusters[cluster_num]:
                dp.cluster = cluster_num
            cluster_num += 1
        self.clusters = new_clusters          
                
    def print_clusters(self):
        '''Print final cluster information'''
        for cluster in self.clusters:
            print('-'*25 + '{:^20}'.format(' CLUSTER: ' + str(cluster) + ' ') + '-'*25)
            [print(dp) for dp in self.clusters[cluster]]
            print('\n')

    def calc_silhouette_coefficient(self):
        '''Calculate silhouette coeffecient for each datapoint
        
        Notes:
            a = average distance from datapoint to all other datapoints in it's cluster
            b = min(average distance from datapoint to all other datapoints in another cluster)
            silhouette-coefficient = (b1 - a1)/max(a1, b1)
        '''
        for dp1 in self.datapoints:
            # calculate distance from datapoints to all other datapoints in it's cluster
            a = (sum(self.euc_distance(dp1, dp2) for dp2 in self.clusters[dp1.cluster] if not self.check_same_dp(dp1, dp2)))/len(self.clusters[dp1.cluster])
            
            # calculate distance from datapoint to all other datapoints in each other cluster
            dist_to_cluster = []
            for cluster, dp_set in self.clusters.items():
                if dp1.cluster != cluster:
                    tot_distance = sum(self.euc_distance(dp1, dp2) for dp2 in dp_set)
                    dist_to_cluster.append(tot_distance/len(dp_set))
            b = min(dist_to_cluster)
                        
            # calculate silhouette coefficient based on a1 and b1 values
            dp1.silhouette_coefficient = (b - a)/max([a, b])

    def calc_avg_silhouette_coefficient(self):
        '''Calculate average silhouette coeffecient of all datapoints'''
        self.avg_silhouette_coefficient = sum(dp.silhouette_coefficient for dp in self.datapoints)/len(self.datapoints)
            
class DataPoint:
    def __init__(self, x, y, z, cluster):
        self.x = x                          # x coordinate
        self.y = y                          # y coordinate
        self.z = z                          # z coordinate
        self.neighbor_count = 0             # neighbor count (applied when identifying outliers)
        self.cluster = cluster              # assigned cluster
        self.silhouette_coefficient = 0     # calculated silhouette coeffecient 
        

    def __str__(self):
        return ("[Cluster " + str(self.cluster) + "] (" + str(self.x) + ", " + str(self.y) + ", " +
                str(self.z) + ")")

    def set_cluster(self, cluster):
        '''Setter method for datapoint cluster'''
        self.cluster = cluster

def main(argv):
    inputfile = ''		# datapoints file (.txt)
    fraction_p = 0		# fraction (p) used to identify outliers
    distance_d = 0		# distance (D) used to identify outliers
    num_clusters_k = 0		# number of clusters (k) to generate

    # specify possible command line arguments
    try:
        options, args = getopt.getopt(argv, 'hi:p:d:k:', ['help=','infile=','fraction=', 'distance=','num_clusters='])
    except getopt.GetoptError:
        print('HierarchicalAgglomerativeClustering.py -i <--infile=> -p <--fraction=> -d <--distance=> -k <--num_clusters=>')
        sys.exit(2)

    # get command line arguemtns
    for opt, arg in options:
        if opt in ['-h', '--help']:
            print('HierarchicalAgglomerativeClustering.py -i <infile> -p <fraction> -d <distance> -k <num_clusters>')
            sys.exit()
        elif opt in ['-i', '--infile']:
            inputfile = str(arg)
        elif opt in ['-p', '--fraction']:
            fraction_p = float(arg)
        elif opt in ['-d', '--distance']:
            distance_d = int(arg)
        elif opt in ['-k', '--num_clusters']:
            num_clusters_k = int(arg)
    
    # input file is required, raise exception if no input file specified
    if not inputfile:
        raise Exception('ERROR: Input file (.txt) must be specified as command-line argument')
        sys.exit(2)

    # input file must be in .txt format, raise exception if input file has incorrect format
    if '.txt' not in inputfile[(len(inputfile)-4):len(inputfile)]:        
        raise Exception('ERROR: Input file must be of (.txt) format')
        sys.exit(2)

    if fraction_p:
        if fraction_p <= 0 or fraction_p >= 1:
            raise Exception('ERROR: Fraction (-p or --fraction) must be a decimal value between 0 and 1')
            sys.exit(2)
    else:
        fraction_p = 0.25       # arbitrary choice for p if p is not specified as command-line argument

    if distance_d:
        if distance_d <= 0:
            raise Exception('ERROR: Distance (-d or --distance) must be an integer greater than 0')
            sys.exit(2)

    if num_clusters_k:
        if num_clusters_k <= 0:
            raise Exception('ERROR: Number of clusters (-k or --num_clusters) must greater than 0')
            sys.exit(2)
            
    s = Graph()                 # initialize graph S
    s.get_data(inputfile)       # gather datapoints from specified file
    print(str(s) + '\n')        # display graph S

    if not distance_d:
        # gather maximum and minimum possible datapoints
        max_x = max_y = max_z = 0
        min_x = min_y = min_z = sys.maxsize
        for dp in s.datapoints:
            max_x = dp.x if dp.x > max_x else max_x
            max_y = dp.y if dp.y > max_y else max_y
            max_z = dp.z if dp.z > max_z else max_z
            min_x = dp.x if dp.x < min_x else min_x
            min_y = dp.y if dp.y < min_y else min_y
            min_z = dp.z if dp.z < min_z else min_z

        dp_max = DataPoint(max_x, max_y, max_z, None)   # farthest possible point in graph
        dp_min = DataPoint(min_x, min_y, min_z, None)   # nearest possible point in graph

        print(s.euc_distance(dp_max, dp_min)*.6)
        # arbitrary distance D based on maximum possible euclidean distance if D is not specified as a command line argument
        distance_d = (s.euc_distance(dp_max, dp_min)*.5)

    s_prime = s.remove_outliers(fraction_p, distance_d) # remove outliers from S to generate S'

    if num_clusters_k:
        if num_clusters_k >= len(s_prime.datapoints):
            raise Exception('ERROR: Number of clusters (-k or --num_clusters) must less than the number of datapoints left on the graph after attempting to remove outliers')
            sys.exit(2)
    else:
        num_clusters_k = math.ceil(math.sqrt((len(s_prime.datapoints)**2)/(len(s_prime.datapoints)*.5)))
        
    s_prime.cluster(num_clusters_k)                     # cluster S' datapoints into k clusters
    s_prime.final_clusters()                            # group final clusters in graph S'
    s_prime.reassign_clusters()                         # reassign cluster numbers for readability

    print('\n')
    s.print_clusters()                                  # display clusters
    s.calc_silhouette_coefficient()                     # calculate silhouette coeffecient of each datapoint in S'
    s.calc_avg_silhouette_coefficient()                 # calculate average silhouette coeffecient of all datapoints in S'

    # display average silhouette coeffecient of all datapoints in S'
    print('AVERAGE SILHOUETTE COEFFECIENT: ' + str(s.avg_silhouette_coefficient))

if __name__ == '__main__':
    main(sys.argv[1:])
