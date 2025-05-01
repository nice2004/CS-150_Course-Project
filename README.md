# Course Project

***Names: Nice Teta Hirwa*** <br />
***Instructor: Professor Mike Ryu*** <br />
***Class: CS-150*** <br />


## Thesis Statement
This dashboard explores the impact of personal remittances on Africa's GDP. Remittances represent money sent back or brought by migrants to their home countries that significantly boosts the local economies and improve living standards.

## Context of my data visualization
After the conference I attended at Yale University, I have always been wondering, 'does making an impact on the 
African continent mean to physically be there or remittances can also be another option of giving back?
This dashboard gives a reassuring answer by exploring how the African countries GDP are increasing due to remittances. When people migrate
and send money back to their countries, they tremendously contribute directly to their nation's economy. 
 

## Data I will be visualizing
I will be visualizing the increase of African countries GDP due to remittances using choropleth map and the line chart.
In the graph, the user is able to move the year slider to see the change of remittances over time. The user also has 
this flexibility by using a line chart beneath the map. As one clicks on the country, the change over time shows up beneath the map 
in terms of a line chart. The dashboard also has an interactive tab called 'Predict impact' that predicts the amount of 
GDP one would contribute by sending money to different countries, and it also forecasts the cumulative GDP over time. 


## Call to Action
This dashboard advocates that migrants or first generation families can still contribute to the 
African continent by sending remittances to their home country.  

## Strategies employed from SWD
1.  Articulating my unique point of view of the project
2. Specifically conveying what’s at stake
3. Displaying what is happening, what should be the audiences response, and how is the data being displayed correctly

## Explaining the coding part of the project
I have two main directories: 
1. Dataset: Has the dataset that I used in the visuals. 
2. Dashboard_Africa's GDP: In this dashboard, I have three main files:
- app.py: Has the layout of the whole dashboard 
- Callbacks.py: Has 7 callbacks that updates the choropleth map, update_year_display, update_country_dropdown_options, 
update_selected_countries, update_prediction_dropdown, update_line_chart, and updates_prediction

And I finally called the main() function to run the code.

## How to use the dashboard
Use the 'Map' tab to explore remittances as a percentage of GDP, with a focus on 
African countries. 
Use the year slider to see how remittance contributions have changed over time. 
You can toggle between global and Africa-specific views, click on countries in the map to add them to the trend chart, 
and select multiple countries to compare their remittance trends over time.

## Source of the Data
1. World in Data: https://ourworldindata.org/grapher/money-sent-or-brought-back-by-migrants-as-a-share-of-gdp



