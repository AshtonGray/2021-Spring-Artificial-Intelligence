import csv
import random
import math

def read_data(csv_path):
    """Read in the training data from a csv file.

    The examples are returned as a list of Python dictionaries, with column names as keys.
    """
    examples = []
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for example in csv_reader:
            for k, v in example.items():
                if v == '':
                    example[k] = None
                else:
                    try:
                        example[k] = float(v)
                    except ValueError:
                        example[k] = v
            examples.append(example)
    return examples


def train_test_split(examples, test_perc):
    """Randomly data set (a list of examples) into a training and test set."""
    test_size = round(test_perc * len(examples))
    shuffled = random.sample(examples, len(examples))
    return shuffled[test_size:], shuffled[:test_size]


class TreeNodeInterface():
    """Simple "interface" to ensure both types of tree nodes must have a classify() method."""

    def classify(self, example):
        pass


class DecisionNode(TreeNodeInterface):
    """Class representing an internal node of a decision tree."""

    def __init__(self, test_attr_name, test_attr_threshold, child_lt, child_ge, child_miss):
        """Constructor for the decision node.  Assumes attribute values are continuous.

        Args:
            test_attr_name: column name of the attribute being used to split data
            test_attr_threshold: value used for splitting
            child_lt: DecisionNode or LeafNode representing examples with test_attr_name
                values that are less than test_attr_threshold
            child_ge: DecisionNode or LeafNode representing examples with test_attr_name
                values that are greater than or equal to test_attr_threshold
            child_miss: DecisionNode or LeafNode representing examples that are missing a
                value for test_attr_name
        """
        self.test_attr_name = test_attr_name
        self.test_attr_threshold = test_attr_threshold
        self.child_ge = child_ge
        self.child_lt = child_lt
        self.child_miss = child_miss

    def classify(self, example):
        """Classify an example based on its test attribute value.

        Args:
            example: a dictionary { attr name -> value } representing a data instance

        Returns: a class label and probability as tuple
        """
        test_val = example[self.test_attr_name]
        if test_val is None:
            return self.child_miss.classify(example)
        elif test_val < self.test_attr_threshold:
            return self.child_lt.classify(example)
        else:
            return self.child_ge.classify(example)

    def __str__(self):
        return "test: {} < {:.4f}".format(self.test_attr_name, self.test_attr_threshold)


class LeafNode(TreeNodeInterface):
    """Class representing a leaf node of a decision tree.  Holds the predicted class."""

    def __init__(self, pred_class, pred_class_count, total_count):
        """Constructor for the leaf node.

        Args:
            pred_class: class label for the majority class that this leaf represents
            pred_class_count: number of training instances represented by this leaf node
            total_count: the total number of training instances used to build the leaf node
        """
        self.pred_class = pred_class
        self.pred_class_count = pred_class_count
        self.total_count = total_count
        self.prob = pred_class_count / total_count  # probability of having the class label

    def classify(self, example):
        """Classify an example.

        Args:
            example: a dictionary { attr name -> value } representing a data instance

        Returns: a class label and probability as tuple as stored in this leaf node.  This will be
            the same for all examples!
        """
        return self.pred_class, self.prob

    def __str__(self):
        return "leaf {} {}/{}={:.2f}".format(self.pred_class, self.pred_class_count,
                                             self.total_count, self.prob)


