import praw,requests,re
import sys

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

    def extract_info(self, subreddit, sort, post_limit=10):
        for post in getattr(self.subreddit(subreddit), sort)(limit=post_limit):
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content

if __name__ == '__main__':
    r = Reddit()
    for url, filename, content in r.extract_info(sys.argv[1], sys.argv[2]):
        try:
            with open(filename, "xb") as f:
                f.write(content)
        except FileExistsError:
            print("[%s] File already exists" % filename)
            continue
