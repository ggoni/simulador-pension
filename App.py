import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import numpy as np


RENTA_TOPE=80.2 # Revisar con frecuencia semestral

#Pide ingresar los datos

st.sidebar.markdown("## Ingresa tus parámetros")

uf=st.sidebar.number_input("Ingrese Valor de la UF actual, en $",min_value=28667,max_value=40000)


r_anual=st.sidebar.slider("Ingrese la rentabilidad ANUAL de sus fondos, en %", min_value=3.0,max_value=7.0,step=0.25,value=5.0)
r_anual/=100
saldo_actual=st.sidebar.number_input("Ingrese su saldo actual, en $",min_value=1)
sueldo_actual=st.sidebar.number_input("Ingrese su sueldo bruto actual, en $",min_value=320500)
edad_actual=st.sidebar.number_input("Ingrese su edad actual",min_value=18,max_value=65)
esperanza_vida=st.sidebar.slider("Ingrese la esperanza de vida en años", min_value=70,max_value=120,step=1,value=80)

#Cálculos derivados
r_mensual=(1+r_anual)**(1/12)-1
aporte_mensual=0.1*min(RENTA_TOPE*uf,sueldo_actual)
annos_restantes_cotizando=65-edad_actual
annos_pensionado=esperanza_vida-65



val_fut_65=np.fv(rate=r_mensual,nper=12*annos_restantes_cotizando,pv=-saldo_actual,pmt=-aporte_mensual)
r_fondos_pensionado_anual=0.05
r_fondos_pensionado_mensual=(1+r_fondos_pensionado_anual)**(1/12)-1

pension=-np.pmt(r_fondos_pensionado_mensual,12*annos_pensionado,val_fut_65)

meses_pensionado=12*annos_pensionado



rentabilidades=[0 for mes in range(meses_pensionado)]
giros=[pension for mes in range(meses_pensionado)]
saldos=[0 for mes in range(meses_pensionado)]




data={'Rentabilidad':[0],'Giro':[0],'Saldo':[val_fut_65]}


df=pd.DataFrame(data=data)
new_values_df=pd.DataFrame(zip(rentabilidades,giros,saldos),columns=['Rentabilidad','Giro','Saldo'])
df=pd.concat([df,new_values_df],axis=0,ignore_index=True)

@st.cache
def llena_df(df):
        for i,row in df.iterrows():
                df.loc[i + 1,'Rentabilidad']=df.loc[i,'Saldo']*r_fondos_pensionado_mensual
                df.loc[i + 1,'Saldo'] = df.loc[i, 'Saldo'] +df.loc[i + 1,'Rentabilidad']-df.loc[i + 1,'Giro']
        return df[:-1]

df=llena_df(df)


monto_pension= f"{int(pension):,}".replace(",",".")

st.markdown("## Debiera pensionarse con un fondo ahorrado de $"+str(int(round(val_fut_65/1e6,0)))+" Millones")
st.markdown("## Su pensión mensual se estimma en  $"+ monto_pension+", dada una esperanza de vida de" + esperanza_vida+ " años")
st.markdown("## ")
st.markdown("## ")

import plotly.graph_objects as go

st.markdown("### Evolución del saldo restante según edad")
fig = go.Figure(data=go.Scatter(
        y = df.Saldo,
        x=65+df.index/12,
        mode='markers',
            marker=dict(
                size=10,
                color='red'
            )
        ))
st.write(fig)


