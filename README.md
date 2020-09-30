# SPUR 2020 Topical Analysis Toolkit

Deliver insights into the topical content of undergraduate degree programmes.

The existing database contains Computer Science programme data from several British and Irish universities. We used the 2012 Association for Computing Machinery Computing Classification System (ACMCCS) to categorise each module. 

https://dl.acm.org/ccs

If you intend to add to the existing database, please ensure the courses and modules are from departments of computer science. 
If you wish to use our tools with any other field, you will need to build a new database including an appropriate classification system. (Our schema uses a polyhierarchical ontology) 

As there is no standardised format for displaying course information on university websites, data collection and validation must be done manually.

Each module entity has the capacity for two primary classifications and two secondary classifications. We deliberately limited the complexity of classifications in our schema due to the time constraints of our project.  

For example, the ACMCCS contains 12 primary classifications. There are 84 secondary classifications spread across those primary topics. Each of those 84 secondary classifications may have tertiary, quaternary, and so on, classifications. Despite limiting the specificity of our classification scheme, our tools provide a clear and insightful breakdown of topic distributions in undergraduate courses.

We recommend using DB Browser for SQLite as the Database Management System

https://sqlitebrowser.org/

This research project was undertaken on behalf of the Department of Computer Science in Maynooth University as part of the Summer Programme for Undergraduate Researchers (SPUR) 2020.

https://padlet.com/MU_EXPLEARING/d4ngte96l3prn9dp


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
