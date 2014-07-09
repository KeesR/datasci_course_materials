import sys
import json

state_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

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
	
def find_state_and_update(tweet, score, states):
	if 'user' in tweet:
		if 'location' in tweet['user']:
			loc = tweet['user']['location'].encode('utf-8')
			state_candidate = loc[-2:]
			if state_candidate in state_dict.keys():
				if len(loc) == 2 or (len(loc) > 2 and loc[-3] == ' '):
					#print "Candidate", loc, state_candidate
					if state_candidate in states:
						states[state_candidate].append(score)
					else:
						states[state_candidate] = [score]

def process_tweets(tweet_file, score_table, states):
	for line in tweet_file:
		tweet = json.loads(line)
		if 'text' in tweet:
			#print_ustring(tweet['text']);
			encoded_string = tweet['text'].encode('utf-8')
			score = score_text(encoded_string, score_table)
			#print score
			find_state_and_update(tweet, score, states)
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
	states = {}		# initialize an empty dictionary
	process_tweets(tweet_file, scores, states)
	average_hist_lists(states)
	for k in sorted(states, key=states.get, reverse=True)[0:1]:
		#print k, states[k]
		print k

if __name__ == '__main__':
    main()
