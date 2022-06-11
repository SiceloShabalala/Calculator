import tkinter as tk
from unicodedata import digit

# COLORS
LIGHT_GREY = "#F5F5F5"
LABEL_COLOR = "#25265E"
LIGHT_BLUE = "#CCEDFF"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"

#FONTS
SMALL_FONT_STYLE = ("Arial",16)
LARGE_FONT_STYLE = ("Arial",40,"bold")
DIGITS_FONT_STYLE = ("Arial",24,"bold")
DEFAULT_FONT_STYLE = ("Arial",20)

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('375x667')
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.displayFrame = self.createDisplayFrame()
        self.buttonsFrame = self.createButtonsFrame()

        self.totalExpression = ""
        self.currentExpression = ""

        self.totalLabel , self.label = self.createDisplayLabels()

        self.digits = {
            7:(1,1),8:(1,2),9:(1,3),
            4:(2,1),5:(2,2),6:(2,3),
            1:(3,1),2:(3,2),3:(3,3),
            0:(4,1),'.':(4,2)  
        }

        self.buttonsFrame.rowconfigure(0, weight=1)

        for i in range(1, 5):
            self.buttonsFrame.rowconfigure(i, weight=1)
            self.buttonsFrame.columnconfigure(i, weight=1)
 
        self.createDigitButtons()

        self.operations = {"/" : "\u00F7", "*" : "\u00D7", "-" : "-", "+" : "+"}

        self.createOperatorButtons()

        self.createSpecialButtons()

        self.bindKeys()
    
    def createDisplayFrame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GREY)
        frame.pack(expand=True, fill="both")
        return frame

    def createButtonsFrame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def createDisplayLabels(self):
        totalLabel = tk.Label(self.displayFrame, text=self.totalExpression,anchor=tk.E, bg=LIGHT_GREY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        totalLabel.pack(expand=True, fill="both")

        label = tk.Label(self.displayFrame, text=self.currentExpression, anchor=tk.E, bg=LIGHT_GREY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        
        return totalLabel, label

    def createDigitButtons(self):
        for digit,gridValue in self.digits.items():
            button = tk.Button(self.buttonsFrame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.addToExpression(x))
            button.grid(row=gridValue[0], column=gridValue[1], sticky=tk.NSEW)

    def createOperatorButtons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttonsFrame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.appendOperator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def createClearButton(self):
        button = tk.Button(self.buttonsFrame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def createEqualsButton(self):
        button = tk.Button(self.buttonsFrame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3,columnspan=2, sticky=tk.NSEW)
    
    def createSpecialButtons(self):
        self.createClearButton()
        self.createEqualsButton()
        self.createSquareButton()
        self.createSquareRootButton()
  
    def updateTotalLabel(self):
        expression = self.totalExpression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.totalLabel.config(text=expression)

    def updateLabel(self):
        self.label.config(text=self.currentExpression[:11])

    def addToExpression(self, value):
        self.currentExpression += str(value)
        self.updateLabel()

    def appendOperator(self, operator):
        self.currentExpression += operator
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.updateTotalLabel()
        self.updateLabel()

    def clear(self):
        self.currentExpression = ""
        self.totalExpression = ""
        self.updateLabel()
        self.updateTotalLabel()

    def evaluate(self):
        self.totalExpression += self.currentExpression
        self.updateTotalLabel()

        try:
            self.currentExpression = str(eval(self.totalExpression))
            self.totalExpression = ""

        except Exception as e:
            self.currentExpression = "Error"

        finally:
            self.updateLabel()

    def createSquareButton(self):
        button = tk.Button(self.buttonsFrame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**2"))
        self.updateLabel()

    def createSquareRootButton(self):
        button = tk.Button(self.buttonsFrame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.squareRoot)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def squareRoot(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**0.5"))
        self.updateLabel()

    def bindKeys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.addToExpression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.appendOperator(operator))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()