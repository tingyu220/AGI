class SelfModel:

    def __init__(self):

        self.knowledge_graph = None
        self.memory_manager = None

    def bind(self, knowledge_graph, memory_manager):

        self.knowledge_graph = knowledge_graph
        self.memory_manager = memory_manager

    def knowledge_count(self):

        if not self.knowledge_graph:
            return 0

        return len(self.knowledge_graph.relations)

    def memory_count(self):

        if not self.memory_manager:
            return 0

        return len(self.memory_manager.memories)

    def report(self):

        return (
            f"我当前学会了 {self.knowledge_count()} 条知识，"
            f"记住了 {self.memory_count()} 件事情。"
        )