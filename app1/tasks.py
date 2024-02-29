# from celery  import shared_task
# import pandas as pd
# from .models import *

# @shared_task()
# def create_db(file_path):
#     # df = pd.read_csv(file_path,delimiter=',')
#     # print(df.values)
#     # list_of_csv = [list(row) for row in df.values]

#     # for row in list_of_csv:
#     #     Employee.objects.create(
#     #         emp_id = row[0],
#     #         name = row[1],
#     #         email = row[2],
#     #         mobile = row[3]
#     #     )
#     for i in range(10):
#         print(i)
#     return None