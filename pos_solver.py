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
tag_binary = defaultdict(float)
tag_all = defaultdict(float)
tag_all_words = defaultdict(dict)

			
def Learning(data):
	global tag_first,tag_all,tag_all_words
	for mytuple in data:
		word_tuple = mytuple[0]
		tag_tuple = mytuple[1]
		tag_binary[('*',tag_tuple[0])] += 1.0
		length = len(tag_tuple)
		for i in range(length):
			tag_all[tag_tuple[i]] += 1
			if tag_tuple[i] not in tag_all_words[word_tuple[i]].keys():
				tag_all_words[word_tuple[i]][tag_tuple[i]] = 1.0
			else:
				tag_all_words[word_tuple[i]][tag_tuple[i]] += 1.0 
			if i < length-1:
				tag_binary[(tag_tuple[i],tag_tuple[i+1])] += 1.0	
	for key in tag_all:
		print str(key) +" :  "+str(tag_all[key])
	
	totalCount = 0
	for key in tag_all:
		totalCount += tag_all[key]
	for key in tag_binary:
		if key[0] == '*':
			print tag_binary[key]	
	pass

class Solver:
	mydata = []
	prob_first = defaultdict(list)
	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def posterior(self, sentence, label):
		return 0

    # Do the training!
    #
	def train(self, data):
		Learning(data)
		
		pass

    # Functions for each algorithm.
    #
	def naive(self, sentence):
		return [ [ [ "noun" ] * len(sentence)], [] ]

	def mcmc(self, sentence, sample_count):
		return [ [ [ "noun" ] * len(sentence) ] * sample_count, [] ]

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

