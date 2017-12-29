import requests
import json
import csv

#API key and file inofrmation at global scope
app_id = '53bbf52b'
app_key = '99fdd7529dd0cb81f7f97e94d0247a1f'
file_name = 'dict.csv'


# Calls Oxford Dictionary API using requests and returns a list of meanings
# Source: https://developer.oxforddictionaries.com/documentation

def make_request(word, language):

	definitions = []
	#construct Api Url
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
	#mak request
	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
	
	#definitons is empty if api call fails
	if r.status_code == 200:
		data = r.json()
		entries = data["results"][0]["lexicalEntries"]
		for entry  in entries:
			sense = entry["entries"][0]["senses"]
			for subsense in sense:

				definitions.append(json.dumps(subsense["definitions"][0])[1:-1])  #json.dumps give a string
				# the [1:-1] at the end gets rid of the double quotes. Probably find a neater way to
				# get rid of this altogether.

	return definitions

### function ends here ###

# checks csv file for meaning.If not found, uses make_request to get meaning and return a list of definitions

def getMeaning(word,language):

	definitions = [] 

	#read and check for meanings of word
	with open(file_name) as file:
		dict_file = csv.DictReader(file, delimiter = ',')

		# check for definition in file
		for row in dict_file:
			if str(row["word"]) == str(word):
				definitions.append(row["meaning"])

	#if found, return
	if definitions:
		#print "\n word found in local copy \n"
		return definitions

	#print "word not found in local copy \n"

	#if list is empty, make an api call
	definitions = make_request(word, language)

	#update csv file
	with open(file_name, "a+") as file:

		#print "Updating Local Copy"

		dict_file = csv.writer(file, delimiter=',')

		for defintion in definitions:
			dict_file.writerow([word, defintion])

	return definitions

### function ends here ###


#Start reading from here
#set default language to english
language = 'en' 

print "\n ###### Enter word for which you require a meaning ###### \n"
input_word = raw_input()  #CHANGE THIS TO INPUT() IF USING PYTHON 3.X

print "#### This word means #### \n"

meanings = getMeaning(input_word, language)

# check if no meaning found
if not meanings:
	print "\n ---> Sorry. I do not know what that means."

for meaning in meanings:
	print "\n ---> "+meaning
