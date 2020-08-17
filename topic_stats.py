import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from common_elements import output_to_png, open_sqlite, primary_query_words, secondary_query_words, output_to_csv, \
    get_uni_list_region, get_region_list, get_course_list, set_max_rows_pandas, year_list, core_list, get_uni_list

# Set Pandas options to view all entries:
set_max_rows_pandas()

freq_label = "Frequency"
prime_class_label = "Primary Classification"
sub_class_label = "Secondary Classification"

alphabet_list = ["A-D", "E-K", "L-P", "Q-Z"]

process_message_1 = "Fetching Popularity Data..."
process_message_2 = "Building Query..."
process_message_3 = "Generating Dictionary..."
process_message_4 = "Transferring to Dataframe..."
process_message_5 = "Generating Figure..."
process_message_6 = "Saving to File..."


# Graphing functions:
def get_simple_barplot(data, title, location):
    print(process_message_5)
    plt.figure(figsize=(24, 10))
    sns.set_style("whitegrid")
    chart = sns.catplot(
        x=f"{prime_class_label}",
        y=f"{freq_label}",
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


def get_heatmap(stats, category_label, title, width, height, annot, location, mode):
    print(process_message_5)
    sns.set()
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }
    stats_2 = None
    cmap = sns.light_palette("green")
    if mode == 1:
        stats_2 = stats.pivot(category_label, prime_class_label, freq_label)
    elif mode == 2:
        stats_2 = stats.pivot(category_label, sub_class_label, freq_label)
    elif mode == 3:
        stats_2 = stats.pivot(category_label, prime_class_label, "Percent")
    f, ax = plt.subplots(figsize=(width, height))
    g = sns.heatmap(
        stats_2,
        square=True,
        ax=ax,
        cbar_kws={'fraction': 0.01},
        annot=annot,
        cmap=cmap,
    )
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
    plt.tight_layout()
    # plt.show()  # Only required for testing
    output_to_png(f, title, location)
    plt.close('all')


