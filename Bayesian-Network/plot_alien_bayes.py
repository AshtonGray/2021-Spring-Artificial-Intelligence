from matplotlib import pyplot as plt
import alien_bayes
import numpy as np

def two_line_plot(xvals1, yvals1, label1, xvals2, yvals2, label2, title, outfile_path):
    plt.plot(xvals1, yvals1, label=label1, color='blue', marker='.', linestyle='solid')
    plt.plot(xvals2, yvals2, label=label2, color='green', marker='.', linestyle='solid')
    plt.title(title)
    plt.legend()
    plt.savefig(outfile_path)

nodes = alien_bayes.ALIEN_NODES

# 
# Fill in this script to empirically calculate P(A=true | M=true, B=true) using the rejection
# sampling and likelihood weighting code found in alien_bayes.py.
#
# Use the two_line_plot() function above to generate a line graph with one line for each 
# approximation technique.  The x-axis should represent different n, the number of samples 
# generated, with the probability estimate for the conditional probability above on the y-axis.  
# 
# You should generate estimates using at least 100 different values of n, and increase it to 
# the point that the estimates appear to stabilize.  Note that for rejectins sampling, n should
# represent the number of simple samples created, not the number retained after rejecting those
# that do not agree with the evidence.  
# 
# Your script should produce a plot named "alien_bayes.pdf". 
#  

if __name__ == '__main__':

    n = np.linspace(100, 10000, 250)


    sampler_reject = alien_bayes.RejectionSampler(nodes)  # samples for reject
    sampler_like = alien_bayes.LikelihoodWeightingSampler(nodes)  # samples for likelihood

    sampler_reject_coords = []
    sampler_like_coords = []

    query = {'A': True}
    evidence = {'M': True, 'B': True}

    for i in n:
        sampler_reject_coords.append(sampler_reject.get_prob(query, evidence, int(i)))
        sampler_like_coords.append(sampler_like.get_prob(query, evidence, int(i)))

    two_line_plot(n, sampler_reject_coords, 'Rejection Sampling', n, sampler_like_coords,
                  'Likelihood Sampling', 'Difference between Rejection and Likelihood Sampling \n over different Sample Sizes',
                  'alien_bayes.pdf')


