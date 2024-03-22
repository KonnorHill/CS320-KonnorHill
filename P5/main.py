# project: p5
# submitter: kkhill4
# partner: none
# hours: 8

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline


class UserPredictor:
    def __init__(self):
        self.x_cols = ["past_purchase_amt", "seconds", "age"]
        self.model = make_pipeline(
            PolynomialFeatures(degree=2),
            StandardScaler(),
            LogisticRegression(max_iter=500),
        )

    def fit(self, users, logs, y):
        train_df = pd.merge(users, logs.groupby("user_id")["seconds"].sum().reset_index(), how="left", on="user_id").fillna(0)
        train_df = pd.merge(train_df, y, on="user_id")
        
        self.model.fit(train_df[self.x_cols], train_df["y"])
        
        scores = cross_val_score(self.model, train_df[self.x_cols], train_df["y"])
        return f"AVG: {scores.mean()}, STD: {scores.std()}"

    def predict(self, users, logs):
        test_df = pd.merge(users, logs.groupby("user_id")["seconds"].sum().reset_index(), how="left", on="user_id").fillna(0)
        return self.model.predict(test_df[self.x_cols])
