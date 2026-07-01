class ReasoningEngine:

    def answer(self, question, knowledge_graph, self_model=None):

        question = question.strip()

        # ===== 自我认知 =====
        if question == "你学会了多少知识？":

            if self_model:
                return f"Yu：{self_model.knowledge_count()} 条知识"

            return "我不知道"

        if question == "你记住了多少事情？":

            if self_model:
                return f"Yu：{self_model.memory_count()} 件事情"

            return "我不知道"

        if question == "你现在知道什么？":

            if self_model:
                return "Yu：" + self_model.report()

            return "我不知道"

        # ===== 原有逻辑 =====

        if question.endswith("颜色是什么"):

            subject = question.replace("颜色是什么", "").strip()

            results = knowledge_graph.query(subject, "颜色")

            if results:
                return f"{subject} 的颜色是 {results[0].obj}"

            return "我不知道"

        if question.endswith("是什么"):

            subject = question.replace("是什么", "").strip()

            results = knowledge_graph.query(subject, "是")

            if results:
                return f"{subject} 是 {results[0].obj}"

            return "我不知道"

        if question.endswith("可以干什么"):

            subject = question.replace("可以干什么", "").strip()

            results = knowledge_graph.query(subject, "可以")

            if results:
                return f"{subject} 可以 {results[0].obj}"

            return "我不知道"

        return None