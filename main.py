# Gerekli Modüllerin Import Edilmesi
import tkinter as tk
from tkinter import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import messagebox

root = Tk() # Tk sınıfından root nesnesi ürettik. Bu bizim penceremiz olacak.
root.title("Twitter Bot") # Pencerenin başlığı.
root.resizable(False, False) # Pencerenin boyutunun büyütülüp, küçültülmesinin önüne geçtik.

# Giriş yap fonksiyonu. Twitter'a giriş yapma sürecini yerine getiren metot.
def girisYap():
    global driver 
    driver = webdriver.Chrome()
    driver.get("https://twitter.com/i/flow/login")
    driver.maximize_window()
    sleep(2)
    
    usernameInput = driver.find_element(By.TAG_NAME, "input")
    usernameInput.send_keys(username)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
    sleep(2)
    
    passwordInput = driver.find_element(By.XPATH, "//input[@type='password']") 
    passwordInput.send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div").click()
    sleep(2)
    
# Bulunduğumuz web sayfasının en aşağısına kadar inip daha sonra en yukarısına çıkmamızı sağlayan metot.
def scrollDown():
    global tur
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        sleep(0.8)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if last_height == new_height:
            break
        last_height = new_height
    tur = driver.execute_script("return document.documentElement.scrollHeight")
    tur = int(tur/3300)
    driver.execute_script("window.scrollTo(0, 0);")

# Arayüzün taslağı
canvas = Canvas(root, height = 700, width = 1000, bg = "#cfffe5")
canvas.pack()

logo_frame = Frame(root, bg = "#add8e6", relief = "ridge", bd = 4, highlightbackground = "black")
logo_frame.place(relx = 0.1, rely = 0.05, relwidth = 0.80, relheight = 0.15)

kullanici_frame = Frame(root, bg = "#add8e6", relief = "ridge", bd = 4, highlightbackground = "black")
kullanici_frame.place(relx = 0.1, rely = 0.22, relwidth = 0.25, relheight = 0.73)

text_frame = Frame(root, bg = "#add8e6", relief = "ridge", bd = 4, highlightbackground = "black")
text_frame.place(relx = 0.37, rely = 0.22, relwidth = 0.53, relheight = 0.73)

# Etiketler
Label(logo_frame, text = "Twitter Otomasyon Botu", font = "Courier 20 bold", bg = "#add8e6").pack(side = "top", padx = 10, pady = 30)

Label(kullanici_frame, text = "Kullanıcı Bilgileri", font = ("Courier", 13, "bold"), bg = "#add8e6").pack(anchor = N, padx = 5, pady = 5)
Label(kullanici_frame, text = "Kullanıcı Adınız", font = ("Courier", 11), bg = "#add8e6").pack(anchor = N, padx = 5, pady = 5)
usernameInput = Entry(kullanici_frame, width = 20, bd=2, relief="groove",  highlightbackground="black")
usernameInput.configure(bg = "#ecf0f1", fg = "black", font = ("Courier", 11))
usernameInput.pack(anchor = N, padx = 5, pady = 5)

Label(kullanici_frame, text = "Şifreniz", font = ("Courier", 11), bg = "#add8e6").pack(anchor = N, padx = 5, pady = 5)
passwordInput = Entry(kullanici_frame, width = 20, show = "*", bd=2, relief="groove",  highlightbackground="black")
passwordInput.configure(bg = "#ecf0f1", fg = "black", font = ("Courier", 11))
passwordInput.pack(anchor = N, padx = 5, pady = 5)

Label(kullanici_frame, text = "Tweetlerini/Takipçilerini\nÇekmek İstediğiniz\nKullanıcı Adı", font = ("Courier", 11), bg = "#add8e6").pack(anchor = N, padx = 5, pady = 5)
userInput = Entry(kullanici_frame, width = 20, bd=2, relief="groove",  highlightbackground="black")
userInput.configure(bg = "#ecf0f1", fg = "black", font = ("Courier", 11))
userInput.pack(anchor = N, padx = 5, pady = 5)

Label(kullanici_frame, text = "Bu alanda Twitter'a\ngiriş yapmak için kendi\nkullanıcı adı ve şifrenizi\ndaha sonra ise tweetlerini çekmek\nistediğiniz kullanıcı adını\ngiriniz.", font = ("Courier", 9), bg = "#add8e6").pack(side = "bottom", padx = 5, pady= (10, 60))

