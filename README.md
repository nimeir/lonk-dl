# lonk-dl

Reddit bulk image downloader script.

## Prerequisites

Latest version of Python and PRAW needs to be installed.
Requires the script to be registered on Reddit as it uses the Reddit API. See instruction below.

## Installing

1. Download the script.
2. Register the script on '''https://old.reddit.com/prefs/apps/'''. Set the app type to 'script'. 'Name' and 'description' can be anything you want. About url can be blank. Redirect url should be http://localhost:8080.
3. Run ```Python lonk_dl.py -i``` to automatically create praw.ini file but you must fill out the values yourself (use the values generated from registering on Reddit). The client_id is the code underneath the script name in Reddit. The user_agent can be a short description of your script. Below is an example praw.ini.

```
[DEFAULT]
client_id=242398s1sst22
client_secret=Sdjslj32491faklkn3test
user_agent=image grab script by boohen
```

## Usage guide
This script is designed as a daily image grab script because the script terminates when a duplicate filename is found.

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
