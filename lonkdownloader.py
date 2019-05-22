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

    def extract_info(self, subreddit, post_limit, sort):
        for post in getattr(self.subreddit(subreddit), sort)(limit=post_limit):
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('subreddit')
    parser.add_argument('--limit', '-l', type=int)
    parser.add_argument('--type', '-t', type=str, default='new')
    args = parser.parse_args()
    r = Reddit()
    for url, filename, content in r.extract_info(args.subreddit, args.limit, args.type):
        try:
            with open(filename, "xb") as f:
                print('[%s] Writing file.')
                f.write(content)
        except FileExistsError:
            print("[%s] File already exists. Terminating script." % filename)
            break
