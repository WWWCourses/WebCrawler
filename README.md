# BNR App - WebCrawler Demo Project

## Instalation:

1. Clone project:

	`git clone https://github.com/WWWCourses/WebCrawler`

2. Install dependencies:


	```
	cd WebCrawler

	# create virtual env for the project:
	python -m venv .venv

	# activate virtual env !!! (for Windows, CMD:)
	.\.venv\Scripts\activate

	# and then install requirements:
	pip install -r requirements.txt
	```

3. Create database:
   Create new database, named 'bnrdb'.
   Then import bnrdb.sql:

   ```
   mysql -u root -p bnrdb < bnrdb.sql
   ```

4. Start the App:

	Just run the 'bnr_app.py' file.
	```
	python bnr_app.py
	```