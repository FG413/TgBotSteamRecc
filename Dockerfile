FROM python:3.9

ADD test.py .
ADD Parser.py .
ADD algoritm.py .
ADD steam_df.csv .
ADD steam_games.csv .
ADD tempsnip.png .
ADD userdata.csv .
ADD df_grouped.csv .
ADD final_df.csv .
ADD GFG.csv .
ADD la_Finale.py .
ADD out.jpg .
ADD picture.py .
ADD steam.csv .
ADD steam_df.csv .
ADD steam_games.csv .

RUN pip install aiogram requests beautifulsoup4 numpy scipy pandas scikit-learn telebot lxml surprise

CMD ["python", "./test.py"]
