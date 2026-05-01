from utils import Helper


class TextScoring:
    def __init__(self, sample_1=[""], sample_2=[""], verbose=False) -> None:
        self.sample_1 = sample_1
        self.sample_2 = sample_2
        self.target_len = (
            len(sample_1) if len(sample_1) > len(sample_2) else len(sample_2)
        )
        self.verbose = verbose
        self.variance_distance_multiplier = 15
        self.helper = Helper(verbose)

    def set_samples(self, sample_1, sample_2):
        self.sample_1 = sample_1
        self.sample_2 = sample_2
        self.target_len = (
            len(sample_1) if len(sample_1) > len(sample_2) else len(sample_2)
        )

    def toggle_verbose(self):
        toggle = not self.verbose
        self.verbose = toggle
        self.helper.verbose = toggle

    def get_color_score(self, score: float):
        if score < 0.6:
            return f"\033[31m{score}\033[0m"
        if score < 0.9:
            return f"\033[33m{score}\033[0m"
        if score >= 0.9:
            return f"\033[32m{score}\033[0m"

    def variance_test(self) -> float:
        sample_1_cpy = self.sample_1.copy() + [""] * (
            self.target_len - len(self.sample_1)
        )
        sample_2_cpy = self.sample_2.copy() + [""] * (
            self.target_len - len(self.sample_2)
        )
        score = 0
        for i in range(self.target_len):
            if sample_1_cpy[i] == sample_2_cpy[i]:
                score += 1
            elif sample_1_cpy[i] in sample_2_cpy:
                self.helper.debug_print(
                    f"\n[~] {sample_1_cpy[i]} found in {sample_2_cpy}", color="yellow"
                )
                distance = 0
                for j in range(self.target_len):
                    if sample_1_cpy[i] == sample_2_cpy[j]:
                        distance = abs(i - j)
                        break
                self.helper.debug_print(f"[~] Distance: {distance}", color="yellow")
                self.helper.debug_print(
                    f"[~] Adding score: {self.target_len / (self.variance_distance_multiplier * distance) / self.target_len}",
                    color="yellow",
                )
                score += self.target_len / (
                    self.variance_distance_multiplier * distance
                )

        score /= self.target_len
        print("\n[=] Variance Score of:", self.get_color_score(score))
        return score

    def subset_test(self) -> float:

        total_len = len(self.sample_1) + len(self.sample_2)
        score = total_len
        for word in self.sample_1:
            if word not in self.sample_2:
                score -= 1
                self.helper.debug_print(
                    f"\n[~] {word} not found in Sample 2", color="yellow"
                )

        for word in self.sample_2:
            if word not in self.sample_1:
                score -= 1
                self.helper.debug_print(
                    f"\n[~] {word} not found in Sample 1", color="yellow"
                )

        score /= total_len
        print("\n[=] Subset Score of:", self.get_color_score(score))
        return score

    def unique_word_count_test(self):
        set_1 = set(self.sample_1)
        set_2 = set(self.sample_2)
        unique_words = set_1 ^ set_2
        self.helper.debug_print(f"\n[~] Unique Words: {unique_words}", color="yellow")
        unique_words_len = len(unique_words)
        self.helper.debug_print(
            f"\n[~] {unique_words_len} Unique Words", color="yellow"
        )
        total_words = len(set_1 | set_2)
        self.helper.debug_print(f"\n[~] {total_words} Total Words", color="yellow")
        score = 1 - (unique_words_len / total_words)
        print("\n[=] Unique Word Count Score of:", self.get_color_score(score))
