# SPUR 2020 Topical Analysis Toolkit
Package Info:

	Environment: Python 3.8

	The package contains the following six scripts and a database:

		* main.py
		* common_elements.py
		* topic_distribution.py
		* keyword_analysis.py
		* topic_stats.py
		* setup.py
		* acm_curricula_2020_spur.db

	Required External Packages:

		* seaborn
		* matplotlib
		* pandas
		* sqlite 3
		* nltk (WordWordNetLemmatizer)
		* nltk.corpus (wordnet)
		* wordcloud
	
Instructions:

	* Before running the program ensure the package contents are located together in the same directory.
	
	* On the first launch of the software run the Setup option from the menu (Option 5) in order to install and update all required packages and libraries.

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
        
        * Topic Distribution:
        
            Typical course structure per year generated from the mean proportion of topics in each course listed in the database. 
        
        * Setup:
        
            Install and update required packages and libraries.
                  
        * Run All:
                
            Run a predetermined sequence of all functions.
