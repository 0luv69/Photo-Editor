from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from setting import* 
from PIL import Image
from tkinter import colorchooser
import requests
import io
import threading
import cv2 as cv
import numpy as np


entred_the_name=False
enterd_both=False

class ImageOutputCloseBTN(ctk.CTkButton):
        def __init__(self,window, closed_func):
            self.closed_func= closed_func
            super().__init__(window,text="X",corner_radius=0,fg_color="transparent",
                             hover_color="red",width=45,height=45,command=self.closed_func)
            self.place(relx=.04,rely=0.01,anchor="ne")

class Pannel(ctk.CTkFrame):
    def __init__(self,window):
        super().__init__(window,fg_color=DARK_GREY)
        self.pack(fill="x",pady=4,padx=2,ipady=8)

class slider_Pannel(Pannel):
    def __init__(self,parent,text,data_var,min_value,max_value,addition_value):
        super().__init__(parent)

        self.data_var=data_var
        self.data_var.trace("w",self.update_text)
        self.min_value=min_value
        self.max_value=max_value
        #labelling the grid
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1,2),weight=1)
        
        #name label
        self.Name_label=ctk.CTkLabel(self,text=text)
        self.Name_label.grid(row=1,column=0,sticky="wn",padx=8)

        #value
        self.Num_label= ctk.CTkLabel(self,text= data_var.get())
        self.Num_label.place(relx=0.7,rely=.5)

        #expand button
        self.expansion_value=True
        self.expandButton= ctk.CTkButton(self,text="▲",
                                            fg_color="transparent",
                                            hover_color="green",
                                            width=10,
                                            command=self.expand_view)
        self.expandButton.place(relx=.85,rely=.5)

        # slider bar 
        self.slider=ctk.CTkSlider(self,fg_color=SLIDER_BG,
                                  variable=data_var,
                                  from_=min_value,to=max_value,
                                  )
        self.slider.grid(row=0,column=0,columnspan=3,sticky="ew",padx=8,pady=6)

        self.slider.bind("<MouseWheel>",command=lambda event:self.mouseWheel_move(event,addition_value))
        self.slider.bind("<Shift-MouseWheel>",command=lambda event:self.mouseWheel_move(event,.1))

    def expand_view(self):

        if self.expansion_value:
            self.expansion_value=False
            self.expandButton.configure(text="▼")
            # sider
            self.slider.grid_forget()

            self.Num_label.place(relx=0.7,rely=.21)
            self.expandButton.place(relx=.85,rely=.21)

        else:
            self.expansion_value=True
            self.expandButton.configure(text="▲")
            #sider
            self.slider.grid(row=0,column=0,columnspan=3,sticky="ew",padx=8,pady=6)

            self.Num_label.place(relx=0.7,rely=.5)
            self.expandButton.place(relx=.85,rely=.5)

    def mouseWheel_move(self,event,addition_value):
        the_value=self.data_var.get()
        if event.delta <0:
           if the_value>self.min_value:
                self.data_var.set(the_value-addition_value)
        else:
           if the_value<self.max_value: 
                self.data_var.set(the_value+addition_value)
    
    def update_text(self,*args):
        self.Num_label.configure(text=(round(self.data_var.get(),2)))

