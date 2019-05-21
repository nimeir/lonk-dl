import praw,requests,re

class Reddit(praw.Reddit):
    def determine_format(id):
        pass

    def extract_url(self):
        for post in self.subreddit('earthporn').hot(limit=15):
            url = post.url
            if re.search('comments', url):
                continue

            # split url and only keep the last item
            file_name = url.split("/")
            file_name = file_name[-1]

            if "." not in file_name:
                file_name += ".jpg"

            file_name = file_name.replace('?', '')  # character not allowed
            yield url, file_name

r = Reddit()
for url, file_name in r.extract_url():
    r = requests.get(url)
    try:
        with open(file_name, "xb") as f:
            f.write(r.content)
    except FileExistsError:
        print("file exists")
        continue
