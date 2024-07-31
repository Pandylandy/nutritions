import datetime
import pandas as pd


def determine_order(meals):
    orders = {}
    priority = {
        "натощак": 0,
        "до завтрака": 1,
        "завтрак": 2,
        "после завтрака": 3,
        "до обеда": 4,
        "обед": 5,
        "после обеда": 6,
        "до ужина": 7,
        "ужин": 8,
        "после ужина": 9,
        "перед сном": 10
    }
    for meal in meals:
        for key in priority:
            if key in meal:
                if priority[key] not in orders.values():
                    orders[meal] = priority[key]
                else:
                    orders[meal] = priority[key] + 1
                break
        if 'после ужина' in meal:
                orders[meal] = max(priority.values()) + 1
    sorted_meals = sorted(orders.items(), key=lambda x: (x[1], meals.index(x[0])))
    return [meal for meal, _ in sorted_meals]


async def create_sc(supplements):
    start_date = datetime.date.today()
    total_days = 60

    def get_meal_times(times_str):
        return times_str.split('+')

    supplements_order = list(supplements.items())
    columns = ['Дата', 'Прием пищи', 'Добавка']
    df = pd.DataFrame(columns=columns)
    with open('nutri_schedule.txt', 'w') as txt, open('nutri_schedule.md', 'w') as md:
        for day in range(total_days):
            current_date = start_date + datetime.timedelta(days=day)
            txt.write('\n\n' + current_date.strftime('%d %B').upper()+'\n')

            meals = {}

            num_supplements = (day // 3) + 1

            for i in range(min(num_supplements, len(supplements_order))):
                supplement, info = supplements_order[i]
                days, meal_times = info
                if day < days:
                    times = get_meal_times(meal_times)
                    for time in times:
                        if time not in meals:
                            meals[time] = []
                        meals[time].append(supplement)
                        print(determine_order([x for x in meals]))
                        meals = {k: meals[k] for k in determine_order([x for x in meals])}
            for meal_time, supplements_list in meals.items():
                if supplements_list:
                    supplements_str = ', '.join(supplements_list)
                    df = df._append({
                        'Дата': current_date.strftime('%d %B'),
                        'Прием пищи': meal_time,
                        'Добавка': supplements_str
                    }, ignore_index=True)
                    txt.write(f" \n{meal_time.capitalize()}:\n")
                    for item in supplements_list:
                        txt.write(f'  ▢ {item}')
                        txt.write('\n')

    df.to_csv('nutri_schedule.xlsx', index=False)
    return df
