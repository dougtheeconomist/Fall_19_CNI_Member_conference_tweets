#Title: CNI analysis functions
#Author: Doug Hart
#Date Created: 2/6/2020
#Last Updated: 2/6/2020


def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower()) if word.isalpha()]

def tidy_up(df):
    df.drop('Profile Image', inplace=True, axis = 1)
    df.drop('Time Zone', inplace=True, axis = 1)
    df.drop('Geo', inplace=True, axis = 1)
    #after looking at a random sample of the media column, have concluded not important
    df.drop('Media', inplace=True, axis = 1)
    df.rename(columns={'Universal Time Stamp': 'univ_ts', 
                    'Local Time Stamp': 'local_ts',
                    'User Mentions': 'user_mentions',
                    'Follower Count': 'follower_count'}, inplace=True)

    indexlist = []
    for i in range(0, 2037):
        if (df['Text'][i][0:2]) == 'RT':
            indexlist.append(i)
        else:
            pass
    len(indexlist)  #786
    for i in indexlist:
        df.drop(axis=0, index=i, inplace=True)
    spamlist =[1943, 1944, 1945, 1946]
    for i in spamlist:
        df.drop(axis=0, index=i, inplace=True)

#From the internet; finding topwords in categories from nmf

def get_nmf_topics(model, n_top_words=10):
    
    #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    feat_names = vectorizer.get_feature_names()
    
    word_dict = {}
    for i in range(num_topics):
        
        #for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-20 - 1:-1]
        words = [feat_names[key] for key in words_ids]
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = words
    
    return pd.DataFrame(word_dict)

# to call; get_nmf_topics(model, 20)

def run_it(data, feat, groups):
    data_ = data
    content = data
    wordnet = WordNetLemmatizer()

    vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features= feat)
    X = vectorizer.fit_transform(content)
    V = X.toarray()
    features = vectorizer.get_feature_names()
    W = np.random.rand(data.shape[0],groups)
    H = np.zeros((groups,feat)) 
    nmf = NMF(n_components=groups)
    W =nmf.fit_transform(V)
    H = nmf.components_
    nmf.inverse_transform(W)
    print('reconstruction error:', nmf.reconstruction_err_)
    return V, H, W