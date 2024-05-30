import pickle
from tmdbv3api import Movie, TMDb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googletrans import Translator


movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'TMDb api 추가'
tmdb.language = 'ko-KR'

movies = pickle.load(open('cosine/movies.pkl', 'rb'))

#영화 정보 데이터 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies['soup'])

# 사용자 입력
#user_input = "Please recommend a movie for Tim Burton."

class CosineSimilarity():
    def __init__(self) -> None:
        pass

    def translate_to_english(self, text):
        translator = Translator()
        translated_text = translator.translate(text, dest='en').text
        return translated_text

    def combine_proper_nouns(self, text):
        combined_text = re.sub(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', lambda m: m.group(0).replace(' ', ''), text)
        return combined_text

    def preprocess(self, text):
        tokens = []
        if isinstance(text, list):
            text = ''.join(text)

        text = self.combine_proper_nouns(text)
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        user_token = word_tokenize(text)
        for word in user_token:
            if word not in stopwords.words('english'):
                tokens.append(word)
        return ' '.join(tokens)

    # 추천 영화 타이틀, 포스터
    def recommend(self, input_vector, tfidf_matrix):
        cosine_sim = cosine_similarity(input_vector, tfidf_matrix)
        similarity_scores = cosine_sim.flatten()
        recommended_movie_indices = similarity_scores.argsort()[-5:][::-1]

        titles = []
        posters = []
        for idx in recommended_movie_indices:
            movie_id = movies.iloc[idx]['id']
            details = movie.details(movie_id)

            #image_path = details['poster_path']
            #if image_path:
            #    image_path = 'https://image.tmdb.org/t/p/w500/' + image_path
            #else:
            #    image_path = 'no_imgae.jpg'

            titles.append(details['title'])
            posters.append('https://image.tmdb.org/t/p/w500/' + details['poster_path'])
            #posters.append(image_path)
        return titles, posters

    def result(self, user_input):
        # 사용자 입력 토큰화
        translated_input = self.translate_to_english(user_input)
        processed_input = self.preprocess(translated_input)
        input_vector = vectorizer.transform([processed_input])
        print('processed input: '+processed_input)

        # 코사인 유사도로 영화 추천
        titles, posters = self.recommend(input_vector, tfidf_matrix)
        return titles, posters
        #for i in range(0, 5):
        #    print(titles[i])
        #    print(posters[i])
        #    i += 1

#CosineSimilarity().result(user_input)