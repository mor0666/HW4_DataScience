import pandas as pd
import numpy as np

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go


class Cluster:

    def preprocess(self, file_path):
        #reading the file
        df = pd.read_excel(file_path.get())
        #handling missing values inside our dataframe
        #first we will see where the missing values are:
        series = df.apply(lambda x: sum(x.isnull()),axis=0) #series of column name and num of missing values
        imputer = SimpleImputer(missing_values=np.NaN, strategy='mean')
        for i in series.index: #for an item in that series we will check if it has NaN values and if it does we will fill them with the mean
            if (series[i] > 0):
                df[i] = imputer.fit_transform(df[i].values.reshape(-1, 1))[:, 0]
        #after we take care of the missing values we will normalize our data using sklearn preprocessing
        scaler = StandardScaler()
        d = df.columns.drop('country')
        df[d] = scaler.fit_transform(df[d])
        #now we will group by the country
        df = df.groupby(['country']).mean()
        #we will drop the year column
        df.drop('year', inplace=True, axis=1)
        return df


    def cluster(self, dataframe, k, runs):
        #create the KMeans model
        kmeans = KMeans(n_clusters=k,n_init=runs).fit(dataframe)
        #adding the output for each country to the dataframe
        vals = []
        for i in range(len(dataframe)):
            newarr = dataframe.iloc[i, :].values
            vals.append(kmeans.predict(newarr.reshape(1, -1))[0])
        dataframe['algorithmOutput'] = vals
        #create figure 1:
        Y = dataframe['Generosity']
        X = dataframe['Social support']
        colors = dataframe['algorithmOutput']
        plt.scatter(X, Y, c=colors, cmap='viridis')

        dsada = plt.colorbar()
        dsada.set_label('Cluster Number to color')

        plt.title('Generosity-Social Support and their corresponding cluster')
        plt.xlabel('Social support')
        plt.ylabel('Generosity')


        plt.savefig('plot1.png',dpi=82)
        plt.close()

        #make the countries be a columns insted of the index
        #dataframe_temp = dataframe.reset_index(level=0)

        #histograma - we need the 3 letter code for the countries to use it:
        # py.sign_in("lidor12","NblOUQlm9HPqrNKAgPUw")
        # fig = go.Figure(data=go.Choropleth(
        #     locations=dataframe_temp['country'],
        #     z=dataframe_temp['algorithmOutput'],
        #     text=dataframe_temp['country'],
        #     colorscale='Blues',
        #     autocolorscale=False,
        #     reversescale=True,
        #     marker_line_color='darkgray',
        #     marker_line_width=0.5,
        #     colorbar_title='Clusters',
        # ))
        # fig.update_layout(
        #     title_text='World countries and the clusters they belong',
        #     geo=dict(
        #         showframe=False,
        #         showcoastlines=False,
        #         projection_type='equirectangular'
        #     )
        # )
        # py.image.save_as(fig,filename='map.png')
        return


