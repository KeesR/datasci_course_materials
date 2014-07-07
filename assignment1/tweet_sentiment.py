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
	
def score_text(str, score_table):
	words = str.lower().split()
	score = 0
	for w in words:
		if w in score_table:
			score = score + score_table[w]
	return score
	
def process_tweets(tweet_file, score_table):
	for line in tweet_file:
		tweet = json.loads(line)
		if 'text' in tweet:
			#print_ustring(tweet['text']);
			encoded_string = tweet['text'].encode('utf-8')
			score = score_text(encoded_string, score_table)
			print score
		#else:
			#print "+++ Ill-formed tweet?"
			#print tweet

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = load_sentiments(sent_file)
    process_tweets(tweet_file, scores)

if __name__ == '__main__':
    main()
