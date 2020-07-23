
Package Info:

	Environment: Python 3.8

	The package contains the following five scripts and a database:

		* main.py
		* common_elements.py
		* course_template.py
		* keyword_popularity.py
		* topic_stats.py
		* TEST_DB_SPUR.db

	Required External Packages:

		* seaborn
		* matplotlib
		* pandas
		* sqlite 3
		* nltk (WordWordNetLemmatizer)
		* nltk.corpus (wordnet)
		* wordcloud
	
Instructions:

	* Before running the program ensure the package contents are located in the same directory and that all required packages are installed.

	* Run main.py file in a suitable IDE (Pycharm recommended). This will launch a menu interface in the python console.
	
	* User-input is numeric: All options will be numbered and the labelled number is the value to be entered.

Main Menu:
	
    The main menu presents four mode selections, Keyword Analysis, Topic Stats, Average Course Content, and Run All. 
			
        * Keyword Analysis:

            The frequencies of unique descriptive keywords can be identified, tabulated, and visualised using NLP methods. 
            The software examines module title, overview, and learning outcome content strings independently. Wordclouds are
            used to visualise the frequency tables. 
        
        * Topic Stats:

            Categorical analysis of the database content and generation of tables and chart
            for each dataset outlining the classification popularity within the scope of each category. The categorys are 
            classification level, university, course, and year. 
        
        * Average Course Content:
        
            Typical course structure per year generated from the mean proportion of topics in each course listed in the database. 
                
        * Run All:
                
            Run a predetermined sequence of all functions.