class Flip_Rotation(slider_Pannel):
    def __init__(self, parent,flipx_var,flipy_var,text,data_var,min_value,max_value,addition_value):
        super().__init__(parent,text,data_var,min_value,max_value,addition_value)
        self.parent= parent
        self.extended_view=True

        self.expandButton.destroy()

        self.rowconfigure((0,1,2,3,4),weight=1)
        self.columnconfigure((0,1,2),weight=1)

        ctk.CTkLabel(self,text="Flip & Rotate").grid(row=0,column=0,columnspan=1,sticky="e")
        self.expand_button=ctk.CTkButton(self,text="▲",
                                            fg_color="transparent",
                                            hover_color="green",
                                            width=10,
                                            command=self.expansion_toggle)
        self.expand_button.place(relx=0.62,rely=.02)

        #rotation box
        self.rotation_name_tag=ctk.CTkLabel(self,text="Rotate")
        self.rotate_left = ctk.CTkButton(self, text="L: ↻",
                                         corner_radius=60,width=8,
                                         fg_color="#373838",
                                          hover_color="#898c8f",
                                         command=lambda :self.parent.window.rotate90degree("r"))  

        self.rotate_right = ctk.CTkButton(self, text="R: ↺",
                                          corner_radius=60,width=8,
                                          fg_color="#373838",
                                          hover_color="#898c8f",
                                          command=lambda :self.parent.window.rotate90degree("l"))  


        # flip box
        self.flip_name_tag=ctk.CTkLabel(self,text="Flip")
        self.X_button= ctk.CTkButton(self,text="X: ↔",corner_radius=60
                                        ,width=8,
                                        fg_color="#373838",
                                        hover_color="#898c8f",
                                        command=lambda : self.change_fliping_value(flipx_var))  

        self.Y_button= ctk.CTkButton(self,text="Y:   ↕",corner_radius=60,
                                        width=8,
                                        fg_color="#373838",
                                        hover_color="#898c8f",                                     
                                        command=lambda : self.change_fliping_value(flipy_var))


        #rotation side
        self.rotation_name_tag.grid(row=1,column=0,sticky="wn",padx=8)
        self.rotate_left.place(relx=0.32,rely=.21,)
        self.rotate_right.place(relx=0.62,rely=.21,)
        #flip side
        self.flip_name_tag.grid(row=2,column=0,sticky="wn",padx=8)
        self.X_button.place(relx=0.32,rely=.4,)
        self.Y_button.place(relx=0.62,rely=.4,)
        #slider
        self.Name_label.grid(row=3,column=0,sticky="wn",padx=8)
        self.Num_label.place(relx=.83,rely=.6)
        self.slider.grid(row=4,column=0,columnspan=5,sticky="ew",padx=8,pady=6)

    def change_fliping_value(self,var):
        if var.get():
            var.set(False)
        else:
            var.set(True)        

    def expansion_toggle(self):
        self.extended_view=not self.extended_view
        if self.extended_view:
            self.expand_button.configure(text="▲")

            #rotation side
            self.rotation_name_tag.grid(row=1,column=0,sticky="wn",padx=8)
            self.rotate_left.place(relx=0.32,rely=.21,)
            self.rotate_right.place(relx=0.62,rely=.21,)

            #flip side
            self.flip_name_tag.grid(row=2,column=0,sticky="wn",padx=8)
            self.X_button.place(relx=0.32,rely=.4,)
            self.Y_button.place(relx=0.62,rely=.4,)

            #slider
            self.Name_label.grid(row=3,column=0,sticky="wn",padx=8)
            self.Num_label.place(relx=.83,rely=.6)
            self.slider.grid(row=4,column=0,columnspan=5,sticky="ew",padx=8,pady=6)
            
        else:
            self.expand_button.configure(text="▼")
            #rotation side
            self.rotation_name_tag.grid_forget()
            self.rotate_left.place_forget()
            self.rotate_right.place_forget()

            #flip side
            self.flip_name_tag.grid_forget()
            self.X_button.place_forget()
            self.Y_button.place_forget()

            #slider
            self.Name_label.grid_forget()
            self.Num_label.place_forget()
            self.slider.grid_forget()

