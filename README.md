# LonkDownloader

LonkDownloader - Python automation script for downloading images from a subreddit using Python and PRAW.

### Prerequisites

Latest version of Python and PRAW needs to be installed.
Requires the script to be registered on Reddit as it uses the Reddit API (https://old.reddit.com/prefs/apps/).

### Installing

Download the script and it can be run using Python. Users are required to create a praw.ini file in the working directory specifying the client_id, client_secret, and user_agent.

## Usage guide
This script is designed to be run daily as it terminates when a duplicate filename is found. Hence this script will slowly build a database of images from the desired subreddit.

For first time users it is recommended to run the script without any options as the maximum request allowed by the API is 1000 (which is the default value when no limit argument is supplied to lonkdownloader).

```
Python lonkdownloader.py [OPTIONS] subreddit
```

Example usage:
```
Python lonkdownloader.py twice --limit 100
```

## Options
```            
  -h, --help            show this help message and exit
  --limit LIMIT, -l LIMIT
                        Do not download images that are marked nsfw
  --sort SORT, -t SORT  Set frontpage sort type. For example: 'hot',
                        'controversial'
  --no-nsfw             Set the limit for maximum number of posts that will be
                        requested
```

## Acknowledgements
Thank you youtube-dl for inspiration.
