import praw, requests, argparse, os


# Extend the praw.Reddit class
class Reddit(praw.Reddit):
    def determine_filename(self, post, url, request):
        if self.submission(id=post).is_self:
            return None
        elif 'text/html' in request.headers['content-type']:
            return None
        else:
            filename = url.split("/")
            filename = filename[-1].replace('?', '')
            return filename

    def extract_info(self, subreddit, post_limit, sort, no_nsfw):
        if '/u/' or 'u/' in subreddit:
            mobj = getattr(self.redditor(subreddit), sort)(limit=post_limit)
        else:
            mobj = getattr(self.subreddit(subreddit), sort)(limit=post_limit)

        for post in mobj:
            if no_nsfw and self.submission(id=post).over_18:
                continue
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('subreddit', nargs='?')
    parser.add_argument('--limit', '-l', type=int, default=1000,
                        help="Set the limit for maximum number of posts that will be requested")
    parser.add_argument('--sort', '-t', type=str, default='new',
                        help="Set frontpage sort type. For example: 'hot', 'controversial'")
    parser.add_argument('--path', '-p', type=str, help="Specify the download directory path")
    parser.add_argument('--no-nsfw', action='store_true',
                        help="Do not download images that are marked nsfw")
    parser.add_argument('-i', action='store_true', help='Create praw.ini')
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
    for url, filename, content in r.extract_info(args.subreddit, args.limit, args.sort, args.no_nsfw):
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
