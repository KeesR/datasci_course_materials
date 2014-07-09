import sys
import json

def print_ustring(unicode_string):
	encoded_string = unicode_string.encode('utf-8')
	print encoded_string
	
def add_to_histogram(str, histogram):
	words = str.lower().split()
	#print words
	for w in words:
		if w in histogram:
			histogram[w] += 1
		else:
			histogram[w] = 1
	return len(words)
	
def process_tweets(tweet_file, histogram):
	total = 0
	for line in tweet_file:
		tweet = json.loads(line)
		if 'entities' in tweet:
			if 'hashtags' in tweet['entities']:
				for h in tweet['entities']['hashtags']:
					encoded_string = h['text'].encode('utf-8')
					total += add_to_histogram(encoded_string, histogram)
	return total

def main():
	tweet_file = open(sys.argv[1])
	histogram = {}	# initialize an empty dictionary
	total = process_tweets(tweet_file, histogram)
	#print "Total", total
	for k in sorted(histogram, key=histogram.get, reverse=True)[0:10]:
		print k, histogram[k]

if __name__ == '__main__':
    main()
