ThesaurusGame
=============

I thought https://twitter.com/ThesaurusGame was well-defined problem, so I write a bot to solve it.

Given the prompt that the game was taken from Roget's 1911 Thesaurus, I found that on Gutenberg ( http://www.gutenberg.org/cache/epub/10681/pg10681.txt). After trying out a few things, I determined the algorithm for linking hints to words:

* Pick a word
* Find first-order related words in Thesaurus index
* Find second-order related words to those first-order related words. Pick hints from these.

It was relatively straightforward to parse the thesaurus and build forward and reverse word-relations. The game prompt gives a word regex and set of hints, so to solve the problem we:

* Find all candidates that match the regex
* Go from this word to all first-order related words
* Go from these to all second-order related words. If any of these is one of the hints, +1 score for this candidate

At the end of the process, submit the candidate with the highest score. This doesn't always win when there are multiple viable solutions, but is capable of guessing words correctly even when there are no letters in the suggestion.

Because it wouldn't be fun if this just broke the game and solved every problem as soon as it was posted, I put some logic in to only try to answer questions once every hour-ish, 12 hours a day. If the latest tweet was an announcement of a winner, it will skip trying to solve the problem.
