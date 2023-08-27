import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#ingredient dictionary of beehoon
ingredient_list_beehoon = pd.read_excel('ingredient_list_beehoon.xlsx')
in_quantity_beehoon = ingredient_list_beehoon["In.quantity"].tolist()
in_name_beehoon = ingredient_list_beehoon["Ingredient list"].tolist()

#ingredient dictionary of chicken rice
ingredient_list_ckrice = pd.read_excel('ingredient_list_chickenrice.xlsx')
in_quantity_ckrice = ingredient_list_ckrice["In.quantity"].tolist()
in_name_ckrice = ingredient_list_ckrice["Ingredient list"].tolist()

#ingredient dictionary of egg fried rice
ingredient_list_eggrice = pd.read_excel('ingredient_list_eggfriedrice.xlsx')
in_quantity_eggrice = ingredient_list_eggrice["In.quantity"].tolist()
in_name_eggrice = ingredient_list_eggrice["Ingredient list"].tolist()

# Setting list and dictionary
restockfreq_beehoon = ingredient_list_beehoon["Restock freq"].tolist()
beehoon_restock_dict_all = dict(zip(in_name_beehoon, restockfreq_beehoon))
beehoon_restock_list_daily = []
beehoon_restock_list_weekly = []
for d in beehoon_restock_dict_all:
    if beehoon_restock_dict_all[d] == "daily":
        beehoon_restock_list_daily.append(d)
    elif beehoon_restock_dict_all[d] == "weekly":
        beehoon_restock_list_weekly.append(d)

restockfreq_ckrice = ingredient_list_ckrice["Restock freq"].tolist()
ckrice_restock_dict_all = dict(zip(in_name_ckrice, restockfreq_ckrice))
ckrice_restock_list_daily = []
ckrice_restock_list_weekly = []
for d in ckrice_restock_dict_all:
    if ckrice_restock_dict_all[d] == "daily":
        ckrice_restock_list_daily.append(d)
    elif ckrice_restock_dict_all[d] == "weekly":
        ckrice_restock_list_weekly.append(d)

restockfreq_eggrice = ingredient_list_eggrice["Restock freq"].tolist()
eggrice_restock_dict_all = dict(zip(in_name_eggrice, restockfreq_eggrice))
eggrice_restock_list_daily = []
eggrice_restock_list_weekly = []

for d in eggrice_restock_dict_all:
    if eggrice_restock_dict_all[d] == "daily":
        eggrice_restock_list_daily.append(d)
    elif eggrice_restock_dict_all[d] == "weekly":
        eggrice_restock_list_weekly.append(d)
weekly_in_name=beehoon_restock_list_weekly+ckrice_restock_list_weekly+eggrice_restock_list_weekly

monitoring_week = pd.read_excel('monitoring_week.xlsx')
monitoring_week2 = pd.read_excel('monitoring_week2.xlsx')
monitoring_week3 = pd.read_excel('monitoring_week3.xlsx')
monitoring_week4 = pd.read_excel('monitoring_week4.xlsx')

# For daily taking the average of each day of the week to get the par level
# Calculate daily average

monitoring_weeks = [monitoring_week, monitoring_week2, monitoring_week3, monitoring_week4]
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
meals = ['beehoon', 'ckrice', 'eggrice']

for day in days:
    for meal in meals:
        averages = []
        for i, week in enumerate(monitoring_weeks):
            average = week.iloc[days.index(day) * 3 + meals.index(meal), 2]
            averages.append(average)
        average = sum(averages) / len(averages)
        globals()[f"{meal}_{day}_average"] = average

# PAR level = (the amount of inventory used each week/month + 10% safety stock) / number of deliveries each week/month.

# Tomorrow aka tuesday daily restock ingredient recommendation

beehoon_in_consumtion_tue = [value * beehoon_tue_average for value in in_quantity_beehoon]
beehoon_restock_dict_tue = dict(zip(in_name_beehoon, beehoon_in_consumtion_tue))

new_beehoon_restock_dict_tue = {}
a = 0
for l in beehoon_restock_dict_tue:
    if l == beehoon_restock_list_daily[a]:
        new_beehoon_restock_dict_tue[l] = beehoon_restock_dict_tue[l]
        a += 1
        if a >= len(beehoon_restock_list_daily):
            break
beehoon_restock_dict_tue = new_beehoon_restock_dict_tue

ckrice_in_consumption_tue = [value * ckrice_tue_average for value in in_quantity_ckrice]
ckrice_restock_dict_tue = dict(zip(in_name_ckrice, ckrice_in_consumption_tue))

