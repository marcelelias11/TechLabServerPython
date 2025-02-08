from sympy.plotting import plot
from sympy import symbols, diff, lambdify
import sympy as sp
import numpy as np
import statistics as stat
import math
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class StatCalc: #Classe que armazena a calculadora estatística
    __statdictlist:list = [] #Lista de armazenamento de dicionários de dados estatísticos
    __calcdict:dict = { #Dicionário que armazena os dados da calculadora estatística
        "avg": 0,
        "std": 0,
        "una": 0,
        "unb": 0,
        "unc": 0,
    }
    def __init__(self, eq:str, incertezab:list,value:list, lowbound:float, upbound:float,value2:list): #Construtor da classe
        self.value = value
        self.value2 = value2
        self.eq = eq
        self.unb = incertezab
        self.lb = lowbound
        self.ub = upbound
        pass

    def __calc(self): #Função que faz o cálculo estatístico, recebe uma lista de dados experimentais e incerteza instrumental
        for i in range(len(self.value)):
            self.__calcdict["avg"] = stat.mean(self.value[i]) #Média
            self.__calcdict["std"] = stat.stdev(self.value[i]) #Desvio Padrão
            self.__calcdict["una"] = self.__calcdict["std"]/math.sqrt(len(self.value[i])) #Incerteza experimental, dada pelo desvio padrão divido pela raíz quadrada do número de valores
            self.__calcdict["unb"] = self.unb[i] #Incerteza instrumental
            self.__calcdict["unc"] = math.sqrt((self.__calcdict["una"]**2)+(self.__calcdict["unb"])**2) #Incerteza combinada, dada pela soma pitagórica das incertezas anteriores
            statdict:dict = dict(avg = self.__calcdict["avg"], std = self.__calcdict["std"], una = self.__calcdict["una"], unb = self.__calcdict["unb"], unc = self.__calcdict["unc"], unz = 0) #Dicionário que armazena os dados
            self.__statdictlist.append(statdict) #Adiciona o dicionário de dados estatísticos na lista
        return(self.__statdictlist)

    def __clean(self): #Limpa a lista após uso
        self.__statdictlist = []

    def __propag(self): #Propagação da incerteza na equação, recebe uma equação em string e um dicionário das variáveis e seus valores
        self.__calc()
        f = sp.sympify(self.eq) #Função convertida por um formato legível pelo sympy
        y = sp.sympify("z - z") #Função que irá armaznar a equação da soma das derivadas parciais
        index = 0 #Variável que irá armezenar o índice pra percorrer a lista de dicionário de dados
        subslist = []
        for i in f.atoms(sp.Symbol): #Loop que irá dinamicamente calcular a soma pitagórica (exceto pela raíz) da incerteza
            diffeq = sp.diff(f, sp.sympify(i)) #Derivada parcial da equação em função da variável do dicionário
            y += sp.sympify(f"({diffeq}*{self.__statdictlist[index]["unc"]})**2") #Monta a equação a ser resolvida
            subslist.append((sp.sympify(i), self.__statdictlist[index]["avg"]))
            #resultlist[index] = resultlist[index]**2
            index += 1 #Incrementa o índice
        for i in self.__statdictlist: #Adiciona a incerteza propagada na lista de dicionários
            i["unz"] = math.sqrt(y.subs(subslist)) #Passo final da propagação da incerteza: tirar a raíz quadrada da soma
        dictsend:dict = self.__statdictlist # Armazena o dicionário numa variável, para o mesmo não ser apagado
        self.__clean()
        return(dictsend)
    def __regression(self):
        #TODO
        dummyvar = 0
    def __statgraph(self, y_min_target=-20, y_max_target=20): 
        f = sp.sympify(self.eq)  # Parse the equation into a SymPy function

        # Ensure the function has exactly one independent variable
        if len(f.free_symbols) != 1:
            raise ValueError("The function must have exactly one independent variable to be plotted.")

        # Identify the variable (e.g., 'x') and create a numerical function
        variable = list(f.free_symbols)[0]
        f_numeric = sp.lambdify(variable, f, "numpy")

        # Generate x-values for the line plot
        x_line = np.linspace(self.lb, self.ub, 500)  # 500 points between bounds
        y_line = f_numeric(x_line)  # Evaluate the function at these x-values

        # Calculate the current y-range of the function
        y_min, y_max = min(y_line), max(y_line)

        # Check if scaling is necessary
        if y_max == y_min:
            raise ValueError("The function's output is constant and cannot be scaled.")

        # Rescale the function to fit within (y_min_target, y_max_target)
        target_range = y_max_target - y_min_target
        current_range = y_max - y_min
        scale_factor = target_range / current_range
        offset = y_min_target - scale_factor * y_min

        # Define the rescaled function
        f_rescaled = scale_factor * f + offset
        f_rescaled_numeric = sp.lambdify(variable, f_rescaled, "numpy")
        y_rescaled = f_rescaled_numeric(x_line)

        # Scatter plot data
        x_scatter = self.value[0]  # Assuming `self.value` is a list of x-values
        y_scatter = self.value2

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.scatter(x_scatter, y_scatter, label="Data Points", color="blue", alpha=0.6)
        plt.plot(x_line, y_rescaled, label="Rescaled Function", color="red", linewidth=2)

        # Set y-axis limits to the target interval
        plt.ylim(y_min_target, y_max_target)

        # Add labels, legend, and title
        plt.title("Rescaled Function and Data Scatter Plot")
        plt.xlabel(str(variable))
        plt.ylabel("f(" + str(variable) + ")")
        plt.legend()
        plt.grid(True)

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

        return plot_base64


    def send(self):
        return ({"stats": self.__propag(), "graph": self.__statgraph()})