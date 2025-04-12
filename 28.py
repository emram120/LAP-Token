import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import pandas as pd  # برای خروجی اکسل
from bidi.algorithm import get_display
import arabic_reshaper


# تابع برای اصلاح متن فارسی جهت نمایش صحیح در رابط کاربری
def reshape_text(text):
    reshaped_text = get_display(arabic_reshaper.reshape(text))
    return text if not text else reshaped_text


# اتصال به پایگاه داده SQLite
def connect_database():
    """
    اتصال به پایگاه داده SQLite و ایجاد جدول در صورت عدم وجود
    """
    conn = sqlite3.connect("diets.db")  # فایل پایگاه داده
    cursor = conn.cursor()
    # ایجاد جدول برای ذخیره اطلاعات جیره‌ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT,
        materials TEXT,
        percentages TEXT,
        results TEXT,
        date TEXT
    )
    """)
    conn.commit()
    return conn, cursor

# اطلاعات مربوط به مواد اولیه
materials_data = {
    "کنجاله سویا": {
        "پروتئین خام (%)": 48,
        "لیپیدهای خام (%)": 1.5,
        "چربی خام (%)": 1.5,
        "فیبر خام (%)": 3.5,
        "خاکستر (%)": 6.5,
        "انرژی ناخالص (kc/k)": 3100,
        "آرژنین (%)": 3.2,
        "لیزین (%)": 2.7,
        "متیونین (%)": 0.7,
        "کلسیم (%)": 0.3,
        "فسفر (%)": 0.65,
        "سدیم (%)": 0.02,
        "کلر (%)": 0,
        "پتاسیم (%)": 2.0,
        "منیزیم (%)": 0.35,
        "مس (mg/kg)": 20,
        "گوگرد (%)": 0.4,
        "آهن (mg/kg)": 100,
        "منگنز (mg/kg)": 30,
        "سلنیوم (mg/kg)": 0.2,
        "روی (mg/kg)": 60,
        "ید (mg/kg)": 0.5,
        "کبالت (mg/kg)": 0.1,
        "ویتامین C (mg/kg)": 200,
        "بیوتین-B7 (mg/kg)": 0.1,
        "اسید فولیک-B9 (mg/kg)": 2.0,
        "نیاسین-B3 (mg/kg)": 30,
        "پانتوتنیک اسید-B5 (mg/kg)": 15,
        "پیریدوکسین-B6 (mg/kg)": 5,
        "ریبوفلاوین-B2 (mg/kg)": 4,
        "تیامین-B1 (mg/kg)": 3,
        "ویتامین B12 (mg/kg)": 0.01,
        "ویتامین A (IU/kg)": 5000,
        "ویتامین D (IU/kg)": 2000,
        "ویتامین E (mg/kg)": 50,
        "ویتامین K (mg/kg)": 2,
        "کولین (mg/kg)": 2000,
        "اینوزیتول (mg/kg)": 1000,
        "مجموع n-3 (%)": 0.1,
        "جمع n-6 (%)": 2.8,
        "فسفولیپیدها (%)": 2.5,
        "کلسترول (mg/kg)": 100,
    },
    "پودر ماهی": {
        "پروتئین خام (%)": 65,
        "لیپیدهای خام (%)": 8,
        "چربی خام (%)": 8,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 15,
        "انرژی ناخالص (kc/k)": 4500,
        "آرژنین (%)": 4.5,
        "لیزین (%)": 5.5,
        "متیونین (%)": 2.2,
        "کلسیم (%)": 5.5,
        "فسفر (%)": 3.0,
        "سدیم (%)": 0.4,
        "کلر (%)": 0,
        "پتاسیم (%)": 0.9,
        "منیزیم (%)": 0.12,
        "مس (mg/kg)": 5,
        "گوگرد (%)": 0.3,
        "آهن (mg/kg)": 120,
        "منگنز (mg/kg)": 10,
        "سلنیوم (mg/kg)": 0.4,
        "روی (mg/kg)": 80,
        "ید (mg/kg)": 1.2,
        "کبالت (mg/kg)": 0.05,
        "ویتامین C (mg/kg)": 50,
        "بیوتین-B7 (mg/kg)": 0.2,
        "اسید فولیک-B9 (mg/kg)": 1.5,
        "نیاسین-B3 (mg/kg)": 20,
        "پانتوتنیک اسید-B5 (mg/kg)": 10,
        "پیریدوکسین-B6 (mg/kg)": 3.5,
        "ریبوفلاوین-B2 (mg/kg)": 2.5,
        "تیامین-B1 (mg/kg)": 1.5,
        "ویتامین B12 (mg/kg)": 0.02,
        "ویتامین A (IU/kg)": 20000,
        "ویتامین D (IU/kg)": 4000,
        "ویتامین E (mg/kg)": 30,
        "ویتامین K (mg/kg)": 1.5,
        "کولین (mg/kg)": 1000,
        "اینوزیتول (mg/kg)": 500,
        "مجموع n-3 (%)": 1.5,
        "جمع n-6 (%)": 0.5,
        "فسفولیپیدها (%)": 3,
        "کلسترول (mg/kg)": 150,
    },
    "آرد گندم": {
        "پروتئین خام (%)": 11,
        "لیپیدهای خام (%)": 1.5,
        "چربی خام (%)": 1.5,
        "فیبر خام (%)": 2.5,
        "خاکستر (%)": 0.5,
        "انرژی ناخالص (kc/k)": 3000,
        "آرژنین (%)": 0,
        "لیزین (%)": 0.3,
        "متیونین (%)": 0.2,
        "کلسیم (%)": 0.02,
        "فسفر (%)": 0.12,
        "سدیم (%)": 0.01,
        "کلر (%)": 0,
        "پتاسیم (%)": 0.3,
        "منیزیم (%)": 0.04,
        "مس (mg/kg)": 0,
        "گوگرد (%)": 0,
        "آهن (mg/kg)": 4.32,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "ویتامین C (mg/kg)": 15,
        "بیوتین-B7 (mg/kg)": 0,
        "اسید فولیک-B9 (mg/kg)": 0,
        "نیاسین-B3 (mg/kg)": 3.5,
        "پانتوتنیک اسید-B5 (mg/kg)": 0.8,
        "پیریدوکسین-B6 (mg/kg)": 0,
        "ریبوفلاوین-B2 (mg/kg)": 0.1,
        "تیامین-B1 (mg/kg)": 0.05,
        "ویتامین B12 (mg/kg)": 0,
        "ویتامین A (IU/kg)": 0,
        "ویتامین D (IU/kg)": 0,
        "ویتامین E (mg/kg)": 0.5,
        "ویتامین K (mg/kg)": 0,
        "کولین (mg/kg)": 0,
        "اینوزیتول (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0,
    },
    "پودر گوشت 50 درصد": {
        "پروتئین خام (%)": 50.2,
        "لیپیدهای خام (%)": 10.01,
        "فیبر خام (%)": 2.32,
        "خاکستر (%)": 30.51,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 3881.45,
        "آرژنین (%)": 3.37,
        "هیستیدین (%)": 1.01,
        "ایزولوسین (%)": 1.74,
        "لوسین (%)": 4.03,
        "لیزین (%)": 3.484,
        "متیونین (%)": 0.98,
        "فنیل آلانین (%)": 1.91,
        "ترئونین (%)": 1.8,
        "تریپتوفان (%)": 0.772,
        "والین (%)": 2.652,
        "سیستین (%)": 0.71,
        "TSAA Met+Cys (%)": 1.69,
        "تیروزین (%)": 1.559,
        "Phe+Tyr (%)": 3.469,
        "گلوتامیک (%)": 6.837,
        "آسپارتیک (%)": 3.71,
        "گلیسین (%)": 6.38,
        "سرین (%)": 2.01,
        "آلانین (%)": 3.82,
        "تائورین (%)": 0.04,
        "کلسیم (%)": 9.598,
        "فسفر (%)": 4.839,
        "سدیم (%)": 0.51,
        "کلر (%)": 0.54,
        "پتاسیم (%)": 1.4,
        "منیزیم (%)": 0.65,
        "گوگرد (%)": 0.34,
        "مس (mg/kg)": 10.5,
        "آهن (mg/kg)": 438,
        "منگنز (mg/kg)": 16.77,
        "سلنیوم (mg/kg)": 0.21,
        "روی (mg/kg)": 93,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0.002,
        "B7 (mg/kg)": 0.11,
        "B9 (mg/kg)": 0.51,
        "B3 (mg/kg)": 54.2,
        "B5 (mg/kg)": 4.25,
        "B6 (mg/kg)": 4.6,
        "B2 (mg/kg)": 4.95,
        "B1 (mg/kg)": 0.3,
        "B12 (mg/kg)": 0.05,
        "C (mg/kg)": 0,
        "A (mg/kg)": 16666.667,
        "D (ug/kg)": 200,
        "E (mg/kg)": 0.89,
        "K (mg/kg)": 1,
        "Choline (mg/kg)": 1998,
        "Inositol (mg/kg)": 100,
        "مجموع n-3 (%)": 0.111,
        "جمع n-6 (%)": 1.134,
        "فسفولیپیدها (%)": 2,
        "کلسترول (mg/kg)": 1000,
    },
    "گلوتن ذرت 40 درصد": {
        "پروتئین خام (%)": 40,
        "لیپیدهای خام (%)": 2.5,
        "چربی خام (%)": 2.5,
        "فیبر خام (%)": 3.5,
        "خاکستر (%)": 1.0,
        "انرژی ناخالص (kc/k)": 3600,
        "آرژنین (%)": 0.5,
        "لیزین (%)": 0.6,
        "متیونین (%)": 0.5,
        "کلسیم (%)": 0.01,
        "فسفر (%)": 0.15,
        "سدیم (%)": 0.01,
        "کلر (%)": 0,
        "پتاسیم (%)": 0.2,
        "منیزیم (%)": 0.02,
        "مس (mg/kg)": 0,
        "گوگرد (%)": 0,
        "آهن (mg/kg)": 7.7,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "ویتامین C (mg/kg)": 10,
        "بیوتین-B7 (mg/kg)": 0,
        "اسید فولیک-B9 (mg/kg)": 0,
        "نیاسین-B3 (mg/kg)": 1.2,
        "پانتوتنیک اسید-B5 (mg/kg)": 0.5,
        "پیریدوکسین-B6 (mg/kg)": 0,
        "ریبوفلاوین-B2 (mg/kg)": 0.1,
        "تیامین-B1 (mg/kg)": 0.02,
        "ویتامین B12 (mg/kg)": 0,
        "ویتامین A (IU/kg)": 800,
        "ویتامین D (IU/kg)": 400,
        "ویتامین E (mg/kg)": 5,
        "ویتامین K (mg/kg)": 0,
        "کولین (mg/kg)": 0,
        "اینوزیتول (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0,
    },
    "گلوتن ذرت 50 درصد": {
        "پروتئین خام (%)": 51.3,
        "لیپیدهای خام (%)": 7.8,
        "فیبر خام (%)": 2.1,
        "خاکستر (%)": 2,
        "نشاسته (%)": 13.1,
        "انرژی ناخالص (kc/k)": 4844.65,
        "آرژنین (%)": 1.54,
        "هیستیدین (%)": 1.03,
        "ایزولوسین (%)": 2.05,
        "لوسین (%)": 8.16,
        "لیزین (%)": 0.87,
        "متیونین (%)": 1.23,
        "فنیل آلانین (%)": 3.13,
        "ترئونین (%)": 1.69,
        "تریپتوفان (%)": 0.26,
        "والین (%)": 2.31,
        "سیستین (%)": 0.92,
        "TSAA Met+Cys (%)": 2.15,
        "تیروزین (%)": 2.46,
        "Phe+Tyr (%)": 5.59,
        "گلوتامیک (%)": 10.31,
        "آسپارتیک (%)": 2.98,
        "گلیسین (%)": 1.28,
        "سرین (%)": 2.51,
        "آلانین (%)": 4.36,
        "تائورین (%)": 0,
        "کلسیم (%)": 0.06,
        "فسفر (%)": 0.42,
        "سدیم (%)": 0.02,
        "کلر (%)": 0.05,
        "پتاسیم (%)": 0.07,
        "منیزیم (%)": 0.06,
        "گوگرد (%)": 0.5,
        "مس (mg/kg)": 10,
        "آهن (mg/kg)": 332,
        "منگنز (mg/kg)": 7.8,
        "سلنیوم (mg/kg)": 2,
        "روی (mg/kg)": 49,
        "ید (mg/kg)": 0.05,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0.19,
        "B9 (mg/kg)": 0.3,
        "B3 (mg/kg)": 49.8,
        "B5 (mg/kg)": 10,
        "B6 (mg/kg)": 7.97,
        "B2 (mg/kg)": 1.5,
        "B1 (mg/kg)": 0.22,
        "B12 (mg/kg)": 0.05,
        "C (mg/kg)": 0,
        "A (mg/kg)": 266.667,
        "D (ug/kg)": 0,
        "E (mg/kg)": 21.74,
        "K (mg/kg)": 0.2,
        "Choline (mg/kg)": 360,
        "Inositol (mg/kg)": 270.22,
        "مجموع n-3 (%)": 0.061,
        "جمع n-6 (%)": 5.027,
        "فسفولیپیدها (%)": 0.02,
        "کلسترول (mg/kg)": 571.35,
    },
    "گلوتن گندم 78 درصد": {
        "پروتئین خام (%)": 78.17,
        "لیپیدهای خام (%)": 2.4,
        "فیبر خام (%)": 0.43,
        "خاکستر (%)": 0.73,
        "نشاسته (%)": 1.5,
        "انرژی ناخالص (kc/k)": 5014.34,
        "آرژنین (%)": 3.09,
        "هیستیدین (%)": 1.72,
        "ایزولوسین (%)": 2.93,
        "لوسین (%)": 5.66,
        "لیزین (%)": 2.16,
        "متیونین (%)": 1.35,
        "فنیل آلانین (%)": 4.13,
        "ترئونین (%)": 1.99,
        "تریپتوفان (%)": 0.77,
        "والین (%)": 3.25,
        "سیستین (%)": 1.56,
        "TSAA Met+Cys (%)": 2.91,
        "تیروزین (%)": 2.36,
        "Phe+Tyr (%)": 6.49,
        "گلوتامیک (%)": 28,
        "آسپارتیک (%)": 2.46,
        "گلیسین (%)": 2.54,
        "سرین (%)": 3.84,
        "آلانین (%)": 1.98,
        "تائورین (%)": 0,
        "کلسیم (%)": 0.1,
        "فسفر (%)": 0.24,
        "سدیم (%)": 0.057,
        "کلر (%)": 0.05,
        "پتاسیم (%)": 0.12,
        "منیزیم (%)": 0.03,
        "گوگرد (%)": 0.1,
        "مس (mg/kg)": 20.91,
        "آهن (mg/kg)": 45.5,
        "منگنز (mg/kg)": 15,
        "سلنیوم (mg/kg)": 0.4,
        "روی (mg/kg)": 50,
        "ید (mg/kg)": 0.06,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0.3,
        "B9 (mg/kg)": 1,
        "B3 (mg/kg)": 100,
        "B5 (mg/kg)": 16,
        "B6 (mg/kg)": 5,
        "B2 (mg/kg)": 2.5,
        "B1 (mg/kg)": 15,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 266.667,
        "D (ug/kg)": 0,
        "E (mg/kg)": 37.22,
        "K (mg/kg)": 0.05,
        "Choline (mg/kg)": 1500,
        "Inositol (mg/kg)": 142.68,
        "مجموع n-3 (%)": 0.133,
        "جمع n-6 (%)": 1.653,
        "فسفولیپیدها (%)": 0.16,
        "کلسترول (mg/kg)": 800,
    },
    "روغن سویا": {
        "پروتئین خام (%)": 0,
        "لیپیدهای خام (%)": 99,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 0,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 9228.01,
        "آرژنین (%)": 0,
        "هیستیدین (%)": 0,
        "ایزولوسین (%)": 0,
        "لوسین (%)": 0,
        "لیزین (%)": 0,
        "متیونین (%)": 0,
        "فنیل آلانین (%)": 0,
        "ترئونین (%)": 0,
        "تریپتوفان (%)": 0,
        "والین (%)": 0,
        "سیستین (%)": 0,
        "TSAA Met+Cys (%)": 0,
        "تیروزین (%)": 0,
        "Phe+Tyr (%)": 0,
        "گلوتامیک (%)": 0,
        "آسپارتیک (%)": 0,
        "گلیسین (%)": 0,
        "سرین (%)": 0,
        "آلانین (%)": 0,
        "تائورین (%)": 0,
        "کلسیم (%)": 0,
        "فسفر (%)": 0,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "گوگرد (%)": 0,
        "مس (mg/kg)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0.05,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0,
        "B9 (mg/kg)": 0,
        "B3 (mg/kg)": 0,
        "B5 (mg/kg)": 0,
        "B6 (mg/kg)": 0,
        "B2 (mg/kg)": 0,
        "B1 (mg/kg)": 0,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 0,
        "D (ug/kg)": 0,
        "E (mg/kg)": 61.04,
        "K (mg/kg)": 0.18,
        "Choline (mg/kg)": 2,
        "Inositol (mg/kg)": 0,
        "مجموع n-3 (%)": 7.557,
        "جمع n-6 (%)": 56.672,
        "فسفولیپیدها (%)": 1.08,
        "کلسترول (mg/kg)": 2460,
    },
    "لیسیتین": {
        "پروتئین خام (%)": 0,
        "لیپیدهای خام (%)": 60,
        "چربی خام (%)": 60,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 0.2,
        "انرژی ناخالص (kc/k)": 8000,
        "آرژنین (%)": 0,
        "لیزین (%)": 0,
        "متیونین (%)": 0,
        "کلسیم (%)": 0.01,
        "فسفر (%)": 0.02,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "مس (mg/kg)": 0,
        "گوگرد (%)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "ویتامین C (mg/kg)": 0,
        "بیوتین-B7 (mg/kg)": 0,
        "اسید فولیک-B9 (mg/kg)": 0,
        "نیاسین-B3 (mg/kg)": 0,
        "پانتوتنیک اسید-B5 (mg/kg)": 0,
        "پیریدوکسین-B6 (mg/kg)": 0,
        "ریبوفلاوین-B2 (mg/kg)": 0,
        "تیامین-B1 (mg/kg)": 0,
        "ویتامین B12 (mg/kg)": 0,
        "ویتامین A (IU/kg)": 0,
        "ویتامین D (IU/kg)": 0,
        "ویتامین E (mg/kg)": 10,
        "ویتامین K (mg/kg)": 0,
        "کولین (mg/kg)": 0,
        "اینوزیتول (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 2.5,
        "کلسترول (mg/kg)": 100,
    },
    "دی کلسیوم فسفات": {
        "پروتئین خام (%)": 0,
        "لیپیدهای خام (%)": 0,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 99,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 0,
        "آرژنین (%)": 0,
        "هیستیدین (%)": 0,
        "ایزولوسین (%)": 0,
        "لوسین (%)": 0,
        "لیزین (%)": 0,
        "متیونین (%)": 0,
        "فنیل آلانین (%)": 0,
        "ترئونین (%)": 0,
        "تریپتوفان (%)": 0,
        "والین (%)": 0,
        "سیستین (%)": 0,
        "TSAA Met+Cys (%)": 0,
        "تیروزین (%)": 0,
        "Phe+Tyr (%)": 0,
        "گلوتامیک (%)": 0,
        "آسپارتیک (%)": 0,
        "گلیسین (%)": 0,
        "سرین (%)": 0,
        "آلانین (%)": 0,
        "تائورین (%)": 0,
        "کلسیم (%)": 29.393,
        "فسفر (%)": 22.8,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "گوگرد (%)": 0,
        "مس (mg/kg)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0,
        "B9 (mg/kg)": 0,
        "B3 (mg/kg)": 0,
        "B5 (mg/kg)": 0,
        "B6 (mg/kg)": 0,
        "B2 (mg/kg)": 0,
        "B1 (mg/kg)": 0,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 0,
        "D (ug/kg)": 0,
        "E (mg/kg)": 0,
        "K (mg/kg)": 0,
        "Choline (mg/kg)": 0,
        "Inositol (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0,
    },
    "ال-آرژنین": {
        "پروتئین خام (%)": 98,
        "لیپیدهای خام (%)": 0,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 0,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 5528.2,
        "آرژنین (%)": 98,
        "هیستیدین (%)": 0,
        "ایزولوسین (%)": 0,
        "لوسین (%)": 0,
        "لیزین (%)": 0,
        "متیونین (%)": 0,
        "فنیل آلانین (%)": 0,
        "ترئونین (%)": 0,
        "تریپتوفان (%)": 0,
        "والین (%)": 0,
        "سیستین (%)": 0,
        "TSAA Met+Cys (%)": 0,
        "تیروزین (%)": 0,
        "Phe+Tyr (%)": 0,
        "گلوتامیک (%)": 0,
        "آسپارتیک (%)": 0,
        "گلیسین (%)": 0,
        "سرین (%)": 0,
        "آلانین (%)": 0,
        "تائورین (%)": 0,
        "کلسیم (%)": 0,
        "فسفر (%)": 0,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "گوگرد (%)": 0,
        "مس (mg/kg)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0,
        "B9 (mg/kg)": 0,
        "B3 (mg/kg)": 0,
        "B5 (mg/kg)": 0,
        "B6 (mg/kg)": 0,
        "B2 (mg/kg)": 0,
        "B1 (mg/kg)": 0,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 0,
        "D (ug/kg)": 0,
        "E (mg/kg)": 0,
        "K (mg/kg)": 0,
        "Choline (mg/kg)": 0,
        "Inositol (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0
    },
    "ال-هیستیدین": {
        "پروتئین خام (%)": 98,
        "لیپیدهای خام (%)": 0,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 0,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 5528.2,
        "آرژنین (%)": 0,
        "هیستیدین (%)": 98,
        "ایزولوسین (%)": 0,
        "لوسین (%)": 0,
        "لیزین (%)": 0,
        "متیونین (%)": 0,
        "فنیل آلانین (%)": 0,
        "ترئونین (%)": 0,
        "تریپتوفان (%)": 0,
        "والین (%)": 0,
        "سیستین (%)": 0,
        "TSAA Met+Cys (%)": 0,
        "تیروزین (%)": 0,
        "Phe+Tyr (%)": 0,
        "گلوتامیک (%)": 0,
        "آسپارتیک (%)": 0,
        "گلیسین (%)": 0,
        "سرین (%)": 0,
        "آلانین (%)": 0,
        "تائورین (%)": 0,
        "کلسیم (%)": 0,
        "فسفر (%)": 0,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "گوگرد (%)": 0,
        "مس (mg/kg)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0,
        "B9 (mg/kg)": 0,
        "B3 (mg/kg)": 0,
        "B5 (mg/kg)": 0,
        "B6 (mg/kg)": 0,
        "B2 (mg/kg)": 0,
        "B1 (mg/kg)": 0,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 0,
        "D (ug/kg)": 0,
        "E (mg/kg)": 0,
        "K (mg/kg)": 0,
        "Choline (mg/kg)": 0,
        "Inositol (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0
    },
    "ال-لیزین": {
        "پروتئین خام (%)": 99,
        "لیپیدهای خام (%)": 0,
        "فیبر خام (%)": 0,
        "خاکستر (%)": 0,
        "نشاسته (%)": 0,
        "انرژی ناخالص (kc/k)": 5583.17,
        "آرژنین (%)": 0,
        "هیستیدین (%)": 0,
        "ایزولوسین (%)": 0,
        "لوسین (%)": 0,
        "لیزین (%)": 82.616,
        "متیونین (%)": 0,
        "فنیل آلانین (%)": 0,
        "ترئونین (%)": 0,
        "تریپتوفان (%)": 0,
        "والین (%)": 0,
        "سیستین (%)": 0,
        "TSAA Met+Cys (%)": 0,
        "تیروزین (%)": 0,
        "Phe+Tyr (%)": 0,
        "گلوتامیک (%)": 0,
        "آسپارتیک (%)": 0,
        "گلیسین (%)": 0,
        "سرین (%)": 0,
        "آلانین (%)": 0,
        "تائورین (%)": 0,
        "کلسیم (%)": 0,
        "فسفر (%)": 0,
        "سدیم (%)": 0,
        "کلر (%)": 0,
        "پتاسیم (%)": 0,
        "منیزیم (%)": 0,
        "گوگرد (%)": 0,
        "مس (mg/kg)": 0,
        "آهن (mg/kg)": 0,
        "منگنز (mg/kg)": 0,
        "سلنیوم (mg/kg)": 0,
        "روی (mg/kg)": 0,
        "ید (mg/kg)": 0,
        "کبالت (mg/kg)": 0,
        "B7 (mg/kg)": 0,
        "B9 (mg/kg)": 0,
        "B3 (mg/kg)": 0,
        "B5 (mg/kg)": 0,
        "B6 (mg/kg)": 0,
        "B2 (mg/kg)": 0,
        "B1 (mg/kg)": 0,
        "B12 (mg/kg)": 0,
        "C (mg/kg)": 0,
        "A (mg/kg)": 0,
        "D (ug/kg)": 0,
        "E (mg/kg)": 0,
        "K (mg/kg)": 0,
        "Choline (mg/kg)": 0,
        "Inositol (mg/kg)": 0,
        "مجموع n-3 (%)": 0,
        "جمع n-6 (%)": 0,
        "فسفولیپیدها (%)": 0,
        "کلسترول (mg/kg)": 0
    },
    "ال والین" : {
    "پروتئین خام (%)": 72,
    "لیپیدهای خام (%)": 0,
    "فیبر خام (%)": 0,
    "خاکستر (%)": 0,
    "نشاسته (%)": 0,
    "انرژی ناخالص (kc/k)": 5117.11,
    "آرژنین (%)": 0,
    "هیستیدین (%)": 0,
    "ایزولوسین (%)": 0,
    "لوسین (%)": 0,
    "لیزین (%)": 0,
    "متیونین (%)": 0,
    "فنیل آلانین (%)": 0,
    "ترئونین (%)": 0,
    "تریپتوفان (%)": 0,
    "والین (%)": 96.005,
    "سیستین (%)": 0,
    "TSAA Met+Cys (%)": 0,
    "تیروزین (%)": 0,
    "Phe+Tyr (%)": 0,
    "گلوتامیک (%)": 0,
    "آسپارتیک (%)": 0,
    "گلیسین (%)": 0,
    "سرین (%)": 0,
    "آلانین (%)": 0,
    "تائورین (%)": 0,
    "کلسیم (%)": 0,
    "فسفر (%)": 0,
    "سدیم (%)": 0,
    "کلر (%)": 0,
    "پتاسیم (%)": 0,
    "منیزیم (%)": 0,
    "گوگرد (%)": 0,
    "مس (mg/kg)": 0,
    "آهن (mg/kg)": 0,
    "منگنز (mg/kg)": 0,
    "سلنیوم (mg/kg)": 0,
    "روی (mg/kg)": 0,
    "ید (mg/kg)": 0,
    "کبالت (mg/kg)": 0,
    "B7 (mg/kg)": 0,
    "B9 (mg/kg)": 0,
    "B3 (mg/kg)": 0,
    "B5 (mg/kg)": 0,
    "B6 (mg/kg)": 0,
    "B2 (mg/kg)": 0,
    "B1 (mg/kg)": 0,
    "B12 (mg/kg)": 0,
    "C (mg/kg)": 0,
    "A (mg/kg)": 0,
    "D (ug/kg)": 0,
    "E (mg/kg)": 0,
    "K (mg/kg)": 0,
    "Choline (mg/kg)": 0,
    "Inositol (mg/kg)": 0,
    "مجموع n-3 (%)": 0,
    "جمع n-6 (%)": 0,
    "فسفولیپیدها (%)": 0,
    "کلسترول (mg/kg)": 0
},
    "ال-ترئونین" : {
    "پروتئین خام (%)": 70.9,
    "لیپیدهای خام (%)": 0,
    "فیبر خام (%)": 0,
    "خاکستر (%)": 0,
    "نشاسته (%)": 0,
    "انرژی ناخالص (kc/k)": 5100.38,
    "آرژنین (%)": 0,
    "هیستیدین (%)": 0,
    "ایزولوسین (%)": 0,
    "لوسین (%)": 0,
    "لیزین (%)": 0,
    "متیونین (%)": 0,
    "فنیل آلانین (%)": 0,
    "ترئونین (%)": 95.995,
    "تریپتوفان (%)": 0,
    "والین (%)": 0,
    "سیستین (%)": 0,
    "TSAA Met+Cys (%)": 0,
    "تیروزین (%)": 0,
    "Phe+Tyr (%)": 0,
    "گلوتامیک (%)": 0,
    "آسپارتیک (%)": 0,
    "گلیسین (%)": 0,
    "سرین (%)": 0,
    "آلانین (%)": 0,
    "تائورین (%)": 0,
    "کلسیم (%)": 0,
    "فسفر (%)": 0,
    "سدیم (%)": 0,
    "کلر (%)": 0,
    "پتاسیم (%)": 0,
    "منیزیم (%)": 0,
    "گوگرد (%)": 0,
    "مس (mg/kg)": 0,
    "آهن (mg/kg)": 0,
    "منگنز (mg/kg)": 0,
    "سلنیوم (mg/kg)": 0,
    "روی (mg/kg)": 0,
    "ید (mg/kg)": 0,
    "کبالت (mg/kg)": 0,
    "B7 (mg/kg)": 0,
    "B9 (mg/kg)": 0,
    "B3 (mg/kg)": 0,
    "B5 (mg/kg)": 0,
    "B6 (mg/kg)": 0,
    "B2 (mg/kg)": 0,
    "B1 (mg/kg)": 0,
    "B12 (mg/kg)": 0,
    "C (mg/kg)": 0,
    "A (mg/kg)": 0,
    "D (ug/kg)": 0,
    "E (mg/kg)": 0,
    "K (mg/kg)": 0,
    "Choline (mg/kg)": 0,
    "Inositol (mg/kg)": 0,
    "مجموع n-3 (%)": 0,
    "جمع n-6 (%)": 0,
    "فسفولیپیدها (%)": 0,
    "کلسترول (mg/kg)": 0
},
    "ال-تریپتوفان" : {
    "پروتئین خام (%)": 82.5,
    "لیپیدهای خام (%)": 0,
    "فیبر خام (%)": 0,
    "خاکستر (%)": 0,
    "نشاسته (%)": 0,
    "انرژی ناخالص (kc/k)": 5284.42,
    "آرژنین (%)": 0,
    "هیستیدین (%)": 0,
    "ایزولوسین (%)": 0,
    "لوسین (%)": 0,
    "لیزین (%)": 0,
    "متیونین (%)": 0,
    "فنیل آلانین (%)": 0,
    "ترئونین (%)": 0,
    "تریپتوفان (%)": 95.997,
    "والین (%)": 0,
    "سیستین (%)": 0,
    "TSAA Met+Cys (%)": 0,
    "تیروزین (%)": 0,
    "Phe+Tyr (%)": 0,
    "گلوتامیک (%)": 0,
    "آسپارتیک (%)": 0,
    "گلیسین (%)": 0,
    "سرین (%)": 0,
    "آلانین (%)": 0,
    "تائورین (%)": 0,
    "کلسیم (%)": 0,
    "فسفر (%)": 0,
    "سدیم (%)": 0,
    "کلر (%)": 0,
    "پتاسیم (%)": 0,
    "منیزیم (%)": 0,
    "گوگرد (%)": 0,
    "مس (mg/kg)": 0,
    "آهن (mg/kg)": 0,
    "منگنز (mg/kg)": 0,
    "سلنیوم (mg/kg)": 0,
    "روی (mg/kg)": 0,
    "ید (mg/kg)": 0,
    "کبالت (mg/kg)": 0,
    "B7 (mg/kg)": 0,
    "B9 (mg/kg)": 0,
    "B3 (mg/kg)": 0,
    "B5 (mg/kg)": 0,
    "B6 (mg/kg)": 0,
    "B2 (mg/kg)": 0,
    "B1 (mg/kg)": 0,
    "B12 (mg/kg)": 0,
    "C (mg/kg)": 0,
    "A (mg/kg)": 0,
    "D (ug/kg)": 0,
    "E (mg/kg)": 0,
    "K (mg/kg)": 0,
    "Choline (mg/kg)": 0,
    "Inositol (mg/kg)": 0,
    "مجموع n-3 (%)": 0,
    "جمع n-6 (%)": 0,
    "فسفولیپیدها (%)": 0,
    "کلسترول (mg/kg)": 0
}

}

species_data = {
    "Seabass": {
        "پروتئین خام (%)": 46,
        "لیپیدهای خام (%)": 13,
        "چربی خام (%)": 13,
        "فیبر خام (%)": 7,
        "خاکستر (%)": 12,
        "انرژی ناخالص (kc/k)": 3793,
        "آرژنین (%)": 2.5,
        "لیزین (%)": 3.5,
        "متیونین (%)": 0.9,
        "کلسیم (%)": 1.0,
        "فسفر (%)": 0.8,
        "سدیم (%)": 0.5,
        "کلر (%)": 0.4,
        "پتاسیم (%)": 0.8,
        "منیزیم (%)": 0.2,
        "مس (mg/kg)": 10,
        "گوگرد (%)": 0.6,
        "آهن (mg/kg)": 120,
        "منگنز (mg/kg)": 15,
        "سلنیوم (mg/kg)": 0.2,
        "روی (mg/kg)": 80,
        "ید (mg/kg)": 0.3,
        "کبالت (mg/kg)": 0.1,
        "ویتامین C (mg/kg)": 250,
        "بیوتین-B7 (mg/kg)": 0.05,
        "اسید فولیک-B9 (mg/kg)": 1.0,
        "نیاسین-B3 (mg/kg)": 20,
        "پانتوتنیک اسید-B5 (mg/kg)": 8,
        "پیریدوکسین-B6 (mg/kg)": 2,
        "ریبوفلاوین-B2 (mg/kg)": 2,
        "تیامین-B1 (mg/kg)": 1.5,
        "ویتامین B12 (mg/kg)": 0.01,
        "ویتامین A (IU/kg)": 8000,
        "ویتامین D (IU/kg)": 2500,
        "ویتامین E (mg/kg)": 70,
        "ویتامین K (mg/kg)": 1.5,
        "کولین (mg/kg)": 2200,
        "اینوزیتول (mg/kg)": 1200
    }
}


# تابع دسته‌بندی پارامترها
def categorize_parameters(materials_data):
    """دسته‌بندی پارامترها به درصدی و غیر درصدی"""
    percentage_params = set()
    non_percentage_params = set()

    for material, params in materials_data.items():
        for param in params.keys():
            if "(%)" in param:  # شناسایی پارامترهای درصدی
                percentage_params.add(param)
            else:  # شناسایی پارامترهای غیر درصدی
                non_percentage_params.add(param)

    return percentage_params, non_percentage_params
     
# کلاس اصلی برنامه
class DietCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("محاسبه جیره غذایی")

        # اتصال به پایگاه داده
        self.conn, self.cursor = connect_database()

        # دسته‌بندی پارامترها
        self.percentage_params, self.non_percentage_params = categorize_parameters(materials_data)

        # ترتیب استاندارد پارامترها (برای مرتب‌سازی نتایج)
        self.standard_order = [
            "پروتئین خام (%)",
            "لیپیدهای خام (%)",
            "چربی خام (%)",
            "فیبر خام (%)",
            "خاکستر (%)",
            "انرژی ناخالص (kc/k)",
            "مس (mg/kg)",
        ]

        # رابط کاربری: انتخاب گونه
        tk.Label(root, text=reshape_text("گونه:")).grid(row=0, column=0, padx=5, pady=5)
        self.species_combobox = ttk.Combobox(root, values=list(species_data.keys()))
        self.species_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.species_combobox.set("Seabass")  # مقدار پیش‌فرض

        # رابط کاربری: جدول مواد اولیه
        self.materials_frame = tk.Frame(root)
        self.materials_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5)
        self.materials_widgets = []
        self.add_material_row()  # اضافه کردن اولین ردیف مواد اولیه

        # دکمه‌ها
        tk.Button(root, text=reshape_text("اضافه کردن ماده اولیه"), command=self.add_material_row).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(root, text=reshape_text("محاسبه جیره"), command=self.calculate_diet).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text=reshape_text("مشاهده جیره‌های ذخیره‌شده"), command=self.show_saved_diets).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(root, text=reshape_text("خروجی اکسل"), command=self.export_to_excel).grid(row=2, column=3, padx=5, pady=5)
        tk.Button(root, text=reshape_text("حذف همه داده‌ها"), command=self.clear_all_data).grid(row=2, column=4, padx=5, pady=5)

        # جدول نمایش نتایج
        self.results_table = ttk.Treeview(root, columns=("param", "calculated", "standard", "difference"), show="headings", height=15)
        self.results_table.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
        self.results_table.heading("param", text=reshape_text("پارامتر"))
        self.results_table.heading("calculated", text=reshape_text("محاسبه‌شده"))
        self.results_table.heading("standard", text=reshape_text("استاندارد"))
        self.results_table.heading("difference", text=reshape_text("تفاوت"))

        # تنظیم فونت رنگ برای تفاوت‌ها
        self.results_table.tag_configure("less_than", foreground="red")
        self.results_table.tag_configure("greater_than", foreground="blue")

    def add_material_row(self):
        """
        اضافه کردن یک ردیف جدید برای انتخاب ماده اولیه و درصد وزنی آن
        """
        row = len(self.materials_widgets)
        material_combobox = ttk.Combobox(self.materials_frame, values=list(materials_data.keys()))
        material_combobox.grid(row=row, column=0, padx=5, pady=5)
        material_combobox.set(list(materials_data.keys())[0])  # مقدار پیش‌فرض

        percentage_entry = tk.Entry(self.materials_frame)
        percentage_entry.grid(row=row, column=1, padx=5, pady=5)
        percentage_entry.insert(0, "0")  # مقدار پیش‌فرض 0

        self.materials_widgets.append((material_combobox, percentage_entry))

    def calculate_diet(self):
        """
        محاسبه جیره بر اساس مواد اولیه و درصدهای وارد شده
        """
        try:
            # دریافت گونه انتخاب‌شده
            selected_species = self.species_combobox.get()
            if selected_species not in species_data:
                raise ValueError("گونه نامعتبر است.")

            # جمع‌آوری اطلاعات مواد اولیه و درصدها
            material_weights = {}
            total_percentage = 0  # جمع درصد کل مواد اولیه
            for combobox, entry in self.materials_widgets:
                material = combobox.get()
                if material not in materials_data:
                    raise ValueError(f"ماده اولیه '{material}' نامعتبر است.")
                try:
                    weight = float(entry.get())
                    if weight < 0 or weight > 100:
                        raise ValueError("درصد وزنی باید بین 0 و 100 باشد.")
                    total_percentage += weight
                    material_weights[material] = weight / 100  # تبدیل به درصد
                except ValueError:
                    raise ValueError("درصد وزنی باید یک عدد معتبر باشد.")

            # بررسی اینکه مجموع درصدها از 100 بیشتر نباشد
            if total_percentage > 100:
                raise ValueError("مجموع درصد مواد اولیه نباید از 100 بیشتر باشد.")

            # محاسبه جیره
            final_composition = {}

            # محاسبه پارامترهای درصدی
            for material, weight in material_weights.items():
                for param, value in materials_data[material].items():
                    if param in self.percentage_params:
                        final_composition[param] = final_composition.get(param, 0) + value * weight

            # محاسبه پارامترهای غیر درصدی
            for material, weight in material_weights.items():
                for param, value in materials_data[material].items():
                    if param in self.non_percentage_params:
                        # تقسیم بر 1000 برای پارامترهای غیر درصدی
                        final_composition[param] = final_composition.get(param, 0) + (value * weight) / 1000

            # ذخیره جیره در پایگاه داده
            self.save_diet_to_db(selected_species, material_weights, final_composition)

            # پاک کردن جدول قدیمی
            for item in self.results_table.get_children():
                self.results_table.delete(item)

            # نمایش نتایج در جدول
            for param, value in final_composition.items():
                difference = value - species_data[selected_species].get(param, 0)
                # تعیین رنگ بر اساس تفاوت
                tag = "less_than" if difference < 0 else "greater_than" if difference > 0 else None
                self.results_table.insert("", "end", values=(param, round(value, 2), species_data[selected_species].get(param, 0), round(difference, 2)), tags=(tag,))

        except ValueError as e:
            messagebox.showerror("خطا", str(e))

    def save_diet_to_db(self, species, material_weights, results):
        """
        ذخیره اطلاعات جیره در پایگاه داده
        """
        materials_str = ";".join([f"{material}:{weight}" for material, weight in material_weights.items()])
        results_str = ";".join([f"{param}:{value}" for param, value in results.items()])
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # درج اطلاعات در پایگاه داده
        self.cursor.execute("""
        INSERT INTO diets (species, materials, percentages, results, date)
        VALUES (?, ?, ?, ?, ?)
        """, (species, materials_str, materials_str, results_str, date_str))
        self.conn.commit()

    def show_saved_diets(self):
        """
        نمایش جیره‌های ذخیره‌شده از پایگاه داده
        """
        try:
            # بازیابی داده‌ها از پایگاه داده
            self.cursor.execute("SELECT species, materials, percentages, results, date FROM diets")
            rows = self.cursor.fetchall()

            # ایجاد پنجره جدید برای نمایش جیره‌ها
            view_window = tk.Toplevel(self.root)
            view_window.title("جیره‌های ذخیره‌شده")

            # جدول نمایش جیره‌های ذخیره‌شده
            saved_diets_table = ttk.Treeview(view_window, columns=("species", "materials", "percentages", "results", "date"), show="headings", height=15)
            saved_diets_table.grid(row=0, column=0, padx=5, pady=5)
            saved_diets_table.heading("species", text=reshape_text("گونه"))
            saved_diets_table.heading("materials", text=reshape_text("مواد اولیه"))
            saved_diets_table.heading("percentages", text=reshape_text("درصدها"))
            saved_diets_table.heading("results", text=reshape_text("نتایج"))
            saved_diets_table.heading("date", text=reshape_text("تاریخ"))

            # اضافه کردن داده‌ها به جدول
            for row in rows:
                saved_diets_table.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("خطا", f"خطا در بازیابی داده‌ها: {e}")

    def export_to_excel(self):
        """
        خروجی گرفتن داده‌های ذخیره‌شده به فایل اکسل
        """
        try:
            # بازیابی داده‌ها از پایگاه داده
            self.cursor.execute("SELECT species, materials, percentages, results, date FROM diets")
            rows = self.cursor.fetchall()

            # تبدیل داده‌ها به DataFrame
            data = pd.DataFrame(rows, columns=["گونه", "مواد اولیه", "درصدها", "نتایج", "تاریخ"])

            # انتخاب مسیر ذخیره فایل اکسل
            file_name = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx")],
                                                     title="ذخیره فایل اکسل")
            if not file_name:  # اگر کاربر فایل را انتخاب نکند
                return

            # ذخیره داده‌ها به فایل اکسل
            data.to_excel(file_name, index=False, engine="openpyxl")

            messagebox.showinfo("موفقیت", f"داده‌ها با موفقیت به فایل اکسل ذخیره شدند.")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خروجی گرفتن داده‌ها: {e}")

    def clear_all_data(self):
        """
        حذف تمام داده‌های ذخیره‌شده در پایگاه داده
        """
        try:
            # هشدار برای تأیید حذف داده‌ها
            confirm = messagebox.askyesno("حذف داده‌ها", "آیا مطمئن هستید که می‌خواهید تمام داده‌ها را حذف کنید؟")
            if confirm:
                # حذف تمام داده‌ها از جدول
                self.cursor.execute("DELETE FROM diets")
                self.conn.commit()
                messagebox.showinfo("موفقیت", "تمام داده‌ها با موفقیت حذف شدند.")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در حذف داده‌ها: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DietCalculatorApp(root)
    root.mainloop()