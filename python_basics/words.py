"""Retrieve and print words from a url
Usage:
  python words.py <<url>>"""

import sys
from urllib.request import urlopen

def fetch_words(url):
  """Fetches the word from the url

    Args:
        A live url

    Returns:
         Collection of iterable words"""

  with urlopen(url) as story:
    story_words = []
    for line in story:
      line_words = line.decode('utf-8').split()
      for word in line_words:
        story_words.append(word)

    return story_words


def print_items(items):
  """Print items one per line
  Args:
      An iterable series of printable"""
  for item in items:
    print(item)


def main(url):
  """Print each word from a text
    Args:
        url: The url of a utf-8 text document"""
  
  words = fetch_words(url)
  print_items(words)

if __name__ == '__main__':
  main(sys.argv[1])








