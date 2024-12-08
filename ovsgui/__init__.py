from customtkinter import *
import hashlib
from firebase_admin import db
import datetime, string, random, socket
from ovsystem import OVS
from tkinter import messagebox

set_appearance_mode("system")

class OnlineVariableSystemGUI(CTk):
    def __init__(self):
        super().__init__()
        self.title("OVS - Online Variables System")
        self.geometry("1300x750")
        self.minsize(1300, 750)

        # Token Giriş Alanı
        self.tokenArea = CTkFrame(self, corner_radius=0)
        self.tokenArea.pack(fill=X, side=TOP)

        self.tokenText = CTkEntry(self.tokenArea, corner_radius=7.5, font=("Consolas", 18), border_width=1, height=40, justify="center", placeholder_text="TOKEN")
        self.tokenText.pack(fill=X, side=LEFT, expand=True, padx=(10+10, 5+5), pady=10+10)
        self.tokenText.bind("<Return>", lambda event: (self.getVariables() if self.tokenText.get() != "" else ...))

        self.bind("<F5>", lambda event: (self.getVariables() if self.tokenText.get() != "" else ...))

        self.listVariables = CTkButton(self.tokenArea, corner_radius=7.5, border_width=0, text="List", font=("Sans Serif", 15), height=40, command=self.getVariables)
        self.listVariables.pack(fill=X, side=RIGHT, padx=(5+5, 10+10), pady=10+10)

        # Ana İçerik Alanı
        self.mainArea = CTkFrame(self, corner_radius=0, bg_color=self.cget("bg"), fg_color=self.cget("bg"))
        self.mainArea.pack(fill=BOTH, expand=True, side=TOP, padx=20, pady=20)

        # Sol Taraftaki Listeleme Alanı
        self.variablesList = CTkFrame(self.mainArea, corner_radius=10, border_width=1)
        self.variablesList.pack(fill=BOTH, expand=True, side=LEFT, padx=(0, 0))

        self.listedVariables = CTkScrollableFrame(self.variablesList, corner_radius=7.5, border_width=1, height=75)
        self.listedVariables.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Sağ Taraftaki Seçim Alanı
        self.selectedVariables = CTkFrame(self.mainArea, corner_radius=10, border_width=1, width=475)
        self.selectedVariables.pack(fill=BOTH, side=RIGHT, padx=(20, 0))
        self.selectedVariables.pack_forget()

        self.selectedVariableHead = CTkLabel(self.selectedVariables, text="Variable Name", font=("Sans Serif", 35, "bold"), text_color="white")
        self.selectedVariableHead.place(x=30, y=30)

        self.selectedVariableValueHead = CTkLabel(self.selectedVariables, text="Variable Value: ", font=("Sans Serif", 20, "bold"), text_color="white")
        self.selectedVariableValueHead.place(x=30, y=100+10)

        self.selectedVariableValue = CTkLabel(self.selectedVariables, text="!!itsavalue!!", font=("Consolas", 20), text_color="#999")
        self.selectedVariableValue.place(x=30, y=130+10)

        self.selectedVariableCreatorIPHead = CTkLabel(self.selectedVariables, text="Creator IP", font=("Sans Serif", 20, "bold"), text_color="white")
        self.selectedVariableCreatorIPHead.place(x=30, y=180+10)

        self.selectedVariableCreatorIP = CTkLabel(self.selectedVariables, text="0.0.0.0", font=("Consolas", 20), text_color="#999")
        self.selectedVariableCreatorIP.place(x=30, y=210+10)

        self.selectedVariableCreatorHead = CTkLabel(self.selectedVariables, text="Creator Name", font=("Sans Serif", 20, "bold"), text_color="white")
        self.selectedVariableCreatorHead.place(x=30, y=260+10)

        self.selectedVariableCreator = CTkLabel(self.selectedVariables, text="!!itsacreatorname!!", font=("Consolas", 20), text_color="#999")
        self.selectedVariableCreator.place(x=30, y=290+10)

        self.selectedVariableCreationTimeHead = CTkLabel(self.selectedVariables, text="Creation Time", font=("Sans Serif", 20, "bold"), text_color="white")
        self.selectedVariableCreationTimeHead.place(x=30, y=340+10)

        self.selectedVariableCreationTime = CTkLabel(self.selectedVariables, text="00.00", font=("Consolas", 20), text_color="#999")
        self.selectedVariableCreationTime.place(x=30, y=370+10)

        self.selectedVariableCreationDateHead = CTkLabel(self.selectedVariables, text="Creation Date", font=("Sans Serif", 20, "bold"), text_color="white")
        self.selectedVariableCreationDateHead.place(x=30, y=420+10)

        self.selectedVariableCreationDate = CTkLabel(self.selectedVariables, text="01/01/2024", font=("Consolas", 20), text_color="#999")
        self.selectedVariableCreationDate.place(x=30, y=450+10)

        self.selectedVariableCloseBtn = CTkButton(self.selectedVariables, corner_radius=7.5, text="X", font=("Sans Serif", 18, "bold"), text_color="#999", width=40, height=40, fg_color=self.selectedVariables.cget("fg_color"), hover_color=f"gray22", command=self.closeSelectedVariable)
        self.selectedVariableCloseBtn.place(x=425, y=10)

        self.selectedVariableDeleteBtn = CTkButton(self.selectedVariables, corner_radius=7.5, width=445, text="Delete This Variable", font=("Consolas", 18), text_color="#e36d6d", border_color="#e36d6d", hover_color="#383838", border_width=1, fg_color="#333", command=self.delVar)
        self.selectedVariableDeleteBtn.pack(side=BOTTOM, padx=15, pady=15) 

        # Konfigürasyon Alanı
        self.configArea = CTkFrame(self, corner_radius=10, height=60, border_width=1)
        self.configArea.pack(fill=X, side=BOTTOM, pady=(0, 20), padx=20)

        self.generateToken_ = CTkButton(self.configArea, corner_radius=6.25, text="Generate Token", border_width=1, border_color="#555", text_color="white", fg_color="#333", hover_color="#383838", width=150, command=self.generateToken)
        self.generateToken_.pack(side=LEFT, padx=(10, 5), pady=10)

        self.delToken = CTkButton(self.configArea, corner_radius=6.25, text="Del", border_width=1, border_color="#e36d6d", text_color="#e36d6d", fg_color="#333", hover_color="#383838", width=100, command=self.delToken_)
        self.delToken.pack(side=RIGHT, padx=10, pady=10)

    def closeSelectedVariable(self): self.selectedVariables.pack_forget()
    def clearScreen(self):
        self.listedVariables.pack_forget()
        self.listedVariables.destroy()
        self.listedVariables = CTkScrollableFrame(self.variablesList, corner_radius=7.5, border_width=1, height=75)
        self.listedVariables.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.tokenText.delete(0 , END)
    def selectVariable(self, selectedVariableName, selectedVariableValue, selectedVariableCreatorIP, selectedVariableCreatorName, selectedVariableCreationTime, selectedVariableCreationDate):
        
        self.selectedVariables.pack(fill=BOTH, expand=False, side=RIGHT, padx=(20, 0))

        self.selectedVariables.configure(width=475)

        if len(selectedVariableName) > 20: selectedVariableName = selectedVariableName[:17] + "..."
        if len(selectedVariableValue) > 35: selectedVariableValue = selectedVariableValue[:32]+ "..."

        self.selectedVariableValue.configure(text=f"{selectedVariableValue}")
        self.selectedVariableHead.configure(text=f"{selectedVariableName}")
        self.selectedVariableCreator.configure(text=f"{selectedVariableCreatorName}")
        self.selectedVariableCreatorIP.configure(text=f"{selectedVariableCreatorIP}")
        self.selectedVariableCreationTime.configure(text=f"{selectedVariableCreationTime}")
        self.selectedVariableCreationDate.configure(text=f"{selectedVariableCreationDate}")

    def delVar(self):
        try:
            shori = messagebox.askyesno("Are you sure?", "Are you sure you want to delete this variable?")
            if shori:
                deleta = self.ovs.delVar(self._value_)
                print(self._value_)
                if deleta:
                    messagebox.showinfo("Success", "Variable deleted successfully.")
                    self.closeSelectedVariable()
                    self.getVariables()
                else:
                    messagebox.showerror("Error", "Failed to delete variable.")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delToken_(self):
        try:
            shori = messagebox.askyesno("Are you sure?", "Are you sure you want to delete this token?")
            if shori:
                delet = self.ovs.delToken()
                if delet:
                    messagebox.showinfo("Success", "Token deleted successfully.")
                    self.closeSelectedVariable()
                    self.clearScreen()
                else:
                    messagebox.showerror("Error", "Failed to delete token.")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def getVariables(self):
        try:
            self.focus()
            self.closeSelectedVariable()
            self.listedVariables.pack_forget()
            self.listedVariables.destroy()
            self.listedVariables = CTkScrollableFrame(self.variablesList, corner_radius=7.5, border_width=1, height=75)
            self.listedVariables.pack(fill=BOTH, expand=True, padx=20, pady=20)
            try:
                self.ovs = OVS(self.tokenText.get())
            except Exception as e: ...
            variables = self.ovs.getAll()
            for key, value in variables.items():
                creator, creatorIP, creationDate, creationTime, value_ = value["creator"], value["creatorIP"], value["creationDate"], value["creationTime"], value["value"]
                self._value_ = key
                if len(key) > 30: key = key[:27]
                if key.endswith(" "): key = key[:26] + "..."
                if len(value_) > 30: value_ = value_[:27] + "..."
                self.variableFrame = CTkFrame(self.listedVariables, corner_radius=6.25, border_width=1, height=40)
                self.variableFrame.pack(fill=X, side=BOTTOM, padx=10, pady=(10, 10))

                self.variableKeyLabel = CTkLabel(self.variableFrame, text=f"{key} : ", font=("Sans Serif", 18,"bold"))
                self.variableKeyLabel.pack(expand=False, side=LEFT, padx=(20, 2), pady=10)

                self.variableValueLabel = CTkLabel(self.variableFrame, text=value_, text_color="#999", font=("Consolas", 18))
                self.variableValueLabel.pack(expand=False, side=LEFT, padx=(2, 10), pady=10)

                self.variableOpen = CTkButton(self.variableFrame, text=">", font=("Sans Serif", 20, "bold"), width=40, fg_color=self.variableFrame.cget("fg_color"), hover_color="gray22", command=lambda _key=key, _creator=creator, _creatorIP=creatorIP, _creationDate=creationDate, _creationTime=creationTime, _value_=value_: self.selectVariable(
                    _key, _value_, _creatorIP, _creator, _creationTime, _creationDate
                ))
                self.variableOpen.pack(expand=False, side=RIGHT, padx=(10, 10), pady=10)
        except Exception as e: print(e)

    def generateToken(self):
        token = ''.join(random.choices(string.digits, k=30))
        con = OVS(token)
        con._generate_token()
        self.tokenText.delete(0, END)
        self.tokenText.insert(END, token)
        self.getVariables()
        self.closeSelectedVariable()

    def convertTo32Bit(self, data):
        md5_hash = hashlib.md5(data.encode()).hexdigest()
        return int(md5_hash[:16], 16)

def main():
    root = OnlineVariableSystemGUI()
    root.mainloop()

if __name__ == "__main__":
    main()