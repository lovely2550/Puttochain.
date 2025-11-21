class KarmaEngineV2:
    def score(self, text: str):
        positive = ["meditate", "kindness", "help", "donate", "forgive"]
        negative = ["anger", "hate", "greed", "harm", "violence"]
        score = 0
        for p in positive:
            if p in text:
                score += 5
        for n in negative:
            if n in text:
                score -= 5
        return score

karma_v2 = KarmaEngineV2()