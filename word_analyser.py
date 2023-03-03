import json, nltk, re, time, sys

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

subreddit = sys.argv[1]
year = sys.argv[2]

#!!!!!!
location = ""
#!!!!!!

with open("/home/cassi/Nextcloud/Programming/reddit-scraper/"+year+"/subreddit_view/"+subreddit+".json", "r") as json_file:
    json_object = json.load(json_file)


word_list = [
    "trans", "transgender", "transgenders", "transsexual", "transsexuals", "transfem", "transfems", "transfeminine", "trans-fem", "trans-fems", "trans-feminine",
    "transmasc", "transmascs", "transmasculine", "trans-masc", "trans-mascs", "trans-masculine",
    "trans-woman", "trans-girl", "trans-man", "trans-guy", "nb", "nbs", "enby", "enbies", "enbys", "non-binary",
    "trans-women", "trans-girls", "trans-men", "trans-guys", "transwoman", "transwomen", "transmen", "transman", "transguy", 
    "transguys", "transgirls", "transgirls", "transgendered", "genderqueer", "agender", "bigender", "polygender", "genderfluid", "genderfuck"
]
single_words_with_trans = ["masc", "masculine", "fem", "feminine", "woman", "women", "girl", "girls", "man", "men", "guy", "guys"]

exclude_list = [",", ".", ":", "(", ")", "SYM", "$"]

word_count = {
    "total": 0,
    "trans": [0, []],
    "transgender": [0, []],
    "transgenders": [0, []],
    "transsexual": [0, []],
    "transsexuals": [0, []],
    "transfem": [0, []],
    "transfeminine": [0, []],
    "trans-fem": [0, []],
    "trans-feminine": [0, []],
    "transmasc": [0, []],
    "transmasculine": [0, []],
    "trans-masc": [0, []],
    "trans-masculine": [0, []],
    "trans-woman": [0, []],
    "trans-girl": [0, []],
    "trans-man": [0, []],
    "trans-guy": [0, []],
    "nb": [0, []],
    "nbs": [0, []],
    "enby": [0, []],
    "enbys": [0, []],
    "non-binary": [0, []],
    "trans masc": [0, []],
    "trans masculine": [0, []],
    "trans fem": [0, []],
    "trans feminine": [0, []],
    "trans woman": [0, []],
    "trans girl": [0, []],
    "trans man": [0, []],
    "trans guy": [0, []],
    "non binary": [0, []],
    "trans guys": [0, []],
    "trans girls": [0, []],
    "trans women": [0, []],
    "trans men": [0, []],
    "enbies": [0, []],
    "transfems": [0, []],
    "transmascs": [0, []],
    "trans-mascs": [0, []],
    "trans-fems": [0, []],
    "trans-girls": [0, []],
    "trans-women": [0, []],
    "trans-men": [0, []],
    "trans-guys": [0, []],
    "transwoman": [0, []],
    "transwomen": [0, []],
    "transman": [0, []],
    "transmen": [0, []],
    "transguy": [0, []],
    "transguys": [0, []],
    "transgirls": [0, []],
    "transgirl": [0, []],
    "transgendered": [0, []],
    "genderqueer": [0, []],
    "agender": [0, []],
    "bigender": [0, []],
    "polygender": [0, []],
    "genderfluid": [0, []],
    "genderfuck": [0, []],
}


words = []
counter = 0

program_start_time = int(time.time())
time_before = program_start_time

