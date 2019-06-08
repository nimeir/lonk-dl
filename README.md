# lonk-dl

Reddit bulk image downloader script. It can be used to download images from subreddits, specific redditors submissions, your saved submissions, etc.

## Prerequisites

Latest version of Python and PRAW (Reddit API Wrapper for Python) needs to be installed.
Requires the script to be registered on Reddit as it uses the Reddit API. See instruction below.

## Installing

1. Download the ```lonk_dl.py``` script.
2. Install PRAW. One way to do this is ```python -m pip install praw```. This should also automatically install the ```requests``` package which is required.
3. Register the script on '''https://old.reddit.com/prefs/apps/'''. Set the app type to 'script'. 'Name' and 'description' can be anything you want. About url can be blank. Redirect url should be http://localhost:8080.
4. Run ```Python lonk_dl.py -i``` to automatically create praw.ini file but you must fill out the values yourself (use the values generated from registering on Reddit). The client_id is the code underneath the script name in Reddit. **Make sure your client_secret is kept private**. The user_agent can be a short description of your script. Below is an example praw.ini.

```
[DEFAULT]
client_id=242398s1sst22
client_secret=Sdjslj32491faklkn3test
user_agent=image grab script by boohen

#complete below section if extraction fails due to authorization error
username=
password=
```

## Usage guide
This script is designed as a daily image grab script because the script terminates when a duplicate filename is found.

Minimum argument needed for the extraction to work succesfully is only the subreddit name or username.

```
python lonk_dl.py [OPTIONS] subreddit
```

Example usage:
* ```python lonk_dl.py cozyplaces --limit 100```
* To download from your saved submissions: ```python lonk_dl.py myredditusername -redditor -sort saved``` **Warning: this requires you to specify your username and password in plaintext on praw.ini. Proceed at your own discretion.**


## Options
```            
  -h, --help            show this help message and exit
  -i                    Create praw.ini (default: False)
  --limit LIMIT, -l LIMIT
                        Set the limit for maximum number of posts that will be
                        requested (default: 1000)
  --no-nsfw             Do not download images that are marked nsfw (default:
                        False)
  --path PATH, -p PATH  Specify the download directory path (default: None)
  --sort SORT, -s SORT  Set frontpage sort type. For example: 'hot',
                        'controversial' (default: new)
  --redditor, -r        Extract from redditor instead of subreddit. (default:
                        False)
```

## Acknowledgements
Thank you youtube-dl for inspiration.