class DecisionTree:
    """Class representing a decision tree model."""

    def __init__(self, examples, id_name, class_name, min_leaf_count=1):
        """Constructor for the decision tree model.  Calls learn_tree().

        Args:
            examples: training data to use for tree learning, as a list of dictionaries
            id_name: the name of an identifier attribute (ignored by learn_tree() function)
            class_name: the name of the class label attribute (assumed categorical)
            min_leaf_count: the minimum number of training examples represented at a leaf node
        """
        self.id_name = id_name
        self.class_name = class_name
        self.min_leaf_count = min_leaf_count

        # build the tree!
        self.root = self.learn_tree(examples)

    def learn_tree(self, examples):
        """Build the decision tree based on entropy and information gain.

        Args:
            examples: training data to use for tree learning, as a list of dictionaries.  The
                attribute stored in self.id_name is ignored, and self.class_name is consided
                the class label.

        Returns: a DecisionNode or LeafNode representing the tree
        """
        #print(examples)

        case = self.check_base_case(examples)
        if case is not None:
            return case
        else:
            # get list of attributes
            attribute_list = []
            for attribute in examples[0]:
                if attribute != 'town' and attribute != '2020_label':
                    attribute_list.append(attribute)

            optimal_split = [None, 0, 0, []]  # attribute, cutoff, infogain, [less, greater]

            # find the best attribute for cutoff
            for attribute in attribute_list:
                attribute_cutoff_values = self.get_cutoffs(examples, attribute)  # get values for attributes

                for cutoff_value in attribute_cutoff_values:
                    if cutoff_value is None:
                        continue
                    groups = self.make_groups(examples, attribute, cutoff_value)
                    if len(groups['less']) < self.min_leaf_count or len(groups['greater']) < self.min_leaf_count:
                        continue
                    infogain = self.get_infoGain(groups, examples)
                    if infogain > optimal_split[2]:  # if new infogain is bigger than prev biggest
                        optimal_split = [attribute, cutoff_value, infogain, groups]
            if optimal_split[0] is None:  # if no split possible...
                labels = []
                for i in examples:
                    labels.append(i[self.class_name])
                predictedColor = max(labels, key=labels.count)
                return LeafNode(predictedColor, labels.count(predictedColor), len(examples))
            nodes = []
            for child in optimal_split[3]:
                nodes.append(self.learn_tree(optimal_split[3][child]))

            if len(optimal_split[3]['less']) < len(optimal_split[3]['greater']):
                decisionNode = DecisionNode(optimal_split[0], optimal_split[1], nodes[0], nodes[1], nodes[1])
            else:
                decisionNode = DecisionNode(optimal_split[0], optimal_split[1], nodes[0], nodes[1], nodes[0])

            return decisionNode

    def classify(self, example):
        """Perform inference on a single example.

        Args:
            example: the instance being classified

        Returns: a tuple containing a class label and a probability
        """
        #
        # fill in the function body here!
        #
        return self.root.classify(example)

    def check_base_case(self, examples):

        colors_list = []
        for i in examples:
            colors_list.append(i[self.class_name])

        if len(examples) == self.min_leaf_count:
            labels = []
            for i in examples:
                labels.append(i[self.class_name])
            predictedColor = max(labels, key=labels.count)
            return LeafNode(predictedColor, labels.count(predictedColor), len(examples))

        elif colors_list.count(examples[0][self.class_name]) == len(colors_list):
            return LeafNode(examples[0][self.class_name], len(examples), len(examples))

        return None

    def make_groups(self, examples, attribute, cutoffVal):

        groups = {'less': [], 'greater': []}

        for townInfo in examples:
            if townInfo[attribute] is None:
                continue
            elif townInfo[attribute] < cutoffVal:
                groups['less'].append(townInfo)
            elif townInfo[attribute] >= cutoffVal:
                groups['greater'].append(townInfo)

        return groups


    def get_Entropy(self, examples):
        # dictionary containing list of towns & info based on color
        town_voting = {'red': [], 'light blue': [],
                       'medium blue': [], 'wicked blue': []}

        # ----- get the entropy of examples -----
        # sort towns by color
        for town in examples:
            for color in town_voting:
                if town['2020_label'] == color:
                    town_voting[color].append(town)

        # decision frequencies
        redPercent = len(town_voting['red']) / len(examples)
        light_bluePercent = len(town_voting['light blue']) / len(examples)
        medium_bluePercent = len(town_voting['medium blue']) / len(examples)
        wicked_bluePercent = len(town_voting['wicked blue']) / len(examples)

        # calculate entropy (should be close to 1)
        try:
            entropy = -(redPercent * math.log(redPercent, 2)) \
                          - (light_bluePercent * math.log(light_bluePercent, 2)) \
                          - (medium_bluePercent * math.log(medium_bluePercent, 2)) \
                          - (wicked_bluePercent * math.log(wicked_bluePercent, 2))
        except:
            entropy = 1

        return entropy

    def get_infoGain(self, groups, examples):
        rootEntropy = self.get_Entropy(examples)

        # ----- get entropy of groups -----

        # group frequencies
        lessThanPercent = len(groups['less']) / len(examples)
        greaterThanPercent = len(groups['greater']) / len(examples)

        lessEntropy = self.get_Entropy(groups['less'])
        greaterEntropy = self.get_Entropy(groups['greater'])

        # childEntropy = lessThanPercent * E(less) + greaterThanPercent * E(Less) + nonePercent * E(none)
        childEntropy = lessThanPercent * lessEntropy + greaterThanPercent * greaterEntropy

        # ----- calculate info gain -----
        infoGain = rootEntropy - childEntropy

        return infoGain

    def get_cutoffs(self, examples, attribute):
        values = []
        for i in examples:
            values.append(i[attribute])
        return values  # return all values for a specific attribute

    def __str__(self):
        """String representation of tree, calls _ascii_tree()."""
        ln_bef, ln, ln_aft = self._ascii_tree(self.root)
        return "\n".join(ln_bef + [ln] + ln_aft)

    def _ascii_tree(self, node):
        """Super high-tech tree-printing ascii-art madness."""
        indent = 7  # adjust this to decrease or increase width of output
        if type(node) == LeafNode:
            return [""], "leaf {} {}/{}={:.2f}".format(node.pred_class, node.pred_class_count, node.total_count,
                                                       node.prob), [""]
        else:
            child_ln_bef, child_ln, child_ln_aft = self._ascii_tree(node.child_ge)
            lines_before = [" " * indent * 2 + " " + " " * indent + line for line in child_ln_bef]
            lines_before.append(" " * indent * 2 + u'\u250c' + " >={}----".format(node.test_attr_threshold) + child_ln)
            lines_before.extend([" " * indent * 2 + "|" + " " * indent + line for line in child_ln_aft])

            line_mid = node.test_attr_name

            child_ln_bef, child_ln, child_ln_aft = self._ascii_tree(node.child_lt)
            lines_after = [" " * indent * 2 + "|" + " " * indent + line for line in child_ln_bef]
            lines_after.append(" " * indent * 2 + u'\u2514' + "- <{}----".format(node.test_attr_threshold) + child_ln)
            lines_after.extend([" " * indent * 2 + " " + " " * indent + line for line in child_ln_aft])

            return lines_before, line_mid, lines_after


