import sys
import json

def load_sentiments(sent_file):
	scores = {} # initialize an empty dictionary
	for line in sent_file:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		scores[term] = int(score)  # Convert the score to an integer.
	#print scores.items() # Print every (term, score) pair in the dictionary
	return scores
	
def print_ustring(unicode_string):
	encoded_string = unicode_string.encode('utf-8')
	print encoded_string
	
def cleanup_words(words):
	clean_words = []
	for w in words:
		#	remove hyperlinks
		if w[0:7] == "http://":	continue
		#	remove Twitter users
		if w[0] == '@': continue
		#	remove spurious hash tag
		if w[0] == '#': continue
		#	strip . comma colon semi colon question/exclamation mark from end of word
		w = w.rstrip('..,:;!?')
		#	rest is OK
		clean_words.append(w)
	return clean_words
		
def score_text(str, score_table, histogram):
	words = cleanup_words(str.lower().split())
	score = 0
	other_words = []
	for w in words:
		if w in score_table:
			score = score + score_table[w]
		else:
			other_words.append(w)
	#	now add score to every other_word in histogram
	for w in other_words:
		if w in histogram:
			histogram[w].append(score)
		else:
			histogram[w] = [score]
	
def process_tweets(tweet_file, score_table, histogram):
	for line in tweet_file:
		tweet = json.loads(line)
		if 'text' in tweet:
			#print_ustring(tweet['text']);
			encoded_string = tweet['text'].encode('utf-8')
			score_text(encoded_string, score_table, histogram)
			#print encoded_string, "\n", other_words
		#else:
			#print "+++ Ill-formed tweet?"
			#print tweet

def average(list):
	sum = 0
	for elem in list:
		sum += elem
	return sum*1.0/len(list)
	
def average_hist_lists(hist):
	for k in hist:
		hist[k] = average(hist[k])
		
def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	scores = load_sentiments(sent_file)
	histogram = {}	# initialize an empty dictionary
	process_tweets(tweet_file, scores, histogram)
	average_hist_lists(histogram)
	for k in sorted(histogram, key=histogram.get, reverse=True):
		print k, histogram[k]

if __name__ == '__main__':
	main()
