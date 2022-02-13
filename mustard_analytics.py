# COMPSCI 383 Homework 0 
#  Ashton Gray
# 32000589
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


import sys
import csv
import datetime


# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: datetime.date
      mileage: integer
      location: string
      gallons: float
      price: float (you'll need to get rid of the '$')

    Do not return a tuple for the header row.  And for the love of all that's holy, do not use
    primitive string functions for parsing (use the csv modules instead).

    Hint: to parse the date field, use the strptime function in the datetime module, and then
    use datetime.date() to create a date object.

    See: 
      https://docs.python.org/3/library/csv.html
      https://docs.python.org/3/library/datetime.html

    """
    rows = []  # this list should contain one tuple per row


    with open('mustard_data.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader, None)  # skip first line
        for line in reader:
            rows.append(((datetime.datetime.strptime(line[0], "%m/%d/%Y").date(), # put in date, 0
                          int(line[1]), # mileage, 1
                          str(line[2]), # location, 2
                          float(line[3]), # gallons, 3
                          float(line[4].replace('$', ''))))) # price, remove the $, 4


    return rows  # a list of (date, mileage, location, gallons, price) tuples


# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.
    
    Hint: calculate by multiplying the price per gallon with the  number of gallons for each row.
    """
    #
    # fill in function body here
    #
    sum = 0.0
    for tuple in rows:
        sum = sum + tuple[3] * tuple[4] # gallons * price

    return float(sum)  # fix this line to return a float


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once.
    
    Hint: store the locations and counts (as keys and values, respectively) in a dictionary, 
    then count up the number of entries with a value equal to one.  
    """

    #
    # fill in function body here
    #
    dict = {}
    totalcount = 0;

    # add to dictionary
    for tuple in rows:
        if tuple[2] not in dict.keys(): #check if location in keys
            dict[tuple[2]] = 1 # add it
        else:
            dict[tuple[2]] += 1 # increment counter by 1

    # deck how many have a value of 1
    for value in dict.values():
        if value == 1:
            totalcount += 1

    return int(totalcount)  # fix this line to return an int


# Exercise 3. (7 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  
    
    Each list item should be a two-element tuple of the form (name, count).  For example, your
    function might return a list of the form: 
      [ ("Honolulu, HI", 42), ("Shermer, IL", 19), ("Box Elder, MO"), ... ]

    Hint: store the locations and counts in a dictionary as above, then convert the dictionary 
    into a list of tuples using the items() method.  Sort the list of tuples using sort() or 
    sorted().

    See:
      https://docs.python.org/3/tutorial/datastructures.html#dictionaries
      https://docs.python.org/3/howto/sorting.html#key-functions
    """
    dict = {}
    top10 = []

    # store locations and counts into dictionary
    for tuple in rows:
        if tuple[2] not in dict.keys():
            dict[tuple[2]] = 1
        else:
            dict[tuple[2]] += 1

    sortedlist = sorted(dict.items(), key=lambda dict: dict[1], reverse=True)  # sort by value, descending order

    for i in range(10):
        top10.append(sortedlist[i])  # put top 10 in top 10 list
    #
    # fill in function body here
    #
    return top10  # fix this line to return a list of strings


# Exercise 4. (7 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as 
    designated by the two-letter abbreviation at the end of the location string (keys).  

    The return value should be a Python dictionary of the form:
      { "CA": 42, "HI": 19, "MA": 8675309, ... }

    Hint: to do this, you'll need to pull apart the location string and extract the state 
    abbreviation.  Note that some of the entries are malformed, and containing a state code but no
    city name.  You still want to count these cases (of course, if the location is blank, ignore
    the entry.
    """
    #
    # fill in function body here
    #
    dict = {}
    for tuple in rows:
        if tuple[2][-2:] not in dict.keys():  # tuple[2][-2:] only grabs last two characters of location string (the state initials)
            dict[tuple[2][-2:]] = 1  # add into dictionary and set count = 1
        else:
            dict[tuple[2][-2:]] += 1  # increment count

    return dict  # fix this line to return a dictionary mapping strings to ints


# Exercise 5. (7 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar that refueling took place.

    That is, if you ignore the year, how many different days had entries? (This number should be 
    less than or equal to 366!)
 
    Hint: the easiest way to do this is create a token representing the calendar day.  These could
    be strings (using strftime()) or integers (using date.toordinal()).  Store them in a Python set
    as you go, and then return the size of the set.

    See:
      https://docs.python.org/3/library/datetime.html#date-objects
    """
    #
    # fill in function body here
    #
    unique = set()
    for tuple in rows:
        unique.add(tuple[0].strftime("%m/%d"))  # only looks at month and day, put into set (only unique)

    return int(len(unique))  # fix this line to return an int


# Exercise 6. (7 points)
#
def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each 
    month of the year (keys).

    The dictionary you return should have 12 entries, with full month names as keys, and floats as
    values.  For example:
        { "January": 3.12, "February": 2.89, ... }

    See:
      https://docs.python.org/3/library/datetime.html
    """
    #
    # fill in function body here
    #
    dict = {}
    # add months and prices to dictionary
    for tuple in rows:
        month = tuple[0].strftime("%B") # month name only
        price = tuple[4] # price
        if month not in dict.keys():
            dict[month] = [price] # put into dictionary
        else:
            dict[month].append(price) # put prices into a list in dictionary

    # average the prices for each month in the dictionary
    for i in dict.keys():
        dict[i] = sum(dict[i]) / len(dict[i])

    return dict  # fix this line to return a dictionary

# Exercise 7. (4 points)
#
def these_are_my_words():
    """Return a string constructed from the course syllabus and code of conduct."""
    # spire ID = 32000589
    # i = 3
    word1 = "be"  # Change this string to be the i-th word of the Homework Lateness Policy
                   # of the Course Syllabus found on Moodle, where i is the first digit of your
                   # Spire ID (don't forget to start counting at 0).
    # j = 9
    word2 = "class"  # Change this string to the j-th word of the Expected Behavior section
                   # of the Code of Conduct found on Moodle, where j is the last digit of your
                   # Spire ID (don't forget to start counting at 0).
    
    return " ".join([word1, word2])


# EXTRA CREDIT (+0 points, do this for fun and glory)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

    The periods should not overlap.  You should find them in a greedy manner; that is, find the
    highest mileage thirty-day period first, and then select the next highest that is outside that
    window).
    
    Return a list with the start and end dates (as a Python datetime object) for each period, 
    followed by the total mileage, stored in a tuple:  
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #
    return []  # fix this line to return a list of tuples


# The main() function below will be executed when your program is run to allow you to check the 
# output of each function.
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    words = these_are_my_words()
    print("Exercise 7: {}\n".format(words))

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = "mustard_data.csv" 
    main(data_file_name)