class crop_pannel(Pannel):
    def __init__(self, parent,crop_variable):
        super().__init__(parent)
        self.crop_variable=crop_variable
        self.rowconfigure((0,1,2),weight=1)
        self.columnconfigure((0,1,2,3),weight=1)
 
        # self.columnconfigure((),weight=2)
        self.window=parent.window
        self.window.LIST_OF_LAST_CROPED_IMAGE.append(self.window.image)


        ctk.CTkLabel(self,text="Crop Box:").grid(row=0,column=0,columnspan=2,sticky="w",padx=10,pady=5)
        
        # Enable or disable button
        self.crop_variable.trace("w",self.update_crop_text)
        self.crop_box=ctk.CTkButton(self,text=f"{self.crop_variable.get()}",
                        fg_color="white",
                        hover_color="white",
                        text_color="green",
                      font=ctk.CTkFont(size=15,),
                      command=self.crop_box_checker
                      )
        self.crop_box.place(relx=.35,rely=.15,relwidth=.48)

        #resolution Box
        self.resolution_box=ctk.CTkFrame(self,)
        # self.resolution_box.grid(row=1,column=0,columnspan=3,sticky="ew",padx=4,pady=6)

        #width
        self.resolution_box_width= ctk.CTkEntry(self.resolution_box)
        self.resolution_box_width.place(relx=.03,rely=0.05,relwidth=.44,relheight=.9)

        #height
        self.resolution_box_height= ctk.CTkEntry(self.resolution_box)
        self.resolution_box_height.place(relx=.54,rely=0.05,relwidth=.44,relheight=.9)

        self.resolution_box_width.insert(0, f"{parent.window.orginal_image.width }")
        self.resolution_box_height.insert(0,f"{parent.window.orginal_image.height}")
        # multiple sign
        ctk.CTkLabel(self.resolution_box,text="X").pack(padx=3,pady=3)

        for childs in self.resolution_box.winfo_children():
            childs.bind("<MouseWheel>",self.lock_update_resolution)

        # #resizing button
        self.resizing_button=ctk.CTkButton(self,text="Resize",
                      fg_color="White",
                      text_color="Black",
                      hover_color="#45FFCA",
                      command=self.update_resolution)
        # self.resizing_button.place(relx=0.75,rely=.38,relwidth=.23)
        
        #back button
        self.back_btn=ctk.CTkButton(self,text="Back",command=self.reverse_image,
                      fg_color="#808080",
                      hover_color="#808AA0"
                      )
        # self.back_btn.grid(row=2,column=0,columnspan=4,sticky="ew",pady=6,padx=30)


        #expand button
        self.expansion_value=False
        self.expandButton=ctk.CTkButton(self,text="▼",
                                            fg_color="transparent",
                                            hover_color="green",
                                            width=10,
                                            command=self.expand_view)
        self.expandButton.place(relx=0.86,rely=.15)

    def expand_view(self):

        if self.expansion_value:
            self.expansion_value=False
            self.expandButton.configure(text="▼")
            #Resolution box

            self.expandButton.place(relx=0.86,rely=.15)
            self.crop_box.place(relx=.35,rely=.15,relwidth=.48)

            self.resolution_box.grid_forget()
            self.resizing_button.place_forget()
            self.back_btn.grid_forget()

        else:
            self.expansion_value=True
            self.expandButton.configure(text="▲")

            self.expandButton.place(relx=0.86,rely=.07)
            self.crop_box.place(relx=.35,rely=.07,relwidth=.48)

            #Resolution box
            self.resolution_box.grid(row=1,column=0,columnspan=3,sticky="ew",padx=4,pady=6)
            # resize btn 
            self.resizing_button.place(relx=0.75,rely=.38,relwidth=.23)
            #back btn
            self.back_btn.grid(row=2,column=0,columnspan=4,sticky="ew",pady=6,padx=30)

    def update_resolution(self,):
        try:
            Width=     int(self.resolution_box_width.get())    
            Height =   int(self.resolution_box_height.get())

            self.resolution_box_width.delete(0,"end")
            self.resolution_box_height.delete(0,"end")
            if Width >0 and Height >0:

                self.resolution_box_width.insert(0,f"{Width}")
                self.resolution_box_height.insert(0,f"{Height}")

                self.window.orginal_image=self.window.orginal_image.resize((Width,Height))  
                self.window.image=self.window.orginal_image
                self.window.resizing_image()
            else:
                ErrorPannel(self.window,text="Numbers are needed to be,\n Grester then Zero(0)") 
                self.resolution_box_width.insert(0, f"{self.window.orginal_image.width}")
                self.resolution_box_height.insert(0,f"{self.window.orginal_image.height}")

        except:
            ErrorPannel(self.window,text="PLZ, enter only numbers,\n no other Charater")

    def lock_update_resolution(self,event):
        Width =int(self.resolution_box_width.get()) 
        Height=int(self.resolution_box_height.get())

        if Width >0 and Height>0:
            if event.delta >0:
                new_width=Width*1.01
                new_height=Height* 1.01
            else:
                new_width=Width* 0.99
                new_height=Height* 0.99

            self.resolution_box_width.delete(0,"end")
            self.resolution_box_height.delete(0,"end")
            self.resolution_box_width.insert(0,f"{int(new_width)}")
            self.resolution_box_height.insert(0,f"{int(new_height)}")

    def reverse_image(self):
        try :
            self.window.orginal_image=self.window.LIST_OF_LAST_CROPED_IMAGE.pop()
            self.window.image=self.window.orginal_image
            self.window.resizing_image()
        except IndexError:
            pass  

    def crop_box_checker(self,*a):
        if self.crop_variable.get() == "Disabled ✗":
            self.crop_variable.set("Enabled    ✓")

        elif self.crop_variable.get() =="Enabled    ✓":
              self.crop_variable.set("Disabled ✗")

    def update_crop_text(self,*args):
        self.crop_box.configure(text=f"{self.crop_variable.get()}")
        pass          
  
