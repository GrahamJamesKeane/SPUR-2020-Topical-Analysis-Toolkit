import pandas as pd
from common_elements import get_course_list, year_list, primary_query_words, open_sqlite, set_max_rows_pandas, \
    output_to_csv
from topic_stats import get_catplot, get_heatmap
from datetime import datetime


# Returns the average course-content as percentage topic per year
def get_topic_distribution():
    c = open_sqlite()

    # Set pandas options to view all entries:
    set_max_rows_pandas()

    # Generate a list of available courses:
    course_list = get_course_list()

    print("Compiling Classification Distributions...")

    # Containers for the frequencies of topics in each year:
    year_1 = {'APPLIED COMPUTING': 0, 'COMPUTER SYSTEMS ORGANISATION': 0,
              'COMPUTING METHODOLOGIES': 0,
              'GENERAL & REFERENCE': 0, 'HARDWARE': 0, 'HUMAN-CENTERED COMPUTING': 0,
              'INFORMATION SYSTEMS': 0,
              'MATHEMATICS OF COMPUTING': 0, 'NETWORKS': 0, 'SECURITY & PRIVACY': 0,
              'SOCIAL & PROFESSIONAL TOPICS': 0, 'SOFTWARE & ITS ENGINEERING': 0,
              'THEORY OF COMPUTATION': 0,
              'UNCLASSIFIABLE': 0}
    year_2 = {'APPLIED COMPUTING': 0, 'COMPUTER SYSTEMS ORGANISATION': 0,
              'COMPUTING METHODOLOGIES': 0,
              'GENERAL & REFERENCE': 0, 'HARDWARE': 0, 'HUMAN-CENTERED COMPUTING': 0,
              'INFORMATION SYSTEMS': 0,
              'MATHEMATICS OF COMPUTING': 0, 'NETWORKS': 0, 'SECURITY & PRIVACY': 0,
              'SOCIAL & PROFESSIONAL TOPICS': 0, 'SOFTWARE & ITS ENGINEERING': 0,
              'THEORY OF COMPUTATION': 0,
              'UNCLASSIFIABLE': 0}
    year_3 = {'APPLIED COMPUTING': 0, 'COMPUTER SYSTEMS ORGANISATION': 0,
              'COMPUTING METHODOLOGIES': 0,
              'GENERAL & REFERENCE': 0, 'HARDWARE': 0, 'HUMAN-CENTERED COMPUTING': 0,
              'INFORMATION SYSTEMS': 0,
              'MATHEMATICS OF COMPUTING': 0, 'NETWORKS': 0, 'SECURITY & PRIVACY': 0,
              'SOCIAL & PROFESSIONAL TOPICS': 0, 'SOFTWARE & ITS ENGINEERING': 0,
              'THEORY OF COMPUTATION': 0,
              'UNCLASSIFIABLE': 0}
    year_4 = {'APPLIED COMPUTING': 0, 'COMPUTER SYSTEMS ORGANISATION': 0,
              'COMPUTING METHODOLOGIES': 0,
              'GENERAL & REFERENCE': 0, 'HARDWARE': 0, 'HUMAN-CENTERED COMPUTING': 0,
              'INFORMATION SYSTEMS': 0,
              'MATHEMATICS OF COMPUTING': 0, 'NETWORKS': 0, 'SECURITY & PRIVACY': 0,
              'SOCIAL & PROFESSIONAL TOPICS': 0, 'SOFTWARE & ITS ENGINEERING': 0,
              'THEORY OF COMPUTATION': 0,
              'UNCLASSIFIABLE': 0}

    # Total recorded number of modules overall for each year:
    year_1_total_modules = year_2_total_modules = year_3_total_modules = year_4_total_modules = 0

    # Generate a frequency table of topics by observing the occurrence of topics in each course
    # listed in the database:
    for year in year_list:
        for course in course_list:
            if course != "UNKNOWN":
                for key in primary_query_words:
                    query = f"SELECT COUNT(Course.ModuleCode) FROM Course INNER JOIN Module " \
                            f"ON Course.ModuleCode = Module.ModuleCode " \
                            f"WHERE CourseCode = '{course}' AND YearOffered = {year} AND (Module.A1 = '{key}' " \
                            f"or Module.B1 = '{key}');"
                    for row in c.execute(query):  # Add the classification frequency to
                        key_count = row[0]
                        if year == 1:
                            year_1[key] += key_count  # Update the topic count
                            year_1_total_modules += key_count  # Update the total year count
                        elif year == 2:
                            year_2[key] += key_count
                            year_2_total_modules += key_count
                        elif year == 3:
                            year_3[key] += key_count
                            year_3_total_modules += key_count
                        elif year == 4:
                            year_4[key] += key_count
                            year_4_total_modules += key_count

    print("Transferring to Dictionary...")

    # Compute percentage of modules for a given topic per year & transfer this information to the
    # course_template container:
    course_template = {"Primary Classification": [], "Year": [], "Num Modules": [], "Total Modules": [], "Percent": []}
    for key, value in year_1.items():
        ratio = round((value / year_1_total_modules) * 100, 2)
        course_template["Primary Classification"].append(key)
        course_template["Year"].append(1)
        course_template["Num Modules"].append(value)
        course_template["Total Modules"].append(year_1_total_modules)
        course_template["Percent"].append(ratio)
    for key, value in year_2.items():
        ratio = round((value / year_2_total_modules) * 100, 2)
        course_template["Primary Classification"].append(key)
        course_template["Year"].append(2)
        course_template["Num Modules"].append(value)
        course_template["Total Modules"].append(year_2_total_modules)
        course_template["Percent"].append(ratio)
    for key, value in year_3.items():
        ratio = round((value / year_3_total_modules) * 100, 2)
        course_template["Primary Classification"].append(key)
        course_template["Year"].append(3)
        course_template["Num Modules"].append(value)
        course_template["Total Modules"].append(year_3_total_modules)
        course_template["Percent"].append(ratio)
    for key, value in year_4.items():
        ratio = round((value / year_4_total_modules) * 100, 2)
        course_template["Primary Classification"].append(key)
        course_template["Year"].append(4)
        course_template["Num Modules"].append(value)
        course_template["Total Modules"].append(year_4_total_modules)
        course_template["Percent"].append(ratio)

    print("Transferring to Dataframe...")

    # Transfer course_template container to a dataframe:
    course_template_df = pd.DataFrame.from_dict(course_template).sort_values(by=["Primary Classification"],
                                                                             ascending=True).reset_index(drop=True)
    location = "Topical_Distribution"

    # Generate plot of the dataset:
    get_catplot(course_template_df, "Year", "Typical Course Topical Distribution per Year", 8, 2, location,
                3, ratio_label="Percent")
    get_heatmap(course_template_df, "Year", "Typical Course Topical Distribution per Year", 20, 9, True,
                location, 3, ratio_label="Percent")

    # Generate subsets of dataframe by year:
    year_1_percent = course_template_df[course_template_df["Year"] == 1].sort_values(by=["Primary Classification"],
                                                                                     ascending=True).reset_index(
        drop=True)
    year_2_percent = course_template_df[course_template_df["Year"] == 2].sort_values(by=["Primary Classification"],
                                                                                     ascending=True).reset_index(
        drop=True)
    year_3_percent = course_template_df[course_template_df["Year"] == 3].sort_values(by=["Primary Classification"],
                                                                                     ascending=True).reset_index(
        drop=True)
    year_4_percent = course_template_df[course_template_df["Year"] == 4].sort_values(by=["Primary Classification"],
                                                                                     ascending=True).reset_index(
        drop=True)
    stat_list = [year_1_percent, year_2_percent, year_3_percent, year_4_percent]

    # Plot the Year-Split Dataset:
    i = 0
    for stat in stat_list:
        caption = f"Typical Course Topical Distribution Year {year_list[i]}"
        get_catplot(stats=stat, category_label="Year", title=caption, height=8, aspect=2, location=location, mode=4,
                    ratio_label="Percent")
        get_heatmap(stat, "Year", caption, 20, 9, True, location, 3, ratio_label="Percent")
        i += 1

    print("Saving to File...")

    # Output the main dataframe to file:
    stamp = str(datetime.today()).replace(":", ".")
    output_to_csv(course_template_df, f"Typical_Course_Topical_Distribution_by_Percent_per_Year_{stamp}", location)

    # print(course_template_df)  # For testing only

# get_topic_distribution()  # For testing only
