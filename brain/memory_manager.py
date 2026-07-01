from brain.memory import Memory


class MemoryManager:

    def __init__(self):
        self.memories = []

    def add_memory(self, content):

        memory = Memory(content)

        self.memories.append(memory)

    def show(self):

        print("\n===== MEMORIES =====")

        if not self.memories:
            print("暂无记忆")

        for memory in self.memories:
            print(memory)

        print("====================\n")