class Switch_pannel(Pannel):
    def __init__(self, parent,*args):
        super().__init__(parent)
        for var, text in args:
            ctk.CTkSwitch(self,text=text,
                          variable=var,
                          corner_radius=2,
                          button_length=14,
                        button_hover_color=WHITE,
                        fg_color=SLIDER_BG,
                        button_color=BLUE,
                        progress_color=GREY,
                        
                        ).pack(side="left",expand=True,fill="both",padx=5,pady=5)

class RemoveBackGround(Pannel):
    def __init__(self, parent,window):
        super().__init__(parent)
        self.window= window
        self.image_list=[]
        self.BackGround_removed= False
        self.image_Backed=2
        self.remove_bg_btn=ctk.CTkButton(self,text="Remove Background 🪄",
                                         fg_color="#40F8FF",
                                         text_color="black",
                                         hover_color="#B6FFFA",
                                         command=self.removing_function_caller)
        self.remove_bg_btn.pack(padx=5, pady=5,side="left")

        
        self.back=ctk.CTkButton(self,text="Back ⮌",
                                fg_color="#808080",
                                hover_color="#8080AA",
                                command=self.back_the_changes) 
        self.back.pack(side="right",padx=5,pady=5) 

    def removing_function_caller(self):
        self.image_list.append(self.window.image)
        self.remove_bg_btn.configure(state="disabled")
        threading.Thread(target=self.removing_function).start()

    def removing_function(self):
        if not self.BackGround_removed:
            #converting pillow img to file image format
            Image_0 = io.BytesIO()
            self.window.orginal_image.save(Image_0, format='PNG')
            Image_0.seek(0)
            files = {'image_file': ('image.png', Image_0, 'image/png')}
            headers = {'X-Api-Key': 'ZwhtYe5vAsBFAkcXNEhzcce8'}
            params = {'size': 'auto'}
            self.remove_bg_btn.configure(text="Removing ......")
            response = requests.post("https://api.remove.bg/v1.0/removebg", headers=headers, params=params, files=files)

            # Check if the request was successful
            if response.status_code == 200:
                self.window.image= self.window.orginal_image = Image.open(io.BytesIO(response.content))
                self.window.resizing_image()
                self.image_list.append(self.window.image)
                self.BackGround_removed= True
            else:
                ErrorPannel(self.window,text=f"Error: {response.status_code, response.text}")
        else:
            self.BackGround_removed= False 
        
        self.remove_bg_btn.configure(state="normal")    
        self.remove_bg_btn.configure(text="Remove Background 🪄")    

    def back_the_changes(self):
        if len(self.image_list) >= 2:
            try:
                seleceted_img=self.image_list[-(self.image_Backed)]
            except IndexError:
                self.image_Backed=1
                seleceted_img=self.image_list[-(self.image_Backed)]

            self.image_Backed+=1
            self.window.image= self.window.orginal_image =seleceted_img 
            self.window.resizing_image()

            
        pass
        
class DropDownPannel(ctk.CTkOptionMenu):
    def __init__(self, master, data_var,option):
        super().__init__(master,values=option,
                         variable=data_var,
                         fg_color=DARK_GREY,
                         button_color=DropDown_Main_color,
                         button_hover_color=DropDown_Hover_color,
                         dropdown_fg_color=DropDown_Menu_color,
                         )
        self.pack(fill="x",pady=8,padx=8)
    
