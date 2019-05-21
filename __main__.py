import praw,requests,re

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

    def extract_info(self, subreddit, post_limit=10):
        for post in self.subreddit(subreddit).hot(limit=post_limit):
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content

r = Reddit()
for url, filename, content in r.extract_info('linkiscute'):
    try:
        with open(filename, "xb") as f:
            f.write(content)
    except FileExistsError:
        print("[%s] File already exists" % filename)
        continue