def get_catplot(stats, category_label, title, height, aspect, location, mode):
    print(process_message_5)
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            }

    plt.figure(figsize=(24, 10))
    sns.set_style("whitegrid")
    chart = None
    if mode == 1:
        chart = sns.catplot(
            x=prime_class_label,
            y=freq_label,
            hue=category_label,
            data=stats,
            kind='bar',
            height=height,
            aspect=aspect,
            legend_out=False,
            palette="Paired")
    elif mode == 2:
        chart = sns.catplot(
            x=sub_class_label,
            y=freq_label,
            hue=category_label,
            data=stats,
            kind='bar',
            height=height,
            aspect=aspect,
            legend_out=False,
            palette="Paired")
    elif mode == 3:
        chart = sns.catplot(
            x=prime_class_label,
            y="Percent",
            hue=category_label,
            data=stats,
            kind='bar',
            height=height,
            aspect=aspect,
            legend_out=False,
            palette="Paired")
    elif mode == 4:
        chart = sns.catplot(
            x=prime_class_label,
            y="Percent",
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
    if mode != 4:
        plt.legend(
            title=category_label,
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

    # Set Values According to Level: (Primary or Secondary)
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
        print(process_message_2)
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
            print(process_message_3)
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
            print(process_message_2)
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
                print(process_message_3)
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
def get_output(result, category_label, level):
    print(process_message_3)

    # Generate Query Output Dictionary:
    stats_d = {}
    if level == 1:
        stats_d = {category_label: result[0], prime_class_label: result[1], freq_label: result[2]}
    elif level == 2:
        stats_d = {category_label: result[0], sub_class_label: result[1], prime_class_label: result[2],
                   freq_label: result[3]}

    print(process_message_4)

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_d)

    return stats


# Construct subsets of the given dataframe in alphabetical ranges:
def get_alphabet_split_subsets_and_plot(stats, category_label, title, location):
    stats_1 = stats[stats[sub_class_label].str.contains('^[A-D]', regex=True, na=False)]  # A-D
    stats_2 = stats[stats[sub_class_label].str.contains('^[E-K]', regex=True, na=False)]  # E-K
    stats_3 = stats[stats[sub_class_label].str.contains('^[L-P]', regex=True, na=False)]  # L-P
    stats_4 = stats[stats[sub_class_label].str.contains('^[Q-Z]', regex=True, na=False)]  # Q-Z
    stat_list = [stats_1, stats_2, stats_3, stats_4]

    # Plot the Alphabetically-Split Dataset:
    i = 0
    for stat in stat_list:
        caption = f"{title} {alphabet_list[i]}"
        get_catplot(stat, category_label, caption, 8, 2, location, 2)
        get_heatmap(stat, category_label, caption, 20, 9, True, location, 2)
        i += 1


# Construct subsets of the given dataframe categorically:
def get_categorically_split_subsets(stats):
    stats_1 = stats[stats[prime_class_label].str.contains('APPLIED COMPUTING', regex=True, na=False)]
    stats_2 = stats[stats[prime_class_label].str.contains('COMPUTER SYSTEMS ORGANISATION', regex=True, na=False)]
    stats_3 = stats[stats[prime_class_label].str.contains('COMPUTING METHODOLOGIES', regex=True, na=False)]
    stats_4 = stats[stats[prime_class_label].str.contains('GENERAL & REFERENCE', regex=True, na=False)]
    stats_5 = stats[stats[prime_class_label].str.contains('HARDWARE', regex=True, na=False)]
    stats_6 = stats[stats[prime_class_label].str.contains('HUMAN-CENTERED COMPUTING', regex=True, na=False)]
    stats_7 = stats[stats[prime_class_label].str.contains('INFORMATION SYSTEMS', regex=True, na=False)]
    stats_8 = stats[stats[prime_class_label].str.contains('MATHEMATICS OF COMPUTING', regex=True, na=False)]
    stats_9 = stats[stats[prime_class_label].str.contains('NETWORKS', regex=True, na=False)]
    stats_10 = stats[stats[prime_class_label].str.contains('SECURITY & PRIVACY', regex=True, na=False)]
    stats_11 = stats[stats[prime_class_label].str.contains('SOCIAL & PROFESSIONAL TOPICS', regex=True, na=False)]
    stats_12 = stats[stats[prime_class_label].str.contains('SOFTWARE & ITS ENGINEERING', regex=True, na=False)]
    stats_13 = stats[stats[prime_class_label].str.contains('THEORY OF COMPUTATION', regex=True, na=False)]
    stats_14 = stats[stats[prime_class_label].str.contains('UNCLASSIFIABLE', regex=True, na=False)]

    cat_split = [stats_1, stats_2, stats_3, stats_4, stats_5, stats_6, stats_7, stats_8, stats_9, stats_10,
                 stats_11, stats_12, stats_13, stats_14]

    return cat_split


# The Following Functions Describe the Popularity of Primary ACM Classifications in Terms of the Frequency of
# Selected Categorical Filters: Module, University, Course, Year, And Core
def get_primary_popularity_by_module():
    start_time = time.time()

    print(process_message_1)

    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []

    print(process_message_2)
    # Generate Query and Transfer to List:
    for word in primary_query_words:
        query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A1 = '{word}' or B1 = '{word}';"
        classification.append(word)
        for row in c.execute(query):
            frequency.append(row[0])

    # Column Label, Graph Title & Location:
    title = "Primary Classification Popularity by Module"
    location = "Topic_stats/Primary/Module"

    print(process_message_3)
    # Generate Query Output Dictionary:
    stats_2d = {prime_class_label: classification, freq_label: frequency}

    print(process_message_4)
    # Generate Data-Frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[prime_class_label] = stats[prime_class_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, title, location)

    # Order the Dataset:
    stats.set_index(prime_class_label, inplace=True)
    stats = stats.sort_values(by=freq_label, ascending=False)

    # print(stats)  # # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    c.close()

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_per_university():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Universities:
    uni_list = get_uni_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(uni_list, 1, 1)

    # Column Label, Graph Title & Location:
    category_label = "University"
    title = "Primary Classification Popularity by University"
    location = "Topic_stats/Primary/University"

    # Get Dataset:
    stats = get_output(result, category_label, 1)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1)
    get_heatmap(stats, category_label, title, 14, 10, True, location, 1)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, freq_label], ascending=False).reset_index(drop=True)

    # print(stats) # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_per_university_by_region():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list_region(region)

        # Collate the Query Data into the Following Lists:
        result = get_pop_lists(uni_list, 1, 1)

        # Column Label, Graph Title & Location:
        category_label = "University"
        title = f"Primary Classification Popularity by Universities in {region}"
        location = "Topic_stats/Primary/University"

        # Get Dataset:
        stats = get_output(result, category_label, 1)

        # Plot the Dataset:
        get_catplot(stats, category_label, title, 8, 2, location, 1)
        get_heatmap(stats, category_label, title, 14, 10, True, location, 1)

        # Order the Dataset by Frequency:
        stats = stats.sort_values(by=[category_label, freq_label], ascending=False).reset_index(drop=True)

        # print(stats) # Only required for testing

        print(process_message_6)

        # Save the Dataframe as .csv:
        output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_course():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 1)

    # Column Label, Graph Title & Location:
    category_label = "Course"
    title = "Primary Classification Popularity by Course"
    location = "Topic_stats/Primary/Course"

    # Get Dataset:
    stats = get_output(result, category_label, 1)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1)
    get_heatmap(stats, category_label, title, 8, 11, True, location, 1)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, freq_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_year():
    start_time = time.time()

    print(process_message_1)

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(year_list, 3, 1)

    # Column Label, Graph Title & Location:
    category_label = "Year"
    title = "Primary Classification Popularity by Year"
    location = "Topic_stats/Primary/Year"

    # Get Dataset:
    stats = get_output(result, category_label, 1)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1)
    get_heatmap(stats, category_label, title, 10, 7, True, location, 1)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, freq_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_core():
    start_time = time.time()

    print(process_message_1)

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 1)

    # Column Label, Graph Title & Location:
    category_label = "Core"
    title = "Primary Classification Popularity by Core and Elective Modules"
    location = "Topic_stats/Primary/Core"

    # Get Dataset:
    stats = get_output(result, category_label, 1)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1)
    get_heatmap(stats, category_label, title, 10, 7, True, location, 1)

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, freq_label], ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# The Following Functions Describe the Popularity of Primary ACM Sub-Classifications in Terms of the Frequency of
# Selected Categorical Filters: Module, University, Course, Year, And Core
# Each dataset is broken down first in two halves alphabetically to make plotting readable
# and then by subcategory to highlight each facet.
def get_secondary_popularity_by_module():
    start_time = time.time()

    print(process_message_1)

    c = open_sqlite()

    # Collate the Query Data into the Following Lists:
    classification = []
    frequency = []
    class_list = []
    class_dic = {}

    print(process_message_2)
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
    title = "Secondary Classification Popularity by Module"
    location = "Topic_stats/Secondary/Module"

    print(process_message_3)

    # Generate Query Output Dictionary:
    stats_2d = {prime_class_label: classification, freq_label: frequency}

    print(process_message_4)

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[prime_class_label] = stats[prime_class_label].astype('category')

    # Plot the Dataset:
    get_simple_barplot(stats, title, location)

    # Order the Dataset:
    stats.set_index(prime_class_label, inplace=True)
    stats = stats.sort_values(by=freq_label, ascending=False)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    c.close()

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_per_university():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Universities:
    uni_list = get_uni_list()

    # Collate the Query Data into the Following Lists:
    pop_list = get_pop_lists(uni_list, 1, 2)

    # Column Label, Graph Title & Location:
    category_label = "University"
    title = "Secondary Classification Popularity by University"
    location = "Topic_stats/Secondary/University"

    # Get Dataset:
    stats = get_output(pop_list, category_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=sub_class_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset & Plot each Subset:
    get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
    heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
    for df in cat_split:
        if df is not None:
            location = f"Topic_stats/Secondary/University/{primary_query_words[i]}"
            title = f"{primary_query_words[i]} Subcategory Popularity by University"
            get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2)
            get_catplot(df, category_label, title, 8, 2, location, 2)
            i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=freq_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_per_university_by_region():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()

    for region in region_list:
        # Generate a List of Available Universities:
        uni_list = get_uni_list_region(region)

        # Collate the Query Data into the Following Lists:
        pop_list = get_pop_lists(uni_list, 1, 2)

        # Column Label, Graph Title & Location:
        category_label = "University"
        title = f"Secondary Classification Popularity by Universities in {region}"
        location = "Topic_stats/Secondary/University"

        # Get Dataset:
        stats = get_output(pop_list, category_label, 2)

        # Order By Sub-Category & Rest Index:
        stats = stats.sort_values(by=sub_class_label).reset_index(drop=True)

        # Get Alphabetically-Split Dataset & Plot each Subset:
        get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

        # Order By Category & Reset Index:
        stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

        # Get Categorically-Split Dataset:
        cat_split = get_categorically_split_subsets(stats)

        # Plot the Categorically-Split Dataset:
        i = 0
        widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
        heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
        for df in cat_split:
            if df is not None:
                location = f"Topic_stats/Secondary/University/{primary_query_words[i]}"
                title = f"{primary_query_words[i]} Subcategory Popularity by University"
                get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2)
                get_catplot(df, category_label, title, 8, 2, location, 2)
                i += 1

        # Order the dataset by Frequency and reset index:
        stats = stats.sort_values(by=freq_label, ascending=False).reset_index(drop=True)

        # print(stats)  # Only required for testing

        print(process_message_6)

        # Save the Dataframe as .csv:
        output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_course():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Courses:
    course_list = get_course_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(course_list, 2, 2)

    # Column Label, Graph Title & Location:
    category_label = "Course"
    title = "Secondary Classification Popularity by Course"
    location = "Topic_stats/Secondary/Course"

    # Get Dataset:
    stats = get_output(result, category_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset:
    get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)
    stats[freq_label] = stats[freq_label].astype('int32')

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [14, 14, 10, 10, 10, 12, 12, 12, 10, 11, 12, 12, 10, 10]
    heights = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    for df in cat_split:
        location = f"Topic_stats/Secondary/Course/{primary_query_words[i]}"
        title = f"{primary_query_words[i]} Subcategory Popularity by Course"
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=freq_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_year():
    start_time = time.time()

    print(process_message_1)

    # Collate the Query Data into the Following Lists:
    pop_list = get_pop_lists(year_list, 3, 2)

    # Column Label, Graph Title & Location:
    category_label = "Year"
    title = "Secondary Classification Popularity by Year"
    location = "Topic_stats/Secondary/Year"

    # Get Dataset:
    stats = get_output(pop_list, category_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=sub_class_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset & Plot each Subset:
    get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [13, 9, 12, 10, 12, 8, 7, 8, 11, 10, 10, 10, 10, 6]
    heights = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    for df in cat_split:
        location = f"Topic_stats/Secondary/Year/{primary_query_words[i]}"
        title = f"{primary_query_words[i]} Subcategory Popularity by Year"
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2)
        get_catplot(df, category_label, title, 8, 2, location, 2)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=freq_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_core():
    start_time = time.time()

    print(process_message_1)

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(core_list, 4, 2)

    # Column Label, Graph Title & Location:
    category_label = "Core"
    title = "Secondary Classification Popularity by Core and Elective Modules"
    location = "Topic_stats/Secondary/Core"

    # Get Dataset:
    stats = get_output(result, category_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=sub_class_label).reset_index(drop=True)

    # Get Alphabetically-Split Dataset & Plot each Subset:
    get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [15, 13, 11, 10, 10, 13, 11, 11, 10, 11, 11, 11, 10, 8]
    heights = [11, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 11]
    for df in cat_split:
        location = f"Topic_stats/Secondary/Core/{primary_query_words[i]}"
        title = f"{primary_query_words[i]} Subcategory Popularity by Core and  Elective Modules"
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2)
        get_catplot(df, category_label, title, 8, 2, location, 2)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=freq_label, ascending=False).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


# This function serves to operate the above functions in sequence:
def get_stats():
    # Overall Topic Popularity:
    get_primary_popularity_by_module()
    get_secondary_popularity_by_module()

    # By University:
    get_primary_popularity_per_university()
    get_primary_popularity_per_university_by_region()
    get_secondary_popularity_per_university()
    get_secondary_popularity_per_university_by_region()

    # By Course:
    # get_primary_popularity_by_course()
    # get_secondary_popularity_by_course()

    # By Year:
    get_primary_popularity_by_year()
    get_secondary_popularity_by_year()

    # By Core:
    get_primary_popularity_by_core()
    get_secondary_popularity_by_core()


# get_stats()  # Only required for testing
