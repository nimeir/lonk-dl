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

    def extract_info(self):
        for post in self.subreddit('linkiscute').hot(limit=5):
            url = post.url
            request = requests.get(url)
            filename = self.determine_filename(post, url, request)
            if filename is None:
                continue
            content = request.content
            yield url, filename, content

r = Reddit()
for url, filename, content in r.extract_info():
    try:
        with open(filename, "xb") as f:
            f.write(content)
    except FileExistsError:
        print("file exists")
        continue
