from brain.knowledge_graph import KnowledgeGraph
from brain.language_learner import LanguageLearner
from brain.reasoning_engine import ReasoningEngine
from brain.memory_manager import MemoryManager
from brain.self_model import SelfModel

brain = KnowledgeGraph()
teacher = LanguageLearner()
reasoner = ReasoningEngine()
memory_manager = MemoryManager()
self_model = SelfModel()

# 绑定系统
self_model.bind(brain, memory_manager)

print("=================================")
print("      Project Yu V0.5")
print("=================================")
print("输入 exit 退出")
print("输入 记忆 查看记忆")
print()

while True:

    sentence = input("你：").strip()

    if sentence == "":
        continue

    if sentence.lower() == "exit":
        print("Yu：再见！")
        break

    if sentence == "记忆":
        memory_manager.show()
        continue

    # 先尝试回答
    answer = reasoner.answer(sentence, brain, self_model)

    if answer:

        print(answer)

    else:

        success = teacher.learn(sentence, brain)

        if success:

            memory_manager.add_memory(sentence)

            print("Yu：我记住了。")

        else:

            print("Yu：我暂时无法理解这句话。")