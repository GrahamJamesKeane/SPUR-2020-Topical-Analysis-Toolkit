import re
from collections import Counter
from datetime import datetime
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk import WordNetLemmatizer
from wordcloud import WordCloud
from common_elements import excluded_words, primary_query_words, open_sqlite, output_to_csv, get_region_list, \
    get_uni_list, output_to_png
from nltk.corpus import wordnet

# Set Pandas options to view all entries:
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def get_word_cloud(keywords, title, length, location, filename):
    if length < 5:
        length = 5
    pattern = re.compile(r'\w[\w\-\']+')
    font = {'family': 'Arial',
            'color': 'white',
            'weight': 'bold',
            'size': length * 1.5,
            }
    wordcloud = WordCloud(width=(length * 100), height=(length * 100),
                          background_color='black',
                          min_font_size=10,
                          regexp=pattern,
                          colormap='gist_stern',
                          normalize_plurals=True).generate_from_frequencies(keywords)

    # plot the WordCloud image
    plt.figure(figsize=(length, length), facecolor='black')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title, fontdict=font)
    plt.figure(constrained_layout=True)
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/{location}/{filename}_{stamp}.png"
    wordcloud.to_file(file_name)
    # plt.show()
    plt.close('all')


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
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


# Takes a keyword list as a parameter and returns a dictionary of unique keyword frequencies:
def get_count(keyword_list):
    count = Counter()
    for word in keyword_list:
        count[word] += 1
    return count


# Takes a query as a parameter and returns a keyword list which has been cleaned:
def process_keywords(query):
    c = open_sqlite()
    keyword_list = []
    for row in c.execute(query):
        keyword_list += clean_data(str(row[0]))
    c.close()
    return keyword_list


def build_dictionary(key, data, keyword_frequency, name, category, label):
    item = []
    cat = []
    keywords = []
    freq = []
    for keyword, frequency in keyword_frequency.items():
        if category > 1:
            item.append(name)
        cat.append(key)
        keywords.append(keyword)
        freq.append(frequency)
    if category > 1:
        data[label] += item
    data["Classification"] += cat
    data["Keyword"] += keywords
    data["Frequency"] += freq

    return data


def get_data(category, name, label, data, column, location):
    title = None
    query = None
    print("flag 1")
    for key in primary_query_words:
        print("flag 2")
        if category == 1:
            title = f"{key} TITLE KEYWORDS"
            query = f"SELECT {column} FROM ModuleDetails WHERE A1 = '{key}' or B1 = '{key}';"
        elif category == 2:
            title = f"{key} {name} TITLE KEYWORDS"
            query = f"SELECT {column} FROM ModuleDetails WHERE UniversityName = '{name}' AND " \
                    f"(A1 = '{key}' or B1 = '{key}');"
        elif category == 3:
            title = f"YEAR {name} {key} TITLE KEYWORDS"
            query = f"SELECT ModuleDetails.{column} FROM ModuleDetails INNER JOIN CourseDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE YearOffered = {name} AND (ModuleDetails.A1 = '{key}' " \
                    f"or ModuleDetails.B1 = '{key}');"
        elif category == 4:
            title = f"{name} {key} TITLE KEYWORDS"
            query = f"SELECT ModuleDetails.{column} FROM ModuleDetails INNER JOIN CourseDetails " \
                      f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                      f"WHERE Core = '{name}' AND (ModuleDetails.A1 = '{key}' " \
                      f"or ModuleDetails.B1 = '{key}');"
        print("flag 3")
        # Get a list of keywords:
        keyword_list = process_keywords(query)
        # print(keyword_list)
        print("flag 4")
        # Return the frequency of unique Keywords:
        keyword_frequency = dict(get_count(keyword_list))
        print("flag 5")
        # Get a wordcloud of the keywords:
        # keyword_string = ' '.join(keyword_list)

        length = len(keyword_frequency)
        if length > 1:
            if length < 10:
                length = 10
            elif length > 50:
                length = 50
            filename = f"Primary_{column}_Keywords_Core_{key}"
            get_word_cloud(keyword_frequency, title, length, location, filename)
        print("flag 6")
        # Add keys, keywords, and frequency to dictionary:
        data = build_dictionary(key, data, keyword_frequency, name, category, label)
    print("flag 7")
    return data


