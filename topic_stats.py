import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import analysis_module
from datetime import datetime

from queries import output_to_file

y_label = "Frequency"


def open_sqlite():
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    c = conn.cursor()
    return c


# Return a Plot of the Query Data
def get_simple_barplot(data, x_label, title):
    plt.figure(figsize=(24, 10))
    sns.set_style("whitegrid")
    chart = sns.catplot(
        x=f"{x_label}",
        y=f"{y_label}",
        data=data,
        kind='bar',
        height=8,
        aspect=2,
        palette="Paired")
    chart.set_xticklabels(
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    plt.title(title)
    # plt.show()
    output_to_png(chart, title)
    plt.close()


def get_heatmap(stats, x1_label, x2_label, title, width, height, annot):
    # sns.set_style("darkgrid")
    sns.set()
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    stats_2 = stats.pivot(x2_label, x1_label, y_label)
    # shape = stats_2.shape
    f, ax = plt.subplots(figsize=(width, height))
    g = sns.heatmap(
        stats_2,
        square=True,
        ax=ax,
        cbar_kws={'fraction': 0.01},
        annot=annot,
        fmt='d',
        cmap='OrRd')
    g.set_xticklabels(
        g.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    g.set_yticklabels(
        g.get_yticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    plt.title(title, fontdict=font)
    ax.set_ylabel('')
    ax.set_xlabel('')
    # plt.show()
    output_to_png(f, title)
    plt.close()


def get_barplot(stats, x1_label, x2_label, title, height, aspect):
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }

    plt.figure(figsize=(24, 10))
    sns.set_style("whitegrid")
    chart = sns.catplot(
        x=x1_label,
        y=y_label,
        hue=x2_label,
        data=stats,
        kind='bar',
        height=height,
        aspect=aspect,
        legend_out=False,
        palette="Paired")
    chart.set_xticklabels(
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    plt.title(title, fontdict=font)
    plt.legend(
        title=x2_label,
        bbox_to_anchor=(1, 1),
        loc=2,
        borderaxespad=0.)
    # plt.show()
    output_to_png(chart, title)
    plt.close()


def output_to_png(fig, name):
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/{name}_{stamp}.png"
    fig.savefig(file_name)


# Populates and Returns a List of Category, Classification and Frequency to Build a Dataframe:
# Category Specifies University, Course, Year,
# Level Specifies Primary or Secondary
def get_pop_lists(item_list, category, level):
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    item_column = []
    if level == 1:
        word_list = analysis_module.primary_query_words
        class_1 = "A1"
        class_2 = "B1"
    elif level == 2:
        word_list = analysis_module.secondary_query_words
        class_1 = "A2"
        class_2 = "B2"

    for item in item_list:
        class_dic = {}
        class_list = []

        if level == 2:
            # Where secondary classification is COMMON, add the subclasses of the primary classification to the count:
            if category == 1:  # University:
                query_a1 = f"SELECT A1 FROM ModuleDetails WHERE UniversityName = '{item}' AND A2 = 'COMMON';"
                query_b1 = f"SELECT B1 FROM ModuleDetails WHERE UniversityName = '{item}' AND B2 = 'COMMON';"
            elif category == 2:  # Course:
                query_a1 = f"SELECT ModuleDetails.A1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE CourseCode = '{item}' AND ModuleDetails.A2 = 'COMMON';"
                query_b1 = f"SELECT ModuleDetails.B1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE CourseCode = '{item}' AND ModuleDetails.B2 = 'COMMON';"
            elif category == 3:  # Year Offered
                query_a1 = f"SELECT ModuleDetails.A1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE YearOffered = {item} AND ModuleDetails.A2 = 'COMMON';"
                query_b1 = f"SELECT ModuleDetails.B1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE YearOffered = {item} AND ModuleDetails.B2 = 'COMMON';"
            elif category == 4:  # Core
                query_a1 = f"SELECT ModuleDetails.A1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE Core = '{item}' AND ModuleDetails.A2 = 'COMMON';"
                query_b1 = f"SELECT ModuleDetails.B1 FROM ModuleDetails INNER JOIN CourseDetails " \
                           f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"WHERE Core = '{item}' AND ModuleDetails.B2 = 'COMMON';"

            for row in c.execute(query_a1):
                word = str(row[0])
                class_list.append(word)

            for row in c.execute(query_b1):
                word = str(row[0])
                class_list.append(word)

            for selection in class_list:
                query_2 = f"SELECT SecondaryClassification FROM Classifications " \
                          f"WHERE PrimaryClassification = '{selection}';"
                for value in c.execute(query_2):
                    word = str(value[0])
                    if word in class_dic:
                        class_dic[word] += 1
                    else:
                        class_dic[word] = 1

        for word in word_list:
            if word != 'COMMON':
                if category == 1:  # University:
                    query_3 = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails " \
                              f"WHERE UniversityName = '{item}' AND {class_1} = '{word}' or {class_2} = '{word}';"
                elif category == 2:  # Course:
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE CourseCode = '{item}' AND (ModuleDetails.{class_1} = '{word}' " \
                              f"or ModuleDetails.{class_2} = '{word}');"
                elif category == 3:  # Year Offered
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE YearOffered = {item} AND (ModuleDetails.{class_1} = '{word}' " \
                              f"or ModuleDetails.{class_2} = '{word}');"
                elif category == 4:  # Core:
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE Core = '{item}' AND (ModuleDetails.{class_1} = '{word}' " \
                              f"or ModuleDetails.{class_2} = '{word}');"

                for row in c.execute(query_3):
                    if word in class_dic:
                        class_dic[word] += row[0]
                    else:
                        class_dic[word] = row[0]

        for key, value in class_dic.items():
            classification.append(key)
            frequency.append(value)
            item_column.append(item)
    c.close()
    return [item_column, classification, frequency]


def get_region_list():
    c = open_sqlite()
    region_list = []
    query = f"SELECT Country FROM Universities ORDER BY Country;"
    for row in c.execute(query):
        region_list.append(str(row[0]))
    c.close()
    return region_list


def get_uni_list(region):
    c = open_sqlite()
    uni_list = []
    query = f"SELECT UniversityName FROM Universities " \
            f"WHERE Country = '{region}' ORDER BY UniversityName;"
    for row in c.execute(query):
        uni_list.append(str(row[0]))
    c.close()
    return uni_list


def get_course_list():
    c = open_sqlite()
    course_list = []
    query = f"SELECT CourseCode FROM CourseList ORDER BY CourseCode;"
    for row in c.execute(query):
        course_list.append(str(row[0]))
    c.close()
    return course_list


# Transform Query Output into Dataframe
def get_output(result, label_1, label_2):
    # Generate Query Output Dictionary:
    stats_d = {label_2: result[0], label_1: result[1], y_label: result[2]}

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype:
    stats[label_1] = stats[label_1].astype('category')
    stats[label_2] = stats[label_2].astype('category')
    stats[y_label] = stats[y_label].astype('int32')

    return stats


def get_primary_popularity():
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    for word in analysis_module.primary_query_words:
        query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A1 = '{word}' or B1 = '{word}';"
        classification.append(word)
        for row in c.execute(query):
            frequency.append(row[0])

    # Column Label & Graph Title:
    x_label = "Classification"
    title = "Primary Classification Popularity by Module"

    # Generate Query Output Dictionary:
    stats_2d = {x_label: classification, y_label: frequency}

    # Generate Data-Frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[x_label] = stats[x_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, x_label, title)

    # Order the Dataset:
    stats.set_index(x_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    print(stats)

    c.close()
    return stats


def get_secondary_popularity():
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    class_list = []
    class_dic = {}

    # Where secondary classification is COMMON, add the subclasses of the primary classification to the count:
    query_1 = f"SELECT A1 FROM ModuleDetails WHERE A2 = 'COMMON';"
    for row in c.execute(query_1):
        word = str(row[0])
        class_list.append(word)
    query_1 = f"SELECT B1 FROM ModuleDetails WHERE B2 = 'COMMON';"
    for row in c.execute(query_1):
        word = str(row[0])
        class_list.append(word)

    for item in class_list:
        query_2 = f"SELECT SecondaryClassification FROM Classifications WHERE PrimaryClassification = '{item}';"
        for value in c.execute(query_2):
            word = str(value[0])
            if word in class_dic:
                class_dic[word] += 1
            else:
                class_dic[word] = 1

    for word in analysis_module.secondary_query_words:
        if word != 'COMMON':
            query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A2 = '{word}' or B2 = '{word}';"
            for row in c.execute(query):
                if word in class_dic:
                    class_dic[word] += row[0]
                else:
                    class_dic[word] = row[0]

    for key, value in class_dic.items():
        classification.append(key)
        frequency.append(value)

    # Column Label & Graph Title:
    x_label = "Classification"
    title = "Secondary Classification Popularity by Module"

    # Generate Query Output Dictionary:
    stats_2d = {x_label: classification, y_label: frequency}

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[x_label] = stats[x_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, x_label, title)

    # Order the Dataset:
    stats.set_index(x_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    print(stats)

    c.close()
    return stats


def get_primary_popularity_per_university():
    # Generate a List of Available Regions:
    region_list = get_region_list()
    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        # Collate the Query Data into the Following Lists:
        result = get_pop_lists(uni_list, 1, 1)

        # Column Labels & Graph Title:
        x1_label = "Primary Classification"
        x2_label = "University"
        title = "Primary Classification Popularity by University"

        # Get Dataset:
        stats = get_output(result, x1_label, x2_label)

        # Plot the Dataset:
        get_barplot(stats, x1_label, x2_label, title, 8, 2)

        # Order the Dataset:
        stats.set_index(x1_label, inplace=True)
        stats = stats.sort_values(by=y_label, ascending=False)

        print(stats)

        return stats


def get_secondary_popularity_per_university():
    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        # Collate the Query Data into the Following Lists:
        result = get_pop_lists(uni_list, 1, 2)

        # Column Labels & Graph Title:
        x1_label = "Secondary Classification"
        x2_label = "University"
        title = "Secondary Classification Popularity by University"

        # Get Dataset:
        stats = get_output(result, x1_label, x2_label)

        # Plot the Dataset:
        get_heatmap(stats, x1_label, x2_label, title, 20, 9, True)

        # Order the dataset:
        stats.set_index(x1_label, inplace=True)
        stats = stats.sort_values(by=y_label, ascending=False)

        print(stats)

        return stats


def get_primary_popularity_by_course():
    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 1)

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "Course"
    title = "Primary Classification Popularity by Course"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2)
    get_heatmap(stats, x1_label, x2_label, title, 6, 9, True)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_secondary_popularity_by_course():
    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 2)

    # Column Labels & Graph Title:
    x1_label = "Classification"
    x2_label = "Course"
    title = "Secondary Classification Popularity by Course"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_heatmap(stats, x1_label, x2_label, title, 20, 9, True)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_primary_popularity_by_year():
    year_list = [1, 2, 3, 4]

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(year_list, 3, 1)

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "Year"
    title = "Primary Classification Popularity by Year"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2)
    get_heatmap(stats, x1_label, x2_label, title, 10, 7, True)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_secondary_popularity_by_year():
    year_list = [1, 2, 3, 4]

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(year_list, 3, 2)

    # Column Labels & Graph Title:
    x1_label = "Secondary Classification"
    x2_label = "Year"
    title = "Secondary Classification Popularity by Year"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_heatmap(stats, x1_label, x2_label, title, 20, 7, False)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_primary_popularity_by_core():
    core_list = ['CORE', 'ELECTIVE']

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 1)

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "Core"
    title = "Primary Classification Popularity by Core and Elective Modules"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2)
    get_heatmap(stats, x1_label, x2_label, title, 10, 5, True)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_secondary_popularity_by_core():
    core_list = ['CORE', 'ELECTIVE']

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 2)

    # Column Labels & Graph Title:
    x1_label = "Secondary Classification"
    x2_label = "Core"
    title = "Secondary Classification Popularity by Core and  Elective Modules"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 9, 2)
    get_heatmap(stats, x1_label, x2_label, title, 20, 6, True)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    return stats


