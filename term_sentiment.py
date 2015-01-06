import sys
import json
import string


def hw():
    print 'Hello, world!'

def sent_dict(ssf):
    """
    #Creates a dictionary from the sentiment input file
    """
    scores = {}
    for line in ssf:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

def assign_sentiment(sf, tf):
    """
    Reads and parses twitter output. Finds tweet text and tries to find any sentiment words in it.
    """     
    i = 0
    j = 0
    tweets = []
    for line in tf:
        row= json.loads(line)
        if "text" in row:
            tweets.append(row["text"])
            i+=1
        else:
            tweets.append("0")
            j+=1          
    #print "Number of tweets:", i, "Number of deleted/empty tweets:", j
    dictionary = sent_dict(sf)
    new_terms = {}
    for line in range(len(tweets)):
        tweet = tweets[line].encode('utf-8').rstrip('?:!.,;"')
        split_tweet = tweet.split()
        #print split_tweet
        sentiments = []
        sent_score = float(0.0)
        for i in range(len(split_tweet)):
            for key,value in dictionary.iteritems():
                if key == split_tweet[i]:
                    sentiments.append(key)
                    sent_score += float(value)
                    for i in range(len(split_tweet)):
                        if not split_tweet[i].startswith('#') and split_tweet[i] != key:                          
                            new_terms.setdefault(split_tweet[i], []).append(value)
    for key, value in new_terms.items():
        total_sent = 0
        for i in range(len(value)):
            total_sent += float(value[i])
        print key, total_sent



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    assign_sentiment(sent_file, tweet_file)

if __name__ == '__main__':
    main()
