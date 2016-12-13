from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/app/access2.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
key_value = pairs.groupByKey()
# key_value = key_value.values().distinct()
# key_value = key_value.distinct()
# pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = key_value.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

output = count.distinct().mapValues(list).collect()                          # bring the data back to the master node so we can print it out

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
    # print (co_view + " " + str(count))
    # f.write("co_view %s count %d\n" % (co_view, count))  
print ("Popular items done")
f.close()

sc.stop()