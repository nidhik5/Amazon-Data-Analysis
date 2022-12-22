import requests
from io import StringIO
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import seaborn as sns

url = "https://www.dataquest.io/wp-content/uploads/2019/09/amazon-orders.csv"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
req = requests.get(url, headers=headers)
data = StringIO(req.text)
df = pd.read_csv(data)


df["Total Charged"] = df["Total Charged"].str.replace('$','',regex=True).astype(float)
df["Subtotal"] = df["Subtotal"].str.replace('$','',regex=True).astype(float)
df["Shipping Charge"] = df["Shipping Charge"].str.replace('$','',regex=True).astype(float)
df["Tax Before Promotions"] = df["Tax Before Promotions"].str.replace('$','',regex=True).astype(float)
df["Tax Charged"] = df["Tax Charged"].str.replace('$','',regex=True).astype(float)
df["Total Promotions"] = df["Total Promotions"].str.replace('$','',regex=True).astype(float)
t=df["Total Charged"].sum()
tx=df["Tax Charged"].sum()
print("percent tax paid {0} %".format((tx/t)*100))

df=df.drop(['Buyer Name','Group Name','Website','Ordering Customer Email','Shipping Address Name','Shipping Address Street 1','Shipping Address Street 2','Shipping Address City','Shipping Address State'],axis=1)
#print(df)

daily_orders=df.groupby("Order Date").sum()["Total Charged"]
print("Daily amount spent",daily_orders)

df['Order Date'] = pd.to_datetime(df['Order Date'])
#print(df.head)

ind=df[df["Total Charged"]==df["Total Charged"].max()].index.values

print("Highest orders Rs.{0} on {1}".format(df["Total Charged"].max(),df["Order Date"].values[ind]))
print("lowest orders",df["Total Charged"].min())
print("Average orders",df["Total Charged"].mean())
print("Average tax paid",df["Tax Charged"].mean()/df["Total Charged"].mean()*100)

m=df.groupby(pd.Grouper(key='Order Date', freq='M', axis=0))
print("Monthly spending is\n",m.sum())

m=df.groupby(pd.Grouper(key='Order Date', freq='W', axis=0))
print("Weekly spending is\n",m.sum())

#'4/1/2019'.split('/')[0]
#def month(x) :
 #   x = pd.to_datetime(x)
  #  x = x.strftime('%d/%m/%Y')
   # x=str(x)
    #return x.split('-')[0]

#df["Month"]=df["Order Date"].apply(month)
#print((df["Month"].astype(int)).__len__)
#print((m.sum()).__len__)
corelation=df.corr()
#print (corelation)
sns.heatmap(corelation, xticklabels=corelation.columns, yticklabels=corelation.columns,annot=True)
#sns.pairplot(df)
#sns.displot(df['Total Charged']) bins=3 makes number of relations equal to 3
#cat plot mein boxen plot,violen
#nunique uniunique values
# #rel plot also der dimaag mein rakho
#joint plot kde kind
sns.relplot(x=df['Total Charged'],y=df['Order Date'],kind='line')
plt.show()
df['month']= pd.DatetimeIndex(df['Order Date']).month
plt.bar(df['month'], df['Total Charged'])
plt.ylabel('Tax charged')
plt.xlabel('Order Date')
plt.title('monthly')
plt.show() 