import customtkinter as ctk
from tkinter import filedialog,Canvas
from PIL import Image,ImageTk,ImageOps,ImageEnhance,ImageFilter
import cv2 as cv
import numpy as np
from setting import *
from menu import *
from pannel import ErrorPannel,ToolTip,ImageOutputCloseBTN

class Window(ctk.CTk):
    def __init__(self):
        #setup window 
        super().__init__()
        self._set_appearance_mode("dark")
        self.geometry("800x500")
        self.title("Photo editor")
        self.minsize(780,430)

        #Calling the parameters or definig the value
        self.init_parameters()

        self.LIST_OF_LAST_CROPED_IMAGE= []

        #layouts
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=6,uniform="a")
        self.columnconfigure(1,weight=2,uniform="a")

        #defining some canvas value 
        self.canvas_height=0
        self.canvas_width=0
        self.height_=0
        self.width_ =0
        # self.last_zoom_value=0
        self.last_saved_path=0
        

        self.tracing_enabled = False
        #calling the first page
        self.image_import=ImageImport_pg1st(self,self.display_image_pg2nd)

        # self.image_import=self.display_image_pg2nd("E:/_Code_/website/Birth_day_website/she/images/6.jpg")

        #run
        self.mainloop()

    def init_parameters(self): 

        self.pos_vars={
            "x":ctk.DoubleVar(value=x_Default),
            "y":ctk.DoubleVar(value=y_Default),
            "straighten":ctk.DoubleVar(value=ROTATE_DEFAULT),
            "flipX":ctk.BooleanVar(value=False),
            "flipY":ctk.BooleanVar(value=False),
            "crop":ctk.StringVar(value="Disabled ✗")}

        self.color_vars={
            "brightness":ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            "grayscale":ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            "invert":ctk.BooleanVar(value=INVERT_DEFAULT),
            "saturation":ctk.DoubleVar(value=SATURATION_DEFAULT),
            "contrast":ctk.DoubleVar(value=CONTRAST_DEFAULT)
            }

        self.effect_vars={
            "blur":ctk.DoubleVar(value=BLUR_DEFAULT),
            "effect":ctk.StringVar(value=EFFECT_OPTIONS[0]),            }
        
        self.Draw_vars={
            "drawORdont":ctk.BooleanVar(value=DRAW_OR_DONT),
            "ballcolor":ctk.StringVar(value=DRAWING_DEFAULT_COLOR),
            "ballSize":ctk.IntVar(value=BALL_SIZE),
        }

        # traceing
        self.variable_name_not_called=[]    
        self.deletecommand_cbname=[]
        for var in list(self.pos_vars.values())+ list(self.color_vars.values())+list(self.effect_vars.values()):
            Tracing_address=var.trace("w",self.manuplate_image)
            self.deletecommand_cbname.append(Tracing_address)
            self.variable_name_not_called.append(var)

    def manuplate_image(self,*args,need_to_append=True):
        self.image=self.orginal_image

        #straighten--rotate
        if self.pos_vars['straighten'].get() != ROTATE_DEFAULT:
            # to add default value only once
            if self.pos_vars["straighten"] in self.variable_name_not_called:
                self.Edited_Value_list.append([self.pos_vars['straighten'],ROTATE_DEFAULT,2])
                self.variable_name_not_called.remove(self.pos_vars['straighten'])

            self.image=self.image.rotate(self.pos_vars['straighten'].get())
            if need_to_append:
                self.Edited_Value_list.append([self.pos_vars['straighten'],self.pos_vars['straighten'].get(),2])
            
        # change_position
        if self.pos_vars['x'].get() != x_Default or self.pos_vars['y'].get() != y_Default:
            left = self.pos_vars['x'].get()
            upper = self.pos_vars['y'].get()
            right = self.image.width+self.pos_vars['x'].get()
            lower = self.image.height+self.pos_vars['y'].get()
            self.image=self.image.crop((left, upper, right, lower))

        #flip
        if self.pos_vars['flipX'].get() != False :
            self.image=ImageOps.mirror(self.image)
            self.Edited_Image_list.append(self.image)

        if self.pos_vars['flipY'].get() != False:
            self.image=ImageOps.flip(self.image)
            self.Edited_Image_list.append(self.image)

        #brightness 
        if self.color_vars["brightness"].get() != BRIGHTNESS_DEFAULT:
            Brightness_enancheer= ImageEnhance.Brightness(self.image)
            self.image=Brightness_enancheer.enhance(self.color_vars["brightness"].get())   

            # to add default value only once
            if self.color_vars['brightness'] in self.variable_name_not_called:
                self.Edited_Value_list.append([self.color_vars['brightness'],BRIGHTNESS_DEFAULT,6])
                self.variable_name_not_called.remove(self.color_vars['brightness'])
            if need_to_append:
                self.Edited_Value_list.append([self.color_vars["brightness"],self.color_vars["brightness"].get(),6])

        #Saturation
        if self.color_vars["saturation"].get() != SATURATION_DEFAULT:
            saturation_enancheer= ImageEnhance.Color(self.image)
            self.image=saturation_enancheer.enhance(self.color_vars["saturation"].get()) 

            # to add default value only once
            if self.color_vars["saturation"] in self.variable_name_not_called:
                self.Edited_Value_list.append([self.color_vars['saturation'],SATURATION_DEFAULT,9])
                self.variable_name_not_called.remove(self.color_vars['saturation'])

            if need_to_append:
                self.Edited_Value_list.append([self.color_vars["saturation"],self.color_vars["saturation"].get(),9])
        
        # constrast
        if self.color_vars["contrast"].get() != CONTRAST_DEFAULT:    
            self.image=self.image.filter(ImageFilter.UnsharpMask(self.color_vars["contrast"].get()))

            # to add default value only once
            if self.color_vars["contrast"] in self.variable_name_not_called:
                self.Edited_Value_list.append([self.color_vars['contrast'],CONTRAST_DEFAULT,10])
                self.variable_name_not_called.remove(self.color_vars['contrast'])

            if need_to_append:
                self.Edited_Value_list.append([self.color_vars["contrast"],self.color_vars["contrast"].get(),10])
               

        # grayscale and invert of the color
        if self.color_vars["grayscale"].get():
            self.image=ImageOps.grayscale(self.image)

        if self.color_vars["invert"].get():
            try:
                self.image=ImageOps.invert(self.image)
            except:pass

        #blur
        if self.effect_vars["blur"].get() != BLUR_DEFAULT:
            self.image=self.image.filter(ImageFilter.GaussianBlur(self.effect_vars["blur"].get()))
            # to add default value only once
            if self.effect_vars["blur"] in self.variable_name_not_called:
                self.Edited_Value_list.append([self.effect_vars['blur'],BLUR_DEFAULT,11])
                self.variable_name_not_called.remove(self.effect_vars['blur'])

            if need_to_append:
                self.Edited_Value_list.append([self.effect_vars["blur"],self.effect_vars["blur"].get(),11])

        # effects 
        match self.effect_vars["effect"].get():
            case "Emboss": self.image=self.image.filter(ImageFilter.EMBOSS)
            case "Find edges": self.image=self.image.filter(ImageFilter.FIND_EDGES)
            case 'Contour': self.image=self.image.filter(ImageFilter.CONTOUR)
            case 'Edge enhance': self.image=self.image.filter(ImageFilter.EDGE_ENHANCE)

        self.place_image_in_canvas()

        # # crop
        if self.pos_vars['crop'].get() == "Enabled    ✓":
            self.crop_action()   

    def display_image_pg2nd(self,path):

        self.pure_image=Image.open(path)
        self.orginal_image=self.pure_image
        self.image=self.orginal_image
        self.image_tk= ImageTk.PhotoImage(self.image)

        # crtl + z features
        self.Edited_Value_list=[]
        self.Edited_Image_list=[]
        self.Backed_image_Number=1

        self.bind("<Control-z>", self.CTRL_Z)
        self.Edited_Image_list.append(self.image)

        # resizing the image
        self.state('zoomed')
        self.minsize(1000,300)


        # #forgetting page one button 
        self.image_import.grid_forget()
        
        # calling the canvas and side menu bar
        self.main_canvas_outputBox=CanvasImageOutput(self,self.resizing_image)  # calling the canvas
        self.down_resolution_and_zoom_bar=Resolution_AND_zoom_bar(self)
        self.menu=Menu(self, 
                       dict(self.pos_vars,**{"x_":self.image.width,"y_":self.image.height}),
                       self.color_vars,
                       self.effect_vars,
                       self.Draw_vars) #calling the side menu bar
        self.close_button =ImageOutputCloseBTN(self,self.close_edit) 

    def close_edit(self):
        # forgeting all the widgets
        self.main_canvas_outputBox.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.init_parameters()

        # adding the import image button
        self.image_import=ImageImport_pg1st(self,self.display_image_pg2nd)

    def resizing_image(self,*args):
        self.canvas_width=self.main_canvas_outputBox.winfo_width()
        self.canvas_height=self.main_canvas_outputBox.winfo_height()

        # ratio of image & canvas
        self.image_ratio= self.image.width/self.image.height
        self.canvas_ratio=self.canvas_width/self.canvas_height
        #resize the image
        if self.canvas_ratio < self.image_ratio: # WHEN image width is large than canvas
            self.width_=int(self.canvas_width)-IMAGE_BORDER_MARGIN        
            self.height_= int(self.width_/self.image_ratio)
        else:                                    # WHEN image height is large than canvas
            self.height_= int(self.canvas_height)-IMAGE_BORDER_MARGIN  #setting height of canvas, since image height is large            
            self.width_ = int(self.height_*self.image_ratio) #since width is ofcource small so the height of canvas * to the actual size difference of image ratio

        # self.dfad=
        self.place_image_in_canvas()

    def place_image_in_canvas(self):
        self.down_resolution_and_zoom_bar.change_resolution_bar_value()
        # image resizing inisilization process
        self.resized_image_=self.image.resize((self.width_,self.height_))
        self.image_tk= ImageTk.PhotoImage(self.resized_image_)

        # destroying the previous inner_canvaas_box
        try:
            self.inner_cavas_box.destroy()
        except:
            pass    
        
        self.inner_cavas_box=ctk.CTkCanvas(self.main_canvas_outputBox,
                                           background="black",
                                           borderwidth=0,highlightthickness=0,
                                           width=self.width_,height=self.height_)
        self.inner_cavas_box.place(relx=0.5, rely=0.5, anchor="center")

        center_point=self.inner_cavas_box.winfo_reqwidth()/2,self.inner_cavas_box.winfo_reqheight()/2
        self.canvas_image=self.inner_cavas_box.create_image(center_point[0],center_point[1],image=self.image_tk,tags="0_image_0")

    def crop_action(self):
        self.inner_cavas_box.bind("<ButtonPress-1>",self.start_crop)
        self.inner_cavas_box.bind("<B1-Motion>",self.draw_crop)
        
    def start_crop(self,event):
        self.start_x=event.x
        self.start_y=event.y

        self.LIST_OF_LAST_CROPED_IMAGE.append(self.image)

    def draw_crop(self,event):
            self.inner_cavas_box.delete("Crop_rect")
            self.make_x,self.make_y=event.x,event.y
            
            self.inner_cavas_box.create_rectangle(self.start_x,self.start_y,self.make_x,self.make_y,
                                           outline="red",
                                           width=4,
                                           tags="Crop_rect")
            self.inner_cavas_box.bind("<ButtonRelease>",self.end_crop)
    
    def end_crop(self,event):
        x_scale = self.orginal_image.width / self.width_
        y_scale = self.orginal_image.height / self.height_

        if self.start_x < self.make_x and self.start_y < self.make_y:
            # normal start= topleft, end bottom right 
            temp_start_x=int(self.start_x*x_scale)
            temp_start_y=int(self.start_y*y_scale)
            temp_make_x=int(self.make_x*x_scale)
            temp_make_y=int(self.make_y*y_scale)

        elif self.start_x> self.make_x and self.start_y > self.make_y:
            # start = bottom right, end= top left
            temp_start_x=int(self.make_x*x_scale)
            temp_start_y=int(self.make_y*y_scale)
            temp_make_x=int(self.start_x*x_scale)
            temp_make_y=int(self.start_y*y_scale)

        elif self.start_x < self.make_x and self.start_y > self.make_y:
            # start= bottom left, end = top right
            temp_start_x=int(self.start_x*x_scale)
            temp_start_y=int(self.make_y*y_scale)
            temp_make_x=int(self.make_x*x_scale)
            temp_make_y=int(self.start_y*y_scale)

        elif self.start_x > self.make_x and self.start_y < self.make_y:
            # normal start= top right, end = bottom left
            temp_start_x=int(self.make_x*x_scale)
            temp_start_y=int(self.start_y*y_scale)
            temp_make_x=int(self.start_x*x_scale)
            temp_make_y=int(self.make_y*y_scale)

        self.width_=temp_make_x-temp_start_x
        self.height_=temp_make_y-temp_start_y
        
        # Crop the image using num py and open cv
        cv_image= cv.cvtColor(np.array(self.image.convert("RGB")),cv.COLOR_RGB2BGR)

        # croped
        x = slice(temp_start_x,temp_make_x, 1)
        y = slice(temp_start_y,temp_make_y, 1)
        cv_image= cv_image[y,x]
        cv_image= cv.cvtColor(cv_image,cv.COLOR_BGR2RGB)
        self.image = Image.fromarray(cv_image)

        self.orginal_image= self.image
        self.resizing_image()
        self.pos_vars['crop'].set("Disabled ✗")

    def rotate90degree(self, direction):
        cv_image= cv.cvtColor(np.array(self.orginal_image.convert("RGB")),cv.COLOR_RGB2BGRA)
        if direction=="r":
            cv_image= cv.rotate(cv_image,cv.ROTATE_90_CLOCKWISE)
        else:
            cv_image= cv.rotate(cv_image,cv.ROTATE_90_COUNTERCLOCKWISE) 

        cv_to_pil_image= cv.cvtColor(cv_image,cv.COLOR_BGR2RGB)
        self.image = Image.fromarray(cv_to_pil_image)
        self.orginal_image= self.image   

        self.image=self.image.rotate(self.pos_vars['straighten'].get())
        self.resizing_image()

    def CTRL_Z(self,event):
            try:
                selected_variable,selected_value,tarce_id_num=self.Edited_Value_list.pop()
                selected_variable.trace_vdelete("w",self.deletecommand_cbname[tarce_id_num])
                selected_variable.set(selected_value)
                self.manuplate_image(need_to_append=False)
                self.deletecommand_cbname[tarce_id_num]=selected_variable.trace("w",self.manuplate_image)

            except IndexError:
                pass 

