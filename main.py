from course_template import get_course_template
from keyword_popularity import modules_all, overview_all, learning_outcomes_all
from setup import get_packages, get_libs
from topic_stats import get_stats
import time

process_message_1 = "Initialising... Please Wait"
process_message_2 = "Process Complete"

start_time = time.time()


# Start here:
def main():
    while True:
        user_input_1 = int(input("""    Main Menu
    1: Keyword Analysis
    2: Topic Stats
    3: Average Course Content
    4: Run All
    5: Setup
    6: Exit
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
                print(process_message_1)
                modules_all()
                print(process_message_2)
            elif user_input_2 == 2:
                print(process_message_1)
                overview_all()
                print(process_message_2)
            elif user_input_2 == 3:
                print(process_message_1)
                learning_outcomes_all()
                print(process_message_2)
            elif user_input_2 == 4:
                main()
                return
            elif user_input_2 == 5:
                print("Total Process Time", "--- %s seconds ---" % (time.time() - start_time))
                exit(0)
        elif user_input_1 == 2:
            print(process_message_1)
            get_stats()
            print(process_message_2)
        elif user_input_1 == 3:
            print(process_message_1)
            get_course_template()
            print(process_message_2)
        elif user_input_1 == 4:
            print(process_message_1)
            modules_all()
            overview_all()
            learning_outcomes_all()
            get_stats()
            get_course_template()
            print(process_message_2)
        elif user_input_1 == 5:
            print(process_message_1)
            get_packages()
            get_libs()
            print(process_message_2)
        elif user_input_1 == 6:
            print("Total Process Time", "--- %s seconds ---" % (time.time() - start_time))
            exit(0)


main()

