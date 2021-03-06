from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "RecommendedItems")

data = sc.textFile("/app/access4.log", 2)

lines = data.map(lambda line: line.split("\t"))
user_clicks = lines.groupByKey()
pairs = user_clicks.flatMap(lambda pair: ((pair[0], x) for x in itertools.combinations(sorted(set(pair[1])), 2)))

 # for pair, count in pairs.collect():
	#  print(str(pair) + " " + str(list(count)))

pair_users = pairs.distinct().groupBy(lambda pair: pair[1])

# for pair, count in pair_users.collect():
# 	print(str(pair) + " " + str(list(count)))

count = pair_users.map(lambda pair: (pair[0], len(pair[1])))
count = count.filter(lambda x: x[1] > 2)
output = count.collect()

f = open('/app/output4.log', 'w+')
if output:
	for pair, count in output:
		print(str(pair) + " " + str(count))
		f.write(str(pair) + "\t" + str(count) + "\n")
else:
	f.write("No co-views with at least 3 clicks.")
print ("Recommended items done")
f.close()

sc.stop()