def confusion4x4(labels, vals):
    """Create an normalized predicted vs. actual confusion matrix for four classes."""
    n = sum([v for v in vals.values()])
    abbr = ["".join(w[0] for w in lab.split()) for lab in labels]
    s = ""
    s += " actual ___________________________________  \n"
    for ab, labp in zip(abbr, labels):
        row = [vals.get((labp, laba), 0) / n for laba in labels]
        s += "       |        |        |        |        | \n"
        s += "  {:^4s} | {:5.2f}  | {:5.2f}  | {:5.2f}  | {:5.2f}  | \n".format(ab, *row)
        s += "       |________|________|________|________| \n"
    s += "          {:^4s}     {:^4s}     {:^4s}     {:^4s} \n".format(*abbr)
    s += "                     predicted \n"
    return s


#############################################

if __name__ == '__main__':

    path_to_csv = 'town_data.csv'
    class_attr_name = '2020_label'
    id_attr_name = 'town'
    min_examples = 10  # minimum number of examples for a leaf node

    # read in the data
    examples = read_data(path_to_csv)
    train_examples, test_examples = train_test_split(examples, 0.25)

    # learn a tree from the training set
    tree = DecisionTree(train_examples, id_attr_name, class_attr_name, min_examples)

    # test the tree on the test set and see how we did
    correct = 0
    almost = 0  # within one level of correct answer
    ordering = ['red', 'light blue', 'medium blue', 'wicked blue']  # used to count "almost" right
    test_act_pred = {}
    for example in test_examples:
        actual = example[class_attr_name]
        pred, prob = tree.classify(example)
        print("{:30} pred {:15} ({:.2f}), actual {:15} {}".format(example[id_attr_name] + ':',
                                                                  "'" + pred + "'", prob,
                                                                  "'" + actual + "'",
                                                                  '*' if pred == actual else ''))
        if pred == actual:
            correct += 1
        if abs(ordering.index(pred) - ordering.index(actual)) < 2:
            almost += 1
        test_act_pred[(actual, pred)] = test_act_pred.get((actual, pred), 0) + 1

    print("\naccuracy: {:.2f}".format(correct / len(test_examples)))
    print("almost:   {:.2f}\n".format(almost / len(test_examples)))
    print(confusion4x4(['red', 'light blue', 'medium blue', 'wicked blue'], test_act_pred))
    print(tree)  # visualize the tree in sweet, 8-bit text



