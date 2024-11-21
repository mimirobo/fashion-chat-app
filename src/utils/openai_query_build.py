class OpenAIQueryBuild:
    def build(self, user_query: str):
        return [{"role": "user", "content": user_query}]
