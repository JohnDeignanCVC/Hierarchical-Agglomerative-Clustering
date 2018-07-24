# Hierarchical-Agglomerative-Clustering

The individual datasets of 500 datapoints used for testing, as well as the source code, can be downloaded from my NJIT personal webpage (https://web.njit.edu/~jtd32/). The datasets are small chunks of data which were taken from a much larger dataset that represents a 3D road network from Denmark and can be found by clicking ‘3D_spatial_network.txt’ at https://archive.ics.uci.edu/ml/machine-learning-databases/00246/.

The program can take a number of command line arguments which are used for execution:<br/>
```
<-i “[INPUT_FILE]”> or <--infile=”[INPUT_FILE]”>
	- The input file containing a 3-Dimensional dataset where each coordinate is separated by a comma
	- The path to the input file must be wrapped in double quotation marks (“)
	- Must be in (.txt) format
	 -Required for execution
<-p [0 < UNSIGNED _DECIMAL_NUMBER < 1]> or <--fraction=[0 < UNSIGNED_DECIMAL_NUMBER < 1]>
	- The fraction of datapoints which must lie outside a given distance to be considered an outlier
	- Optional 
	- Default: 0.25
<-d [UNSIGNED_INT > 0]> or <--distance=[UNSIGNED_INT > 0]>
	- The distance which is used to determine if a maximum number of datapoints lie far enough away to be considered an outlier
	- Optional
	- Default: The maximum euclidean distance is calculated (by finding the minimum and maximum possible axis values), then multiplied by 0.5
<-k [0 < UNSIGNED_INT < # OF DATAPOINTS IN S’] or <--num_clusters=[0 < UNSIGNED_INT < # OF DATAPOINTS IN S’]>
	- The number of clusters which will be generated
	- Optional
	- Default: ⌈√((# of datapoints)^2/((# of datapoints)×0.5))  ⌉
<-h> or <--help>
	- Shows the command line arguments available for execution
```

Examples:
```
On Windows:
  >> py HierarchicalAgglomerativeClustering.py -i “C:\path\to\DataSet1.txt” -k 28 -d 76000000 -p 0.3
  
On Linux/MacOS:
  >> python3 HierarchicalAgglomerativeClustering.py -i “/path/to/DataSet1.txt” -k 28 -d 76000000 -p 0.3

Other valid execution statements:
  >> (py|python3) HierarchicalAgglomerativeClustering.py -i “C:\path\to\DataSet2.txt” 

  >> (py|python3) HierarchicalAgglomerativeClustering.py -i “/path/to/DataSet3.txt” --num_clusters=18

  >> (py|python3) HierarchicalAgglomerativeClustering.py --infile=“C:\path\to\DataSet3.txt” -p 0.8 -k 9

  >> (py|python3) HierarchicalAgglomerativeClustering.py -i “C:\path\to\DataSet1.txt” --distance= 80000000

  >> (py|python3) HierarchicalAgglomerativeClustering.py --infile=“C:\path\to\DataSet2.txt” --distance=71000000 --fraction=0.77

  >> (py|python3) HierarchicalAgglomerativeClustering.py -i “/path/to/DataSet3.txt” -p 0.52

  >> (py|python3) HierarchicalAgglomerativeClustering.py -i “/path/to/DataSet2.txt” --num_clusters=133 -d 734817463
```

Help:
```
  >> (py|python3) HierarchicalAgglomerativeClustering.py -h
  
    HierarchicalAgglomerativeClustering.py -i <infile> -p <fraction> -d <distance> -k <num_clusters>
```
