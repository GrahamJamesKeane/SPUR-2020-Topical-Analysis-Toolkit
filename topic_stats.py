import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from common_elements import output_to_png, open_sqlite, primary_query_words, secondary_query_words, output_to_csv, \
    get_uni_list, get_region_list, get_course_list

y_label = "Frequency"
z_label = "Primary Classification"

message_1 = "Fetching Popularity Data..."
message_2 = "Building Query..."
message_3 = "Generating Dictionary..."
message_4 = "Transferring to Dataframe..."
message_5 = "Generating Figure..."
message_6 = "Saving to File..."


# Graphing functions:
def get_simple_barplot(data, x_label, title, location):
    print(message_5)
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
    plt.figure(constrained_layout=True)
    # plt.show()  # Only required for testing
    output_to_png(chart, title, location)
    plt.close('all')


def get_heatmap(stats, x1_label, x2_label, title, width, height, annot, location):
    print(message_5)
    sns.set()
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    stats_2 = stats.pivot(x2_label, x1_label, y_label)
    f, ax = plt.subplots(figsize=(width, height))
    g = sns.heatmap(
        stats_2,
        square=True,
        ax=ax,
        cbar_kws={'fraction': 0.01},
        annot=annot,
        cmap='OrRd',
        fmt='d')
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
    plt.figure(constrained_layout=True)
    # plt.show()  # Only required for testing
    output_to_png(f, title, location)
    plt.close('all')


def get_barplot(stats, x1_label, x2_label, title, height, aspect, location):
    print(message_5)
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
    plt.figure(constrained_layout=True)
    # plt.show()  # Only required for testing
    output_to_png(chart, title, location)
    plt.close('all')


# Populates and Returns a List of Category, Classification and Frequency to Build a Dataframe:
# Category Specifies University, Course, Year,
# Level Specifies Primary or Secondary
def get_pop_lists(item_list, category, level):
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    s_classification = []
    p_classification = []
    frequency = []
    item_column = []
    key_list = []
    class_1 = None
    class_2 = None
    if level == 1:
        key_list = primary_query_words
        class_1 = "A1"
        class_2 = "B1"
    elif level == 2:
        key_list = secondary_query_words
        class_1 = "A2"
        class_2 = "B2"

    for item in item_list:
        class_dic = {}
        class_list = []
        print(message_2)
        if level == 2:
            query_a1 = query_b1 = None
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
            print(message_3)
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

        for key in key_list:
            print(message_2)
            query_3 = None
            if key != 'COMMON':
                if category == 1:  # University:
                    query_3 = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails " \
                              f"WHERE UniversityName = '{item}' AND {class_1} = '{key}' or {class_2} = '{key}';"
                elif category == 2:  # Course:
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE CourseCode = '{item}' AND (ModuleDetails.{class_1} = '{key}' " \
                              f"or ModuleDetails.{class_2} = '{key}');"
                elif category == 3:  # Year Offered
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE YearOffered = {item} AND (ModuleDetails.{class_1} = '{key}' " \
                              f"or ModuleDetails.{class_2} = '{key}');"
                elif category == 4:  # Core:
                    query_3 = f"SELECT COUNT(CourseDetails.ModuleCode) FROM CourseDetails INNER JOIN ModuleDetails " \
                              f"ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"WHERE Core = '{item}' AND (ModuleDetails.{class_1} = '{key}' " \
                              f"or ModuleDetails.{class_2} = '{key}');"
                print(message_3)
                for row in c.execute(query_3):
                    if key in class_dic:
                        class_dic[key] += row[0]
                    else:
                        class_dic[key] = row[0]

        for key, value in class_dic.items():
            frequency.append(value)
            item_column.append(item)
            if level == 1:
                p_classification.append(key)
            elif level == 2:
                s_classification.append(key)

    if level == 2:
        for item in s_classification:
            query = f"SELECT PrimaryClassification FROM Classifications " \
                    f"WHERE  SecondaryClassification = '{item}';"
            for i in c.execute(query):
                word = str(i[0])
                p_classification.append(word)

    c.close()
    if level == 1:
        return [item_column, p_classification, frequency]
    elif level == 2:
        return [item_column, s_classification, p_classification, frequency]


