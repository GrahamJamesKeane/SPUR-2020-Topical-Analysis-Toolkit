import inspect
import os
import pathlib
import sqlite3
import pandas as pd
from datetime import datetime


# Open a connection to the database:
def open_sqlite():
    conn = sqlite3.connect('acm_curricula_2020_spur.db')
    c = conn.cursor()
    return c


def get_p_classifications():
    c = open_sqlite()
    p_list = []
    query = f"SELECT PrimaryClassification FROM Classifications " \
            f"GROUP BY PrimaryClassification;"
    for row in c.execute(query):
        p_list.append(str(row[0]))
    c.close()
    return p_list


def get_s_classifications():
    c = open_sqlite()
    s_list = []
    query = f"SELECT SecondaryClassification FROM Classifications " \
            f"ORDER BY SecondaryClassification;"
    for row in c.execute(query):
        s_list.append(str(row[0]))
    c.close()
    return s_list


primary_query_words = get_p_classifications()

secondary_query_words = get_s_classifications()

excluded_words = ['&', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'able', 'about', 'achieved', 'administer',
                  'adv', 'against', 'aim', 'aims', 'all', 'allow', 'almost', 'also', 'an', 'and', 'any', 'any', 'apply',
                  'appreciate', 'approaches', 'appropriate', 'are', 'arise', 'around', 'as', 'aspects', 'assess',
                  'associated', 'at', 'attain', 'attention', 'based', 'based', 'basic', 'basis', 'be', 'before',
                  'begin', 'better', 'between', 'both', 'by', 'ca', 'can', 'carry', 'challenges', 'comes', 'completion',
                  'compt', 'concepts', 'course', 'covering', 'cs', 'csse', 'define', 'depend', 'describe', 'different',
                  'do', 'drawn', 'ds', 'e', 'each', 'each', 'equip', 'error', 'especially', 'evaluate', 'explain',
                  'exam',
                  'final', 'find', 'findings', 'firm', 'first', 'focuses', 'for', 'from', 'fyp', 'g', 'give', 'given',
                  'gives', 'goal', 'goals', 'grasp', 'has', 'have', 'having', 'help', 'higher', 'hon', 'how', 'i',
                  'identify', 'ii', 'iii', 'importance', 'important', 'in', 'include', 'includes', 'including',
                  'into', 'intro', 'introduce', 'introduces', 'introducing', 'introduction', 'involving', 'is',
                  'issues', 'it', 'its', 'know', 'knowledge', 'known', 'large', 'learn', 'lectures', 'level', 'lo1',
                  'lo1', 'lo2', 'lo3', 'lo4', 'lo5', 'lo6', 'lo7', 'lost', 'make', 'makes', 'may', 'meant', 'merits',
                  'might', 'module', 'more', 'most', 'multiple', 'near', 'necessary', 'need', 'never', 'new', 'no',
                  'none', 'objective', 'objectives', 'of', 'on', 'one', 'or', 'other', 'others', 'our', 'out',
                  'overcome', 'own', 'p', 'part', 'particular', 'paying', 'perform', 'persuasive', 'practical',
                  'previous',
                  'problems', 'prove', 'provide', 'provision', 'pure', 'related', 'relevance', 'relevant',
                  'requirements', 's', 'sci', 'seen', 'seminars', 'sense', 'several', 'should', 'significantly',
                  'simple',
                  'single', 'small', 'so', 'solve', 'some', 'specific', 'starting', 'stopping', 'student', 'students',
                  'substantive', 'successful', 'such', 'suitable', 'syllabus', 'take', 'teach', 'terms', 'than', 'that',
                  'the', 'their', 'them', 'themselves', 'these', 'they', 'thing', 'third', 'this', 'those', 'through',
                  'timely', 'to',
                  'together', 'topics', 'two', 'typed', 'types', 'ug', 'ui', 'understand', 'understanding', 'unseen',
                  'up', 'us', 'use', 'used', 'uses', 'using', 'ux', 'value', 'variety', 'various', 'view', 'was',
                  'ways', 'we', 'well', 'when', 'what', 'where', 'whether', 'which', 'while', 'wide', 'will', 'with',
                  'within',
                  'without', 'work', 'workshops', 'write', 'year']

year_list = [1, 2, 3, 4]
core_list = ['CORE', 'ELECTIVE']


# This is only used when adding new words to the excluded_words list:
# It alphabetically sorts the entries and transforms them to lowercase
def alphabetically_sort_text_lists(text_list):
    text_list.sort()
    for i in range(len(text_list)):
        text_list[i] = text_list[i].lower()
    print(list(text_list))


# Check if directory exists and create location if not for saving files:
def check_dir_exists(location):
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    new_folder = f"{currentdir}/Output/{location}/"

    if not os.path.exists(new_folder):
        pathlib.Path(new_folder).mkdir(parents=True, exist_ok=True)


def output_to_png(fig, filename, location):
    check_dir_exists(location)
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output/{location}/{filename}_{stamp}.png"
    fig.savefig(file_name)


def output_to_csv(database, filename, location):
    check_dir_exists(location)
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output/{location}/{filename}_{stamp}.csv"
    database.to_csv(file_name)


def get_region_list():
    c = open_sqlite()
    region_list = []
    query = f"SELECT Country FROM University GROUP BY Country;"
    for row in c.execute(query):
        region_list.append(str(row[0]))
    c.close()
    return region_list


def get_course_list():
    c = open_sqlite()
    course_list = []
    query = f"SELECT CourseCode FROM Course GROUP BY CourseCode;"
    for row in c.execute(query):
        course_list.append(str(row[0]))
    c.close()
    return course_list


def get_uni_list():
    c = open_sqlite()
    uni_list = []
    query = f"SELECT UniversityName FROM University " \
            f"ORDER BY UniversityName;"
    for row in c.execute(query):
        uni_list.append(str(row[0]))
    c.close()
    return uni_list


# Set Pandas options to view all row and column entries (Viewed in python console):
def set_max_rows_pandas():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

# alphabetically_sort_text_lists(excluded_words)  # Only needed to sort word_lists
