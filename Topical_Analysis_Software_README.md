
Package Info:

	Environment: Python 3.8

	The package contains the following four scripts and a database:

		* main_menu.py
		* filters_and_organisation.py
		* queries.py
		* analysis_module.py
		* TEST_DB_SPUR.db

	Required External Packages:

		* seaborn
		* matplotlib
		* pandas
	
Instructions:

	* Before running the program ensure the package contents are located in the same directory.

	* To use the programme, run the main_menu.py file in a suitable IDE (Pycharm recommended). This will launch a menu interface in the python console.
	
	* User-input is numeric: All options will be numbered and the labelled number is the value to be entered.

	Main Menu:
	
		The main menu presents two mode selections, Keyword Analysis and Topic Stats. 
			
			* Keyword Analysis:
	
				The Keyword analysis mode performs an examination of the content strings of module titles, 
				module overviews, and module learning outcomes which highlights keywords used in these descriptions. 
				The user may filter each query by classification level, semester taken, university name, course, 
				core/elective, and year offered. The user may then select an individual classification, iterate the 
				classification set, or return an overview of all classifications within the selected classification level.
				The programme then returns a table and graphic illustraing the data.
			
			* Topic Stats:

				The topic stats mode performs a categorical analysis of the curricula database and produces a table and chart(s)
				for each dataset outlining the classification popularity within the scope of each category. The categorys are 
				classification level, university, course, and year. 
