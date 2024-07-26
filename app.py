import pandas as pd
from config import FREQUENCE, START_DATE
from supplements import supplements


start_date = pd.to_datetime(START_DATE)

schedule = pd.DataFrame(index=pd.date_range(start=start_date, periods=max([v[0] for v in supplements.values()])))

for n, supplement in enumerate(supplements):
    start = start_date + pd.DateOffset(days=n * FREQUENCE)
    end = start + pd.DateOffset(days=supplements[supplement][0])
    schedule.loc[start:end, supplement] = '+'

for supplement in supplements:
    schedule[supplement] = schedule[supplement].apply(lambda x: supplements[supplement][1] if x == '+' else '')


schedule.reset_index(inplace=True)
schedule.rename(columns={'index': 'Дата'}, inplace=True)
for n, k in enumerate(schedule['Дата']):
    schedule.loc[n, 'Дата'] = k.to_pydatetime().strftime('%d %B').upper()

with open('nutri_schedule.md', 'w') as md, open('nutri_schedule.txt', 'w') as txt:
    md.write('## Мой график приёма\n\n')
    for di in schedule.to_dict('records'):
        md.write(f"**{di['Дата']}**\n\n")
        txt.write(f"{di['Дата']}\n")
        for nutri, times in {k: v for k, v in di.items() if v}.items():
            if nutri != 'Дата':
                md.write(f" - [ ] {nutri} - {times}\n\n")
                txt.write(f"    ▢ {nutri} - {times}\n")
        md.write('\n\n\n')
        txt.write('\n')

schedule = schedule.reindex(index=schedule.index[::-1])
schedule.reset_index(inplace=True, drop=True)
schedule.iloc[::-1].to_excel('nutri_schedule.xlsx', index=False)
