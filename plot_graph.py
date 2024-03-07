import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'stat_4.csv'
data = pd.read_csv(csv_file)

plt.figure(figsize=(30, 6))
plt.title('Stat of Silhouette Score')

plt.bar(data['Category'], data['uncovered_nodes'])

plt.xlabel('parameters')
plt.ylabel('value')
plt.savefig('stat_openai_uncovered_nodes.png', dpi=300, bbox_inches='tight')
plt.show()