# Transform Query Output into Dataframe
def get_output(result, label_1, label_2, level):
    print(message_3)

    # Generate Query Output Dictionary:
    stats_d = {}
    if level == 1:
        stats_d = {label_2: result[0], label_1: result[1], y_label: result[2]}
    elif level == 2:
        stats_d = {label_2: result[0], label_1: result[1], z_label: result[2], y_label: result[3]}

    print(message_4)

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    # Set Column Datatype:
    stats[label_1] = stats[label_1].astype('category')
    stats[label_2] = stats[label_2].astype('category')
    stats[y_label] = stats[y_label].astype('int32')
    if level == 2:
        stats[z_label] = stats[z_label].astype('category')

    return stats


# The Following Functions Describe the Popularity of Primary ACM Classifications in Terms of the Frequency of
# Selected Categorical Filters: Module, University, Course, Year, And Core
def get_primary_popularity_by_module():
    start_time = time.time()
    print(message_1)
    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    print(message_2)
    for word in primary_query_words:
        query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A1 = '{word}' or B1 = '{word}';"
        classification.append(word)
        for row in c.execute(query):
            frequency.append(row[0])

    # Column Label, Graph Title & Location:
    x_label = "Classification"
    title = "Primary Classification Popularity by Module"
    location = "Topic_stats/Primary/Module"

    print(message_3)
    # Generate Query Output Dictionary:
    stats_2d = {x_label: classification, y_label: frequency}

    print(message_4)
    # Generate Data-Frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[x_label] = stats[x_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, x_label, title, location)

    # Order the Dataset:
    stats.set_index(x_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    # print(stats)  # # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    c.close()
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_per_university():
    start_time = time.time()

    print(message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()
    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        # Collate the Query Data into the Following Lists:
        result = get_pop_lists(uni_list, 1, 1)

        # Column Label, Graph Title & Location:
        x1_label = "Primary Classification"
        x2_label = "University"
        title = "Primary Classification Popularity by University"
        location = "Topic_stats/Primary/University"

        # Get Dataset:
        stats = get_output(result, x1_label, x2_label, 1)

        # Plot the Dataset:
        get_barplot(stats, x1_label, x2_label, title, 8, 2, location)
        get_heatmap(stats, x1_label, x2_label, title, 14, 10, True, location)

        # Order the Dataset by Frequency:
        stats = stats.sort_values(by=[x2_label, y_label], ascending=False).reset_index(drop=True)

        # print(stats) # Only required for testing

        print(message_6)
        output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_course():
    start_time = time.time()

    print(message_1)

    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 1)

    # Column Label, Graph Title & Location:
    x1_label = "Primary Classification"
    x2_label = "Course"
    title = "Primary Classification Popularity by Course"
    location = "Topic_stats/Primary/Course"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 1)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2, location)
    get_heatmap(stats, x1_label, x2_label, title, 8, 11, True, location)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_year():
    start_time = time.time()

    print(message_1)

    year_list = [1, 2, 3, 4]

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(year_list, 3, 1)

    # Column Label, Graph Title & Location:
    x1_label = "Primary Classification"
    x2_label = "Year"
    title = "Primary Classification Popularity by Year"
    location = "Topic_stats/Primary/Year"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 1)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2, location)
    get_heatmap(stats, x1_label, x2_label, title, 10, 7, True, location)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_core():
    start_time = time.time()

    print(message_1)

    core_list = ['CORE', 'ELECTIVE', 'UNKNOWN']

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 1)

    # Column Label, Graph Title & Location:
    x1_label = "Primary Classification"
    x2_label = "Core"
    title = "Primary Classification Popularity by Core and Elective Modules"
    location = "Topic_stats/Primary/Core"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 1)

    # Plot the Dataset:
    get_barplot(stats, x1_label, x2_label, title, 8, 2, location)
    get_heatmap(stats, x1_label, x2_label, title, 10, 7, True, location)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[x2_label, y_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# The Following Functions Describe the Popularity of Primary ACM Sub-Classifications in Terms of the Frequency of
# Selected Categorical Filters: Module, University, Course, Year, And Core
# Each dataset is broken down first in two halves alphabetically to make plotting readable
# and then by subcategory to highlight each facet.
def get_secondary_popularity_by_module():
    start_time = time.time()

    print(message_1)

    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    class_list = []
    class_dic = {}

    print(message_2)
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

    for word in secondary_query_words:
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

    # Column Label, Graph Title & Location:
    x_label = "Classification"
    title = "Secondary Classification Popularity by Module"
    location = "Topic_stats/Secondary/Module"

    print(message_3)

    # Generate Query Output Dictionary:
    stats_2d = {x_label: classification, y_label: frequency}

    print(message_4)

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[x_label] = stats[x_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, x_label, title, location)

    # Order the Dataset:
    stats.set_index(x_label, inplace=True)
    stats = stats.sort_values(by=y_label, ascending=False)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    c.close()

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_per_university():
    start_time = time.time()

    print(message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list(region)

        # Collate the Query Data into the Following Lists:
        result = get_pop_lists(uni_list, 1, 2)

        # Column Label, Graph Title & Location:
        x1_label = "Secondary Classification"
        x2_label = "University"
        title = "Secondary Classification Popularity by University"
        title_1 = "Secondary Classification Popularity by University A-K"
        title_2 = "Secondary Classification Popularity by University L-Z"
        location = "Topic_stats/Secondary/University"

        # Get Dataset:
        stats = get_output(result, x1_label, x2_label, 2)

        # Order By Sub-Category & Rest Index:
        stats = stats.sort_values(by=x1_label).reset_index(drop=True)

        # Get Alphabetically-Split Dataset:
        stats_1 = stats.iloc[:294]
        stats_2 = stats.iloc[294:]

        # Plot the Alphabetically-Split Dataset:
        get_heatmap(stats_1, x1_label, x2_label, title_1, 20, 9, True, location)
        get_heatmap(stats_2, x1_label, x2_label, title_2, 20, 9, True, location)

        # Order By Category & Reset Index:
        stats = stats.sort_values(by=z_label).reset_index(drop=True)

        # Get Categorically-Split Dataset:
        cat_split = [stats.iloc[:77], stats.iloc[77: 105], stats.iloc[105: 161], stats.iloc[161: 175],
                     stats.iloc[175: 245], stats.iloc[245: 287], stats.iloc[287: 322], stats.iloc[322: 364],
                     stats.iloc[364: 420], stats.iloc[420: 490], stats.iloc[490: 511], stats.iloc[511: 532],
                     stats.iloc[532:588], stats.iloc[588:]]

        # Plot the Categorically-Split Dataset:
        i = 0
        widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
        heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
        for df in cat_split:
            title = f"{primary_query_words[i]} Subcategory Popularity by University"
            get_heatmap(df, x1_label, x2_label, title, widths[i], heights[i], True, location)
            i += 1

        # Order the dataset by Frequency and reset index:
        stats = stats.sort_values(by=y_label, ascending=False).reset_index(drop=True)

        # print(stats)  # Only required for testing

        print(message_6)
        output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_course():
    start_time = time.time()

    print(message_1)

    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 2)

    # Column Label, Graph Title & Location:
    x1_label = "Classification"
    x2_label = "Course"
    title = "Secondary Classification Popularity by Course"
    title_1 = "Secondary Classification Popularity by Course A-K"
    title_2 = "Secondary Classification Popularity by Course L-Z"
    location = "Topic_stats/Secondary/Course"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=x1_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset:
    stats_1 = stats.iloc[:924]
    stats_2 = stats.iloc[924:]

    # Plot the Alphabetically-Split Dataset:
    get_heatmap(stats_1, x1_label, x2_label, title_1, 20, 9, True, location)
    get_heatmap(stats_2, x1_label, x2_label, title_2, 20, 9, True, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=z_label).reset_index(drop=True)
    stats[y_label] = stats[y_label].astype('int32')

    # Get Categorically-Split Dataset:
    cat_split = [stats.iloc[:242], stats.iloc[242: 330], stats.iloc[330: 506], stats.iloc[506: 550],
                 stats.iloc[550: 770], stats.iloc[770: 902], stats.iloc[902: 1012], stats.iloc[1012: 1144],
                 stats.iloc[1144: 1320], stats.iloc[1320: 1540], stats.iloc[1540: 1606], stats.iloc[1606: 1672],
                 stats.iloc[1672:1848], stats.iloc[1848:]]

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [14, 14, 10, 10, 10, 12, 12, 12, 10, 11, 12, 12, 10, 10]
    heights = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    for df in cat_split:
        title = f"{primary_query_words[i]} Subcategory Popularity by Course"
        get_heatmap(df, x1_label, x2_label, title, widths[i], heights[i], True, location)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=y_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_year():
    start_time = time.time()

    print(message_1)

    year_list = [1, 2, 3, 4]

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(year_list, 3, 2)

    # Column Label, Graph Title & Location:
    x1_label = "Secondary Classification"
    x2_label = "Year"
    title = "Secondary Classification Popularity by Year"
    title_1 = "Secondary Classification Popularity by Year A-K"
    title_2 = "Secondary Classification Popularity by Year L-Z"
    location = "Topic_stats/Secondary/Year"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=x1_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset:
    stats_1 = stats.iloc[:168]
    stats_2 = stats.iloc[168:]

    # Plot the Alphabetically-Split Dataset:
    get_barplot(stats_1, x1_label, x2_label, title_1, 8, 2, location)
    get_barplot(stats_2, x1_label, x2_label, title_2, 8, 2, location)
    get_heatmap(stats_1, x1_label, x2_label, title_1, 20, 9, True, location)
    get_heatmap(stats_2, x1_label, x2_label, title_2, 20, 9, True, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=z_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = [stats.iloc[:44], stats.iloc[44: 60], stats.iloc[60: 92], stats.iloc[92: 100],
                 stats.iloc[100: 140], stats.iloc[140: 164], stats.iloc[164: 184], stats.iloc[184: 208],
                 stats.iloc[208: 240], stats.iloc[240: 280], stats.iloc[280: 292], stats.iloc[292: 304],
                 stats.iloc[304:336], stats.iloc[336:]]

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
    heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
    for df in cat_split:
        title = f"{primary_query_words[i]} Subcategory Popularity by Year"
        get_heatmap(df, x1_label, x2_label, title, widths[i], heights[i], True, location)
        get_barplot(df, x1_label, x2_label, title, 8, 2, location)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=y_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_core():
    start_time = time.time()

    print(message_1)

    core_list = ['CORE', 'ELECTIVE']

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 2)

    # Column Label, Graph Title & Location:
    x1_label = "Secondary Classification"
    x2_label = "Core"
    title = "Secondary Classification Popularity by Core and  Elective Modules"
    title_1 = "Secondary Classification Popularity by Core and  Elective Modules A-K"
    title_2 = "Secondary Classification Popularity by Core and  Elective Modules L-Z"
    location = "Topic_stats/Secondary/Core"

    # Get Dataset:
    stats = get_output(result, x1_label, x2_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=x1_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset:
    stats_1 = stats.iloc[:84]
    stats_2 = stats.iloc[84:]

    # Plot the Alphabetically-Split Dataset:
    get_barplot(stats_1, x1_label, x2_label, title_1, 8, 2, location)
    get_barplot(stats_2, x1_label, x2_label, title_2, 8, 2, location)
    get_heatmap(stats_1, x1_label, x2_label, title_1, 20, 9, True, location)
    get_heatmap(stats_2, x1_label, x2_label, title_2, 20, 9, True, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=z_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = [stats.iloc[:22], stats.iloc[22: 30], stats.iloc[30: 46], stats.iloc[46: 50],
                 stats.iloc[50: 70], stats.iloc[70: 82], stats.iloc[82: 92], stats.iloc[92: 104],
                 stats.iloc[104: 120], stats.iloc[120: 140], stats.iloc[140: 146], stats.iloc[146: 152],
                 stats.iloc[152:168], stats.iloc[168:]]

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
    heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
    for df in cat_split:
        title = f"{primary_query_words[i]} Subcategory Popularity by Core and  Elective Modules"
        get_heatmap(df, x1_label, x2_label, title, widths[i], heights[i], True, location)
        get_barplot(df, x1_label, x2_label, title, 8, 2, location)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=y_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(message_6)
    output_to_csv(stats, title, location)

    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# This function serves to operate the above functions in sequence:
def get_stats():
    # Overall Topic Popularity:
    get_primary_popularity_by_module()
    get_secondary_popularity_by_module()

    # By University:
    get_primary_popularity_per_university()
    get_secondary_popularity_per_university()

    # By Course:
    # get_primary_popularity_by_course()
    # get_secondary_popularity_by_course()

    # By Year:
    get_primary_popularity_by_year()
    get_secondary_popularity_by_year()

    # By Core:
    get_primary_popularity_by_core()
    get_secondary_popularity_by_core()

# get_stats()
