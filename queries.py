import sqlite3
from collections import Counter
from datetime import datetime
import pandas as pd

import analysis_module as am

excluded_words = ['&', '(c)', '(ui)', '(ux)', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'able', 'about',
                  'achieved', 'administer', 'against', 'aim', 'aims', 'all', 'also', 'an', 'and', 'any', 'any', 'apply',
                  'appreciate', 'approaches', 'appropriate', 'are', 'as', 'aspects', 'assess', 'associated', 'at',
                  'basic', 'be', 'begin', 'between', 'better', 'both', 'by', 'can', 'carry', 'challenges', 'comes',
                  'completion',
                  'concepts', 'course', 'define', 'depend', 'describe', 'different', 'do', 'drawn', 'e', 'equip',
                  'error', 'evaluate', 'explain', 'final', 'find', 'findings', 'first', 'focuses', 'for', 'from', 'fyp',
                  'g', 'given', 'gives', 'goal', 'grasp', 'has', 'have', 'help', 'higher', 'how', 'i', 'identify', 'ii',
                  'iii', 'importance', 'in', 'includes', 'including', 'into', 'intro', 'introduction', 'involving',
                  'is', 'issues', 'it', 'its', 'know', 'knowledge', 'known', 'large', 'learn', 'lectures', 'level',
                  'lo1', 'lo1', 'lo2', 'lo3', 'lo4', 'lo5', 'lo6', 'lo7', 'make', 'makes', 'merits', 'module', 'more',
                  'multiple', 'near',
                  'necessary', 'need', 'new', 'no', 'objectives', 'of', 'on', 'or', 'other', 'others', 'our', 'out',
                  'overcome', 'own', 'part', 'perform', 'persuasive', 'practical', 'problems', 'prove', 'provide',
                  'provision', 'pure', 'related', 'relevant', 'seen', 'seminars', 'sense', 'several', 'should',
                  'significantly', 'simple', 'single', 'so', 'solve', 'some', 'specific', 'starting', 'stopping',
                  'student', 'students', 'substantive', 'successful', 'such', 'suitable', 'syllabus', 'take', 'teach',
                  'terms', 'than', 'that', 'the', 'their', 'them', 'these', 'they', 'this', 'through', 'timely', 'to',
                  'together', 'topics', 'two', 'typed', 'types', 'understand', 'understanding', 'unseen', 'up', 'us',
                  'use', 'used', 'uses', 'using', 'value', 'variety', 'various', 'view', 'was', 'we', 'well', 'when',
                  'where', 'which', 'while', 'wide', 'will', 'with', 'within', 'without', 'work', 'workshops', 'write',
                  'year', 'each', 'based', 'allow', 'basis', 'important', 'especially', 'one', 'give', 'firm',
                  'whether', 'lost', 'might', 'relevance', 'introduce', 'objective', 'around', 'never', 'before',
                  'having', 'ways', 'attain', 'goals', 'paying', 'particular', 'attention', 'requirements', 'include',
                  'arise', 'introducing', 'previous', 'covering', 'each', 'based', 'almost', 'introduces', 'may',
                  'small', ]


def get_category_names(category, table, filter_category, filter_name):
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    c = conn.cursor()
    category_names = {}
    if filter_category and filter_name == "NA":
        query = f"SELECT {category} FROM {table} ORDER BY {category};"
    else:
        query = f"SELECT {category} FROM {table} Where {filter_category} = '{filter_name}'ORDER BY {category};"
    i = 1
    for row in c.execute(query):
        x = str(row[0])
        category_names[i] = x
        i += 1
    conn.close()
    return category_names


def query_builder(class_query_word, category, filter_list, filter_list_flags):
    count = 0
    query = None
    if filter_list_flags["class_col_1"] and filter_list_flags["class_col_2"]:
        query = f"SELECT {category} FROM ModuleDetails "
    elif filter_list_flags["class_all"]:
        query = f"SELECT {category}, A1, A2, B1, B2 FROM ModuleDetails "
    if filter_list_flags["university_name"] and filter_list_flags["year_offered"] or filter_list_flags["course"] or \
            filter_list_flags["core"]:
        query += f"INNER JOIN CourseDetails ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode "
    if filter_list_flags["year_offered"] or filter_list_flags["university_name"] or filter_list_flags["course"] or \
            filter_list_flags["core"] or filter_list_flags["semester1"] or filter_list_flags["semester2"] \
            or class_query_word is not None:
        query += "WHERE "
    if filter_list_flags["semester1"] or filter_list_flags["semester2"]:
        count += 1
        query += f"ModuleDetails.Semester1 = '{filter_list['semester1']}' AND ModuleDetails.Semester2 = '{filter_list['semester2']}' "
    if filter_list_flags["university_name"]:
        if count == 1:
            count += 1
            query += f"AND ModuleDetails.UniversityName = '{filter_list.get('university_name')}' "
        else:
            count += 1
            query += f"ModuleDetails.UniversityName = '{filter_list.get('university_name')}' "
    if filter_list_flags["year_offered"]:
        if count > 0:
            count += 1
            query += f"AND CourseDetails.YearOffered = {filter_list.get('year_offered')} "
        else:
            count += 1
            query += f"CourseDetails.YearOffered = {filter_list.get('year_offered')} "
    if filter_list_flags["core"]:
        if count > 0:
            count += 1
            query += f" AND CourseDetails.Core = '{filter_list.get('core')}' "
        else:
            count += 1
            query += f" CourseDetails.Core = '{filter_list.get('core')}' "
    if filter_list_flags["course"]:
        if count > 0:
            count += 1
            query += f"AND CourseDetails.CourseTitle = '{filter_list.get('course')}' "
        else:
            count += 1
            query += f"CourseDetails.CourseTitle = '{filter_list.get('course')}' "
    if filter_list_flags["class_col_1"] and filter_list_flags["class_col_2"]:
        if count > 0:
            count += 1
            query += f"AND ModuleDetails.{filter_list['class_col_1']} = '{class_query_word}' "
            query += f"OR ModuleDetails.{filter_list['class_col_2']} = '{class_query_word}' "
        else:
            count += 1
            query += f"ModuleDetails.{filter_list['class_col_1']} = '{class_query_word}' "
            query += f"OR ModuleDetails.{filter_list['class_col_2']} = '{class_query_word}' "
    if filter_list_flags["class_col_1"] and filter_list_flags["class_col_2"]:
        query += f"ORDER BY {filter_list['class_col_1']} ;"
    elif filter_list_flags["class_all"]:
        query += f"ORDER BY ModuleDetails.A1, ModuleDetails.A2, ModuleDetails.B1, ModuleDetails.B2 ;"
    # print(query)
    return query


