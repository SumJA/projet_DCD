#!/usr/bin/python
import time

class Movies():
	def __init__(self, movie_file_tmdb, credit_file_tmdb):
		self.world = monde()
		self.my_movies = {}#Id as key, movie() as value.
		self.read_tmdb_credit(credit_file_tmdb)
		self.read_tmdb_movie(movie_file_tmdb)
		self.write_tsv()
		
	def read_tmdb_credit(self,credit_file_tmdb):
		"""
		Input: credit file from the tmdb dataset
		Initialize the Movies() class and affiliated with data
		"""
		
		with open(credit_file_tmdb, "r") as f:
			for i in f.readlines()[1:]:#skip first line, it's just column names.
				line = i.split("[")[0] #not interested in crew and cast for now. If we are, gotta change all of this.
				data = line.split(",")
				ID = int(data[0])
				
				title = ''.join(data[1:]).replace('"','')#in case there are "," in the title, and if some '"' are kept.
				self.my_movies[ID] = movie(title, ID)
				
	def read_tmdb_movie(self, movie_file_tmdb):
		"""
		Input: movie file from the tmdb dataset
		Fills in the Movies() class and affiliated with data.
		It takes code because of shitty csv with commas within the values.
		"""		
		with open(movie_file_tmdb, "r") as f:
			for i in f.readlines()[1:]:#skip first line, it's column names
				fail = False#We have not failed. Yet.
				data = i.split("[")
				try:
					budget = float(data[0][:-2])
				except:
					budget = 0
				#print(budget)
				other = data[1].split("]")
				dic_genre = eval( "[" + other[0].replace('""','"') + "]")
				genre = []
				for j in dic_genre:
					genre.append(j["name"])
				#print(genre)
				other = other[1].split(",")
				if len(other) != 2:
					homepage = other[1]
					try:
						ID = int(other[2])
					except:
						fail = True
						continue
				else:
					fail = True
					continue#We have failed retrieving the movie's ID. This happens 3 times.
				#print(homepage)
				#print(ID)
				other = data[2].split("]")
				dic_keywords = eval("[" + other[0].replace('""','"') + "]")
				keyword = []
				for j in dic_keywords:
					keyword.append(j["name"])
				#print(keyword)
				truc = other[1].split(",")
				language = truc[1]
				#print(language)
				try:
					popularity = float(truc[-2])
				except:#no popularity data?
					#happens 6 times
					fail = True
					continue
				#summary = ''.join(truc[2:-2]) Zut pour le résumé. Si tu le veut, utilise cette ligne, mais sache qu'il y a des choses très vilaine dedans.
				prod = []
				if len(data) > 3:
					if len(data[3]) > 3:
						if data[3][-3:] == '","':
							#print(data[3])
							other = eval ( "[" + data[3][:-3].replace('""','"'))
						elif data[3][-3:] == ']",':
							other = eval ( "[" + data[3][:-2].replace('""','"'))
						prod = []
						for j in other:
							prod.append(j["name"])
				#print(prod)
				
				other = data[4].split(']')
				pays = eval("[" + other[0].replace('""','"') + "]")
				country = []
				for i in pays:
					country.append(i['iso_3166_1'])#taking the letters rather than the full name.
				#print(country)
				other = other[1].split(",")
				release_date = other[1]
				#print(release_date)
				revenu = float(other[2])
				#print(revenu)
				try:
					runtime = float(other[3])
				except:
					runtime = 0
				#print(runtime)
				other = data[5].split(",")
				try:
					nb_vote = int(other[-1][:-1])
				except:
					nb_vote = 0
				#print(nb_vote)
				try:
					moy_vote = float(other[-2])
				except:
					moy_vote = 0
				#print(moy_vote)
				#print(ID)
				if not fail:
					self.my_movies[int(ID)].set_stuff(budget, genre, homepage, keyword, language, prod, country, release_date, revenu, runtime, nb_vote, moy_vote)
				else:
					print("WTF?")
					
	def write_tsv(self):
		f = open("MyMoviesInAProperFormat.tsv", "w")
		f.write("ID\ttitle\tbudget\trevenu\tnb_vote\tmoy_vote\truntime\trelease_date\thomepage\tprod\tlanguage\tcountry\tkeyword\tgenre\n")
		for i in self.my_movies.keys():
			c = self.my_movies[i]
			f.write('\t'.join([str(c.ID),c.title,str(c.budget),str(c.revenu), str(c.nb_vote), str(c.moy_vote), str(c.runtime), c.release_date, c.homepage, "|".join(c.prod), c.language, "|".join(c.country),"|".join(c.keyword),"|".join(c.genre)]))
			f.write("\n")
		f.close()
			
class movie():
	def __init__(self, m_title, m_ID):
		self.title = m_title#string
		self.ID = m_ID#integer
		self.budget = 0.
		self.genre = []
		self.homepage = ""
		self.keyword = []
		self.language = ""
		self.prod = []
		self.country = []
		self.release_date = ""
		self.revenu = 0.
		self.runtime = 0.
		self.nb_vote = 0
		self.moy_vote = 0.

	def get_ID(self):
		return self.ID
		
	def get_title(self):
		return self.title

	def set_stuff(self, budget, genre, homepage, keyword, language, prod, country, release_date, revenu, runtime, nb_vote, moy_vote):
		self.budget = budget
		self.genre = genre
		self.homepage = homepage
		self.keyword = keyword
		self.language = language
		self.prod = prod
		self.country = country
		self.release_date = release_date
		self.revenu = revenu
		self.runtime = runtime
		self.nb_vote = nb_vote
		self.moy_vote = moy_vote
		

class monde():
	def __init__(self):
		self.peuple = {}		

class personne():
	def __init__(self, p_ID, p_job, p_name):
		self.ID = p_ID#clef de la personne.
		self.job = [p_job] #list in case the person can have more than one job.
		self.name = p_name#son nom.
		
		
		
def main():
	movie_tmdb = "/home/adelme/master/MASTER_2/DCD/TopSecretProject/tmdb_5000_movies.csv"
	credits_tmdb = "/home/adelme/master/MASTER_2/DCD/TopSecretProject/tmdb_5000_credits.csv"
	Movies(movie_tmdb, credits_tmdb)
	
	
	
if "__main__" == __name__:
	main()
