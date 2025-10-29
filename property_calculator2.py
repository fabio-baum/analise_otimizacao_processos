import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math

# Use the COMPONENTS dictionary from previous script

COMPONENTS = {
            # n-alkanes
            "n-heptane":        {"A":6.893,"B":1264.9,"C":216.7,"Tb":98.4,"Tf":-91.0,"Hf":8.5,"LFL":1.05},
            "n-octane":         {"A":6.946,"B":1344.8,"C":216.4,"Tb":125.6,"Tf":-57.0,"Hf":9.0,"LFL":1.00},
            "n-nonane":         {"A":6.998,"B":1410.0,"C":216.0,"Tb":150.8,"Tf":-53.0,"Hf":9.5,"LFL":0.80},
            "n-decane":         {"A":7.033,"B":1470.0,"C":216.0,"Tb":174.0,"Tf":-30.0,"Hf":10.0,"LFL":0.80},
            "n-undecane":       {"A":7.070,"B":1520.0,"C":216.0,"Tb":196.0,"Tf":-26.0,"Hf":10.5,"LFL":0.70},
            "n-dodecane":       {"A":6.878,"B":1741.7,"C":222.65,"Tb":216.3,"Tf":-9.6,"Hf":12.5,"LFL":0.60},
            "n-tetradecane":    {"A":7.2,"B":1920.0,"C":220.0,"Tb":253.0,"Tf":5.0,"Hf":13.0,"LFL":0.50},
            "n-pentadecane":    {"A":7.25,"B":2000.0,"C":220.0,"Tb":270.0,"Tf":8.0,"Hf":13.5,"LFL":0.55},
            "n-hexadecane":     {"A":7.3,"B":2100.0,"C":220.0,"Tb":287.0,"Tf":18.0,"Hf":14.0,"LFL":0.50},
            "n-octadecane":     {"A":7.4,"B":2300.0,"C":220.0,"Tb":315.0,"Tf":28.0,"Hf":14.5,"LFL":0.40},

            # iso-alkanes (≈ +10% higher LFL)
            "iso-dodecane":     {"A":6.88,"B":1620.0,"C":215.0,"Tb":205.0,"Tf":-12.0,"Hf":11.8,"LFL":0.66},
            "iso-hexadecane":   {"A":6.97,"B":2020.0,"C":225.0,"Tb":270.0,"Tf":10.0,"Hf":13.5,"LFL":0.55},
            "iso-octadecane":   {"A":7.4,"B":2300.0,"C":220.0,"Tb":315.0,"Tf":28.0,"Hf":14.5,"LFL":0.44},

            # multi-branched iso-alkanes (≈ +20% higher LFL)
            "multibranch-iso-dodecane":   {"A":6.88,"B":1620.0,"C":215.0,"Tb":205.0,"Tf":-10.0,"Hf":11.8,"LFL":0.72},
            "multibranch-iso-hexadecane": {"A":6.97,"B":2020.0,"C":225.0,"Tb":270.0,"Tf":10.0,"Hf":13.5,"LFL":0.60},
            "multibranch-iso-octadecane": {"A":7.4,"B":2300.0,"C":220.0,"Tb":315.0,"Tf":28.0,"Hf":14.5,"LFL":0.48},

            # 1-alkenes (from PDF or close analogues)
            "1-octene":         {"A":6.95,"B":1350.0,"C":216.0,"Tb":121.0,"Tf":-100.0,"Hf":8.8,"LFL":1.00},
            "1-decene":         {"A":7.03,"B":1470.0,"C":216.0,"Tb":169.0,"Tf":-20.0,"Hf":10.0,"LFL":0.75},
            "1-dodecene":       {"A":6.88,"B":1741.7,"C":222.65,"Tb":216.3,"Tf":-15.0,"Hf":12.5,"LFL":0.60},
            "1-tetradecene":    {"A":7.2,"B":1920.0,"C":220.0,"Tb":253.0,"Tf":5.0,"Hf":13.0,"LFL":0.50},
            "1-hexadecene":     {"A":7.3,"B":2100.0,"C":220.0,"Tb":287.0,"Tf":18.0,"Hf":14.0,"LFL":0.45},

            # methyl-substituted alkanes (~ +15% LFL)
            "2-methyl-heptadecane":  {"A":7.35,"B":2150.0,"C":220.0,"Tb":295.0,"Tf":20.0,"Hf":14.0,"LFL":0.58},
            "2-methyl-pentadecane":  {"A":7.28,"B":2050.0,"C":220.0,"Tb":280.0,"Tf":15.0,"Hf":13.7,"LFL":0.63},
            "2-methyl-decane":       {"A":7.05,"B":1500.0,"C":216.0,"Tb":176.0,"Tf":-25.0,"Hf":10.2,"LFL":0.92},
            "2-methyl-undecane":     {"A":7.07,"B":1520.0,"C":216.0,"Tb":196.0,"Tf":-20.0,"Hf":10.5,"LFL":0.86},
            "2-methyl-tetradecane":  {"A":7.22,"B":1920.0,"C":220.0,"Tb":254.0,"Tf":5.0,"Hf":13.0,"LFL":0.65},
            "2-methyl-nonane":       {"A":6.99,"B":1400.0,"C":216.0,"Tb":151.0,"Tf":-50.0,"Hf":9.5,"LFL":0.96},
            "2,2,4-trimethyl-pentane":{"A":6.98,"B":1375.0,"C":216.0,"Tb":99.0,"Tf":-80.0,"Hf":9.0,"LFL":1.10},

            # ethanol (from PDF)
            "ethanol": {"A":8.20417,"B":1642.89,"C":230.3,"Tb":78.37,"Tf":-114.1,"Hf":5.02,"LFL":3.30},
        }

