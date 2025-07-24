import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"D:\aave-credit-scoring\data\wallet_score.csv")

bins = [0, 200, 400, 600, 800, 1000]
labels = ['0-200', '201-400', '401-600', '601-800', '801-1000']


df['score_range'] = pd.cut(df['credit_score'], bins=bins, labels=labels, include_lowest=True)


score_distribution = df['score_range'].value_counts().sort_index()


plt.figure(figsize=(10, 6))
bars = plt.bar(score_distribution.index, score_distribution.values, color='#4a90e2')
plt.title("Credit Score Distribution of Wallets", fontsize=14)
plt.xlabel("Credit Score Range")
plt.ylabel("Number of Wallets")
plt.grid(axis='y', linestyle='--', alpha=0.7)


for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', va='bottom')

plt.tight_layout()
plt.savefig("credit_score_distribution.png")
plt.show()
