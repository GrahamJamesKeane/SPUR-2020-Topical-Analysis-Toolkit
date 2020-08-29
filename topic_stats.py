import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common_elements import output_to_png, open_sqlite, primary_query_words, secondary_query_words, output_to_csv, \
    get_region_list, get_course_list, set_max_rows_pandas, year_list, core_list, get_uni_list

# Set Pandas options to view all entries:
set_max_rows_pandas()

percent_label = "Percentage"
rel_percent_label = "Relative Percentage"
freq_label = "Frequency"
prime_class_label = "Primary Classification"
sub_class_label = "Secondary Classification"

alphabet_list = ["A-D", "E-K", "L-P", "Q-Z"]

process_message_1 = "Fetching Popularity Data..."
process_message_2 = "Building Query..."
process_message_3 = "Generating Dictionary..."
process_message_4 = "Transferring to Dataframe..."
process_message_5 = "Generating Figure..."
process_message_6 = "Exporting .csv ..."


# Graphing functions:
def get_simple_barplot(data, title, location, label):
    print(process_message_5)
    plt.figure(figsize=(24, 10))
    sns.set_style("whitegrid")
    chart = sns.catplot(
        x=f"{label}",
        y=f"{percent_label}",
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


def get_heatmap(stats, category_label, title, width, height, annot, location, mode, ratio_label):
    print(process_message_5)
    sns.set()
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 25,
            }
    stats_2 = None
    cmap = sns.light_palette("green")
    if mode == 1:
        stats_2 = stats.pivot(category_label, prime_class_label, ratio_label)
    elif mode == 2:
        stats_2 = stats.pivot(category_label, sub_class_label, ratio_label)
    elif mode == 3:
        stats_2 = stats.pivot(category_label, prime_class_label, ratio_label)
    elif mode == 4:
        stats_2 = stats.pivot(category_label, sub_class_label, ratio_label)
    f, ax = plt.subplots(figsize=(width, height))
    g = sns.heatmap(
        stats_2,
        square=True,
        ax=ax,
        cbar_kws={'fraction': 0.01, 'label': 'Percent'},
        annot=annot,
        cmap=cmap,
        fmt="05.2f"
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
    plt.subplots_adjust(top=0.8)
    plt.suptitle(title, fontdict=font)
    ax.set_ylabel('')
    ax.set_xlabel('')
    plt.autoscale(tight=True)
    # plt.show()  # Only required for testing
    output_to_png(f, title, location)
    plt.close('all')


def get_catplot(stats, category_label, title, height, aspect, location, mode, ratio_label):
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
            y=ratio_label,
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
            y=ratio_label,
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
            y=ratio_label,
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
            y=ratio_label,
            data=stats,
            kind='bar',
            height=height,
            aspect=aspect,
            legend_out=False,
            palette="Paired")
    elif mode == 5:
        chart = sns.catplot(
            x=sub_class_label,
            y=ratio_label,
            hue=category_label,
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
    percentage = []
    relative_percentage = []  # Subtopic distribution as a percentage of total modules for a given primary topic
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

    # Iterate through the category list (University, Region etc.)
    for item in item_list:
        total_count = 0  # Track the total number of modules for the current item (Used to calculate percentage later)
        class_dic = {}
        class_list = []

        print(process_message_2)

        # Where the secondary classification is COMMON for a given primary classification,
        # we select all of that classification's subclasses and give them each a count of 1.
        # If there are several occurrence's of a primary classification having a COMMON subclass
        # the count is accumulated.
        if level == 2:
            query_a1 = query_b1 = None
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
            elif category == 5:  # Region
                query_a1 = f"SELECT ModuleDetails.A1 FROM ModuleDetails " \
                           f"INNER JOIN CourseDetails ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"INNER JOIN Universities ON CourseDetails.UniversityName = Universities.UniversityName " \
                           f"WHERE Country = '{item}' AND ModuleDetails.A2 = 'COMMON';"
                query_b1 = f"SELECT ModuleDetails.B1 FROM ModuleDetails " \
                           f"INNER JOIN CourseDetails ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                           f"INNER JOIN Universities ON CourseDetails.UniversityName = Universities.UniversityName " \
                           f"WHERE Country = '{item}' AND ModuleDetails.B2 = 'COMMON';"

            print(process_message_3)

            # From the selected queries generate a list of primary classifications
            # having the secondary classification 'COMMON':
            for row in c.execute(query_a1):
                word = str(row[0])
                class_list.append(word)

            for row in c.execute(query_b1):
                word = str(row[0])
                class_list.append(word)

            # Using the classification table, for each primary class in the list
            # we select all of its subclasses and increment its count by 1
            for selection in class_list:
                query_2 = f"SELECT SecondaryClassification FROM Classifications " \
                          f"WHERE PrimaryClassification = '{selection}';"
                for value in c.execute(query_2):
                    word = str(value[0])
                    total_count += 1
                    if word in class_dic:
                        class_dic[word] += 1
                    else:
                        class_dic[word] = 1

        # Iterate through the topic keywords to query the number of modules satisfying the given criteria
        for key in key_list:

            print(process_message_2)

            query_3 = None
            if key != 'COMMON':
                if category == 1:  # University:
                    query_3 = f"SELECT COUNT(ModuleCode) FROM ModuleDetails " \
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
                elif category == 5:  # Region
                    query_3 = f"SELECT COUNT(ModuleDetails.A1) FROM ModuleDetails " \
                              f"INNER JOIN CourseDetails ON CourseDetails.ModuleCode = ModuleDetails.ModuleCode " \
                              f"INNER JOIN Universities " \
                              f"ON CourseDetails.UniversityName = Universities.UniversityName " \
                              f"WHERE Country = '{item}' AND (ModuleDetails.{class_1} = '{key}' " \
                              f"or ModuleDetails.{class_2} = '{key}');"

                print(process_message_3)

                # Add the keyword and the number of associated modules to the class dictionary
                # Increment the total modules accumulator
                for row in c.execute(query_3):
                    total_count += row[0]
                    if key in class_dic:
                        class_dic[key] += row[0]
                    else:
                        class_dic[key] = row[0]

        # Transfer the keywords and their frequencies to lists. We also compute the percentage of each
        # keyword w.r.t. the total_count for each item in item_list
        for key, value in class_dic.items():
            ratio = (value / total_count) * 100  # Calculate percentage of modules with current classification
            percentage.append(ratio)
            frequency.append(value)
            item_column.append(item)
            if level == 1:
                p_classification.append(key)
            elif level == 2:
                s_classification.append(key)

    # For secondary classifications we can quantify the relative percentage of each subtopic w.r.t.
    # its parent topic for a given item in item_list. We first assign each subtopic its primary topic
    # handle and then tally the total number of entries for each handle. We then compute the relative
    # percentage as the frequency of the entry divided by the total count for that handle times 100
    if level == 2:

        for topic in s_classification:  # Add primary topic handle for each subtopic
            query = f"SELECT PrimaryClassification FROM Classifications " \
                    f"WHERE  SecondaryClassification = '{topic}';"
            for i in c.execute(query):
                word = str(i[0])
                p_classification.append(word)

        for item in item_list:
            ap_count = cso_count = cm_count = gr_count = hw_count = hci_count = is_count = moc_count = nw_count = \
                sap_count = spt_count = swe_count = toc_count = u_count = 0
            for i in range(len(p_classification)):  # Tally the total num of modules for a given classification
                if p_classification[i] == "APPLIED COMPUTING" and item_column[i] == item:
                    ap_count += frequency[i]
                elif p_classification[i] == "COMPUTER SYSTEMS ORGANISATION" and item_column[i] == item:
                    cso_count += frequency[i]
                elif p_classification[i] == "COMPUTING METHODOLOGIES" and item_column[i] == item:
                    cm_count += frequency[i]
                elif p_classification[i] == "GENERAL & REFERENCE" and item_column[i] == item:
                    gr_count += frequency[i]
                elif p_classification[i] == "HARDWARE" and item_column[i] == item:
                    hw_count += frequency[i]
                elif p_classification[i] == "HUMAN-CENTERED COMPUTING" and item_column[i] == item:
                    hci_count += frequency[i]
                elif p_classification[i] == "INFORMATION SYSTEMS" and item_column[i] == item:
                    is_count += frequency[i]
                elif p_classification[i] == "MATHEMATICS OF COMPUTING" and item_column[i] == item:
                    moc_count += frequency[i]
                elif p_classification[i] == "NETWORKS" and item_column[i] == item:
                    nw_count += frequency[i]
                elif p_classification[i] == "SECURITY & PRIVACY" and item_column[i] == item:
                    sap_count += frequency[i]
                elif p_classification[i] == "SOCIAL & PROFESSIONAL TOPICS" and item_column[i] == item:
                    spt_count += frequency[i]
                elif p_classification[i] == "SOFTWARE & ITS ENGINEERING" and item_column[i] == item:
                    swe_count += frequency[i]
                elif p_classification[i] == "THEORY OF COMPUTATION" and item_column[i] == item:
                    toc_count += frequency[i]
                elif p_classification[i] == "UNCLASSIFIABLE" and item_column[i] == item:
                    u_count += frequency[i]

            # Provision for division by zero:
            if ap_count == 0:
                ap_count = 1
            if cso_count == 0:
                cso_count = 1
            if cm_count == 0:
                cm_count = 1
            if gr_count == 0:
                gr_count = 1
            if hw_count == 0:
                hw_count = 1
            if hci_count == 0:
                hci_count = 1
            if is_count == 0:
                is_count = 1
            if moc_count == 0:
                moc_count = 1
            if nw_count == 0:
                nw_count = 1
            if sap_count == 0:
                sap_count = 1
            if spt_count == 0:
                spt_count = 1
            if swe_count == 0:
                swe_count = 1
            if toc_count == 0:
                toc_count = 1
            if u_count == 0:
                u_count = 1

            for i in range(
                    len(p_classification)):  # Calculate the percentage of each subtopic within its classification
                if p_classification[i] == "APPLIED COMPUTING" and item_column[i] == item:
                    ratio = (frequency[i] / ap_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "COMPUTER SYSTEMS ORGANISATION" and item_column[i] == item:
                    ratio = (frequency[i] / cso_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "COMPUTING METHODOLOGIES" and item_column[i] == item:
                    ratio = (frequency[i] / cm_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "GENERAL & REFERENCE" and item_column[i] == item:
                    ratio = (frequency[i] / gr_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "HARDWARE" and item_column[i] == item:
                    ratio = (frequency[i] / hw_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "HUMAN-CENTERED COMPUTING" and item_column[i] == item:
                    ratio = (frequency[i] / hci_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "INFORMATION SYSTEMS" and item_column[i] == item:
                    ratio = (frequency[i] / is_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "MATHEMATICS OF COMPUTING" and item_column[i] == item:
                    ratio = (frequency[i] / moc_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "NETWORKS" and item_column[i] == item:
                    ratio = (frequency[i] / nw_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "SECURITY & PRIVACY" and item_column[i] == item:
                    ratio = (frequency[i] / sap_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "SOCIAL & PROFESSIONAL TOPICS" and item_column[i] == item:
                    ratio = (frequency[i] / spt_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "SOFTWARE & ITS ENGINEERING" and item_column[i] == item:
                    ratio = (frequency[i] / swe_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "THEORY OF COMPUTATION" and item_column[i] == item:
                    ratio = (frequency[i] / toc_count) * 100
                    relative_percentage.insert(i, ratio)
                elif p_classification[i] == "UNCLASSIFIABLE" and item_column[i] == item:
                    ratio = (frequency[i] / u_count) * 100
                    relative_percentage.insert(i, ratio)

    c.close()
    if level == 1:
        return [item_column, p_classification, percentage, frequency]
    elif level == 2:
        return [item_column, s_classification, p_classification, percentage, frequency, relative_percentage]


# Transform Query Output into Dataframe
def get_output(result, category_label, level):
    print(process_message_3)

    # Generate Query Output Dictionary:
    stats_d = {}
    if level == 1:
        stats_d = {category_label: result[0], prime_class_label: result[1],
                   f"{category_label} {percent_label}": result[2],
                   freq_label: result[3]}
    elif level == 2:
        stats_d = {category_label: result[0], sub_class_label: result[1], prime_class_label: result[2],
                   f"{category_label} {percent_label}": result[3], freq_label: result[4],
                   f"{prime_class_label} {rel_percent_label}": result[5]}

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
        get_catplot(stat, category_label, caption, 8, 2, location, 2, f"{category_label} {percent_label}")
        get_heatmap(stat, category_label, caption, 20, 15, True, location, 2, f"{category_label} {percent_label}")
        i += 1


# Construct subsets of the given dataframe categorically and order each subset alphabetically:
def get_categorically_split_subsets(stats):
    stats_1 = stats[stats[prime_class_label].str.contains('APPLIED COMPUTING', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_2 = stats[
        stats[prime_class_label].str.contains('COMPUTER SYSTEMS ORGANISATION', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_3 = stats[stats[prime_class_label].str.contains('COMPUTING METHODOLOGIES', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_4 = stats[stats[prime_class_label].str.contains('GENERAL & REFERENCE', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_5 = stats[stats[prime_class_label].str.contains('HARDWARE', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_6 = stats[
        stats[prime_class_label].str.contains('HUMAN-CENTERED COMPUTING', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_7 = stats[stats[prime_class_label].str.contains('INFORMATION SYSTEMS', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_8 = stats[
        stats[prime_class_label].str.contains('MATHEMATICS OF COMPUTING', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_9 = stats[stats[prime_class_label].str.contains('NETWORKS', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_10 = stats[stats[prime_class_label].str.contains('SECURITY & PRIVACY', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_11 = stats[
        stats[prime_class_label].str.contains('SOCIAL & PROFESSIONAL TOPICS', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_12 = stats[
        stats[prime_class_label].str.contains('SOFTWARE & ITS ENGINEERING', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_13 = stats[stats[prime_class_label].str.contains('THEORY OF COMPUTATION', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)
    stats_14 = stats[stats[prime_class_label].str.contains('UNCLASSIFIABLE', regex=True, na=False)].sort_values(
        by=sub_class_label, ascending=False)

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
    percentage = []
    total_count = 0

    print(process_message_2)

    # Generate Query and Transfer to List:
    for word in primary_query_words:
        query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A1 = '{word}' or B1 = '{word}';"
        classification.append(word)
        for row in c.execute(query):
            total_count += row[0]
            frequency.append(row[0])
    for value in frequency:
        ratio = (value / total_count) * 100  # Calculate percentage of modules with current classification
        percentage.append(ratio)

    # Column Label, Graph Title & Location:
    title = "Primary Classification Popularity by Module"
    location = "Topic_stats/Primary/Module"

    print(process_message_3)
    # Generate Query Output Dictionary:
    stats_2d = {prime_class_label: classification, percent_label: percentage, freq_label: frequency}

    print(process_message_4)
    # Generate Data-Frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Set the Classification Column Datatype as Categorical:
    stats[prime_class_label] = stats[prime_class_label].astype('category')

    # Order the Dataset:
    stats = stats.sort_values(by=prime_class_label, ascending=False)

    # Plot the Dataset:
    get_simple_barplot(stats, title, location, prime_class_label)

    stats.set_index(prime_class_label, inplace=True)
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

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, prime_class_label], ascending=False).reset_index(drop=True)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1, f"{category_label} {percent_label}")
    get_heatmap(stats, category_label, title, 14, 10, True, location, 1, f"{category_label} {percent_label}")

    # print(stats) # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_primary_popularity_by_region():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()

    # Collate the Query Data into the Following Lists:
    result = get_pop_lists(region_list, 5, 1)

    # Column Label, Graph Title & Location:
    category_label = "Region"
    title = f"Primary Classification Popularity by Region"
    location = "Topic_stats/Primary/Region"

    # Get Dataset:
    stats = get_output(result, category_label, 1)

    # Plot the Dataset:
    get_catplot(stats, category_label, title, 8, 2, location, 1, f"{category_label} {percent_label}")
    get_heatmap(stats, category_label, title, 14, 10, True, location, 1, f"{category_label} {percent_label}")

    # Order the Dataset by category:
    stats = stats.sort_values(by=[category_label], ascending=False).reset_index(drop=True)

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
    get_catplot(stats, category_label, title, 8, 2, location, 1, f"{category_label} {percent_label}")
    get_heatmap(stats, category_label, title, 8, 11, True, location, 1, f"{category_label} {percent_label}")

    # Order the Dataset by Frequency:
    stats = stats.sort_values(by=[category_label, percent_label], ascending=False).reset_index(drop=True)

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
    get_catplot(stats, category_label, title, 8, 2, location, 1, f"{category_label} {percent_label}")
    get_heatmap(stats, category_label, title, 10, 7, True, location, 1, f"{category_label} {percent_label}")

    # Order the Dataset by category:
    stats = stats.sort_values(by=[category_label], ascending=False).reset_index(drop=True)

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
    get_catplot(stats, category_label, title, 8, 2, location, 1, f"{category_label} {percent_label}")
    get_heatmap(stats, category_label, title, 10, 7, True, location, 1, f"{category_label} {percent_label}")

    # Order the Dataset by category:
    stats = stats.sort_values(by=[category_label], ascending=False).reset_index(drop=True)

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
    s_classification = []
    p_classification = []
    frequency = []
    percentage = []
    relative_percentage = []
    class_list = []
    class_dic = {}
    total_count = 0

    print(process_message_2)

    # Where secondary s_classification is COMMON, add the subclasses of the primary s_classification to the count:
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
            total_count += 1
            if word in class_dic:
                class_dic[word] += 1
            else:
                class_dic[word] = 1

    for word in secondary_query_words:
        if word != 'COMMON':
            query = f"SELECT COUNT(ModuleCode) AS 'Count' FROM ModuleDetails WHERE A2 = '{word}' or B2 = '{word}';"
            for row in c.execute(query):
                total_count += row[0]
                if word in class_dic:
                    class_dic[word] += row[0]
                else:
                    class_dic[word] = row[0]

    for key, value in class_dic.items():
        s_classification.append(key)
        frequency.append(value)
        ratio = (value / total_count) * 100  # Calculate percentage of modules with current classification
        percentage.append(ratio)

    for topic in s_classification:
        query = f"SELECT PrimaryClassification FROM Classifications " \
                f"WHERE  SecondaryClassification = '{topic}';"
        for i in c.execute(query):
            word = str(i[0])
            p_classification.append(word)

    ap_count = cso_count = cm_count = gr_count = hw_count = hci_count = is_count = moc_count = nw_count = \
        sap_count = spt_count = swe_count = toc_count = u_count = 0
    for i in range(len(p_classification)):  # Tally the total num of modules for a given s_classification
        if p_classification[i] == "APPLIED COMPUTING":
            ap_count += frequency[i]
        elif p_classification[i] == "COMPUTER SYSTEMS ORGANISATION":
            cso_count += frequency[i]
        elif p_classification[i] == "COMPUTING METHODOLOGIES":
            cm_count += frequency[i]
        elif p_classification[i] == "GENERAL & REFERENCE":
            gr_count += frequency[i]
        elif p_classification[i] == "HARDWARE":
            hw_count += frequency[i]
        elif p_classification[i] == "HUMAN-CENTERED COMPUTING":
            hci_count += frequency[i]
        elif p_classification[i] == "INFORMATION SYSTEMS":
            is_count += frequency[i]
        elif p_classification[i] == "MATHEMATICS OF COMPUTING":
            moc_count += frequency[i]
        elif p_classification[i] == "NETWORKS":
            nw_count += frequency[i]
        elif p_classification[i] == "SECURITY & PRIVACY":
            sap_count += frequency[i]
        elif p_classification[i] == "SOCIAL & PROFESSIONAL TOPICS":
            spt_count += frequency[i]
        elif p_classification[i] == "SOFTWARE & ITS ENGINEERING":
            swe_count += frequency[i]
        elif p_classification[i] == "THEORY OF COMPUTATION":
            toc_count += frequency[i]
        elif p_classification[i] == "UNCLASSIFIABLE":
            u_count += frequency[i]

    # Adjustments to accommodate division by zero
    if ap_count == 0:
        ap_count = 1
    if cso_count == 0:
        cso_count = 1
    if cm_count == 0:
        cm_count = 1
    if gr_count == 0:
        gr_count = 1
    if hw_count == 0:
        hw_count = 1
    if hci_count == 0:
        hci_count = 1
    if is_count == 0:
        is_count = 1
    if moc_count == 0:
        moc_count = 1
    if nw_count == 0:
        nw_count = 1
    if sap_count == 0:
        sap_count = 1
    if spt_count == 0:
        spt_count = 1
    if swe_count == 0:
        swe_count = 1
    if toc_count == 0:
        toc_count = 1
    if u_count == 0:
        u_count = 1

    for i in range(
            len(p_classification)):  # Calculate the percentage of each subtopic within its s_classification
        if p_classification[i] == "APPLIED COMPUTING":
            ratio = (frequency[i] / ap_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "COMPUTER SYSTEMS ORGANISATION":
            ratio = (frequency[i] / cso_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "COMPUTING METHODOLOGIES":
            ratio = (frequency[i] / cm_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "GENERAL & REFERENCE":
            ratio = (frequency[i] / gr_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "HARDWARE":
            ratio = (frequency[i] / hw_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "HUMAN-CENTERED COMPUTING":
            ratio = (frequency[i] / hci_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "INFORMATION SYSTEMS":
            ratio = (frequency[i] / is_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "MATHEMATICS OF COMPUTING":
            ratio = (frequency[i] / moc_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "NETWORKS":
            ratio = (frequency[i] / nw_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "SECURITY & PRIVACY":
            ratio = (frequency[i] / sap_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "SOCIAL & PROFESSIONAL TOPICS":
            ratio = (frequency[i] / spt_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "SOFTWARE & ITS ENGINEERING":
            ratio = (frequency[i] / swe_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "THEORY OF COMPUTATION":
            ratio = (frequency[i] / toc_count) * 100
            relative_percentage.insert(i, ratio)
        elif p_classification[i] == "UNCLASSIFIABLE":
            ratio = (frequency[i] / u_count) * 100
            relative_percentage.insert(i, ratio)

    # Column Label, Graph Title & Location:
    title = "Secondary Classification Popularity by Module"
    location = "Topic_stats/Secondary/Module"

    print(process_message_3)

    # Generate Query Output Dictionary:
    stats_2d = {prime_class_label: p_classification, sub_class_label: s_classification, percent_label: percentage,
                freq_label: frequency, rel_percent_label: relative_percentage, }

    print(process_message_4)

    # Generate Data-frame from Dictionary:
    stats = pd.DataFrame.from_dict(stats_2d)

    # Plot the Dataset:
    get_simple_barplot(stats, title, location, sub_class_label)

    # Order the Dataset:
    stats = stats.sort_values(by=sub_class_label, ascending=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Get Alphabetically-Split Dataset & Plot each Subset:
    stats_1 = stats[stats[sub_class_label].str.contains('^[A-D]', regex=True, na=False)]  # A-D
    stats_2 = stats[stats[sub_class_label].str.contains('^[E-K]', regex=True, na=False)]  # E-K
    stats_3 = stats[stats[sub_class_label].str.contains('^[L-P]', regex=True, na=False)]  # L-P
    stats_4 = stats[stats[sub_class_label].str.contains('^[Q-Z]', regex=True, na=False)]  # Q-Z
    stat_list = [stats_1, stats_2, stats_3, stats_4]

    # Plot the Alphabetically-Split Dataset:
    i = 0
    for stat in stat_list:
        caption = f"{title} {alphabet_list[i]}"
        get_simple_barplot(stat, caption, location, sub_class_label)
        i += 1

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

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

    # Get Alphabetically-Split Dataset & Plot each Subset:
    get_alphabet_split_subsets_and_plot(stats, category_label, title, location)

    # Order By Category & Reset Index:
    stats = stats.sort_values(by=prime_class_label).reset_index(drop=True)

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    heights = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
    for df in cat_split:
        if df is not None:
            location = f"Topic_stats/Secondary/University/{primary_query_words[i]}"
            title = f"{primary_query_words[i]} Subcategory Popularity by University"
            get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 4,
                        f"{prime_class_label} {rel_percent_label}")
            get_catplot(df, category_label, title, 8, 2, location, 5, f"{prime_class_label} {rel_percent_label}")
            i += 1

    # Display the Process Runtime:
    print("Process Time:", "--- %s seconds ---" % (time.time() - start_time))


def get_secondary_popularity_by_region():
    start_time = time.time()

    print(process_message_1)

    # Generate a List of Available Regions:
    region_list = get_region_list()

    # Collate the Query Data into the Following Lists:
    pop_list = get_pop_lists(region_list, 5, 2)

    # Column Label, Graph Title & Location:
    category_label = "Region"
    title = f"Secondary Classification Popularity by Region"
    location = "Topic_stats/Secondary/Region"

    # Get Dataset:
    stats = get_output(pop_list, category_label, 2)

    # Order By Sub-Category & Rest Index:
    stats = stats.sort_values(by=sub_class_label).reset_index(drop=True)

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

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
            location = f"Topic_stats/Secondary/Region/{primary_query_words[i]}"
            title = f"{primary_query_words[i]} Subcategory Popularity by Region"
            get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 4,
                        f"{prime_class_label} {rel_percent_label}")
            get_catplot(df, category_label, title, 8, 2, location, 5, f"{prime_class_label} {rel_percent_label}")
            i += 1

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
    stats[percent_label] = stats[percent_label].astype('int32')

    # Get Categorically-Split Dataset:
    cat_split = get_categorically_split_subsets(stats)

    # Plot the Categorically-Split Dataset:
    i = 0
    widths = [14, 14, 10, 10, 10, 12, 12, 12, 10, 11, 12, 12, 10, 10]
    heights = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    for df in cat_split:
        location = f"Topic_stats/Secondary/Course/{primary_query_words[i]}"
        title = f"{primary_query_words[i]} Subcategory Popularity by Course"
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 2, None)
        i += 1

    # Order the dataset by Frequency and reset index:
    stats = stats.sort_values(by=percent_label, ascending=False).reset_index(drop=True)

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

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

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
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 4,
                    f"{prime_class_label} {rel_percent_label}")
        get_catplot(df, category_label, title, 8, 2, location, 5, f"{prime_class_label} {rel_percent_label}")
        i += 1

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

    # print(stats)  # Only required for testing

    print(process_message_6)

    # Save the Dataframe as .csv:
    output_to_csv(stats, title, location)

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
        get_heatmap(df, category_label, title, widths[i], heights[i], True, location, 4,
                    f"{prime_class_label} {rel_percent_label}")
        get_catplot(df, category_label, title, 8, 2, location, 5, f"{prime_class_label} {rel_percent_label}")
        i += 1

    # Display the Process Runtime:
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

    # By Region:
    get_primary_popularity_by_region()
    get_secondary_popularity_by_region()


# get_stats()  # Only required for testing
