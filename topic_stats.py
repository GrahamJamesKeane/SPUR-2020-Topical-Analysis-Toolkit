import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_module import primary_query_words, secondary_query_words
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
    chart = sns.catplot(x=f"{x_label}", y=f"{y_label}", data=data, kind='bar', height=8, aspect=2)
    chart.set_xticklabels(
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    # chart.set_title(query_selection)
    plt.title(title)
    plt.show()
    output_to_png(chart, title)
    plt.close()


def get_heatmap(stats, x1_label, x2_label, title, width, height):
    sns.set_style("darkgrid")
    sns.set()
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    stats_2 = stats.pivot(x2_label, x1_label, y_label)
    shape = stats_2.shape
    f, ax = plt.subplots(figsize=(width, height))
    g = sns.heatmap(stats_2, square=True, ax=ax, cbar_kws={'fraction': 0.01})
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
    plt.show()
    output_to_png(f, title)
    plt.close()


def get_barplot(stats, x1_label, x2_label, title):
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
        height=8,
        aspect=2,
        legend_out=False,
        palette="Paired")
    chart.set_xticklabels(
        rotation=45,
        horizontalalignment='right',
        fontweight='book',
        fontsize='small')
    plt.title(title, fontdict=font)
    plt.legend(title=x2_label, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.show()
    output_to_png(chart, title)
    plt.close()


def output_to_png(fig, name):
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/{name}_{stamp}.png"
    fig.savefig(file_name)


def get_primary_popularity():
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    for word in primary_query_words:
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
    for word in secondary_query_words:
        query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A2 = '{word}' or B2 = '{word}';"
        classification.append(word)
        for row in c.execute(query):
            frequency.append(row[0])

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
    c = open_sqlite()

    # Generate a List of Available Universities:
    uni_list = []
    query = f"SELECT UniversityName FROM Universities ORDER BY UniversityName;"
    for row in c.execute(query):
        uni_list.append(str(row[0]))

    # Collate the Query Data into the Following Lists:
    uni_columns = []
    classification = []
    frequency = []
    for uni in uni_list:
        for word in primary_query_words:
            query = f"SELECT COUNT(ModuleCode) FROM ModuleDetails WHERE UniversityName = '{uni}' AND A1 = '{word}' or B1 = '{word}';"
            uni_columns.append(uni)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "University"
    title = "Primary Classification Popularity by University"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: uni_columns, x1_label: classification, y_label: frequency}

    # Generate Data-Frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype as Categorical:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title)

    # Order the Dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    print(stats)

    c.close()
    return stats


def get_secondary_popularity_per_university():
    c = open_sqlite()

    # Generate a List of Available Universities:
    uni_list = []
    query = f"SELECT UniversityName FROM Universities ORDER BY UniversityName;"
    for row in c.execute(query):
        uni_list.append(str(row[0]))

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    uni_columns = []
    for uni in uni_list:
        for word in secondary_query_words:
            query = f"SELECT COUNT(ModuleCode) FROM ModuleDetails WHERE UniversityName = '{uni}' AND A2 = '{word}' or B2 = '{word}';"
            uni_columns.append(uni)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Secondary Classification"
    x2_label = "University"
    title = "Secondary Classification Popularity by University"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: uni_columns, x1_label: classification, y_label: frequency}

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')
    stats[y_label] = stats[y_label].astype('int32')

    # Plot the Dataset:
    get_heatmap(stats, x1_label, x2_label, title, 20, 9)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    print(stats)

    c.close()
    return stats


def get_primary_popularity_by_course():
    c = open_sqlite()

    # Generate a List of Available Courses:
    course_list = []
    query = f"SELECT CourseCode FROM CourseList ORDER BY CourseCode;"
    for row in c.execute(query):
        course_list.append(str(row[0]))

    # Collate the Query Data into the Following Lists:
    course_columns = []
    classification = []
    frequency = []
    for course in course_list:
        for word in primary_query_words:
            query = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE CourseCode = '{course}' AND (ModuleDetails.A1 = '{word}' or ModuleDetails.B1 = '{word}');"
            course_columns.append(course)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "Course"
    title = "Primary Classification Popularity by Course"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: course_columns, x1_label: classification, y_label: frequency}

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype as Categorical:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title)
    get_heatmap(stats, x1_label, x2_label, title, 6, 9)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    c.close()
    return stats


def get_secondary_popularity_by_course():
    c = open_sqlite()

    # Generate a list of available courses:
    course_list = []
    query = f"SELECT CourseCode FROM CourseList ORDER BY CourseCode;"
    for row in c.execute(query):
        course_list.append(str(row[0]))

    # Collate the query data into the following Lists:
    classification = []
    frequency = []
    course_columns = []
    for course in course_list:
        for word in secondary_query_words:
            query = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE CourseCode = '{course}' AND (ModuleDetails.A2 = '{word}' or ModuleDetails.B2 = '{word}');"
            course_columns.append(course)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Classification"
    x2_label = "Course"
    title = "Secondary Classification Popularity by Course"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: course_columns, x1_label: classification, y_label: frequency}

    # Generate Dataframe from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype as Categorical:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')
    stats[y_label] = stats[y_label].astype('int32')

    # Plot the Dataset:
    get_heatmap(stats, x1_label, x2_label, title, 20, 9)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    c.close()
    return stats


def get_primary_popularity_by_year():
    c = open_sqlite()

    # Collate the query data into the following Lists:
    year_list = [1, 2, 3, 4]
    classification = []
    frequency = []
    year_columns = []
    for year in year_list:
        for word in primary_query_words:
            query = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE YearOffered = {year} AND (ModuleDetails.A1 = '{word}' or ModuleDetails.B1 = '{word}');"
            year_columns.append(year)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Primary Classification"
    x2_label = "Year"
    title = "Primary Classification Popularity by Year"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: year_columns, x1_label: classification, y_label: frequency}

    # Generate Dataframe from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype as Categorical:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')
    stats[y_label] = stats[y_label].astype('int32')

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title)
    get_heatmap(stats, x1_label, x2_label, title, 10, 5)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    c.close()
    return stats


def get_secondary_popularity_by_year():
    c = open_sqlite()

    # Collate the query data into the following Lists:
    year_list = [1, 2, 3, 4]
    classification = []
    frequency = []
    year_column = []
    for year in year_list:
        for word in secondary_query_words:
            query = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                    f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                    f"WHERE YearOffered = {year} AND (ModuleDetails.A2 = '{word}' or ModuleDetails.B2 = '{word}');"
            year_column.append(year)
            classification.append(word)
            for row in c.execute(query):
                frequency.append(row[0])

    # Column Labels & Graph Title:
    x1_label = "Secondary Classification"
    x2_label = "Year"
    title = "Secondary Classification Popularity by Year"

    # Generate Query Output Dictionary:
    stats_d = {x2_label: year_column, x1_label: classification, y_label: frequency}

    # Generate Dataframe from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype as Categorical:
    stats[x1_label] = stats[x1_label].astype('category')
    stats[x2_label] = stats[x2_label].astype('category')
    stats[y_label] = stats[y_label].astype('int32')

    # Plot the Dataset:
    get_heatmap(stats, x1_label, x2_label, title, 14, 7)

    # Order the dataset:
    stats.set_index(x1_label, inplace=True)
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False)

    print(stats)

    c.close()
    return stats


def get_primary_popularity_by_core():
    pass


def get_secondary_popularity_by_core():
    pass


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


get_stats()
# get_secondary_popularity_per_university()