def kaydet():
    global username, password, keyword, user
    username = usernameInput.get()
    password = passwordInput.get()
    user = userInput.get()
    
    usernameInput.delete(0, "end")
    passwordInput.delete(0, "end")
    userInput.delete(0, "end")
    
    with open("kullanıcılar.txt", "r", encoding = "utf-8") as kullanicilar:
        c = kullanicilar.readlines()
        kullanicilarListesi = list()
        for i in c:
            if "Kullanıcı Adı" in i:
                a = i
                a = a.split(":")[1].strip()
                kullanicilarListesi.append(a)
   
    if username not in kullanicilarListesi:
        cizgiler = 40*"-"
        with open("kullanıcılar.txt", "a", encoding = "utf-8") as kullanicilar:
            kullanicilar.write(f"Kullanıcı Adı: {username}\nŞifre: {password}\n{cizgiler}\n")
        messagebox.showinfo("Başarılı İşlem", "Bilgiler başarıyla kaydedildi.\nŞimdi girmiş olduğunuz kullanıcının tweetlerini çekebilirsiniz.")
    
    else:
        messagebox.showinfo("Başarılı İşlem", "Bilgiler başarıyla kaydedildi.\nŞimdi girmiş olduğunuz kullanıcının tweetlerini çekebilirsiniz.")
        
kaydetButonu = Button(kullanici_frame, text = "Bilgileri Kaydet", font = ("Courier", 11, "bold"), command = kaydet, bd=2, relief="groove",  highlightbackground="black")
kaydetButonu.pack(anchor = N, padx = 5, pady = 10)

text_area = Text(text_frame, height = 24, width = 60)
text_area.configure(bg = "#ecf0f1", fg = "black", font = ("Courier", 12))
text_area.pack(anchor = N, padx = 15, pady = 10)

def uygula():
    girisYap()
    
    driver.get("https://twitter.com/" + user)
    sleep(2)
    
    scrollDown()
    sleep(2)
    
    results = []
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.execute_script("window.scrollBy(0, 500);")
    sleep(2)
    
    liste = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']/span")
    for j in liste:
        results.append(j.text)
        
    for i in range(tur):
        driver.execute_script("window.scrollBy(0, 3300);")
        sleep(1)
        liste = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']/span")
        
        for j in liste:
            results.append(j.text)
      
    a = set(results)
    results = list(a)
    text_area.insert(tk.END, " " * 15 + f"{user} Tweetleri")
    text_area.insert(tk.END, "\n\n")
    count = 1
    for j in results:
        a = f"{count}-) {j}"
        text_area.insert(tk.END, a + "\n")
        count += 1

uygulaButton = Button(text_frame, text = "Tweetleri Çek", font = ("Courier", 12, "bold"), command = uygula, bd=2, relief="groove",  highlightbackground="black")
uygulaButton.pack(side = "left", padx = (90, 10), pady = 7)

def takipciCek():
    girisYap()
    
    driver.get("https://twitter.com/" + user + "/followers")
    sleep(2)
    
    scrollDown()
    sleep(2)
    
    results = []
    liste = driver.find_elements(By.XPATH, "//div[@data-testid='UserCell']/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.execute_script("window.scrollBy(0, 500);")
    sleep(1)
    
    liste = driver.find_elements(By.XPATH, "//div[@data-testid='UserCell']/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span")
    for j in liste:
        results.append(j.text)

    innerHeight = driver.execute_script("return window.innerHeight")
    for i in range(tur):
        liste = driver.find_elements(By.XPATH, "//div[@data-testid='UserCell']/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span") 
        driver.execute_script("window.scrollBy(0, 3300);")
        sleep(0.3)
        liste = driver.find_elements(By.XPATH, "//div[@data-testid='UserCell']/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span")                                                                    
        for j in liste:
            results.append(j.text)
    
    b = set(results)
    results = list(b)
    newResults = []
    
    text_area.insert(tk.END, " " * 15 + f"{user} Takipçileri")
    text_area.insert(tk.END, "\n\n")
    
    count = 1
    for j in results:
        b = j.strip("@")
        b = b.lower()
        newResults.append(b)
    newResults.sort()
    
    count = 1
    for i in newResults:
        a = i.strip("@")
        text_area.insert(tk.END, f"{count}-) {a}" + "\n")
        count += 1
    
takipciButton = Button(text_frame, text = "Takipçileri Çek", font = ("Courier", 12, "bold"), command = takipciCek, bd = 2, relief = "groove", highlightbackground = "black")
takipciButton.pack(side = "right", padx = (10, 90), pady = 7)

root.mainloop()