new_ckrice_restock_dict_tue = {}
a = 0
for l in ckrice_restock_dict_tue:
    if l == ckrice_restock_list_daily[a]:
        new_ckrice_restock_dict_tue[l] = ckrice_restock_dict_tue[l]
        a += 1
        if a >= len(ckrice_restock_list_daily):
            break
ckrice_restock_dict_tue = new_ckrice_restock_dict_tue

eggrice_in_consumtion_tue = [value * eggrice_tue_average for value in in_quantity_eggrice]
eggrice_restock_dict_tue = dict(zip(in_name_eggrice, eggrice_in_consumtion_tue))

new_eggrice_restock_dict_tue = {}
a = 0
for l in eggrice_restock_dict_tue:
    if l == eggrice_restock_list_daily[a]:
        new_eggrice_restock_dict_tue[l] = eggrice_restock_dict_tue[l]
        a += 1
        if a >= len(eggrice_restock_list_daily):
            break
eggrice_restock_dict_tue = new_eggrice_restock_dict_tue

# PAR level = (the amount of inventory used each week/month + 10% safety stock) / number of deliveries each week/month.

monitoring_weeks = [monitoring_week, monitoring_week2, monitoring_week3, monitoring_week4]
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
meals = ['beehoon', 'ckrice', 'eggrice']

meal_weekly_totals = {meal: [0, 0, 0, 0] for meal in meals}

for week_idx, week in enumerate(monitoring_weeks):
    for day in days:
        for meal in meals:
            sale = week.iloc[days.index(day) * 3 + meals.index(meal), 2]
            meal_weekly_totals[meal][week_idx] += sale
par_level_weekly = {}
for key, values in meal_weekly_totals.items():
    average = sum(values) / len(values)
    increased_average = average + 0.1 * average  # Adding 10% of the average
    par_level_weekly[key] = increased_average

beehoon_in_par_level_list = [num * par_level_weekly["beehoon"] for num in in_quantity_beehoon]
beehoon_in_par_level_dict = dict(zip(in_name_beehoon, beehoon_in_par_level_list))
beehoon_in_par_level = {key: value for key, value in beehoon_in_par_level_dict.items() if key in beehoon_restock_list_weekly}

ckrice_in_par_level_list = [num * par_level_weekly["ckrice"] for num in in_quantity_ckrice]
ckrice_in_par_level_dict = dict(zip(in_name_ckrice, ckrice_in_par_level_list))
ckrice_in_par_level = {key: value for key, value in ckrice_in_par_level_dict.items() if key in ckrice_restock_list_weekly}

eggrice_in_par_level_list = [num * par_level_weekly["eggrice"] for num in in_quantity_beehoon]
eggrice_in_par_level_dict = dict(zip(in_name_beehoon, eggrice_in_par_level_list))
eggrice_in_par_level = {key: value for key, value in eggrice_in_par_level_dict.items() if key in beehoon_restock_list_weekly}


# Create an excel sheet and transfer the recommended to the excel sheet
data_tue_restock = {
    'Ingredient': list(beehoon_restock_dict_tue.keys())+list(ckrice_restock_dict_tue.keys())+list(eggrice_restock_dict_tue.keys()),
    'Amount to order': list(beehoon_restock_dict_tue.values())+list(ckrice_restock_dict_tue.values())+list(eggrice_restock_dict_tue.values())
}
df = pd.DataFrame(data_tue_restock)
df.to_excel('Tue_restock.xlsx')

data_weekly_restock = {
    'Ingredient': weekly_in_name,
    'Amount to order': list(beehoon_in_par_level.values())+list(ckrice_in_par_level.values())+list(eggrice_in_par_level.values())

}
df = pd.DataFrame(data_weekly_restock)
df.to_excel('Weekly_restock.xlsx')

# plot trend graph
# Collect data for plotting
data = {meal: [globals()[f"{meal}_{day}_average"] for day in days] for meal in meals}

# Plotting
plt.figure(figsize=(10, 6))
bar_width = 0.2
index = np.arange(len(days))

for i, meal in enumerate(meals):
    plt.bar(index + i * bar_width, data[meal], bar_width, label=meal)

plt.xlabel('Day')
plt.ylabel('Daily Average Sale')
plt.title('Daily Average Sale for Each Meal')
plt.xticks(index + bar_width * (len(meals) - 1) / 2, days)
plt.legend()
plt.grid(True)
plt.show()