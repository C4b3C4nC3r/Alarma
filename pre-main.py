# #Lib 
# from tkinter import messagebox, Label, Tk, ttk, Toplevel,Button
# from time import strftime
# from pygame import mixer 

# #code

# window = Tk()
# window.config(bg='black')
# window.geometry('550x300')
# window.title("Reloj")
# window.minsize(width=550,height=300)
# mixer.init()

# h_list = []
# m_list = []
# s_list = []

# #buclees 
# for i in range(0,24): #bucle dias (24 hours) 
#     h_list.append(i)
    
# for i in range(0,60): #bucle dias (24 hours) 
#     m_list.append(i)

# for i in range(0,60): #bucle dias (24 hours) 
#     s_list.append(i)


# #interfaz de usuario o textos

# #Reloj
# txt1 = Label(window, text='Hour', bg='black',fg='magenta',font=('Arial',12,'bold'))
# txt1.grid(row=1,column=0, padx=5,pady=5)

# txt2 = Label(window, text='Minute', bg='black',fg='magenta',font=('Arial',12,'bold'))
# txt2.grid(row=1,column=1, padx=5,pady=5)

# txt3 = Label(window, text='Second', bg='black',fg='magenta',font=('Arial',12,'bold'))
# txt3.grid(row=1,column=2, padx=5,pady=5)

# #selector de hora

# cmb1 = ttk.Combobox(window,values=h_list,style="TCombobox", justify='center',width='12',font='Arial')
# cmb1.grid(row=2,column=0,padx=15,pady=5)
# cmb1.current(0)

# cmb2 = ttk.Combobox(window,values=m_list,style="TCombobox", justify='center',width='12',font='Arial')
# cmb2.grid(row=2,column=1,padx=15,pady=5)
# cmb2.current(0)

# cmb3 = ttk.Combobox(window,values=s_list,style="TCombobox", justify='center',width='12',font='Arial')
# cmb3.grid(row=2,column=2,padx=15,pady=5)
# cmb3.current(0)

# #estilos combobox

# style = ttk.Style()
# style.theme_create(
#     'combostyle',
#     parent='alt',
#     settings={
#         'TCombobox':
#         {
#             'configure':
#             {
#                 'selectbackground':'red',
#                 'fieldbackground':'gold',
#                 'background':'blue'
#             }
#         }
#     }
# )

# style.theme_use('combostyle')

# window.option_add('*TCombobox*Listbox*Background','white')
# window.option_add('*TCombobox*Listbox*Foreground','black')
# window.option_add('*TCombobox*Listbox*selectBackground','green2')
# window.option_add('*TCombobox*Listbox*selectForeground','black')

# #para alarma interfaz
# alarma = Label(window, fg='violet', bg='black', font=('Radioland',20))
# alarma.grid(column=0,row=3,sticky='nsew',ipadx=5,ipady=20)
# repetir = Label(window,fg='white', bg='black',text='Repetir', font='Arial')
# repetir.grid(column=1,row=3, ipadx=5, ipady=20)
# cantidad = ttk.Combobox(window,values=(1,2,3,4,5,6), justify='center',width='8',font='Arial')
# cantidad.grid(column=2, row=3, padx=5,pady=5)
# cantidad.current(0)


# #funciones

# def getTime():
#     x_hour = cmb1.get()
#     x_minute = cmb2.get()
#     x_second = cmb3.get()

#     hour = strftime('%H')
#     minute = strftime('%M')
#     second = strftime('%S')

#     hour_total = (hour + ' : ' + minute + ' : ' + second)
#     txt_hour.config(text=hour_total, font=('Radioland',25))

#     hour_alamar = x_hour + ' : ' + x_minute + ' : ' + x_second
#     alarma['text'] = hour_alamar

#     #condicion
#     res = False

#     if int(hour) == int(x_hour):
#         if int(minute) == int(x_minute):
#             if int(second) == int(x_second):
        
#                 mixer.music.load("musictmp\herta singing kururing.mp3")
#                 mixer.music.play(loops=int(cantidad.get()))
#                 ###
#                 #mixer.music.play = None 
#                 ###
#                 res = messagebox.askyesno(message="Alarma de las " + hour_alamar + "quiere posponer presione `si` o ignorar `no`", title='Alarma')
                
#     txt_hour.after(100,getTime)


# txt_hour = Label(window,fg='green2',bg='black')
# txt_hour.grid(columnspan=3,row=0,sticky='nsew',ipadx=5,ipady=20)

# getTime()


# window.mainloop()