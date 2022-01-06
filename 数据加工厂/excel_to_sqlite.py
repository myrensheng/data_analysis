from sqlalchemy import create_engine
import os
import pandas as pd

db_path = os.path.join(os.getcwd(), "data.db")
engine_path = "sqlite:///" + db_path
engine = create_engine(engine_path)


def excel_write_to_sqlite(excel_path, table_name):
    df = pd.read_excel(excel_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Excel写入sqlite3完成！")


def link_sqlite(sql):
    df = pd.read_sql(sql, con=engine)
    return df


def sqlite_write_to_excel(sql, excel_path):
    df = link_sqlite(sql)
    df.to_excel(excel_path, index=False)
    print("sqlite3写入Excel完成！")


if __name__ == '__main__':
    # excel_write_to_sqlite("./aaa.xlsx","predictSalesSummary")
    print(link_sqlite("select * from predictSalesSummary"))
