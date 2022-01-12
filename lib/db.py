import mysql.connector as mc

class DB():
	def __init__(self):
		mysql_config = {
			'host':'localhost',
			'user':'test',
			'password':'qazwsxedc',
			'database':'bnrdb'
		}
		self.connect(mysql_config)

	def connect(self, config):
		try:
			self.conn = mc.connect(**config)
		except mc.Error as e:
			print(e)


	def create_radiotheaters_table(self):
		sql = """
			CREATE TABLE IF NOT EXISTS radiotheaters(
				id INT AUTO_INCREMENT PRIMARY KEY,
				title VARCHAR(100) NOT NULL,
				date DATE NOT NULL,
				content TEXT
			);
		"""

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def drop_radiotheaters_table(self):
		sql = "DROP TABLE IF EXISTS radiotheaters";

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			self.conn.commit()

	def insert_rows(self, rows_data):
		sql = """
			INSERT INTO radiotheaters
			(title, date, content)
			VALUES ( %s, %s, %s)
		"""

		with self.conn.cursor() as cursor:
			cursor.executemany(sql, rows_data)
			self.conn.commit()

	def insert_row(self, row_data):
		sql = """
			INSERT INTO radiotheaters
				(title, date, content)
				VALUES ( %s, %s, %s)
		"""

		with self.conn.cursor(prepared=True) as cursor:
			cursor.execute(sql, tuple(row_data.values()))
			self.conn.commit()


if __name__ == '__main__':
	db = DB()
	db.create_radiotheaters_table()

	data = {
		'title':'title',
		'pub_date_str':'2021-01-23',
		'pub_content':'pub_content'
	}
	db.insert_row(data)