class Reverse_Btn(ctk.CTkButton):
    def __init__(self,parent,*args):
        super().__init__(parent,text="Reverse ⮌",command=lambda :self.reverse_value(args))  
        self.pack(side="bottom",pady=15) 
        ToolTip(self,"Reverse all the change")
    def reverse_value(self,args):
        for variable, default_value in args:
            variable.set(default_value) 

class ErrorPannel(ctk.CTkFrame):
    def __init__(self,window,text,color_="red"):
        super().__init__(window,fg_color=color_,border_width=2,border_color="#A6FF96",corner_radius=0)
        self.window=window 
        self.place(relx=0.2,rely=.65,relwidth=.6,relheight=.07)
        ctk.CTkLabel(self,text=text).pack(pady=4)
        self.window.after(4300,self.unhide)
    def unhide(self):self.destroy()

class position_x_y(Pannel):
    def __init__(self,parent,text,data_var_x,data_var_y,distance_x,distance_y,window):
        super().__init__(parent)
        self.data_var_x=data_var_x
        self.data_var_y=data_var_y

        self.window=window
        self.distance_x=distance_x
        self.distance_y=distance_y

        #labelling the grid
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1,2),weight=1)
        
        #name label
        self.Name_label=ctk.CTkLabel(self,text=text)
        self.Name_label.grid(row=0,column=0,sticky="wns",padx=8)

        # slider bar 
        self.slider=ctk.CTkSlider(self,fg_color=SLIDER_BG,command=self.select_x_y,state="disabled")
        self.slider.grid(row=1,column=0,columnspan=3,sticky="ew",padx=8,pady=6)
        ToolTip(self.slider,"Select (x or y), and then scroll")
        self.slider.bind("<Button-1>", self.select_x_y)

        reverse_bttn=ctk.CTkButton(self,text="⮌",command=self.reverse,
                      fg_color="#494b5c",hover_color="red")
        reverse_bttn.place(relx=0.25,rely=0.037,relwidth=.1)
        ToolTip(reverse_bttn,"Reverse the changes")

        self.once_selected_or_not=False
        # x
        ctk.CTkLabel(self,text="X:").place(relx=.38,rely=0.03)
        self.x_label= ctk.CTkEntry(self,width=50)
        self.x_label.insert(0,0.0)
        self.x_label.grid(row=0,column=1,sticky="ens",padx=4,pady=0)
        self.x_label.bind("<Button-1>",self.x_slider_On)
        self.x_label.bind("<KeyRelease>",
                          lambda e: self.enter_box_bind(
                              self.x_label,self.data_var_x,self.distance_x))

        # y
        ctk.CTkLabel(self,text="Y:").place(relx=.73,rely=0.03)
        self.y_label= ctk.CTkEntry(self,width=50)
        self.y_label.insert(0,0.0)
        self.y_label.grid(row=0,column=2,sticky="ens",padx=8,pady=0)
        self.y_label.bind("<Button-1>",self.y_slider_On)
        self.y_label.bind("<KeyRelease>",
                          lambda e: self.enter_box_bind(
                              self.y_label,self.data_var_y,self.distance_y))

    def select_x_y(self,event):
        if self.once_selected_or_not==False:
            ErrorPannel(self.window,"Plz, first select the X or Y box, then scrool","#5B0888")

    def x_slider_On(self,event):
        self.slider.unbind("<MouseWheel>")
        self.once_selected_or_not=True
        self.x_label.bind("<MouseWheel>",
                          command=lambda event:self.mouseWheel_move(event,
                                                                    self.x_label,self.data_var_x,
                                                                    self.distance_x,5))
        self.slider.configure(state="normal",from_=-self.distance_x, 
                              to =self.distance_x,variable=self.data_var_x,
                              command=lambda event:self.update_data_(
                                  self.x_label,self.data_var_x))
        self.slider.bind("<MouseWheel>",
                         command=lambda event:self.mouseWheel_move(event,
                                                                   self.x_label,self.data_var_x,
                                                                   self.distance_x,3))

    def y_slider_On(self,event):
        self.slider.unbind("<MouseWheel>")
        self.once_selected_or_not=True
        self.y_label.bind("<MouseWheel>",
                          command=lambda event:self.mouseWheel_move(event,
                                                                    self.y_label,self.data_var_y,
                                                                    self.distance_y,5))
        self.slider.configure(state="normal",from_=-self.distance_y, 
                              to =self.distance_y,variable=self.data_var_y,
                              command=lambda event:self.update_data_(
                                  self.y_label,self.data_var_y))
        self.slider.bind("<MouseWheel>",
                         command=lambda event:self.mouseWheel_move(event,
                                                                   self.y_label,self.data_var_y,
                                                                   self.distance_y,3))
        
    def mouseWheel_move(self,event,label_Value,data_variable,distance__,upadte_value):
        the_value=data_variable.get()
        if event.delta <0:
            if the_value>-distance__:
                data_variable.set(data_variable.get()-upadte_value)
                self.update_data_(label_Value,data_variable)
        else:
            if the_value<distance__:
                data_variable.set(data_variable.get()+upadte_value)
                self.update_data_(label_Value,data_variable)

    def update_data_(self,label_Value,data_variable):
        input_value = float(data_variable.get())
        label_Value.delete(0, "end")  # Clear the entry widget
        label_Value.insert(0, str(round(input_value, 2)))

    def enter_box_bind(self,label_Value,data_variable,distance):
        input_value_=label_Value.get()
        try:
            float_value = float(input_value_)
            if float_value > -distance:data_variable.set(float_value)
            else:self.update_data_(label_Value,data_variable)

            if float_value < distance:data_variable.set(float_value)
            else:self.update_data_(label_Value,data_variable)                        

        except:
            data_variable.set(0)
            label_Value.delete(0, "end") 
            label_Value.insert(0,0)
            if input_value_ =="":pass
            else: ErrorPannel(self.window,"You Can only type Number not string, \nBad Input")

    def reverse(self):
        self.window.focus()
        self.once_selected_or_not=False
        self.slider.configure(state="disable")
        self.data_var_x.set(0)
        self.data_var_y.set(0)
        self.x_label.delete(0, "end") 
        self.x_label.insert(0,0.0)

        self.y_label.delete(0, "end") 
        self.y_label.insert(0,0.0)

