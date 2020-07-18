import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from queries import get_keywords_single_class, get_primary_or_secondary_keywords_combined, transfer_to_df, \
    output_to_file


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

primary_query_words = ['APPLIED COMPUTING', 'COMPUTER SYSTEMS ORGANISATION', 'COMPUTING METHODOLOGIES',
                       'GENERAL & REFERENCE', 'HARDWARE', 'HUMAN-CENTERED COMPUTING', 'INFORMATION SYSTEMS',
                       'MATHEMATICS OF COMPUTING', 'NETWORKS', 'SECURITY & PRIVACY', 'SOCIAL & PROFESSIONAL TOPICS',
                       'SOFTWARE & ITS ENGINEERING', 'THEORY OF COMPUTATION', 'UNCLASSIFIABLE']

secondary_query_words = ['ACCESSIBILITY', 'ARCHITECTURES', 'ARTIFICIAL INTELLIGENCE', 'ARTS & HUMANITIES',
                         'COLLABORATIVE & SOCIAL COMPUTING', 'COMMON', 'COMMUNICATION HARDWARE, INTERFACES & STORAGE',
                         'COMPUTATIONAL COMPLEXITY & CRYPTOGRAPHY', 'COMPUTER FORENSICS',
                         'COMPUTER GRAPHICS', 'COMPUTERS IN OTHER DOMAINS', 'COMPUTING / TECHNOLOGY POLICY',
                         'CONCURRENT COMPUTING METHODOLOGIES', 'CONTINUOUS MATHEMATICS',
                         'CROSS-COMPUTING TOOLS & TECHNIQUES', 'CRYPTOGRAPHY', 'DATA MANAGEMENT SYSTEMS',
                         'DATABASE & STORAGE SECURITY', 'DEPENDABLE & FAULT-TOLERANT SYSTEMS & NETWORKS',
                         'DESIGN & ANALYSIS OF ALGORITHMS', 'DISCRETE MATHEMATICS',
                         'DISTRIBUTED COMPUTING METHODOLOGIES', 'DOCUMENT MANAGEMENT & TEXT PROCESSING',
                         'DOCUMENT TYPES', 'EDUCATION', 'ELECTRONIC COMMERCE', 'ELECTRONIC DESIGN AUTOMATION',
                         'EMBEDDED & CYBER-PHYSICAL SYSTEMS', 'EMERGING TECHNOLOGIES', 'ENTERPRISE COMPUTING',
                         'FORMAL LANGUAGES & AUTOMATA THEORY', 'FORMAL METHODS & THEORY OF SECURITY', 'HARDWARE TEST',
                         'HARDWARE VALIDATION', 'HUMAN & SOCIETAL ASPECTS OF SECURITY & PRIVACY',
                         'HUMAN COMPUTER INTERACTION (HCI)', 'INFORMATION RETRIEVAL', 'INFORMATION STORAGE SYSTEMS',
                         'INFORMATION SYSTEMS APPLICATIONS', 'INFORMATION THEORY', 'INTEGRATED CIRCUITS',
                         'INTERACTION DESIGN',
                         'INTRUSION / ANOMALY DETECTION & MALWARE MITIGATION', 'LAW, SOCIAL & BEHAVIORAL SCIENCES',
                         'LIFE & MEDICAL SCIENCES', 'LOGIC', 'MACHINE LEARNING', 'MATHEMATICAL ANALYSIS',
                         'MATHEMATICAL SOFTWARE', 'MODELLING & SIMULATION', 'MODELS OF COMPUTATION',
                         'NETWORK ALGORITHMS', 'NETWORK ARCHITECTURES', 'NETWORK COMPONENTS',
                         'NETWORK PERFORMANCE EVALUATION', 'NETWORK PROPERTIES', 'NETWORK PROTOCOLS',
                         'NETWORK SECURITY', 'NETWORK SERVICES', 'NETWORK TYPES',
                         'OPERATIONS RESEARCH', 'PARALLEL COMPUTING METHODOLOGIES', 'PHYSICAL SCIENCES & ENGINEERING',
                         'POWER & ENERGY', 'PRINTED CIRCUIT BOARDS', 'PROBABILITY & STATISTICS', 'PROFESSIONAL TOPICS',
                         'RANDOMNESS, GEOMETRY & DISCRETE STRUCTURES', 'REAL-TIME SYSTEMS', 'ROBUSTNESS',
                         'SECURITY IN HARDWARE', 'SECURITY SERVICES', 'SEMANTICS & REASONING',
                         'SOFTWARE & APPLICATION SECURITY', 'SOFTWARE CREATION & MANAGEMENT',
                         'SOFTWARE NOTATIONS & TOOLS', 'SOFTWARE ORGANISATION & PROPERTIES',
                         'SYMBOLIC & ALGEBRAIC MANIPULATION', 'SYSTEMS SECURITY',
                         'THEORY & ALGORITHMS FOR APPLICATION DOMAINS', 'UBIQUITOUS & MOBILE COMPUTING',
                         'UNCLASSIFIABLE', 'USER CHARACTERISTICS', 'VERY LARGE SCALE INTEGRATION DESIGN',
                         'VISUALISATION', 'WORLD WIDE WEB']


