import mysql.connector as mc

class DB():
	def __init__(self):
		# TODO: use config.ini and python configparser module
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

	def select_all_data(self):
		sql = "SELECT * FROM  radiotheaters"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchall()

		return result

	def get_column_names(self):
		sql = "SELECT * FROM  radiotheaters LIMIT 1;"

		with self.conn.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchone()

		return cursor.column_names

if __name__ == '__main__':
	db = DB()

	db.get_column_names()