class Paint(Pannel):
    def __init__(self, parent,dontdraw,ballColor,ballsize,window):
        super().__init__(parent)
        self.dontdraw= dontdraw
        self.columnconfigure((0,1,2),weight=1)
        self.rowconfigure((0,1,2),weight=1)
        self.image_output=window.inner_cavas_box
        self.window=window


        self.LAST_PEN_DRAWN=[self.window.image]
        self.LAST_IMAGE_SELECTED=[self.window.image]

        self.ballColor_var,self.ballsize_var=ballColor,ballsize

        # brush button check or uncheck
        self.d_or_und_Button=ctk.CTkButton(self,text="DRAW",
                                           fg_color="#a881af",
                                           hover_color="#33b249",
                                           command=lambda :self.draw_or_disable(dontdraw))
        
        self.d_or_und_Button.grid(row=0,column=0,columnspan=2,sticky="sn",pady=10)

        #color selecting
        ctk.CTkLabel(self,text="Color :").grid(row=1,column=0,sticky="nw",padx=20)
        self.color_selection=ctk.CTkButton(self,text="",
                                           command=lambda:self.choose_color(),
                                           fg_color=ballColor.get(),
                                           hover=None,
                                           corner_radius=5,
                                           width=50,
                                           border_color="#3C2A21",
                                           border_width=2
                                           )
        
        self.color_selection.place(relx=.26,rely=.42)


        #back & revert 

        self.get_back=ctk.CTkButton(self,text="Back",fg_color="#A77979",
                                    command=self.get__pen_draw_back,
                                    text_color="black",hover_color="white")
        self.get_back.place(relx=.5,rely=.42, relwidth=.25)

        self.bind("<Control-z>",self.get__pen_draw_back)
        

        self.get_revert=ctk.CTkButton(self, text="⮌",fg_color="#A7797b",
                                      command=self.get__revert,
                                      text_color="black",hover_color="white")
        self.get_revert.place(relx=.79,rely=.42, relwidth=.14)


        #size manageing
        self.slider=ctk.CTkSlider(self,fg_color=SLIDER_BG,
                                  variable=ballsize,
                                  from_=.4,to=20,
                                  command=lambda e:self.update(ballsize))
        
        self.slider.grid(row=3,column=0,sticky="ew",pady=10)

        self.size_entry_box= ctk.CTkEntry(self,width=55)
        self.size_entry_box.grid(row=3,column=1, sticky="e",padx=3,pady=6)
        self.size_entry_box.insert(0,ballsize.get())

    def get__revert(self):
        try:    
            self.window.image=self.window.orginal_image=self.LAST_IMAGE_SELECTED.pop()
            self.window.resizing_image()
        except IndexError:
            pass

    def get__pen_draw_back(self,*args):
        
        try :
            self.window.image=self.window.orginal_image=self.LAST_PEN_DRAWN.pop()          
            self.window.resizing_image()
        except IndexError:
            self.window.unbind("<Control-z>")
            pass 

    def update(self,ballsize):
        self.size_entry_box.delete(0, "end")
        self.size_entry_box.insert(0,ballsize.get())

    def draw_or_disable(self,dontdraw):
        if dontdraw.get() ==False:
            self.window.bind("<Control-b>",self.get__pen_draw_back)
            self.window.inner_cavas_box.bind("<ButtonPress>",self.Start_brush)
            self.LAST_IMAGE_SELECTED.append(self.window.image)
            dontdraw.set(True)
            self.d_or_und_Button.configure(text="UnCheck Brush",
                                            fg_color="#80669d",
                                           hover_color="red",)
        else:
            self.window.unbind("<Control-b>")
            self.window.inner_cavas_box.unbind("<B1-Motion>")
            dontdraw.set(False)
            self.d_or_und_Button.configure(text="Add Brush",
                                           fg_color="#a881af",
                                           hover_color="#33b249",)

    def Start_brush(self,event):
        self.startX= event.x   
        self.startY= event.y 
        self.window.inner_cavas_box.bind("<B1-Motion>",lambda event :self.Draw_brush(event))

    def Draw_brush(self,event):
        brushsize=self.ballsize_var.get()
        ball_hex_color= self.ballColor_var.get()

        ball_hex_color = ball_hex_color.lstrip('#')
        red = int(ball_hex_color[0:2], 16)
        green = int(ball_hex_color[2:4], 16)
        blue = int(ball_hex_color[4:6], 16)

        ball_color=(blue,green,red)
        position_place=[(int(self.startX  ), int(self.startY )),
                 (int(event.x ), int(event.y ))]   

        cv_image= cv.cvtColor(np.array(self.window.resized_image_.convert("RGB")),cv.COLOR_RGB2BGR)
        cv_image =cv.line(cv_image, position_place[0],position_place[1],
                 ball_color, thickness=int(brushsize))
        cv_image= cv.cvtColor(cv_image,cv.COLOR_BGR2RGB)
        self.window.orginal_image=self.window.image=Image.fromarray(cv_image)
        self.LAST_PEN_DRAWN.append(self.window.orginal_image)

        # self.window.resizing_image()
        self.window.place_image_in_canvas()

        self.window.inner_cavas_box.bind("<B1-Motion>",lambda event :self.Draw_brush(event))
        self.startX= event.x   
        self.startY= event.y 
        self.window.inner_cavas_box.bind("<ButtonRelease>",self.button_released)

        # self.window.inner_cavas_box.create_oval((event.x-brushsize,event.y -brushsize,event.x+brushsize,event.y +brushsize),
        #                               outline=ballColor.get(),
        #                               fill=ballColor.get(),
        #                               )        
    
    def button_released(self,*args):
        self.window.inner_cavas_box.bind("<ButtonPress>",self.Start_brush)
  
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color != None:
            self.ballColor_var.set(color)   
            self.color_selection.configure(fg_color=self.ballColor_var.get())
        else:
            ErrorPannel(self.window,
                        "You have to select color, \n!! May be you forget to click ok !!")    
   
