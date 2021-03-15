"""
title: postholer-scraper.py
author: James Kitchens
date: March 14, 2021
description:
    This script scrapes Appalachian Trail waypoint information from the Postholer website and saves it as a CSV.
"""

import requests
from bs4 import BeautifulSoup


def table_to_array(table):
    array = []
    for row in table.findAll('tr'):
        columns = row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        array.append(output_row)
    return array


# Postholer has broken the AT into segments defined by starting mileage
# These starting mileages are used for the URLs 
sections = [
    0.0,
    53.3,
    166.4,
    276.5,
    393.9,
    467.6,
    587.9,
    703.1,
    784.7,
    862.0,
    979.9,
    1026.1,
    1124.5,
    1223.5,
    1299.5,
    1408.3,
    1503.2,
    1613.4,
    1706.1,
    1750.1,
    1856.9,
    1963.8,
    2064.6
]

# Loops through the sections and scrapes waypoints table
# Aggregates to all_data array
all_data = []
header = True
for sec in sections:
    section_data = BeautifulSoup(requests.get("https://www.postholer.com/databook/Appalachian-Trail/3/" + str(sec)).text, "html.parser")
    waypoints = section_data.find("table", {"class": "wptTable"})
    array = table_to_array(table=waypoints)
    if header:
        all_data.append(array[1])
        header = False
    for row in array[2:]:
        all_data.append(row)


# Save select waypoint's description, mile, and elevation to CSV
# Removes waypoints without mileage and elevation data
with open('../AT-waypoints.csv', 'w') as outfile:
    number_of_rows = len(all_data)
    for row in range(number_of_rows):
        row_length = len(all_data[row])
        if all_data[row][0] != "" and all_data[row][1] != "" and all_data[row][5] != "":
            for column in [0,1,5]:
                if column != 5:
                    outfile.write(all_data[row][column] + ",")
                else:
                    outfile.write(all_data[row][column])
            if row != number_of_rows - 1:
                outfile.write("\n")