for item in json_object:
    time_difference = int(int(time.time())-program_start_time)
    if time_before != time_difference: print(counter, "/", len(json_object), "Objects processed. Running for:", time_difference , "seconds.")
    time_before = time_difference
    counter += 1

    text_words = item["title"] + " " +  item["text"]
    # remove urls
    text_words = re.sub(r'https?:\/\/\S+', '', text_words)
    # remove brackets
    text_words = re.sub(r'\[.*?\]', '', text_words)


    text_words = nltk.word_tokenize(text_words)
    text_words = nltk.pos_tag(text_words)

    for index in range(len(text_words)):
        word = text_words[index][0].lower()
        #Check Edgecases
        if not text_words[index][1] in exclude_list: #Ignore if item is punctuation
            words.append(word)
            if index == 0: #Add first word into list 
            #Check for compounding words in index 1
                if word == "non" and len(text_words) > 1: #Do not add the word non to list if succeeded by the word binary
                    if not text_words[index+1][0].lower() == "binary":
                        word_count["total"] = word_count["total"] +1
                if word in word_list: 
                    if word == "trans": #Make sure that trans is not used in combination with other terms
                        if len(text_words) > 1: #Prevent out of bounds error
                            if not text_words[index+1][0].lower() in single_words_with_trans:
                                word_count["trans"][0] = word_count["trans"][0] +1
                                word_count["trans"][1].append(item["permalink"])
                                word_count["total"] = word_count["total"] +1
                                #This code is now at 6x nested "if". This is so horrible but it works; I want to die.
                    else: #Add if not compound word separated by space
                        word_count[word][0] = word_count[word][0] +1
                        word_count[word][1].append("reddit.com" + item["permalink"])
                        word_count["total"] = word_count["total"] +1
                else: word_count["total"] = word_count["total"] +1 #Add word if no edge-case matching
            #Check compounding words
            #Check for compounding words up until last 
            elif index > 0 and not index > len(text_words) -2: #Ignore this check if it's the first word
                if word in single_words_with_trans: #Check if preceeded by trans
                    if text_words[index-1][0].lower() == "trans":
                        word_count["trans "+ word][0] = word_count["trans "+ word][0] +1
                        word_count["trans "+ word][1].append("reddit.com" + item["permalink"])
                        word_count["total"] = word_count["total"] +1
                elif word == "binary": #Check if preceeded by non (binary)
                    if text_words[index-1][0].lower() == "non":
                        word_count["non binary"][0] = word_count["non binary"][0] +1
                        word_count["non binary"][1].append("reddit.com" + item["permalink"])
                        word_count["total"] = word_count["total"] +1
                else: 
                    if word in word_list:
                        if word == "trans": #Check if the word trans is not a compound word separated by space
                            if not text_words[index+1][0].lower() in single_words_with_trans: #Add trans to the list if it is not used as a compound word
                                word_count["trans"][0] = word_count["trans"][0] +1
                                word_count["trans"][1].append("reddit.com" + item["permalink"])
                                word_count["total"] = word_count ["total"] +1
                        else: #If the word is not trans, which is used as a compound word sometimes, add itto the list
                            word_count[word][0] = word_count[word][0] +1
                            word_count[word][1].append("reddit.com" + item["permalink"])
                            word_count["total"] = word_count ["total"] +1
                    elif word == "non": #If non is not used in conjunction with binary add it to the total 
                        if not text_words[index+1][0].lower() == "binary": word_count["total"] = word_count ["total"] +1
                    #If the word has nothing to do with being trans add to total word count
                    else: word_count["total"] = word_count ["total"] +1
            #Check for compounding words of last element
            else:
                if word == "binary": 
                    if text_words[index -1][0].lower() == "non": #If binary is used as a compound word with non, add it to the list of non binary
                        word_count["non binary"][0] = word_count["non binary"][0] +1
                        word_count["non binary"][1].append("reddit.com" + item["permalink"])
                        word_count["total"] = word_count["total"] +1
                elif word in single_words_with_trans: #If the word is used as a compound word with trans, add it to the list of compounded words
                    if text_words[index -1][0].lower() == "trans":
                        word_count["trans "+ word][0] = word_count["trans "+ word][0] +1
                        word_count["trans "+ word][1].append("reddit.com" + item["permalink"])
                        word_count["total"] = word_count["total"]+1
                elif word in word_list: 
                    word_count[word][0] = word_count[word][0] +1
                    word_count[word][1].append("reddit.com" + item["permalink"])
                    word_count["total"] = word_count["total"] +1
                else:
                    word_count["total"] = word_count["total"]+1

with open("./"+year+"/subreddit_view/"+year+"-"+subreddit+"-result.json", "w") as result_file:
    json.dump(word_count, result_file)
result_file.close()