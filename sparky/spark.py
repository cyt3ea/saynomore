from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/app/access3.log", 2)

pairs = data.map(lambda line: line.split("\t"))
count = pairs.groupByKey()

output = count.distinct().mapValues(list).collect()

all_pairs = []
f = open('/app/output.log', 'w+')
for co_view, item_list in output:
	items = list(set(item_list))
	combinations = list(itertools.combinations(items, 2))
	all_pairs = all_pairs + combinations

print(all_pairs)
rdd = sc.parallelize(all_pairs)
pairs = rdd.map(lambda pair: (pair, 1))
count = pairs.reduceByKey(lambda x,y: x+y)
count = count.filter(lambda x: x[1] > 2)
output = count.collect()

for pair, count in output:
	print(str(pair) + " " + str(count))
	f.write(str(pair) + "\t" + str(count) + "\n") 
print ("Popular items done")
f.close()

sc.stop()