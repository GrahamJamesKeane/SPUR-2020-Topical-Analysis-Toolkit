import re
from collections import Counter
from datetime import datetime
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk import WordNetLemmatizer
from wordcloud import WordCloud
from common_elements import excluded_words, primary_query_words, open_sqlite, output_to_csv, get_region_list, \
    get_uni_list, check_dir_exists
from nltk.corpus import wordnet
import time
from pathlib import Path

# Set Pandas options to view all entries:
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

process_message_1 = "Fetching Keyword Data..."
process_message_2 = "Building Query..."
process_message_3 = "Processing Keywords..."
process_message_4 = "Computing Keyword Frequencies..."
process_message_5 = "Generating WordCloud..."
process_message_6 = "Generating Dictionary..."
process_message_7 = "Transferring to Dataframe..."
process_message_8 = "Saving to File..."


# Returns a wordcloud image based on the keyword frequency set provided:
def get_word_cloud(keywords, length, location, filename):
    print(process_message_5)

    check_dir_exists(location)

    pattern = re.compile(r'\w[\w\-\']+')

    wordcloud = WordCloud(width=(length * 25), height=(length * 25),
                          background_color='black',
                          min_font_size=10,
                          regexp=pattern,
                          colormap='gist_stern',
                          normalize_plurals=True).generate_from_frequencies(keywords)

    # plot the WordCloud image
    plt.figure(figsize=(length, length), facecolor='black')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.figure(constrained_layout=True)

    # Output to File:
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output/{location}/{filename}_{stamp}.png"
    wordcloud.to_file(file_name)
    # plt.show()  # Only required for testing
    plt.close('all')


# Map POS tag to first character lemmatize() accepts: the tag is required for the function to find the root of a given
# word
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


# Takes a string as a parameter and removes unwanted special characters, digits, & whitespace; transforms the string
# to lowercase, removes excluded words, and returns a keyword list:
def clean_data(text):
    lemmatizer = WordNetLemmatizer()
    keyword_list = []
    pattern = re.compile(r'[^\w+\-?\w+]')
    text = re.sub(pattern, ' ', text)
    pattern = re.compile(r'(?<=\s)-+(?=\s?)')
    text = re.sub(pattern, ' ', text)
    pattern = re.compile(r'(?<=\w)-+(?=\s+)')
    text = re.sub(pattern, ' ', text)
    text = text.strip(" ").lower()
    regex = re.compile(r"\s+")
    tokens = re.split(regex, text)
    for keyword in tokens:
        key_lemma = lemmatizer.lemmatize(keyword, get_wordnet_pos(keyword))
        if key_lemma not in excluded_words:
            keyword_list.append(key_lemma)
    return keyword_list


# Takes a keyword list as a parameter and returns a dictionary of unique keyword frequencies for get_data():
def get_count(keyword_list):
    print(process_message_4)
    count = Counter()
    for word in keyword_list:
        count[word] += 1
    return count


# Takes a query as a parameter and returns a keyword list which has been cleaned for get_data():
def process_keywords(query):
    print(process_message_3)
    c = open_sqlite()
    keyword_list = []
    for row in c.execute(query):
        keyword_list += clean_data(str(row[0]))
    c.close()
    return keyword_list


# Dictionary constructor for get_data():
def build_dictionary(key, data, keyword_frequency, name, category, label):
    print(process_message_6)
    item = []
    cat = []
    keywords = []
    freq = []
    for keyword, frequency in keyword_frequency.items():
        cat.append(key)
        keywords.append(keyword)
        freq.append(frequency)
        if category > 1:
            item.append(name)
    if category > 1:
        data[label] += item
    data["Classification"] += cat
    data["Keyword"] += keywords
    data["Frequency"] += freq

    return data


# Selectively executes the parameters of each keyword function and returns a dictionary:
# For each set of parameters given, the function iterates through the list of primary classifications and
# generates a query for each classification. The information is cleaned and then a frequency table of unique
# keywords generated. The frequency table is sent to the wordcloud generator after which the function constructs
# a dictionary for the purpose of transferring the data to a Dataframe.
def get_data(category, name, label, data, column, location):
    print(process_message_2)
    query = None
    filename = None
    for key in primary_query_words:
        if category == 1:
            filename = f"{key} TITLE KEYWORDS"
            query = f"SELECT {column} FROM ModuleDetails WHERE A1 = '{key}' or B1 = '{key}';"
        elif category == 2:
            filename = f"{key} {name} TITLE KEYWORDS"
            query = f"SELECT {column} FROM ModuleDetails WHERE UniversityName = '{name}' AND " \
                    f"(A1 = '{key}' or B1 = '{key}');"
        elif category == 3:
            filename = f"YEAR {name} {key} TITLE KEYWORDS"
            query = f"SELECT ModuleDetails.{column} FROM ModuleDetails INNER JOIN CourseDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE YearOffered = {name} AND (ModuleDetails.A1 = '{key}' " \
                    f"or ModuleDetails.B1 = '{key}');"
        elif category == 4:
            filename = f"{name} {key} TITLE KEYWORDS"
            query = f"SELECT ModuleDetails.{column} FROM ModuleDetails INNER JOIN CourseDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE Core = '{name}' AND (ModuleDetails.A1 = '{key}' " \
                    f"or ModuleDetails.B1 = '{key}');"

        # Get a list of keywords:
        keyword_list = process_keywords(query)

        # Return the frequency of unique Keywords:
        keyword_frequency = dict(get_count(keyword_list))

        # Get a wordcloud of the keywords:
        length = len(keyword_frequency)
        if length > 1:
            if length < 10:
                length = 10
            elif length > 50:
                length = 50
            get_word_cloud(keyword_frequency, length, location, filename)

        # Add keys, keywords, and frequency to dictionary:
        data = build_dictionary(key, data, keyword_frequency, name, category, label)

    return data


