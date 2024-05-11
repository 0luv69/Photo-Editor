from pannel import *

class Menu(ctk.CTkTabview):
    def __init__(self,window,pos_var,color_var,effect_var,Draw_vars):
        super().__init__(window)
        self.grid(row=0,column=1,sticky="nsew")
        
        #tabs
        self.add("Position")
        self.add("Color")
        self.add("Effect")
        self.add("Draw")
        self.add("Export")

        #widgets
        PositionFrame(self.tab("Position"),pos_var,window)
        ColorFrame(self.tab("Color"),color_var)
        EffectFrame(self.tab("Effect"),effect_var,window)
        DrawFrame(self.tab("Draw"),Draw_vars,window)
        ExportFrame(self.tab("Export"),window)

class PositionFrame(ctk.CTkFrame):
    def __init__(self,parent,pos_var,window):
        super().__init__(parent,fg_color=BackGround_color)
        self.pack(expand=True,fill="both")
        self.window=window
        Flip_Rotation(self,pos_var['flipX'],pos_var['flipY'],"Straighten",pos_var['straighten'],-45,45,5)
        position_x_y(self,"Position:",pos_var['x'],pos_var['y'],pos_var['x_'],pos_var['y_'],window,)
        crop_pannel(self,pos_var["crop"])
        Reverse_Btn(self,
                    (pos_var['straighten'],ROTATE_DEFAULT),                    
                    (pos_var['x'],x_Default),
                    (pos_var['y'],y_Default),)
            
class ColorFrame(ctk.CTkFrame):
    def __init__(self,parent,color_var):
        super().__init__(parent,fg_color=BackGround_color)
        self.pack(expand=True,fill="both")
        Switch_pannel(self,(color_var["grayscale"],"B/W"),(color_var["invert"],"Invert"))
        slider_Pannel(self,"Brightness",color_var["brightness"],0.15,10,.1)
        slider_Pannel(self,'Saturation',color_var["saturation"],0,5,.1)
        slider_Pannel(self,"Contrast",color_var["contrast"],0,10,.4)
        Reverse_Btn(self,
                    (color_var["grayscale"],GRAYSCALE_DEFAULT),
                    (color_var["invert"],INVERT_DEFAULT),
                    (color_var["saturation"],SATURATION_DEFAULT),
                    (color_var["brightness"],BRIGHTNESS_DEFAULT),
                    (color_var["contrast"],CONTRAST_DEFAULT))

class EffectFrame(ctk.CTkFrame):
    def __init__(self,parent,effect_var,window):
        super().__init__(parent,fg_color=BackGround_color)
        self.pack(expand=True,fill="both")
        DropDownPannel(self,effect_var["effect"],EFFECT_OPTIONS)
        slider_Pannel(self,"Blur",effect_var["blur"],0,30,.6)
        RemoveBackGround(self,window)
        Adjust_hue(self,window)

        Reverse_Btn(self,
                    (effect_var["effect"],EFFECT_OPTIONS[0]),
                    (effect_var["blur"],BLUR_DEFAULT),
                    )

class DrawFrame(ctk.CTkFrame):
    def __init__(self,parent,Draw_var,window):
        super().__init__(parent,fg_color=BackGround_color)
        self.pack(expand=True,fill="both")

        Paint(self,
              Draw_var['drawORdont'],
              Draw_var['ballcolor'],
              Draw_var['ballSize'],
              window)

class ExportFrame(ctk.CTkFrame):
    def __init__(self,parent,window):
        super().__init__(parent,fg_color=BackGround_color)
        self.pack(expand=True,fill="both") 

        self.window= window
        self.window.bind("<Control-s>",self.save)

        ctk.CTkButton(self,text="save",command=self.save).pack(pady=40,padx=40)

    def save(self,*args):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])         
            if file_path:
                self.window.image.save(file_path)
                ErrorPannel(self.window,f"Saved {file_path}","green")
            else:
                ErrorPannel(self.window,'Sorry, You have not \nentered the Path to save')    




