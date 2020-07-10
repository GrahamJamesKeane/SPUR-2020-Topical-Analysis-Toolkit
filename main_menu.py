from filters_and_organisation import select_filters


def menu():
    while True:
        user_input_1 = int(input("""    Main Menu
    1: Keyword Analysis
    2: Topic Popularity
    3: 
    4: Exit
    """))
        if user_input_1 == 1:
            user_input_2 = int(input("""    Keyword Analysis Menu
    1: Module Title
    2: Overview
    3: Learning Outcomes
    4: Return
    5: Exit
    """))
            if user_input_2 == 1:
                select_filters("ModuleTitle")
            elif user_input_2 == 2:
                select_filters("Overview")
            elif user_input_2 == 3:
                select_filters("LearningOutcomes")
            elif user_input_2 == 4:
                menu()
                return
            elif user_input_2 == 5:
                exit(0)
        elif user_input_1 == 2:
            pass
        elif user_input_1 == 3:
            pass
        elif user_input_1 == 4:
            exit(0)


menu()