class MixtureCalculatorGUI:

    def __init__(self, root):
        root.title("Mixture Property Calculator")

        # ===== Scrollable Frame Setup =====
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Second frame inside the canvas
        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # ===== Now place all your widgets here =====
        tk.Label(scrollable_frame, text="Mixture Calculator", font=("Arial", 16)).pack(pady=10)
        
        # Create dictionaries to store the variables and entries
        self.component_vars = {}
        self.fraction_entries = {}
        
        # Create a frame for components
        components_frame = tk.Frame(scrollable_frame)
        components_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Header
        tk.Label(components_frame, text="Component", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 20))
        tk.Label(components_frame, text="Molar Fraction", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w")
        
        # Create checkboxes and entry fields for each component
        for i, comp in enumerate(COMPONENTS.keys(), 1):
            # Checkbox
            var = tk.BooleanVar()
            cb = tk.Checkbutton(components_frame, text=comp, variable=var)
            cb.grid(row=i, column=0, sticky="w", padx=(0, 20))
            self.component_vars[comp] = var
            
            # Entry field for molar fraction
            entry = tk.Entry(components_frame, width=10)
            entry.grid(row=i, column=1, sticky="w")
            entry.insert(0, "0.0")  # Default value
            self.fraction_entries[comp] = entry
            
            # Disable entry initially
            entry.config(state="disabled")
            
            # Bind checkbox to enable/disable entry
            cb.config(command=lambda c=comp, e=entry, v=var: self.toggle_component(c, e, v))

        # Add output text area
        tk.Label(scrollable_frame, text="Results:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        self.output_text = tk.Text(scrollable_frame, height=15, width=80)
        self.output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Calculate button
        tk.Button(scrollable_frame, text="Calculate", command=self.calculate, font=("Arial", 12)).pack(pady=10)

        # Keep a reference
        self.scrollable_frame = scrollable_frame

    def toggle_component(self, comp, entry, var):
        """Enable or disable the entry field based on checkbox state"""
        if var.get():
            entry.config(state="normal")
        else:
            entry.config(state="disabled")
            entry.delete(0, tk.END)
            entry.insert(0, "0.0")

    def calculate(self):
        mixture = {}
        for comp, var in self.component_vars.items():
            if var.get():
                try:
                    f = float(self.fraction_entries[comp].get())
                    if f < 0:
                        raise ValueError
                    mixture[comp] = f
                except:
                    messagebox.showerror("Input Error", f"Invalid fraction for {comp}")
                    return
        if not mixture:
            messagebox.showerror("Input Error", "No components selected")
            return
        total = sum(mixture.values())
        if abs(total - 1.0) > 1e-6:
            messagebox.showerror("Input Error", f"Molar fractions sum to {total:.4f}, must be 1.0")
            return
        
        # Call your previous functions here
        R = 8.31446261815324  # J/mol·K
        P_ATM_TO_MMHG = 760.0

        # ---------- Safe Antoine vapor pressure ----------
        def Psat_mmHg_safe(comp, T_C):
            A = COMPONENTS[comp]["A"]
            B = COMPONENTS[comp]["B"]
            C = COMPONENTS[comp]["C"]
            exponent = A - B/(T_C+C)
            exponent = max(min(exponent,50),-50)  # clamp exponent
            return 10**exponent

        def dPsat_dT_mmHg(comp,T_C):
            Ps=Psat_mmHg_safe(comp,T_C)
            B = COMPONENTS[comp]["B"]
            C = COMPONENTS[comp]["C"]
            return Ps * B / ((T_C + C)**2 * math.log(10))

        # ---------- Bubble point (bisection) ----------
        def bubble_point_bisection(x_dict,P_target_atm=1.0,T_min_C=-80.0,T_max_C=400.0,tol_mmHg=1e-3,maxiter=200):
            total=sum(x_dict.values())
            x={k:v/total for k,v in x_dict.items()}
            P_target=P_target_atm*P_ATM_TO_MMHG
            def f(T):
                return sum(x[c]*Psat_mmHg_safe(c,T) for c in x)-P_target
            a,b=T_min_C,T_max_C
            fa,fb=f(a),f(b)
            if fa*fb>0:  # fallback to weighted Tb
                Tb_guess=sum(x[c]*COMPONENTS[c]["Tb"] for c in x)
                return Tb_guess
            for _ in range(maxiter):
                m=0.5*(a+b)
                fm=f(m)
                if abs(fm)<tol_mmHg:
                    return m
                if fa*fm<=0:
                    b,fb=m,fm
                else:
                    a,fa=m,fm
            return 0.5*(a+b)

        # ---------- Schröder–van Laar melting ----------
        def liquidus_temperature_SvL(comp,x_i):
            if x_i<=0 or x_i>=1: return None
            data=COMPONENTS[comp]
            Tf_K=data["Tf"]+273.15
            DeltaH=1000.0*data["Hf"]
            invT=1/Tf_K - (math.log(x_i)*R/DeltaH)
            if invT<=0: return None
            return 1/invT - 273.15

        def melting_onset(z_dict):
            total=sum(z_dict.values())
            z={k:v/total for k,v in z_dict.items()}
            liqs={c:liquidus_temperature_SvL(c,x_i) for c,x_i in z.items()}
            valid=[t for t in liqs.values() if t is not None]
            return (max(valid) if valid else None), liqs

        # ---------- Flash point (Le Châtelier, bisection) ----------
        def lechatelier_sum_at_T(x_dict,T_C):
            total=sum(x_dict.values())
            x={k:v/total for k,v in x_dict.items()}
            p_i={c:x[c]*Psat_mmHg_safe(c,T_C) for c in x}
            P_total=sum(p_i.values())
            y={c:p_i[c]/P_total for c in x} if P_total>0 else {c:0.0 for c in x}
            sumL=0.0
            for c,yi in y.items():
                LFL=COMPONENTS[c].get("LFL",0.01)/100.0
                sumL+=yi/LFL
            return sumL,y

        def flash_point_bisection(x_dict,T_low_C=-80.0,T_high_C=None,tol=1e-3,maxiter=200):
            if T_high_C is None: T_high_C=bubble_point_bisection(x_dict)
            a,b=T_low_C,T_high_C
            sa,_=lechatelier_sum_at_T(x_dict,a)
            sb,_=lechatelier_sum_at_T(x_dict,b)
            if sa<1 and sb<1: return None,None,sa
            for _ in range(maxiter):
                m=0.5*(a+b)
                sm,y_m=lechatelier_sum_at_T(x_dict,m)
                if abs(sm-1)<tol: return m,y_m,sm
                if sm>1: a=m
                else: b=m
            return m,y_m,sm

        Tb = bubble_point_bisection(mixture)
        Tm,liq = melting_onset(mixture)
        Tf,yf,sumL = flash_point_bisection(mixture)

        self.output_text.delete(1.0,"end")
        self.output_text.insert("end", f"--- Results ---\n")
        self.output_text.insert("end", f"Estimated bubble-point (1 atm): {Tb:.2f} °C\n")
        self.output_text.insert("end", f"Estimated melting onset (first solid appears): {Tm:.2f} °C\n")
        self.output_text.insert("end", f"Per-component liquidus (SvL) estimates:\n")
        for c,t in liq.items():
            self.output_text.insert("end", f"  {c:20} : {t if t is not None else 'N/A':>7} °C\n")
        self.output_text.insert("end", f"Estimated flash point (Le Chatelier): {Tf if Tf is not None else 'N/A'} °C   (Le Chatelier sum = {sumL:.3f})\n")
        if Tf is not None:
            self.output_text.insert("end", f"Vapor composition at flash point (y_i):\n")
            for c,yi in yf.items():
                self.output_text.insert("end", f"  {c:20} : {yi:>7.4f}\n")


if __name__=="__main__":
    root = tk.Tk()
    gui = MixtureCalculatorGUI(root)
    root.mainloop()