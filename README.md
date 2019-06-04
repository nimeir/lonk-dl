# lonk-dl

Reddit bulk image downloader script.

### Prerequisites

Latest version of Python and PRAW needs to be installed.
Requires the script to be registered on Reddit as it uses the Reddit API ().

### Installing

1. Download the script and it can be run using Python. 
2. Register the script on '''https://old.reddit.com/prefs/apps/'''.
3. Run ```Python lonk_dl.py -i``` to automatically create praw.ini file but you must fill out the values yourself (use the values generated from registering on Reddit). The user_agent can be a short description of your script. For example ```user_agent=image downloader by ...```.

## Usage guide
This script is designed to be run daily as it terminates when a duplicate filename is found. Hence this script will slowly build a database of images from the desired subreddit.

For first time users it is recommended to run the script without any options as the maximum request allowed by the API is 1000 (which is the default value when no limit argument is supplied to lonkdownloader).

Minimum argument needed for the extraction to work succesfully is only the subreddit name.

```
Python lonk_dl.py [OPTIONS] subreddit
```

Example usage:
```
Python lonk_dl.py twice --limit 100
```

## Options
```            
  -h, --help            show this help message and exit
  --limit LIMIT, -l LIMIT
                        Set the limit for maximum number of posts that will be
                        requested (default: 1000)
  --sort SORT, -t SORT  Set frontpage sort type. For example: 'hot',
                        'controversial' (default: new)
  --path PATH, -p PATH  Specify the download directory path (default: None)
  --no-nsfw             Do not download images that are marked nsfw (default:
                        False)
  -i                    Create praw.ini (default: False)
```

## Acknowledgements
Thank you youtube-dl for inspiration.
