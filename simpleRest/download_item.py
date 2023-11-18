class DownloadItem():

    def __init__(self, id: int, url: str, tags: str) -> None:
        self._id = id
        self._url = url
        self._tags = tags

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._url

    @property
    def tags(self):
        return self._tags

    def __str__(self):
        return str(self._id) + " " + str(self._tags)
