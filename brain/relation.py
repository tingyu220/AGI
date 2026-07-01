class Relation:
    def __init__(self, subject, predicate, obj):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj

    def __str__(self):
        return f"{self.subject} --{self.predicate}--> {self.obj}"