import re
import sqlite3
import pandas as pd

excluded_words = ['&', '(c)', '(ui)', '(ux)', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'able', 'about',
                  'achieved', 'administer', 'against', 'aim', 'aims', 'all', 'also', 'an', 'and', 'any', 'any', 'apply',
                  'appreciate', 'approaches', 'appropriate', 'are', 'as', 'aspects', 'assess', 'associated', 'at',
                  'basic', 'be', 'begin', 'between', 'both', 'by', 'can', 'carry', 'challenges', 'comes', 'completion',
                  'concepts', 'course', 'define', 'depend', 'describe', 'different', 'do', 'drawn', 'e', 'equip',
                  'error', 'evaluate', 'explain', 'final', 'find', 'findings', 'first', 'focuses', 'for', 'from', 'fyp',
                  'g', 'given', 'gives', 'goal', 'grasp', 'has', 'have', 'help', 'higher', 'how', 'i', 'identify', 'ii',
                  'iii', 'importance', 'in', 'includes', 'including', 'into', 'intro', 'introduction', 'involving',
                  'is', 'issues', 'it', 'its', 'know', 'knowledge', 'known', 'large', 'learn', 'lectures', 'level',
                  'lo1', 'lo1', 'lo2', 'lo3', 'lo4', 'lo5', 'lo6', 'lo7', 'make', 'makes', 'merits', 'module', 'more', 'multiple', 'near',
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


# Clean strings taken from tables
def clean_row(row):
    chars = ['(', ')', '/', '.', ';', ':', ',', '"', '?', '+', '•', '●', '[', ']', '*', '--']
    for char in chars:
        row = row.replace(char, ' ')
    row = row.strip(" .").lower()
    regex = re.compile(r"\s+")
    return re.split(regex, row)


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


# Returns a list containing the keywords for a given classification
def get_keywords(class_query_word, category, filter_list, filter_list_flags):
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    title_keywords = []
    count = 0
    query = f"SELECT {category} FROM ModuleDetails "
    if filter_list_flags["university_name"] and filter_list_flags["year_offered"] or filter_list_flags["course"] or \
            filter_list_flags["core"]:
        query += f"INNER JOIN CourseDetails ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode "
    if filter_list_flags["year_offered"] or filter_list_flags["university_name"] or filter_list_flags["course"] or \
            filter_list_flags["core"] or filter_list_flags["semester1"] or filter_list_flags["semester2"]:
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
        if count in (1,2):
            count += 1
            query += f"AND CourseDetails.YearOffered = {filter_list.get('year_offered')} "
        else:
            count += 1
            query += f"CourseDetails.YearOffered = {filter_list.get('year_offered')} "
    if filter_list_flags["core"]:
        if count > 1:
            count += 1
            query += f" AND CourseDetails.Core = '{filter_list.get('core')}' "
        else:
            count += 1
            query += f" CourseDetails.Core = '{filter_list.get('core')}' "
    if filter_list_flags["course"]:
        if count > 1:
            count += 1
            query += f"AND CourseDetails.CourseTitle = '{filter_list.get('course')}' "
        else:
            query += f"CourseDetails.CourseTitle = '{filter_list.get('course')}' "
    query += ";"
    data_frame = pd.read_sql_query(query, conn)
    if not data_frame.empty:
        for row in data_frame[category]:
            if row is not None:
                category_title = clean_row(row)  # remove whitespace & commas
                for title in category_title:
                    if title not in excluded_words:
                        title_keywords.append(title)
        # for key in title_keywords:
        #    print(key)
        conn.close()
        return title_keywords
    else:
        print(f"There are 0 entries with the classification {class_query_word}.")
        print("-------------------")
        conn.close()
        return
