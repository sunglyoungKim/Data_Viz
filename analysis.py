import json
import altair as alt
import pandas as pd

def createChart(data, name):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    total_selection    = alt.selection_single(name="total", empty="all", encodings=['y'])
    # maxCount            = int(data['total'].value_counts().max())

    barMean = alt.Chart() \
        .mark_bar(stroke="Black") \
        .encode(
            alt.X("total:Q", axis=alt.Axis(title="Total")),
            alt.Y('cuisine:O', axis=alt.Axis(title="{} Cuisine Name".format(name)),
                  sort=alt.SortField(field="total", op="mean", order='descending')),
            alt.ColorValue("LightGrey", condition=color_condition),
        ).properties(
            selection = highlight_selection+total_selection,
        )

    return alt.hconcat(barMean,
        data=data,
        title="{} Cuisine Counts".format(name)
    )


def loadData(zipcode):
    import os
    cur_dir= os.path.dirname(__file__)
    nyc_restaurnat = json.load(open(os.path.join(cur_dir, 'nyc_restaurants_by_cuisine.json'), 'r'))
    # android_reviews = json.load(open(os.path.join(cur_dir, 'nyc_restaurants_by_cuisine.json'), 'r'))

    df_res = pd.DataFrame([(nyc_restaurnat[i].get('cuisine'), nyc_restaurnat[i].get('perZip').get(zipcode))
                       for i in range(len(nyc_restaurnat))][:25],
                      columns=['cuisine', 'total'])
    df_res.dropna()

    # dfAndroid = pd.DataFrame(((app, review['rating'], review['review'])
    #                           for app,reviews in android_reviews.items()
    #                           for review in reviews), columns=['name', 'rating', 'content'])
    return df_res
