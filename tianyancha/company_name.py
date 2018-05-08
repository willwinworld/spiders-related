#! python3
# -*- coding: utf-8 -*-
import pandas as pd


def get_company_name():
    """
    :return: company pandas series
    """
    df = pd.read_excel('A_Stocks.xlsx', sheetname='Sheet1')
    company_df = df['简称']
    return company_df


__all__ = [get_company_name]