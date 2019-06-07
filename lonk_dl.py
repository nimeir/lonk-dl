import praw, requests, argparse, os


# Extend the praw.Reddit class
import prawcore


class Reddit(praw.Reddit):
    def determine_filename(self, url):
        filename = url.split("/")
        filename = filename[-1].replace('?', '')
        return filename

    def extract_info(self, subreddit, post_limit, sort, no_nsfw):
        #for redditors
        if args.redditor:
            if args.sort == 'saved':
                mobj = self.redditor(subreddit).saved(limit=post_limit)
            else:
                mobj = getattr(self.redditor(subreddit).submissions, sort)(limit=post_limit)
        else:
            mobj = getattr(self.subreddit(subreddit), sort)(limit=post_limit)

        #begin extraction with correct mobj and skip iteration depending on CLI args
        for post in mobj:
            try:
                if type(post) == praw.models.reddit.comment.Comment:
                    continue
                if self.submission(id=post).is_self:
                    continue
                if no_nsfw and self.submission(id=post).over_18:
                    continue
                url = post.url
                request = requests.get(url)
                if 'text/html' in request.headers['content-type']:
                    continue
                filename = self.determine_filename(url)
                content = request.content
                yield filename, content
            except FileNotFoundError:
                print("Could not extract file. Continuing extraction from next post.")
                continue


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('subreddit', nargs='?')
    parser.add_argument('-i', action='store_true', help='Create praw.ini')
    parser.add_argument('--limit', '-l', type=int, default=1000,
                        help="Set the limit for maximum number of posts that will be requested")
    parser.add_argument('--no-nsfw', action='store_true',
                        help="Do not download images that are marked nsfw")
    parser.add_argument('--path', '-p', type=str, help="Specify the download directory path")
    parser.add_argument('--sort', '-s', type=str, default='new',
                        help="Set frontpage sort type. For example: 'hot', 'controversial'")
    parser.add_argument('--redditor', '-r', action='store_true',
                        help="Extract from redditor instead of subreddit.")
    return parser.parse_args()


def determine_path_or_file(path, filename):
    if path and os.path.isdir(path):
        return os.path.join(path, filename)
    else:
        return filename


def create_init():
    with open('praw.ini', 'w') as f:
        f.write('[DEFAULT]\ncllient_id=\nclient_secret=\nuser_agent=')


def main():
    r = Reddit()
    for filename, content in r.extract_info(args.subreddit, args.limit, args.sort, args.no_nsfw):
        try:
            with open(determine_path_or_file(args.path, filename), "xb") as f:
                print('[%s] Writing file.' % filename)
                f.write(content)
        except FileExistsError:
            print("[%s] File already exists.\nTerminating script." % filename)
            break





if __name__ == '__main__':
    args = parse_arguments()
    if args.i:
        create_init()
    else:
        main()