# Clean strings taken from tables to improve processing
def clean_row(row):
    chars = ['(', ')', '/', '.', ';', ':', ',', '"', '?', '+', '•', '●', '[', ']', '*', '--']
    for char in chars:
        row = row.replace(char, ' ')
    row = row.strip(" .").lower()
    regex = re.compile(r"\s+")
    return re.split(regex, row)


# Sorts the compiled lists above, only used when adding new words to the list
def sort_query_words(list_):
    list_.sort()
    for i in range(len(list_)):
        list_[i] = list_[i].lower()
    print(list(list_))


# Returns a count of unique keywords
def get_count(category_keywords):
    count = Counter()
    for word in category_keywords:
        count[word] += 1
    return count


# Return a plot of the query data
def plot_query(data, query_selection):
    plt.figure(figsize=(12, 5))
    chart = sns.barplot(x='Keyword', y='Frequency', data=data)
    chart.set_xticklabels(
        chart.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='x-large')
    chart.set_title(query_selection)
    plt.show()
    plt.close()


# Selects module title keywords for primary or secondary classifications either in a detailed iterative mode
# or collectively in a combined mode:
def iterate_classifications(category, filter_list, filter_list_flags, mode):
    data = {}

    # Primary Classifications:
    if filter_list["class_col_1"] == "A1" and filter_list["class_col_2"] == "B1":
        for class_query_word in primary_query_words:
            if mode:  # Individual Mode:
                get_data(class_query_word, category, filter_list, filter_list_flags)
            else:  # All mode
                data = get_primary_or_secondary_keywords_combined(class_query_word, category,
                                                                  filter_list, filter_list_flags, data)
    # Secondary Classifications:
    elif filter_list["class_col_1"] == "A2" and filter_list["class_col_2"] == "B2":
        for class_query_word in secondary_query_words:
            if mode:  # Individual Mode:
                get_data(class_query_word, category, filter_list, filter_list_flags)
            else:  # All mode
                data = get_primary_or_secondary_keywords_combined(class_query_word, category,
                                                                  filter_list, filter_list_flags, data)

    if not mode:
        # Transfer information to data-frame:
        category_keyword_df = transfer_to_df(data, filter_list["length"])

        # Output data-frame to .csv
        output_to_file(category_keyword_df)
        print(category_keyword_df)

        # plot function to go here


# Returns the query data with a description for primary or secondary classification queries:
def get_data(class_query_word, category, filter_list, filter_list_flags):
    title_keywords = get_keywords_single_class(class_query_word, category, filter_list, filter_list_flags)
    if title_keywords is not None:
        count = get_count(title_keywords)
        result = f"There are a total of {len(count)} unique keywords in the class {class_query_word} "
        if filter_list_flags["year_offered"]:
            result += f"from modules that are offered in year {filter_list.get('year_offered')} "
        if filter_list_flags["university_name"]:
            result += f"by {filter_list.get('university_name')} "
        if filter_list_flags["semester1"] and filter_list_flags["semester2"]:
            result += "over both semesters "
        elif filter_list_flags["semester1"] and not filter_list_flags["semester2"]:
            result += "in the first semester "
        elif filter_list_flags["semester2"] and not filter_list_flags["semester1"]:
            result += "in the second semester "
        if filter_list_flags.get("core"):
            if filter_list.get('core'):
                result += f"which are core modules "
            else:
                result += f"which are optional modules "
        if filter_list_flags.get("course"):
            result += f"in the programme {filter_list.get('course')}"
        print(result + ".")
        print("-------------------")
        count_length = None
        if len(count) > filter_list.get("length"):
            count_length = filter_list.get("length")
            print(f"The {count_length} most common keywords are: ")
        else:
            count_length = len(count)
        data = pd.DataFrame(Counter(count).most_common(count_length), columns=["Keyword", "Frequency"],
                            index=range(1, count_length + 1))
        print(data)
        print("-------------------")
        plot_query(data, class_query_word)


# Returns a query word selected by the user for primary & secondary classifications when the individual
# option is selected
def get_query_word(class_key_1, class_key_2):
    print("Please enter a Classification")
    if class_key_1 and class_key_2 in ["A1", "B1"]:
        for i in range(len(primary_query_words)):
            print(str(i + 1) + ":    " + primary_query_words[i])
        query_input = int(input())
        if type(query_input) == int:
            return primary_query_words[query_input - 1]
    elif class_key_1 and class_key_2 in ["A2", "B2"]:
        for i in range(len(secondary_query_words)):
            print(str(i + 1) + ":    " + secondary_query_words[i])
        query_input = int(input())
        if type(query_input) == int:
            return secondary_query_words[query_input - 1]

# sort_query_words(excluded_words)
