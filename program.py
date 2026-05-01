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
        self.fragment = ""
        self.book = "Genesis"
        self.chapter = "1"
        self.verse = "1"

        # Initialization Steps
        self.show_translations()
        self.dss = BibleLoader("DSS")
        self.translation = ""
        self.b = self.select_translation()
        self.books = list(
            set(self.dss.dictionary.keys()) & (set(self.b.dictionary.keys()))
        )

    def select_translation(self) -> BibleLoader:
        t_index = input("\n[?] Select translation: ").strip()
        while not t_index.isdigit() or int(t_index) >= len(available_translations):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            t_index = input("\n[?] Select translation:").strip()
        translation = available_translations[int(t_index)]
        self.translation = translation
        return BibleLoader(translation)

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
        book = input("\n[?] Select book: ").strip()
        while (
            book not in self.dss.dictionary.keys()
            and book not in self.b.dictionary.keys()
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            book = input("\n[?] Select book:").strip()
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

        self.helper.color_print(
            f"\n[+] Showing {len(self.books)} Availible Books in DSS and Selected Translation:"
        )
        print_books(self.books)

    def _get_book_len(self):
        return len(self.books)

    # Fragment Operations
    def select_fragment(self):
        self.show_fragments()
        frag_num = input("\n[?] Select fragment: ").strip()
        while not frag_num.isdigit() or int(frag_num) >= self._get_frag_num():
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            frag_num = input("\n[?] Select fragment:").strip()
        self.fragment = list(self.dss.dictionary[self.book].keys())[int(frag_num)]

    def show_fragments(self):
        def print_fragments(frag_lst: list[str]):
            for i in range(len(frag_lst)):
                self.helper.color_print(f"    [{i}] {frag_lst[i]}")

        num_frags = self._get_frag_num()
        self.helper.color_print(
            f"\n[+] Showing {num_frags} Availible Fragments for {self.book}:"
        )
        print_fragments(list(self.dss.dictionary[self.book].keys()))

    def _get_frag_num(self):
        return len(self.dss.dictionary[self.book].keys())

    def _get_frag_len(self):
        return len(self.dss.dictionary[self.book][self.fragment].keys())

    # Chapter Operations

    def select_chapter(self):
        self.show_chapters()
        frag_len = self._get_frag_len()
        chapter_index = input("\n[?] Select chapter: ").strip()
        while (
            not chapter_index.isdigit()
            or int(chapter_index) > frag_len
            or int(chapter_index) <= 0
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            chapter_index = input("\n[?] Select chapter:").strip()
        self.chapter = chapter_index

    def show_chapters(self):
        self.helper.color_print(
            f"[-] {self._get_frag_len()} Chapters in {self.fragment}"
        )

    def _get_chapter_len(self) -> int:
        frag_len = len(
            self.dss.dictionary[self.book][self.fragment][self.chapter].keys()
        )
        # b_len = len(self.b.dictionary[self.book][self.chapter].keys())
        # return frag_len if frag_len <= b_len else b_len
        # SHOULD ALWAYS BE FRAG LENGTH
        return frag_len

    # Verse Operations

    def select_verse(self):
        self.show_verses()
        chapter_len = self._get_chapter_len()
        verse_index = input("\n[?] Select verse: ").strip()
        while (
            not verse_index.isdigit()
            or int(verse_index) > chapter_len
            or int(verse_index) <= 0
        ):
            self.helper.color_print(
                "\n[!] Incorrect input format. Please try again.", "red"
            )
            verse_index = input("\n[?] Select verse:").strip()
        self.verse = verse_index

    def show_verses(self):
        self.helper.color_print(
            f"[-] {self._get_chapter_len()} Verses in {self.fragment} {self.chapter}"
        )

    # Main Program Flow

    def standard_flow(self):
        sample_1 = self.dss.dictionary[self.book][self.fragment][self.chapter][
            self.verse
        ]
        sample_2 = self.b.dictionary[self.book][self.chapter][self.verse]

        self.helper.color_print(f"\n[+] Sample 1 (DSS): {sample_1}", "cyan")
        self.helper.color_print(
            f"\n[+] Sample 2 ({self.translation}): {sample_2}", "cyan"
        )

        self.helper.color_print(
            f"\n[r] {self.fragment}/{self.book} {self.chapter}:{self.verse}", "cyan"
        )

        sample_1 = self.tokenizer.tokenize(sample_1)
        sample_2 = self.tokenizer.tokenize(sample_2)

        self.helper.debug_print(f"\n[~] Sample 1 Tokens: {sample_1}")
        self.helper.debug_print(f"\n[~] Sample 2 Tokens: {sample_2}")

        self.scoring.set_samples(sample_1, sample_2)

        self._run_tests()

        self.move()

    def _run_tests(self):
        self.scoring.variance_test()
        self.scoring.subset_test()
        self.scoring.unique_word_count_test()

    # Movement

    def move(self):
        self.show_movement_options()

        inpt = input("\n[?] How would you like to proceed?: ").strip().upper()
        if inpt == "E":
            exit()
        elif inpt == "C":
            self.helper.color_print("\n[+] Moving on!", "green")
            self.select_book()
            self.select_fragment()
            self.select_chapter()
            self.select_verse()
        elif inpt == "SB":
            self.step_back()
            self.helper.debug_print(
                f"\n[~] b: {self.book} f: {self.fragment} c: {self.chapter} v: {self.verse}"
            )
        elif inpt == "V":
            toggle = not self.verbose
            self.verbose = toggle
            self.helper.verbose = toggle
            self.scoring.toggle_verbose()
        else:
            self.step_forward()
            self.helper.debug_print(
                f"\n[~] b: {self.book} f: {self.fragment} c: {self.chapter} v: {self.verse}"
            )

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

        next_frag = self.get_next_frag()
        if next_frag:
            # Moved to the next fragment in the book
            self.fragment = next_frag
            return

        next_book = self.get_next_book()
        self.book = next_book
        self.fragment = list(self.dss.dictionary[next_book].keys())[0]

    def get_next_verse(self) -> str:
        next_verse = str(int(self.verse) + 1)
        chapter_len = self._get_chapter_len()
        while not (
            next_verse in self.dss.dictionary[self.book][self.fragment][self.chapter]
            and next_verse in self.b.dictionary[self.book][self.chapter]
        ):
            # Verse is not in either source chapter
            if int(next_verse) > chapter_len:
                return "1"
            next_verse = str(int(next_verse) + 1)
        return next_verse

    def get_next_chapter(self) -> str:
        next_chapter = str(int(self.chapter) + 1)
        frag_len = self._get_frag_len()
        while not (
            next_chapter in self.dss.dictionary[self.book][self.fragment]
            and next_chapter in self.b.dictionary[self.book]
        ):
            # Chapter is not in either source book/fragment
            if int(next_chapter) > frag_len:
                return "1"
            next_chapter = str(int(next_chapter) + 1)
        return next_chapter

    def get_next_frag(self) -> None | str:
        cur_frags = list(self.dss.dictionary[self.book].keys())
        cur_frag_index = cur_frags.index(self.fragment)
        next_frag_index = cur_frag_index + 1

        if next_frag_index >= len(cur_frags):
            # Need to move to the next book
            return None

        return cur_frags[next_frag_index]

    def get_next_book(self) -> str:
        cur_book_index = self.books.index(self.book)
        next_b1_index = cur_book_index + 1

        if next_b1_index >= len(self.books):
            next_b1_index = 0

        return self.books[next_b1_index]

    def step_back(self):

        prev_verse, chapter_change = self.get_prev_verse()
        self.verse = prev_verse
        if not chapter_change:
            # Verse is within the current chapter
            return

        prev_chapter, frag_change = self.get_prev_chapter()
        self.chapter = prev_chapter
        if not frag_change:
            # Chapter is within the current fragment
            return

        prev_frag, book_change = self.get_prev_frag()
        self.fragment = prev_frag
        if not book_change:
            # Frag is within the current book
            return

        self.book = self.get_prev_book()
        self.fragment = list(self.dss.dictionary[self.book].keys())[-1]

    def get_prev_verse(self) -> tuple[str, bool]:
        prev_verse = str(int(self.verse) - 1)
        prev_chapter, frag_change = self.get_prev_chapter()
        if not (
            prev_verse in self.dss.dictionary[self.book][self.fragment][self.chapter]
            and prev_verse in self.b.dictionary[self.book][self.chapter]
        ):
            if frag_change:
                prev_frag, book_change = self.get_prev_frag()
                if book_change:
                    prev_book = self.get_prev_book()
                    return list(
                        self.dss.dictionary[prev_book][prev_frag][prev_chapter].keys()
                    )[-1], True
                return list(
                    self.dss.dictionary[self.book][prev_frag][prev_chapter].keys()
                )[-1], True
            return list(
                self.dss.dictionary[self.book][self.fragment][prev_chapter].keys()
            )[-1], True

            # Verse is not in the current chapter
        return prev_verse, False

    def get_prev_chapter(self) -> tuple[str, bool]:
        prev_chapter = str(int(self.chapter) - 1)
        if not (
            prev_chapter in self.dss.dictionary[self.book][self.fragment]
            and prev_chapter in self.b.dictionary[self.book]
        ):
            # Chapter is not in the current fragment
            prev_frag, book_change = self.get_prev_frag()
            if book_change:
                prev_book = self.get_prev_book()
                return list(self.dss.dictionary[prev_book][prev_frag].keys())[-1], True
            return list(self.dss.dictionary[self.book][prev_frag].keys())[-1], True
        return prev_chapter, False

    def get_prev_frag(self) -> tuple[str, bool]:
        cur_frags = list(self.dss.dictionary[self.book].keys())
        cur_frag_index = cur_frags.index(self.fragment)
        prev_frag_index = cur_frag_index - 1

        prev_book = self.get_prev_book()

        if prev_frag_index < 0:
            # Need to move to the prev book
            return list(self.dss.dictionary[prev_book].keys())[-1], True
        return cur_frags[prev_frag_index], False

    def get_prev_book(self) -> str:
        cur_book_index = self.books.index(self.book)
        prev_index = cur_book_index - 1

        if prev_index < 0:
            prev_index = len(self.books) - 1

        return self.books[prev_index]

    def show_movement_options(self):
        self.helper.color_print("\n[+] Movement Options: ")
        self.helper.color_print("    [-] step forward (S)")
        self.helper.color_print("    [-] step back    (sb)")
        self.helper.color_print("    [-] continue     (c)")
        self.helper.color_print("    [-] verbose      (v)")
        self.helper.color_print("    [-] exit         (e)")
