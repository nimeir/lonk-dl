import praw,requests
import argparse

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
        for post in getattr(self.subreddit(subreddit), sort)(limit=post_limit):
            if no_nsfw and self.submission(id=post).over_18:
                continue
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('subreddit')
    parser.add_argument('--limit', '-l', type=int, default=1000, help="Do not download images that are marked nsfw")
    parser.add_argument('--sort', '-t', type=str, default='new',
                        help="Set frontpage sort type. For example: 'hot', 'controversial'")
    parser.add_argument('--no-nsfw', action='store_true',
                        help="Set the limit for maximum number of posts that will be requested")
    args = parser.parse_args()
    r = Reddit()
    for url, filename, content in r.extract_info(args.subreddit, args.limit, args.sort, args.no_nsfw):
        try:
            with open(filename, "xb") as f:
                print('[%s] Writing file.' % filename)
                f.write(content)
        except FileExistsError:
            print("[%s] File already exists.\nTerminating script." % filename)
            break
