# %%
import pandas as pd
import streamlit as st
from collections import Counter
from PIL import Image

# %%
im = Image.open("./logo_ugry.png")
st.set_page_config(page_title="Количество созданных задач", page_icon=im)

# %%
st.title("Информация о провайдерах")
st.write("Количество провайдеров с откликом, процент таких провайдеров.")


uploaded_file = st.file_uploader("Выбирете файл")


if uploaded_file is not None:
     df = pd.read_csv(uploaded_file, sep='|')
     df.columns=[
         'phone',
         'count_responds',
         'count_pre_matched',
         'count_accepted'
         ]

     # изменение типов
     df['count_responds'] = df['count_responds'].astype(int)
     df['count_pre_matched'] = df['count_pre_matched'].astype(int)
     df['count_accepted'] = df['count_accepted'].astype(int)

     # удвление тестовых номеров, которые начинаются на 520...
     df = df[~df.phone.str.contains('1000')]
     df = df[~df.phone.str.contains('5200')]
     df = df[~df.phone.str.contains('052')]

     # удаление пропусков, которые появляются из за особенностей выгрузки
     df = df.dropna()
     file_container = st.expander("Check your uploaded .csv")   
     st.write(df)
else:
    st.info(
        f"""
             👆 Загрузите файл с расширением csv. В файле должны стого содержаться следующие столбцы:
             - id задачи, название задачи
             - текущий статус задачи
             - выбранный способ связи в приложении
             - дата создания задачи в формате ГГГГ-ММ-ДД
             - телефон заказчика
             """
    )
    st.stop()

# %%
st.write("""
**Поля датафрейма:**
- phone - телефон провайдера;
- count_responds - количество откликов у провайдера за период;
- count_pre_matched - количество прематчей у провайдера за период;
- count_accepted - количество матчей у провайдера за период;
""")

# %%
st.write("# Рассчеты")

# %%
st.write('Всего провайдеров:' ,df['phone'].nunique())

# %%
st.write('Провайдеры, которые оставили хотя бы один отклик:' ,df.query('count_responds > 0').count()[0])

# %%
st.write('Процент провайдеров, которые оставили отклик: ',
    round(df.query('count_responds > 0').count()[0] * 100 / df['phone'].nunique(), 2))

# %%
def count_resp(count_responds):
    if count_responds < 1:
        return '0 откликов'
    
    elif 1 <= count_responds <= 3:
        return 'От 1 до 3 откликов'
    
    elif 3 < count_responds <= 5:
        return 'От 3 до 5 откликов'
    
    elif 5 < count_responds <= 8:
        return 'От 5 до 8 откликов'
    
    elif 8 < count_responds <= 12:
        return 'От 8 до 12 откликов'
    
    elif 12 < count_responds <= 16:
        return 'От 12 до 16 откликов'
    
    elif 16 < count_responds <= 25:
        return 'От 16 до 25 откликов'
    
    elif 25 < count_responds <= 35:
        return 'От 25 до 35 откликов'
    
    elif 35 < count_responds <= 45:
        return 'От 35 до 45 откликов'
    
    elif 45 < count_responds <= 55:
        return 'От 45 до 55 откликов'
    
    else:
        return 'Более 55 откликов'
df['count_responds'].apply(count_resp).value_counts()

# %%
st.write("## Прематчи")

# %%
st.write('Количество провайдеров, которые перешли в хотя бы один прематч', df.query('count_pre_matched > 0').count()[0])

# %%
st.write('Процент провайдеров, которые перешли в прематч',
      round(df.query('count_pre_matched > 0').count()[0] * 100 / df.query('count_responds > 0').count()[0], 2))

# %%
st.write("## Матчи")

# %%
st.write('Количество провайдеров, которые были выбраны хотя бы один раз', df.query('count_accepted > 0').count()[0])

# %%
st.write('Процент провайдеров, которые перешлои в прематч',
      round(df.query('count_accepted > 0').count()[0] * 100 / df.query('count_pre_matched > 0').count()[0], 2))