class ImageImport_pg1st(ctk.CTkFrame):
    """This function will call the (self.display_image_pg2nd) function with the path of image"""
    def __init__(self,window, pg2_caller_function):
        super().__init__(window)
        self.window=window
        self.pg2_caller_function= pg2_caller_function
        self.grid(row=0,column=0,columnspan=2,sticky="nsew")
        # self.window.configure(fg_col)

        self.upload_frame_box= ctk.CTkFrame(self,cursor="star")
        self.upload_frame_box.place(relx=.15,rely=.15,relwidth=.7,relheight=.7)

        ctk.CTkLabel(self.upload_frame_box,text="+",
                     cursor="hand2",
                     font=ctk.CTkFont(size=120)
                     ).pack(pady=50)

        ctk.CTkLabel(self.upload_frame_box,
                     text="Drag Your Image Here",
                     fg_color="#413F42",
                     font=ctk.CTkFont(size=15),
                     corner_radius=30
                     ).place(relx=.1,rely=.52,relwidth=.8)

        self.import_button= ctk.CTkButton(self,text="Choose File",
                                          fg_color="#9772FB",
                                          command=self.open_dialog,
                                          hover_color="#764AF1",
                                          cursor="hand2",
                                          font=ctk.CTkFont(family="Verdana",size=25)
                                          )
        self.import_button.place(relx=.4,rely=.67,relwidth=.2)

        for childs in self.upload_frame_box.winfo_children():
            childs.bind("<ButtonPress-1>", self.open_dialog)
        self.upload_frame_box.bind("<ButtonPress-1>", self.open_dialog)    

        # animation instance/ value
        self.dot="."
        self.total_animation_call=0
        self.error_made_stop=0
        self.loading_text=ctk.StringVar() 
    
    def open_dialog(self,*args):
        self.loading_=ctk.CTkLabel(self.upload_frame_box,textvariable=self.loading_text)
        self.loading_.place(relx=.35,rely=.88)
        self.Animate_loading()
        allowed_filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ppm;*.pgm;*.pbm;*.pnm;*.tiff;*.webp"), ]
        try:
            path=filedialog.askopenfile(filetypes=allowed_filetypes,title="Select the Image").name
            self.error_made_stop= True
            self.pg2_caller_function(path)
        except  AttributeError:
            self.error_made_stop= True
        
    def Animate_loading(self):
        if not self.error_made_stop:
            if self.total_animation_call <=4:
                self.loading_text.set(f"Selection of Image in process{self.dot}")
                self.dot+="."
                self.total_animation_call+=1
            else:
                self.dot="."
                self.total_animation_call=0  
            self.window.after(400,self.Animate_loading)   
        else:
            self.loading_.destroy()     