class ToolTip():
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
 
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 35

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, background="#FFC7EA", relief="solid",)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class Adjust_hue(Pannel):
    def __init__(self,parent,window):
        super().__init__(parent)

        self.window= window

        self.columnconfigure((0,1),weight=1,uniform="a")
        self.red_variable   =ctk.IntVar(value=128)
        self.green_variable =ctk.IntVar(value=128)
        self.blue_variable  =ctk.IntVar(value=128) 

        self.red_variable  .trace("w",lambda *e:self.update_value("red"))
        self.green_variable.trace("w",lambda *e:self.update_value("green"))
        self.blue_variable .trace("w",lambda *e:self.update_value("blue"))


        ctk.CTkLabel(self,text="Color Pannel",text_color="White",fg_color="grey",corner_radius=10
                     ).grid(row =0,column= 0,columnspan=2,pady=9)

        self.red_value  = ctk.CTkLabel(self,text=self.red_variable  .get(),width=35,)
        self.green_value= ctk.CTkLabel(self,text=self.green_variable.get(),width=35,)
        self.blue_value = ctk.CTkLabel(self,text=self.blue_variable .get(),width=35,)


        self.red_slider  =ctk.CTkSlider(self,fg_color="red",from_=0,to=255,button_color="red"    ,
                       variable=self.red_variable  ,                 
                        button_hover_color="WHITE")        
        self.green_slider =ctk.CTkSlider(self,fg_color="green",from_=0,to=255,button_color="green",
                       variable=self.green_variable,                  
                        button_hover_color="WHITE")
        self.blue_slider =ctk.CTkSlider(self,fg_color="Blue",from_=0,to=255,button_color="blue"  ,
                        variable=self.blue_variable ,                
                        button_hover_color="WHITE")

        self.revertchanges= ctk.CTkButton(self, text="Revert", fg_color="SKY BLUE",text_color="black", command= self.Revert_)
        
        #expand button
        self.expansion_value=True
        self.expandButton=ctk.CTkButton(self,text="▼",
                                            fg_color="transparent",
                                            hover_color="green",
                                            width=10,
                                            command=self.expand_view)
        self.expand_view()

    def Revert_(self):
        self.red_variable  .set(1)
        self.green_variable.set(1)
        self.blue_variable .set(1)

        self.window.image= self.window.orginal_image
        self.window.resizing_image()

    def update_value(self,selected_color):
        cv_image=cv.cvtColor(np.array(self.window.orginal_image.convert("RGB")),cv.COLOR_RGB2BGR)

        if selected_color == "red":
            self.red_value.configure(text=self.red_variable.get())

        elif selected_color == "green":
            self.green_value.configure(text=self.green_variable.get())

        elif selected_color == "blue":
            self.blue_value.configure(text=self.blue_variable.get())

        red__ = self.red_variable.get()
        green__ =self.green_variable.get()
        blue__ =     self.blue_variable.get()

        # Apply color adjustments
        adjusted_image = cv_image.copy()
        adjusted_image[:, :, 0] = cv.addWeighted(adjusted_image[:, :, 0], 1, 0, 0, red__ - 128)
        adjusted_image[:, :, 1] = cv.addWeighted(adjusted_image[:, :, 1], 1, 0, 0, green__ - 128)
        adjusted_image[:, :, 2] = cv.addWeighted(adjusted_image[:, :, 2], 1, 0, 0, blue__ - 128)

        
        self.window.image = Image.fromarray(adjusted_image)
        self.window.resizing_image()

    def expand_view(self):
        if self.expansion_value:
            self.expansion_value=False
            self.expandButton.configure(text="▼")
            self.expandButton.place(relx=0.76,rely=.06)

            self.revertchanges.place(relx=0.05,rely=.05,relwidth= .22)

            self.red_value .grid(column=0,sticky= "nw",pady=5)
            self.green_value.grid(column=0,sticky= "nw",pady=5)
            self.blue_value.grid(column=0,sticky= "nw",pady=5)


            self.red_slider  .place(relx =.18,rely=0.33, relwidth=.78)
            self.green_slider.place(relx=.18,rely=0.55, relwidth=.78)
            self.blue_slider .place(relx=.18,rely=0.77, relwidth=.78)
       
        else:
            self.expansion_value=True
            self.expandButton.configure(text="▲")
            self.expandButton.place(relx=0.76,rely=.17)

            self.revertchanges.place_forget()

            self.red_value  .grid_forget()
            self.green_value.grid_forget()
            self.blue_value .grid_forget()

            self.red_slider  .place_forget()
            self.green_slider.place_forget()
            self.blue_slider .place_forget()