def get_stats():
    # Overall Topic Popularity:
    p_mod_stats = get_primary_popularity()
    s_mod_stats = get_secondary_popularity()
    output_to_file(p_mod_stats)
    output_to_file(s_mod_stats)

    # By University:
    p_uni_stats = get_primary_popularity_per_university()
    s_uni_stats = get_secondary_popularity_per_university()
    output_to_file(p_uni_stats)
    output_to_file(s_uni_stats)

    # By Course:
    p_course_stats = get_primary_popularity_by_course()
    s_course_stats = get_secondary_popularity_by_course()
    output_to_file(p_course_stats)
    output_to_file(s_course_stats)

    # By Year:
    p_year_stats = get_primary_popularity_by_year()
    s_year_stats = get_secondary_popularity_by_year()
    output_to_file(p_year_stats)
    output_to_file(s_year_stats)

    # By Core:
    p_core_stats = get_primary_popularity_by_core()
    s_core_stats = get_secondary_popularity_by_core()
    output_to_file(p_core_stats)
    output_to_file(s_core_stats)

# get_stats()
# get_primary_popularity_per_university()
# get_secondary_popularity_per_university()
# get_primary_popularity_by_course()
# get_secondary_popularity_by_course()
# get_primary_popularity_by_year()
# get_secondary_popularity_by_year()
# get_primary_popularity_by_core()
# get_secondary_popularity_by_core()
