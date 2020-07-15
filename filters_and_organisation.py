from analysis_module import get_query_word, get_data, iterate_classifications
from queries import get_category_names, get_combined_class_keywords


def print_category_names(category_names):
    for key, value in category_names.items():
        print(str(key) + ": " + value)


def return_category_name(category_list, category_selection):
    for key, value in category_list.items():
        if category_selection == key:
            category_selection = value
    return category_selection


def select_filters(category):
    filter_list = {"class_col_1": None, "class_col_2": None, "class_all": None, "year_offered": None,
                   "university_name": None, "course": None,
                   "core": None, "semester1": None, "semester2": None, "length": None}
    filter_list_flags = {"class_col_1": False, "class_col_2": False, "class_all": False,
                         "year_offered": False, "university_name": False, "course": False,
                         "core": False, "semester1": False, "semester2": False, "length": False}

    if category == "ModuleTitle":
        filter_list["length"] = 5
        filter_list_flags["length"] = True
    elif category == "Overview":
        filter_list["length"] = 20
        filter_list_flags["length"] = True
    elif category == "LearningOutcomes":
        filter_list["length"] = 20
        filter_list_flags["length"] = True

    classification = int(input("""Select Classification:
    1: Primary
    2: Secondary
    3: All
    4: None
    """))
    if classification != 4:
        if classification == 1:
            filter_list["class_col_1"] = "A1"
            filter_list_flags["class_col_1"] = True
            filter_list["class_col_2"] = "B1"
            filter_list_flags["class_col_2"] = True
        elif classification == 2:
            filter_list["class_col_1"] = "A2"
            filter_list_flags["class_col_1"] = True
            filter_list["class_col_2"] = "B2"
            filter_list_flags["class_col_2"] = True
        elif classification == 3:
            filter_list_flags["class_all"] = True

    semester = int(input("""Filter by Semester taken?
        1: First
        2: Second
        3: Both
        4: None
        """))
    semester1 = None
    semester2 = None
    if semester != 4:
        if semester == 1:
            semester1 = "TRUE"
            semester2 = "FALSE"
            filter_list_flags["semester1"] = True
            filter_list_flags["semester2"] = False
        elif semester == 2:
            semester1 = "FALSE"
            semester2 = "TRUE"
            filter_list_flags["semester1"] = False
            filter_list_flags["semester2"] = True
        elif semester == 3:
            semester1 = "TRUE"
            semester2 = "TRUE"
        filter_list["semester1"] = semester1
        filter_list["semester2"] = semester2

    university_name = int(input("""Filter by University?
    1: Yes
    2: No
    """))
    if university_name == 1:
        print("Select University:")
        university_list = get_category_names("UniversityName", "Universities", "NA", "NA")
        print_category_names(university_list)
        university_name = int(input())
        university_name = return_category_name(university_list, university_name)
        print(university_name)
        filter_list["university_name"] = university_name
        filter_list_flags["university_name"] = True

    if filter_list_flags["university_name"]:
        course = int(input("""Filter by Course?
    1: Yes
    2: No
    """))
        if course == 1:
            print("Select Course:")
            course_list = get_category_names("CourseTitle", "CourseList", "UniversityName", university_name)
            print_category_names(course_list)
            course = int(input())
            course = return_category_name(course_list, course)
            filter_list["course"] = course
            filter_list_flags["course"] = True

    if filter_list_flags["course"]:
        core = int(input("""Filter Core Modules?
    1: Core
    2: Optional
    3: All
    """))
        if core != 3:
            if core == 1:
                core = "TRUE"
            elif core == 2:
                core = "FALSE"
            filter_list["core"] = core
            filter_list_flags["core"] = True

    if filter_list_flags["course"]:
        year_offered = int(input("""Select Year:
            1: First
            2: Second
            3: Third
            4: Fourth
            5: None
            """))
        if year_offered != 5:
            if 1 <= year_offered <= 4:
                filter_list["year_offered"] = year_offered
                filter_list_flags["year_offered"] = True

    organise_query(category, filter_list, filter_list_flags)


def organise_query(category, filter_list, filter_list_flags):
    if filter_list_flags["class_col_1"] and filter_list_flags["class_col_2"]:
        mode = int(input("""Select Mode:
    1: Individual
    2: Iterate
    3: All
    4: Exit
    """))
        if mode == 1:
            class_query_word = get_query_word(filter_list.get("class_col_1"), filter_list.get("class_col_2"))
            get_data(class_query_word,
                     category, filter_list, filter_list_flags)
        elif mode == 2:
            iterate_classifications(category, filter_list, filter_list_flags, True)
        elif mode == 3:
            iterate_classifications(category, filter_list, filter_list_flags, False)
        elif mode == 4:
            exit(0)
    elif filter_list_flags["class_all"]:
        result = get_combined_class_keywords(category, filter_list, filter_list_flags)
        print(result[0])
        # plot function to go here
