from datetime import datetime


class Memory:

    def __init__(self, content, source="user"):

        self.content = content
        self.source = source
        self.timestamp = datetime.now()

    def __str__(self):

        return (
            f"[{self.timestamp}] "
            f"{self.source}: "
            f"{self.content}"
        )