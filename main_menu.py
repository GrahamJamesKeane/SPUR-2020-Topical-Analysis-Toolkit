from keyword_popularity import modules_all, overview_all, learning_outcomes_all
from topic_stats import get_stats


# Start here:
def menu():
    while True:
        user_input_1 = int(input("""    Main Menu
    1: Keyword Analysis
    2: Topic Stats
    3: Exit
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
                modules_all()
            elif user_input_2 == 2:
                overview_all()
            elif user_input_2 == 3:
                learning_outcomes_all()
            elif user_input_2 == 4:
                menu()
                return
            elif user_input_2 == 5:
                exit(0)
        elif user_input_1 == 2:
            get_stats()
        elif user_input_1 == 3:
            exit(0)


menu()
