class LanguageLearner:

    def learn(self, sentence, knowledge_graph):

        sentence = sentence.strip()

        if "颜色是" in sentence:

            parts = sentence.split("颜色是")

            if len(parts) == 2:

                knowledge_graph.add_relation(
                    parts[0].strip(),
                    "颜色",
                    parts[1].strip()
                )

                return True

        if "是" in sentence:

            parts = sentence.split("是")

            if len(parts) == 2:

                knowledge_graph.add_relation(
                    parts[0].strip(),
                    "是",
                    parts[1].strip()
                )

                return True

        if "可以" in sentence:

            parts = sentence.split("可以")

            if len(parts) == 2:

                knowledge_graph.add_relation(
                    parts[0].strip(),
                    "可以",
                    parts[1].strip()
                )

                return True

        return False