#!/usr/bin/env python
# https://docs.python.org/2/library/random.html
# The 'random' library has a 'shuffle' function in it that we will use
# to jumble up our items
import random

class ShuffleBag(object):
    """This is a ShuffleBag. You put a number of different items into it
and you receive the same items back, but in a random order. A
ShuffleBag ensures even distribution of randomness by taking that list
of items, randomizing it, and then returning items from the list in a
sequential order. Once all the randomized items have been returned
once, the bag is automatically re-shuffled (randomized again) and the
counter resets.
    """
    def __init__(self, *args):
        """The ShuffleBag constructor accepts an arbitrary number of
parameters. Initialize the ShuffleBag by providing *tuples* of
items-count's. Each item-count tuple represents an item we want to
return, and how many times the item should appear. For example:

    sb = ShuffleBag( ("cat hats", 3) )

Would create a very not-random ShuffleBag with three "cat hats"
strings in it. In the ShuffleBag constructor above, ``("cat hats",
3)`` is a tuple. The item is "cat hats", that is a string (which is an
object). The number of occurrences in this case is 3. Now let's add
some dogs into the mix. Specifically, let's add twice as many dogs:

    sb = ShuffleBag( ("cat hats", 3), ("dog farts", 6) )

Now we have a ShuffleBag containing 9 items total (in a random
order). 3 of those items are "cat hats" and 6 of those items are "dog
farts".

You can extend this pattern as far as you like by continuing to add
item-count tuples as demonstrated above.


In the ShuffleBag constructor, the "*args" parameter means (in Python
Speak) that this method (__init__ is a method!) accepts a "variable
number" of arguments. The implication of this is that the variable
"args" (without the leading asterisk!) is a list. To access all of the
item-count tuples provided we will run over the list using a for loop.
        """
        self.bag = []

        # Each item in 'args' is a tuple, we can assign each item in
        # the tuple directly to a variable name in our loop. Here we
        # assign the first item in each tuple to the variable named
        # 'item' and we assign the second item in each tuple to the
        # variable named 'count'.
        for item, count in args:
            # 'xrange' is a function that yields a finite set of
            # numbers. We are using it as a counter here so that we
            # add each 'item' to our bag only as many times as was
            # specified
            #
            # The '_' in this for-loop means that we're not assigning
            # the value of the items from xrange to any
            # variables. We're just literally using xrange to loop
            # "count" number of times.
            for _ in xrange(count):
                self.bag.append(item)

        # All of our items have been added to our bag. Now let's
        # shuffle it up calling the semi-private instance method
        # '_shuffle'. In Python any method with a single or
        # double-underscore prefix ('_' or '__') is considered
        # 'private' and should not be accessed directly outside of the
        # class.
        self._shuffle()

        # pos is our "position" in the list of items. We'll begin with
        # our position at the end of the list (remember, ``len()``
        # returns a COUNT of objects in a list. We subtract 1 from
        # this because we use self.pos to index each position in the
        # bag.
        #
        # Don't forget, list indices begin at 0 so the last item is
        # accessed using an index one less than the number of items in
        # the list.
        self.pos = len(self.bag) - 1

    def _shuffle(self):
        """Mix up all the items in our bag"""
        print "Shuffled the bag"
        # The 'random' library provides a really handy function we can
        # use called 'shuffle'. You provide 'shuffle' with a
        # 'sequence' (basically, a list) and the shuffle function
        # randomizes the placement of all items in the sequence
        # automatically. There is no return value from
        # "random.shuffle" because "self.bag" is modified in place.
        random.shuffle(self.bag)

    def next(self):
        """Get the next random item from our bag

Automatically re-shuffles once all previously randomized items have
been selected from.
        """
        # The contents of self.bag have already been randomized so the
        # next item is always the item at our current position.
        next_item = self.bag[self.pos]

        # Each time an item is selected we decrement our position
        # until we finally arrive back at the beginning of the list.
        if self.pos == 0:
            # We've given out as many items as are in our list, reset
            # our position to the end of the list for the next time
            # the next() method is called.
            self.pos = len(self.bag) - 1
            # Also, shuffle that bag back up. Nobody likes predictable
            # randomness.
            self._shuffle()
        else:
            # We have not yet reached the beginning of the
            # bag. Decrement our position by one.
            self.pos -= 1

        # Give back the item. It wasn't 'randomly selected', so much
        # as it was selected sequentially from a randomized list of
        # stuff.
        return next_item


# This code only runs if this file is ran directly. When a python
# script is ran directly then the '__name__' variable equals the
# string '__main__'
if __name__ == '__main__':
    # Create a bag with a bunch of stuff.
    sb = ShuffleBag(("cat", 13), ("  butts", 2), ("   dog", 4), ("    hats", 5))

    # Now let's test out the bag and grab stuff from it over and over
    # again. We expect to see the message "Shuffled the bag" appear a
    # few times here.
    #
    # Again we're using the 'xrange' function and not assigning the
    # values to any variables, we're just using it as a counter to
    # print out the 'next' item in our bag 50 times.
    for _ in xrange(50):
        print sb.next()
