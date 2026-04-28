from scoring import TextScoring
from tokens import Tokenizer
from utils import BibleLoader, Helper

available_translations = ["ESV", "KJV", "NIV", "NLT", "WEB"]


class ProgramFlow:
    def __init__(self, verbose=False) -> None:
        self.helper = Helper(verbose)
        self.tokenizer = Tokenizer()
        self.verbose = verbose
        self.scoring = TextScoring(verbose=verbose)
        self.book = "Genesis"
        self.chapter = "1"
        self.verse = "1"

        # Initialization Steps
        self.show_translations()
        self.b1 = self.select_translation(1)
        self.b2 = self.select_translation(2)

    def select_translation(self, sample: int) -> BibleLoader:
        t_index = input(f"\n[i] Select translation for Sample {sample}: ").strip()
        while not t_index.isdigit() or int(t_index) >= len(available_translations):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            t_index = input(f"\n[i] Select translation for Sample {sample}:").strip()
        return BibleLoader(available_translations[int(t_index)])

    def show_translations(self):
        """
        Shows translations that can be used by the program
        """
        self.helper.color_print(
            f"\n[+] Showing {len(available_translations)} translations:"
        )
        for i in range(len(available_translations)):
            self.helper.color_print(f"    [{i}] {available_translations[i]}")

    def select_book(self):
        self.show_books()
        book = input("\n[i] Select book: ").strip()
        while (
            book not in self.b1.dictionary.keys()
            and book not in self.b2.dictionary.keys()
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            book = input("\n[i] Select book:").strip()
        self.book = book

    def show_books(self):
        def print_books(books_lst: list[str]):
            self.helper.color_print("    [-] ", end="")
            for i in range(len(books_lst)):
                self.helper.color_print(
                    f"{books_lst[i]}, {'\n' if (i + 1) % 5 == 0 else ''}", end=""
                )
                if (i + 1) % 5 == 0:
                    self.helper.color_print("    [-] ", end="")
            print()

        b1_books = self.b1.dictionary.keys()
        self.helper.color_print(
            f"\n[+] Showing {len(b1_books)} Books in Translation 1:"
        )
        print_books(list(b1_books))

        b2_books = self.b2.dictionary.keys()
        self.helper.color_print(
            f"\n[+] Showing {len(b2_books)} Books in Translation 2:"
        )
        print_books(list(b2_books))

    def _get_book_len(self):
        return len(self.b1.dictionary[self.book].keys())

    # Chapter Operations

    def select_chapter(self):
        self.show_chapters()
        book_len = self._get_book_len()
        chapter_index = input("\n[i] Select chapter: ").strip()
        while (
            not chapter_index.isdigit()
            or int(chapter_index) > book_len
            or int(chapter_index) <= 0
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            chapter_index = input("\n[i] Select chapter:").strip()
        self.chapter = chapter_index

    def show_chapters(self):
        self.helper.color_print(f"[-] {self._get_book_len()} Chapters in {self.book}")

    def _get_chapter_len(self):
        return len(self.b1.dictionary[self.book][self.chapter].keys())

    # Verse Operations

    def select_verse(self):
        self.show_verses()
        chapter_len = self._get_chapter_len()
        verse_index = input("\n[i] Select verse: ").strip()
        while (
            not verse_index.isdigit()
            or int(verse_index) > chapter_len
            or int(verse_index) <= 0
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            verse_index = input("\n[i] Select verse:").strip()
        self.verse = verse_index

    def show_verses(self):
        self.helper.color_print(
            f"[-] {self._get_chapter_len()} Verses in {self.book} {self.chapter}"
        )

    # Main Program Flow

    def standard_flow(self):
        sample_1 = self.b1.dictionary[self.book][self.chapter][self.verse]
        sample_2 = self.b2.dictionary[self.book][self.chapter][self.verse]

        self.helper.color_print(f"\n[+] Sample 1: {sample_1}", "cyan")
        self.helper.color_print(f"\n[+] Sample 2: {sample_2}", "cyan")

        self.helper.color_print(
            f"\n[r] {self.book} {self.chapter}:{self.verse}", "cyan"
        )

        self.scoring.sample_1 = self.tokenizer.tokenize(sample_1)
        self.scoring.sample_2 = self.tokenizer.tokenize(sample_2)

        self.helper.debug_print(f"\n[~] Sample 1 Tokens: {self.scoring.sample_1}")
        self.helper.debug_print(f"\n[~] Sample 2 Tokens: {self.scoring.sample_2}")

        target_len = len(self.scoring.sample_1)
        if len(self.scoring.sample_2) > target_len:
            target_len = len(self.scoring.sample_2)

        self.helper.debug_print(f"\n[~] Target Length: {target_len}")

        self.scoring.variance_test(target_len)
        self.scoring.subset_test()

        self.move()

    def move(self):
        self.show_movement_options()

        inpt = input("\n[i] How would you like to proceed?: ").strip().upper()
        if inpt == "E":
            exit()
        elif inpt == "C":
            self.helper.color_print("\n[+] Moving on!", "green")
            self.select_book()
            self.select_chapter()
            self.select_verse()
        elif inpt == "SB":
            self.step_back()
        elif inpt == "V":
            toggle = not self.verbose
            self.verbose = toggle
            self.helper.verbose = toggle
            self.scoring.verbose = toggle
        else:
            self.step_forward()

    def step_forward(self):

        next_verse = self.get_next_verse()
        self.verse = next_verse

        if next_verse != "1":
            # Verse is within the current chapter
            return

        next_chapter = self.get_next_chapter()
        self.chapter = next_chapter
        if next_chapter != "1":
            # Chapter is within the current book
            return

        self.book = self.get_next_book()

    def get_next_verse(self) -> str:
        next_verse = str(int(self.verse) + 1)
        if (
            next_verse in self.b1.dictionary[self.book][self.chapter]
            and next_verse in self.b2.dictionary[self.book][self.chapter]
        ):
            return next_verse
        return "1"

    def get_next_chapter(self) -> str:
        next_chapter = str(int(self.chapter) + 1)
        if (
            next_chapter in self.b1.dictionary[self.book]
            and next_chapter in self.b2.dictionary[self.book]
        ):
            return next_chapter
        return "1"

    def get_next_book(self) -> str:
        b1_books = list(self.b1.dictionary.keys())
        cur_b1_book_index = b1_books.index(self.book)
        next_b1_index = cur_b1_book_index + 1

        if next_b1_index >= len(b1_books):
            next_b1_index = 0

        # b2_books = list(self.b2.dictionary.keys())
        # cur_b2_book_index = b2_books.index(self.book)
        # next_b2_index = cur_b2_book_index + 1

        # if next_b2_index >= len(b1_books):
        #     next_b2_index = 0

        return b1_books[next_b1_index]

    def step_back(self):

        prev_verse, chapter_change = self.get_prev_verse()
        self.verse = prev_verse
        if not chapter_change:
            # Verse is within the current chapter
            return

        prev_chapter, book_change = self.get_prev_chapter()
        self.chapter = prev_chapter
        if not book_change:
            # Chapter is within the current book
            return

        self.book = self.get_prev_book()

    def get_prev_verse(self) -> tuple[str, bool]:
        prev_verse = str(int(self.verse) - 1)
        if (
            prev_verse in self.b1.dictionary[self.book][self.chapter]
            and prev_verse in self.b2.dictionary[self.book][self.chapter]
        ):
            return prev_verse, False
        prev_book = self.get_prev_book()
        prev_chapter, book_change = self.get_prev_chapter()
        return list(self.b1.dictionary[prev_book][prev_chapter].keys())[-1], True

    def get_prev_chapter(self) -> tuple[str, bool]:
        prev_chapter = str(int(self.chapter) - 1)
        if (
            prev_chapter in self.b1.dictionary[self.book]
            and prev_chapter in self.b2.dictionary[self.book]
        ):
            return prev_chapter, False
        prev_book = self.get_prev_book()
        return list(self.b1.dictionary[prev_book].keys())[-1], True

    def get_prev_book(self) -> str:
        b1_books = list(self.b1.dictionary.keys())
        cur_b1_book_index = b1_books.index(self.book)
        prev_b1_index = cur_b1_book_index - 1

        if prev_b1_index < 0:
            prev_b1_index = len(b1_books) - 1

        # b2_books = list(self.b2.dictionary.keys())
        # cur_b2_book_index = b2_books.index(self.book)
        # next_b2_index = cur_b2_book_index + 1

        # if next_b2_index >= len(b1_books):
        #     next_b2_index = 0

        return b1_books[prev_b1_index]

    def show_movement_options(self):
        self.helper.color_print("\n[+] Movement Options: ")
        self.helper.color_print("    [-] step forward (S)")
        self.helper.color_print("    [-] step back    (sb)")
        self.helper.color_print("    [-] continue     (c)")
        self.helper.color_print("    [-] verbose      (v)")
        self.helper.color_print("    [-] exit         (e)")
