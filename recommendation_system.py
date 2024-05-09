from sqlalchemy.engine.result import result_tuple
import pandas as pd

class RecomendationSystem:
    def __init__(self, data):
      self.df = pd.read_csv(data)

    def recommendation(self, genre=None, year=None, duration=None, top=20):
      df = self.df.copy()
      df = self.demographic_filtering(df, genre=genre, duration=duration, year=year)
      df = self.run_imdb_score(df)

      result = df.loc[:, "title" : "release_year"]
      result = result.sort_values ("vote_average", ascending=False)
      result = result.head(top)
      return result

    @staticmethod
    def demographic_filtering(df, genre=None, year=None, duration=None):
      df = df.copy()

      if genre is not None:
          df = df[df[genre].all(axis=1)]

      if year is not None:
          df = df[df.release_year.between(year[0], year[1])]

      if duration is not None:
          df = df [df.runtime.between(duration[0], duration[1])]
      return df

    @staticmethod
    def run_imdb_score (df):
      df = df.copy()
      m = df.vote_count.quantile(0.7)
      C = (df.vote_average * df.vote_count).sum() / df.vote_count.sum()
      df = df[df.vote_count >= m]
      df["score"] = df.apply(lambda x: (x.vote_average * x.vote_count + C*m)/(x.vote_count + m), axis=1)
      return df