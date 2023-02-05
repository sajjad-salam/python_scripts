import tkinter as tk

def login():
    # إزالة النصوص من الحقول النصية
    username.delete(0, tk.END)
    password.delete(0, tk.END)

    # إضافة رسالة تأكيد
    response_label.config(text="تم تسجيل الدخول بنجاح")

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("نافذة تسجيل الدخول")

# إضافة عنوان للنافذة
title_label = tk.Label(root, text="تسجيل الدخول", font=("TkDefaultFont", 24))
title_label.pack()

# إضافة حقل اسم المستخدم
username_label = tk.Label(root, text="اسم المستخدم")
username_label.pack()
username = tk.Entry(root)
username.pack()

# إضافة حقل كلمة المرور
password_label = tk.Label(root, text="كلمة المرور")
password_label.pack()
password = tk.Entry(root, show="*")
password.pack()

# إضافة زر تسجيل الدخول
login_button = tk.Button(root, text="تسجيل الدخول", command=login)
login_button.pack()

# إضافة عنوان للرد
response_label = tk.Label(root, text="لا تسجيل للان")
response_label.pack()

# تشغيل النافذة
root.mainloop()
