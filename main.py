from program import ProgramFlow

if __name__ == "__main__":
    verbose = input("Run in verbose mode (y/N)").upper()
    if verbose == "Y":
        verbose = True
    else:
        verbose = False

    program = ProgramFlow(verbose)

    # Book Selection
    program.select_book()

    # Fragment Selection
    program.select_fragment()

    # Chapter Selection
    program.select_chapter()

    # Verse Selection
    program.select_verse()

    # Event Loop
    while True:
        program.standard_flow()
