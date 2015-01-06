import sys
import json
import string
import operator 

def search_state(abbr):
    states = {
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
    for key,value in states.iteritems():
        if abbr == key:
            return key


def sent_dict(ssf):
    """
    #Creates a dictionary from the sentiment input file
    """
    scores = {}
    for line in ssf:
       term, score = line.split("\t")
       scores[term] = int(score)
    return scores

def split_tweet(text):
    tweet = text.encode('utf-8').rstrip('?:!.,;')
    split_tweet = tweet.split(" ")
    return split_tweet

def assign_sentiment(sf, tf):
    """
    Reads and parses twitter output. Finds tweet text and tries to find any sentiment words in it. Sorts tweets by state.
    """
    i = 0
    j = 0
    tweets = {}
    dictionary = sent_dict(sf)
    for line in tf:
       row = json.loads(line)

       if "text" in row and 'place' in row and type(row['place']) is dict:
          attributes = row['place']
          places = attributes['country']
          if places == 'United States':
              state_name = str(attributes['full_name'])[-2:]
              confirmed_name = search_state(state_name)   
              if confirmed_name !=  None:   
                  split_tweetm = split_tweet(row["text"]) 
                  for i in range(len(split_tweetm)):   
                      for key,value in dictionary.iteritems():
                          if key == split_tweetm[i]:
                              #print key
                              sent_score = float(value) 
                              tweets.setdefault(confirmed_name, []).append(sent_score)
    final_scores ={}

    for key, value in tweets.items():
        total_happiness = 0
        for i in range(len(value)):
            total_happiness += float(value[i])
            final_scores[key] = total_happiness

    sorted_scores = sorted(final_scores.iteritems(), key=operator.itemgetter(1))
    happiest = sorted_scores[0][0]
    print happiest

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #lines(sent_file)
    #lines(tweet_file)
    #hw()

    assign_sentiment(sent_file, tweet_file)



if __name__ == '__main__':
    main()
