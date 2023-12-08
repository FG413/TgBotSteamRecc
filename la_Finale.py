from surprise import Reader, Dataset, SVD
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel



steam_games = pd.read_csv('steam_games.csv', low_memory=False)





def NoGames(df):
    for i in df[df.columns[1]]:
        if list(steam_games[steam_games.columns[0]]).count(i) == 0:
            df.drop(df[df['appid'] == i].index, inplace=True)
    return df

def get_user(steam_id):
 steam_id = pd.DataFrame(our_user, columns=['user', 'appid', 'rating'])
 NoGames(steam_id)
 return steam_id


our_user = [['YUZH1542', 381210, 0.8585413273568598], ['YUZH1542', 570, 0.846203955184673],
 ['YUZH1542', 1966720, 0.5502518907629605], ['YUZH1542', 359550, 0.21241669277825437],
 ['YUZH1542', 730, 0.17976154640026176], ['YUZH1542', 440, 0.13617110024733045],
 ['YUZH1542', 512900, 0.1322739297684637], ['YUZH1542', 304930, 0.10032414995869667],
 ['YUZH1542', 632360, 0.08891102030178387], ['YUZH1542', 312530, 0.08262687563499269],
 ['YUZH1542', 1172620, 0.07979501154360376], ['YUZH1542', 1621690, 0.07579544508048934],
 ['YUZH1542', 466240, 0.07093988675257049], ['YUZH1542', 438740, 0.06933252164027025],
 ['YUZH1542', 4000, 0.06834996102206033], ['YUZH1542', 945360, 0.06768699713777802],
 ['YUZH1542', 646570, 0.06419947719080635], ['YUZH1542', 544920, 0.06013752876966535],
 ['YUZH1542', 274190, 0.05815526314990437], ['YUZH1542', 739630, 0.05447175155226524]]

our_user = get_user(our_user)


def update(df):
    users_df = pd.read_csv("steam.csv")
    NoGames(users_df)
    users_df = pd.concat([users_df, df], ignore_index=True)
    users_df = users_df.drop_duplicates()


    ratings_count = pd.DataFrame(columns=["user", "rating_counter"])
    ratings_count = users_df.groupby('appid')['user'].count() > 10
    ratings_count = ratings_count.loc[ratings_count]
    rating_viable = ratings_count.index.tolist()
    users_df = users_df[users_df['appid'].isin(rating_viable)]
    users_df[users_df.columns[2]] = users_df[users_df.columns[2]] * 5
    users_df = round(users_df, 1)

    final_df = pd.read_csv("final_df.csv").drop("Unnamed: 0", axis=1)

    final_df = users_df.merge(steam_games, on='appid')
    df_grouped = pd.read_csv("df_grouped.csv").drop("Unnamed: 0", axis=1)

    return users_df, final_df, df_grouped




# Функция для получения рекомендаций
dset = pd.read_csv("steam_df.csv").drop("Unnamed: 0", axis=1)
tfidf = TfidfVectorizer(stop_words='english')
data_matrix = tfidf.fit_transform(dset['tags'])
# Построение матрицы схожести косинусного расстояния
cosine_similarities = linear_kernel(data_matrix, data_matrix)

def get_recommendations(user_games):
    user_games = list(user_games[user_games.columns[1]][:])
# Индексы игр, которые пользователь уже играл
    indices = [dset[dset['appid'] == game_id].index[0] for game_id in user_games]
    indices = list(filter(None, indices))
# Суммируем схожести всех игр, в которые играл пользователь
    similarity_scores = cosine_similarities[indices].sum(axis=0)

# Сортировка схожих игр по убыванию
    top_indices = similarity_scores.argsort()[::-1]

# Исключаем игры, которые пользователь уже играл
    top_indices = [index for index in top_indices if index not in indices]

# Получаем список рекомендованных игр
    recommendations =list(dset.iloc[top_indices[:20]]['appid'])
    recommendations = recommendations[:5] + recommendations[15:20]
    recommendations = (steam_games.loc[steam_games['appid'].isin(recommendations),\
    ['name', 'short_description', 'header_image']]).to_numpy().tolist()
    return recommendations

first_recommended = get_recommendations(our_user) #первые рекоммендации
print(first_recommended)

def proxy(df):
    x=NoGames(df)
    return get_recommendations(list(x[x.columns[1]]))





def generate_recommendationsSVD(user, get_recommend = 10):
    users_df, final_df, df_grouped = update(user)
    user = user['user'][0]
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(final_df[['user','appid','rating']], reader)
    trainset = data.build_full_trainset()
    model = SVD(n_factors=50, n_epochs=10, lr_all=0.005, reg_all= 0.2)
    model.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = model.test(testset)
    predictions_df = pd.DataFrame(predictions)
# get the top get_recommend predictions for userID

    predictions_userID = predictions_df[predictions_df['uid'] == user].\
    sort_values(by="est", ascending = False).head(get_recommend)
    recommendations = []
    recommendations.append(list(predictions_userID['iid']))
    recommendations = recommendations[0]
    rec_games = (df_grouped.loc[df_grouped['appid'].isin(recommendations),['name', 'short_description', 'header_image']]).to_numpy().tolist()
    return rec_games

print(generate_recommendationsSVD(our_user))

#second_recommended = generate_recommendationsSVD(our_user) #вторые рекомендации