# Primary by Modules:
def get_primary_keywords_module_title():
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/ModuleTitle/All"
    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="ModuleTitle",
        location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = "Primary_MT_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_module_title_uni():
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/ModuleTitle/University"
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

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_MT_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_module_title_year():
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/ModuleTitle/Year"
    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="ModuleTitle",
            location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_MT_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_module_title_core():
    label = "Core and Elective Modules"
    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/ModuleTitle/Core"
    filename = f"Primary_MT_Keywords_Core"
    for core in core_list:
        data = get_data(
            category=4,
            name=core,
            label=label,
            data=data,
            column="ModuleTitle",
            location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


# Primary by Overview:
def get_primary_keywords_overview():
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/Overview/All"
    print("flag 1")
    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="Overview",
        location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = "Primary_OV_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_overview_uni():
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/Overview/University"
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

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_OV_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_overview_year():
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/Overview/Year"

    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="Overview",
            location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_OV_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_overview_core():
    label = "Core and Elective Modules"
    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/Overview/Core"

    for core in core_list:
        data = get_data(
            category=4,
            name=core,
            label=label,
            data=data,
            column="Overview",
            location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_OV_Keywords_Core"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


# Primary by Learning Outcomes:
def get_primary_keywords_learning_outcomes():
    data = {"Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/LearningOutcomes/All"

    data = get_data(
        category=1,
        name=None,
        label=None,
        data=data,
        column="LearningOutcomes",
        location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = "Primary_LO_Keywords"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_learning_outcomes_uni():
    label = "University"
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/LearningOutcomes/University"

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

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_LO_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_learning_outcomes_year():
    label = "Year Offered"
    year_list = [1, 2, 3, 4]
    data = {label: [], "Classification": [], "Keyword": [], "Frequency": []}
    location = "Keyword_Analysis/LearningOutcomes/Year"

    for year in year_list:
        data = get_data(
            category=3,
            name=year,
            label=label,
            data=data,
            column="LearningOutcomes",
            location=location)

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_LO_Keywords_{label}"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_primary_keywords_learning_outcomes_core():
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

    # Transfer information to data-frame:
    primary_keywords = pd.DataFrame(data)

    # Output to File:
    filename = f"Primary_LO_Keywords_Core"
    output_to_csv(primary_keywords, filename, location)

    # print(primary_keywords)


def get_secondary_keywords_module_title():
    pass


def get_secondary_keywords_overview():
    pass


def get_secondary_keywords_learning_outcomes():
    pass


def modules_all():
    # Primary by Modules:
    get_primary_keywords_module_title()
    get_primary_keywords_module_title_uni()
    get_primary_keywords_module_title_year()
    get_primary_keywords_module_title_core()

    # Secondary by Module:
    # get_secondary_keywords_module_title()


def overview_all():
    # Primary by Overview:
    get_primary_keywords_overview()
    get_primary_keywords_overview_uni()
    get_primary_keywords_overview_year()
    get_primary_keywords_overview_core()

    # Secondary by Overview:
    # get_secondary_keywords_overview()


def learning_outcomes_all():
    # Primary by Learning Outcomes:
    get_primary_keywords_learning_outcomes()
    get_primary_keywords_learning_outcomes_uni()
    get_primary_keywords_learning_outcomes_year()
    get_primary_keywords_learning_outcomes_core()

    # Secondary by Learning Outcomes:
    # get_secondary_keywords_learning_outcomes()


# modules_all()
overview_all()
# learning_outcomes_all()