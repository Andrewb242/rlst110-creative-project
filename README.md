# Andrew RLST 110 Creative Project

> [!abstract]
> This python command line interface allows for the comparison of translated dead sea scroll fragments with the user's choice of Bible Translation. 

## Setup

### 1. Install Python

Make sure python is installed on your computer. You can download an official version of python [here](https://www.python.org/downloads/).

### 2. Clone the Repository

Clone the repository by running the folloing command in your terminal:

```bash
git clone https://github.com/Andrewb242/rlst110-creative-project.git andrew-b-creative-project
```

### 3. Navigate to the Project Directory

```bash
cd andrew-b-creative-project
```

### 4. Prepare Assets

In order for the code to run correctly, an `/assets` directory must be created in the project root, with a specific structure. (see the 'Assets Structure' section below)

### 5. Run the Program

```bash
python ./main.py
```

## Assets Structure

The `/assets` folder required to run the program must hold a standard structure. To effectively run the program. You must have the `DSS` directory and **at least one** translation directory.

```text
├───DSS                   # Dead Sea Scrolls
│   └───DSS_bible.json
├───ESV                   # Translation
│   └───ESV_bible.json
```

The `DSS_bible.json` file must follow the following structure:

```json
{
  "Ruth": {
    "4Q104 Ruth": {
      "1": {
        "1": "In the days when the judges judged, there was a famine in the land. A certain man of Bethlehem Judah went to live in the country of Moab, he, and his wife, and his two sons.",
        "2": "The name of the man was Elimelech, and the name of his wife Naomi. The names of his two sons were Mahlon and Chilion, Ephrathites of Bethlehem Judah. They came into the country of Moab and lived dwelled there.",
        "3": "Elimelech, Naomi’s husband, died; and she was left with her two sons."
      }
    }
  },
  "Isaiah": {
    "1Q Isaiah": {
      "1": {
        "1": "The vision of Isaiah the son of Amoz, which he saw concerning Judah and Jerusalem, in the days of Uzziah, Jotham, Ahaz, and Hezekiah, kings of Judah.",
        "2": "Hear, heavens,\nand listen, earth; for Yahweh has spoken:\n“I have nourished and brought up children,\nand they have rebelled against me.",
        "3": "The ox knows his owner,\nand the donkey his master’s crib;\nbut Israel doesn’t know,"
      },
      "2": {
        "1": "This is what Isaiah the son of Amoz saw concerning Judah and Jerusalem.",
        "2": "It shall happen in the latter days, that the mountain of Yahweh’s house shall be established on the top of the mountains,"
      }
    },
    "4Q55 Isaiah": {
      "1": {
        "1": "The vision of Isaiah the son of Amoz, which he saw concerning Judah and Jerusalem, in the days of Uzziah, Jotham, Ahaz, and Hezekiah, kings of Judah.",
        "2": "Hear, heavens,\nand listen, earth; for Yahweh has spoken:\n“I have nourished and brought up children,\nand they have rebelled against me. "
      }
    }
  }
}
```

Your `translation_bible.json` structures must hold a similar structrue, but without the fragmaent layer.

```json
{
    "Genesis": {
        "1": {
            "1": "In the beginning, God created the heavens and the earth.",
            ...
```

## Translation Information

Translations were used in this project can be found at the following links:

1. [Dead Sea Scrolls](https://dssenglishbible.com/index.htm)
2. [Other Translations](https://github.com/jadenzaleski/bible-translations)
