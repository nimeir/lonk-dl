import praw,requests,re

class Reddit(praw.Reddit):
    def determine_filename(self, post, url):
        if self.submission(id=post).is_self:
            return None
        else:
            filename = url.split("/")
            filename = filename[-1].replace('?', '')
            return filename

    def extract_url(self):
        for post in self.subreddit('earthporn').hot(limit=5):
            url = post.url
            content = requests.get(url).content
            filename = self.determine_filename(post, url, content)
            if filename is None:
                continue
            yield url, filename, content

r = Reddit()
for url, filename, content in r.extract_url():
    try:
        with open(filename, "xb") as f:
            f.write(content)
    except FileExistsError:
        print("file exists")
        continue
