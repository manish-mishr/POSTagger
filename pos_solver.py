###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
from collections import defaultdict


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#ot

											# tag_first keeps the count of 



class Solver:


    
    def __init__(self):
        self.tag_binary = defaultdict(float)
        self.tag_all = defaultdict(float)
        self.tag_all_words = defaultdict(dict)
        self.pos = ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']

	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
    def posterior(self, sentence, label):
		return 0
#
    # Do the training!
    #
    def train(self, data):
        tag_binary = self.tag_binary
        tag_all = self.tag_all
        tag_all_words = self.tag_all_words

        for mytuple in data:
            word_tuple = mytuple[0]
            tag_tuple = mytuple[1]
            tag_binary[('*',tag_tuple[0])] += 100.0
            length = len(tag_tuple)
            for i in range(length):
                tag_all[tag_tuple[i]] += 100
                if tag_tuple[i] not in tag_all_words[word_tuple[i]].keys():
                    for p in self.pos:
                        tag_all_words[word_tuple[i]][p] = 1.0
                tag_all_words[word_tuple[i]][tag_tuple[i]] += 100.0 

                if i < length-1:
                    tag_binary[(tag_tuple[i],tag_tuple[i+1])] += 100.0
                elif i == length-1:
                    tag_binary[(tag_tuple[i],'*')] += 100.0

        # print tag_all.keys()
        
        totalCount = 0
        for key in tag_all:
            totalCount += tag_all[key]
        for key in tag_binary:
            if key[0] == '*':
                pass
                # print key, tag_binary[key]   

    # Functions for each algorithm.
    def naive(self, sentence):
		return [ [ [ "noun" ] * len(sentence)], [] ]

    def mcmc(self, sentence, sample_count):
        tag_binary = self.tag_binary
        tag_all = self.tag_all
        tag_all_words = self.tag_all_words

        # print tag_all_words['can']
        ret = []
        #generate initial sample based on P(S|W)
        samp = {}
        count = 0
        for word in sentence:
            if len(tag_all_words[word]) == 0:
                tag_all_words[word] = tag_all
            samp[count] = self.max_pos(tag_all_words[word])
            count += 1


        burn_in = 10000
        #sample sample_count times + some burn in
        for i in range(burn_in + sample_count):
            # print samp
            new_samp = samp
            new_prob = defaultdict(list)

            #calculate probabilities of each part of speech
            count = 0
            for w in sentence:
                for p in self.pos:
                    #print p
                    #P(S_2 | S_1=noun) P(S3=noun | S2) P(W_2=dog | S2)
                    # print samp[count]
                    # print tag_all[p]
                    prob = (tag_binary[(samp[count-1] if count-1 >=0 else '*',p)]/tag_all[samp[count]]) * (tag_binary[(p,samp[count+1] if count+1 < len(sentence) else '*')]/tag_all[p]) * (tag_all_words[w][p]/tag_all[p])
                    new_prob[count].append((p,prob))
                count += 1

            # print new_prob
            # generate new sample based on these probabilities
            count = 0
            for w in new_prob:
                #total of small probabilities
                # print w
                pr_sum = 0
                for tu in new_prob[w]:
                    # print tu
                    pr_sum += tu[1]

                #normalize probabilities, should sum to 1
                new_dict = defaultdict(float)
                for tu in new_prob[w]:
                    new_dict[tu[0]] = tu[1]/pr_sum

                #sample from normalized probability space
                r = random.random()
                c_sum = 0 
                new_tag = ""
                done = False
                for nd in new_dict:
                    c_sum += new_dict[nd]
                    if r <= c_sum and not done:
                        new_tag = nd
                        done = True
                # print w, r, c_sum
                        
                new_samp[count] = new_tag
                count += 1

            #replace the existing sample
            samp = new_samp
            if i >= burn_in:
                samp_list = []
                for key in sorted(samp.keys()):
                    samp_list += [samp[key]]
                ret.append(samp_list)

                if i == burn_in + sample_count -1 :
                    print ret

        return [ret, []]

    def best(self, sentence):
		return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
		return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def viterbi(self, sentence):
		return [ [ [ "noun" ] * len(sentence)], [] ]

    # This solve() method is called by label.py, so you should keep the listerface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
		if algo == "Naive":
			return self.naive(sentence)
		elif algo == "Sampler":
			return self.mcmc(sentence, 5)
		elif algo == "Max marginal":
			return self.max_marginal(sentence)
		elif algo == "MAP":
			return self.viterbi(sentence)
		elif algo == "Best":
			return self.best(sentence)
		else:
			print "Unknown algo!"

    def max_pos(self, d):
        m = 0
        b = ""
        for p in d:
            if d[p] > m:
                m = max(m,d[p])
                b = p
        return b