class CanvasImageOutput(Canvas):
    def __init__(self,window,resizing_image_function):
        super().__init__(window,background=BackGround_color,borderwidth=0,highlightthickness=0)
        self.grid(row=0,column=0,sticky="snew",padx=10,pady=10)
        self.bind("<Configure>",resizing_image_function)

class Resolution_AND_zoom_bar(ctk.CTkFrame):
    def __init__(self, Window):
        super().__init__(Window, fg_color="#3C3E4D")

        self.window= Window
        self.zoom_scale=100
        self.place(relx=.49, rely=1, relheight=.049, relwidth=.25, anchor="sw")

        # resolution box
        self.resolution_box=ctk.CTkLabel(self,corner_radius=0, text=f"{self.window.orginal_image.width}px X {self.window.orginal_image.height}px",
                                         fg_color="#61677A")
        self.resolution_box.place(relx=0,rely=0,relheight=1,relwidth=.38)


        #reset box
        self.reset_zoom_button= ctk.CTkButton(self,text="⮌",
                                              fg_color="#494b5c",hover_color="red",
                                              corner_radius=0,command=self.window.resizing_image)
        self.reset_zoom_button.place(relx=.395,rely=0.1,relheight=.8,relwidth=.075)
        ToolTip(self.reset_zoom_button,"Reset the zoomed image")

        # zoom box
        self.zoom_frame_box = ctk.CTkFrame(self, fg_color="#61677C")
        self.zoom_frame_box.place(relx=0.48,rely=0,relheight=1,relwidth=.6)

        self.minus_btn= ctk.CTkButton(self.zoom_frame_box, text="➖",
                                      fg_color="transparent",hover_color="#4C4C6D",
                                      command=lambda :self.change_IMAGE_BORDER_MARGIN("sub"))
        self.minus_btn.place(relx=0,rely=0,relheight=1,relwidth=.25)
        # ToolTip(self.minus_btn,"Zoom out, can use mousewheel too")

        self.zoomed_percentage= ctk.CTkLabel(self.zoom_frame_box,text="100%")
        self.zoomed_percentage.place(relx=.27,rely=0,relheight=1,relwidth=.35)

        self.plus_btn= ctk.CTkButton(self.zoom_frame_box, text="➕",
                                     fg_color="transparent",hover_color="#4C4C6D",
                                     command=lambda:self.change_IMAGE_BORDER_MARGIN("add"))
        self.plus_btn.place(relx=.6,rely=0,relheight=1,relwidth=.3)
        ToolTip(self.plus_btn,"Zoom In, can use mousewheel too")

        for childs in self.zoom_frame_box.winfo_children():
            childs.bind("<MouseWheel>", lambda event:self.change_IMAGE_BORDER_MARGIN(event.delta))

    def update_resolution(self,*args):

        try:
            Width=int(self.resolution_box_width.get()[:-2])
            Height=int(self.resolution_box_height.get()[:-2])
            self.window.image.resize(Width,Height)

        except:
            self.window.width_,self.window.height_=self.window.image.size
            pass  

    def change_resolution_bar_value(self):

        self.resolution_box.configure(text=f"{self.window.orginal_image.width}px X {self.window.orginal_image.height}px")
        
        try:
            previous_size= self.window.resized_image_.size
            present_size= (self.window.width_,self.window.height_)
        except:
            previous_size=self.window.image.size
            present_size= (self.window.width_,self.window.height_)
        self.zoom_scale=self.zoom_scale- round(((previous_size[0]-present_size[0])/previous_size[0])*100)
        if self.zoom_scale>250:
            self.zoom_scale=250
        self.zoomed_percentage.configure(text=f"{self.zoom_scale}%")

    def change_IMAGE_BORDER_MARGIN(self, value):
        # it zooms and zoomout accordingly
        zoom_factor=1
        try:
            if value == "add"and self.zoom_scale <250:
                zoom_factor = 1.01 
            elif value == "sub"and self.zoom_scale >35:
                zoom_factor = 0.99    
            elif value >0 and self.zoom_scale <=240:
                zoom_factor = 1.1          
            elif value<0 and self.zoom_scale >=45:
                zoom_factor = 0.9
        except   TypeError:
            pass      

        # disablind and enabling between value 35 to 250
        if self.zoom_scale==250:
            self.plus_btn.configure(state="disabled")
        elif self.zoom_scale<250:
            self.plus_btn.configure(state="normal")
        if self.zoom_scale==35:
            self.minus_btn.configure(state="disabled")
        elif self.zoom_scale>35:
            self.minus_btn.configure(state="normal")

        self.window.width_= int(self.window.width_ * zoom_factor)
        self.window.height_ = int(self.window.height_ * zoom_factor)
        self.window.place_image_in_canvas()


if __name__=="__main__":
    Window()