# Returns a list containing the keywords for a given classification
def get_keywords_single_class(class_query_word, category, filter_list, filter_list_flags):
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    category_keywords = []
    query = query_builder(class_query_word, category, filter_list, filter_list_flags)
    data_frame = pd.read_sql_query(query, conn)
    if not data_frame.empty:
        for row in data_frame[category]:
            if row is not None:
                category_title = am.clean_row(row)  # remove whitespace & commas
                for title in category_title:
                    if title not in excluded_words:
                        category_keywords.append(title)
        conn.close()
        return category_keywords
    else:
        print(f"There are 0 entries with the classification {class_query_word}.")
        print("-------------------")
        conn.close()
        return


def build_dictionary(key, data, keyword_count):
    if key not in data:
        data[key] = keyword_count
    else:
        group = dict(data.get(key))
        for value, count in keyword_count.items():
            if value in group:
                group[value] += count
            else:
                group[value] = count
        data[key] = group

    return data


def filter_excluded_words(category_content):
    category_keywords = []
    for title in category_content:
        if title not in excluded_words:
            category_keywords.append(title)
    return category_keywords


def transfer_to_df(data, length):
    category_keyword_df = pd.DataFrame(columns=["Classification", "Keyword", "Frequency"])
    for item, value in data.items():

        popular = dict(Counter(value).most_common(length))

        for keyword, count in popular.items():
            new_row = pd.Series(data={"Classification": item, "Keyword": keyword, "Frequency": count})
            category_keyword_df = category_keyword_df.append(new_row, ignore_index=True)

    # sort the data-frame:
    category_keyword_df = category_keyword_df.sort_values(by=["Classification", "Keyword"],
                                                          kind="heapsort")
    # Assign indices:
    category_keyword_df.set_index(["Classification", "Keyword"], inplace=True)
    return category_keyword_df


def output_to_file(category_keyword_df):
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/all_classifications_{stamp}.csv"
    category_keyword_df.to_csv(file_name)


# Returns categorical keywords and their frequency with all associated classifications
def get_combined_class_keywords(category, filter_list, filter_list_flags):
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    c = conn.cursor()
    data = {}
    query = query_builder(None, category, filter_list, filter_list_flags)

    # Fetch query from DB:
    for row in c.execute(query):
        category_keywords = []
        if row[0] is not None:
            category_content = am.clean_row(row[0])
            class_a1 = row[1]
            class_a2 = row[2]
            class_b1 = row[3]
            class_b2 = row[4]
            if class_b1 and class_b2 is not None:
                key = f"{class_a1}, {class_a2}, {class_b1}, {class_b2}"
            else:
                key = f"{class_a1}, {class_a2}"

            # Filter excluded words
            category_keywords = filter_excluded_words(category_content)

            # Get most popular keywords
            keyword_count = dict(Counter(am.get_count(category_keywords)).most_common(filter_list["length"]))

            # Add keys, keywords, and frequency to dictionary
            data = build_dictionary(key, data, keyword_count)

    # Transfer information to data-frame:
    category_keyword_df = transfer_to_df(data, filter_list["length"])

    # Output data-frame to .csv
    output_to_file(category_keyword_df)

    # Return data-frame and key  as list
    result = [category_keyword_df, key]

    conn.close()
    return result


# Returns categorical keywords and their frequency with all associated classifications for primary &
# secondary classifications:
def get_primary_or_secondary_keywords_combined(class_query_word, category, filter_list, filter_list_flags, data):
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    c = conn.cursor()

    query = query_builder(class_query_word, category, filter_list, filter_list_flags)

    # Fetch query from DB:
    for row in c.execute(query):
        category_keywords = []
        if row is not None:
            category_content = am.clean_row(row[0])

            # Filter excluded words
            category_keywords = filter_excluded_words(category_content)

            # Get most popular keywords
            keyword_count = dict(Counter(am.get_count(category_keywords)).most_common(filter_list["length"]))

            # Add keys, keywords, and frequency to dictionary
            data = build_dictionary(class_query_word, data, keyword_count)

    conn.close()

    return data