# The following functions set-out the parameters necessary to view keyword frequencies based on classification
# for the ModuleTitle, Overview, and LearningOutcomes columns of the database:

# Primary by Modules:
def get_primary_keywords_module_title():
    start_time = time.time()
    print(process_message_1)
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Output_files/Keyword_Analysis/ModuleTitle/All"

    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="ModuleTitle",
        location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = "Primary_MT_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_module_title_uni():
    start_time = time.time()
    print(process_message_1)
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output_files/Keyword_Analysis/ModuleTitle/University"

    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        for uni in uni_list:
            data = get_data(
                category=2,
                name=uni,
                label=label,
                data=data,
                column="ModuleTitle",
                location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_MT_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_module_title_year():
    start_time = time.time()
    print(process_message_1)
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output_files/Keyword_Analysis/ModuleTitle/Year"
    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="ModuleTitle",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_MT_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_module_title_core():
    start_time = time.time()
    print(process_message_1)
    label = "Core and Elective Modules"
    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output_files/Keyword_Analysis/ModuleTitle/Core"
    filename = f"Primary_MT_Keywords_Core"
    for core in core_list:
        data = get_data(
            category=4,
            name=core,
            label=label,
            data=data,
            column="ModuleTitle",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# Primary by Overview:
def get_primary_keywords_overview():
    start_time = time.time()
    print(process_message_1)
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/Overview/All"

    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="Overview",
        location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = "Primary_OV_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_overview_uni():
    start_time = time.time()
    print(process_message_1)
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/Overview/University"
    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        for uni in uni_list:
            data = get_data(
                category=2,
                name=uni,
                label=label,
                data=data,
                column="Overview",
                location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_OV_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_overview_year():
    start_time = time.time()
    print(process_message_1)
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/Overview/Year"

    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="Overview",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_OV_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_overview_core():
    start_time = time.time()
    print(process_message_1)
    label = "Core and Elective Modules"
    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/Overview/Core"

    for core in core_list:
        data = get_data(
            category=4,
            name=core,
            label=label,
            data=data,
            column="Overview",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_OV_Keywords_Core"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# Primary by Learning Outcomes:
def get_primary_keywords_learning_outcomes():
    start_time = time.time()
    print(process_message_1)
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/LearningOutcomes/All"

    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="LearningOutcomes",
        location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = "Primary_LO_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_learning_outcomes_uni():
    start_time = time.time()
    print(process_message_1)
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/LearningOutcomes/University"

    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        for uni in uni_list:
            data = get_data(
                category=2,
                name=uni,
                label=label,
                data=data,
                column="LearningOutcomes",
                location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_LO_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_learning_outcomes_year():
    start_time = time.time()
    print(process_message_1)
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Output/Keyword_Analysis/LearningOutcomes/Year"

    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="LearningOutcomes",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_LO_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_keywords_learning_outcomes_core():
    start_time = time.time()
    print(process_message_1)
    label = "Core and Elective Modules"
    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/LearningOutcomes/Core"

    for core in core_list:
        data = get_data(
            category=4,
            name=core,
            label=label,
            data=data,
            column="LearningOutcomes",
            location=location)

    print(process_message_7)
    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    print(process_message_8)
    # Output to File:
    filename = f"Primary_LO_Keywords_Core"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)  # Only required for testing
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# Secondary by Modules:
def get_secondary_keywords_module_title():
    pass


# Secondary by Overview:
def get_secondary_keywords_overview():
    pass


# Secondary by Learning Outcomes:
def get_secondary_keywords_learning_outcomes():
    pass


# Master Functions:
def modules_all():
    # Primary by Modules:
    get_primary_keywords_module_title()
    get_primary_keywords_module_title_uni()
    get_primary_keywords_module_title_year()
    get_primary_keywords_module_title_core()

    # Secondary by Module:
    # get_secondary_keywords_module_title()  # Not yet available


def overview_all():
    # Primary by Overview:
    get_primary_keywords_overview()
    get_primary_keywords_overview_uni()
    get_primary_keywords_overview_year()
    get_primary_keywords_overview_core()

    # Secondary by Overview:
    # get_secondary_keywords_overview()  # Not yet available


def learning_outcomes_all():
    # Primary by Learning Outcomes:
    get_primary_keywords_learning_outcomes()
    get_primary_keywords_learning_outcomes_uni()
    get_primary_keywords_learning_outcomes_year()
    get_primary_keywords_learning_outcomes_core()

    # Secondary by Learning Outcomes:
    # get_secondary_keywords_learning_outcomes()  # Not yet available

# modules_all()  # Only required for testing
# overview_all()  # Only required for testing
# learning_outcomes_all()  # Only required for testing
