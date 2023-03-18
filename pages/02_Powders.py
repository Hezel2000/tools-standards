import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.title("IfG Powder Standards Database")
###st.write('Data')
df_data = pd.read_csv('OxAndEl2.csv', sep=';')
LookUp = pd.read_csv('LookUpTable.csv', sep=';')
#error_bad_lines=False
### st.write(df_data) # zeigt alle Daten

std_names = df_data['Standard'].drop_duplicates()

LookUp.set_index("Element", inplace=True)
###st.write(LookUp) # zeigt Zusatzinformationen
#st.write(LookUp.loc[['Al'], ['Further information']])

tab1, tab2, tab3 = st.tabs(["Standard", "Element", "Owl"])

with tab1:
   standard = st.multiselect("Select one or more standards:", options = df_data["Standard"].unique()) #, default = df_data["Standard"].unique())
   if len(standard) > 0:
      st.write("Element concentrations for selected standard(s):")
      df_data_selection = df_data.query("Standard == @standard")
      ###df_data_selection
      #df_data_selection.index = df_data_selection['Standard']
      st.dataframe(df_data_selection.T)

      st.write('Information for the selected standard(s):')
      df_meta = pd.read_csv('Meta.csv', sep=';')
      df_meta.set_index("Standard", inplace = True)

      standardlist = []
      for i in standard:
         standardlist.append(i)

      metadata = df_meta.loc[standardlist]
      st.dataframe(metadata.T)

      ###TESTSTATION ###

      ### Cosmetics

      #df_meta
      #st.write('meta normal')

      def dfdark(styler):
       #styler.background_gradient(cmap='coolwarm')
       #styler.color('white')
       styler.set_table_styles([
           {
               "selector":"thead",
               "props":[("background-color","grey")]
           },
           {
               "selector":"tbody tr:nth-child(even)",
               "props":[("background-color","lightgrey")]
           },
           {
               "selector":"th.row_heading",
               "props":[("background-color","grey")]
           },
           {
               "selector":"td",
               "props":[("border","white")]
           },

       ])
       return styler
       #styler.format(color='grey')

   #df=pd.DataFrame(index=np.arange(10),columns=[1,2],data=np.random.normal(size=[10,2]))

      #df_meta.style.pipe(dfdark)
      #dfdark(df_meta)
      #st.write('meta neu')

      #df_meta.style.set_table_styles( [ {'selector': 'th', 'props': [('background-color', 'lightgray')] }, {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', EVEN_ROW_COLOR)] }])
    
with tab2:
   elements = df_data.columns[26:104]
   element = st.multiselect("Select one or more elements", options=list(elements)) #, default=list(df_data.columns[26:27]))
   if len(element) > 0:
      fil = df_data['Constituent'] == 'Concentration'
      df_data_conc_only = df_data[fil]

      ###furtherinfo = LookUp.loc[element]
      #st.write(furtherinfo) 
      #st.write(element)

      fullEllist = []

      for i in element:
         furtherinfo = LookUp.loc[i]
         fullEllist.append(i)
         for j in furtherinfo: #['Further information']  
            if isinstance(j, str):
               res = j.split('_')
               fullEllist.append(res)
            else:
               res = 'none'
      ### fullEllist

     ### flat nested list
      newlist = []
      for i in fullEllist:
         if type(i) is list:
            for j in i:
               newlist.append(j)
         else:
            newlist.append(i)
         #newlist.append(i)
      ### newlist

      dfselected = df_data[newlist]
      #st.write(dfselected)

      dfstd = df_data[['Standard','Constituent']]
      dfstandard = pd.DataFrame(dfstd)
      dfstandard.columns = ['Standard', 'Constituent']
      #dfstandard

      dfstandard = dfstandard.join(dfselected)
      dfstandard

      #zeilen = df_data[df_data['Constituent'] == 'Concentration'].index # Jede Zeile zeigen in der Concentration steht
      #for i in element:
        #auswahl = df_data.columns.get_loc(i)
        #d = df_data.iloc[zeilen, auswahl]
        #scale = st.radio('Choose a scale', ("linear scale", "log scale"))
        #if scale == "log scale":
            #fig2 = px.scatter(x=std_names, y=d, log_y=True,  title = i)
        #else:
            #fig2 = px.scatter(x=std_names, y=d, title = i)

        #fig2 = px.scatter(x=std_names, y=d, log_y=True,  title = i)
            #fig2.update_layout(xaxis_title="Standards", yaxis_title="Concentration in ppm")
            #st.plotly_chart(fig2)

      #zeilen = df_data[df_data['Constituent'] == 'Concentration'].index # Jede Zeile zeigen in der Concentration steht
      #for i in element:
        #auswahl = df_data.columns.get_loc(i)
        #d = df_data.iloc[zeilen, auswahl]
        #fig2 = px.scatter(x=std_names, y=d, log_y=True,  title = i)
        #fig2.update_layout(xaxis_title="Standards", yaxis_title="Concentration in ppm")
        #st.plotly_chart(fig2)


      zeilen = df_data[df_data['Constituent'] == 'Concentration'].index # Jede Zeile zeigen in der Concentration steht
      for i in element:
        auswahl = df_data.columns.get_loc(i)
        d = df_data.iloc[zeilen, auswahl]
        updatemenus = [dict(type="buttons",direction="right",buttons=list([dict(args=[{'yaxis.type': 'linear'}],label="Linear Scale",method="relayout"),
              dict(args=[{'yaxis.type': 'log'}],label="Log Scale", method="relayout" )  ]) ),]
        fig2 = px.scatter(x=std_names, y=d,  title = i)
        fig2.update_layout(updatemenus=updatemenus, xaxis_title="Standards", yaxis_title="Concentration in ppm")
        st.plotly_chart(fig2)
   
   
with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



#st.write(LookUp['Element'])
#Element(e) auswählen und Infos aus df_data anzeigen. In LookUp schauen: Wenn nicht N/A in LookUp für diese Element(e) die eingetragenen Werte als Spalten aus df_data anzeigen

#Anforderungen Befehl
# Ich möchte ein Element / mehrere Elemente auswählen und dann alle Einträge, die es zu meiner Auswahl gibt für alle Standards angezeigt bekommen.
# Es sollen also die Spalten Standard und zum Beispiel Al und Al2O3 meiner ursprünglichen Tabelle angezeigt werden
# Vorgang: Element auswählen -> in der Look Up Tabelle schauen ob es weitere Einträge gibt -> wenn ja auch diese anzeigen -> alle relevanten Spalten in einer Tabelle

# Vorbereitung Befehl
# df_data[fullEllist] # zeigt alle zusätzlichen Spalten zum ausgewählten Element
# df_data[element] # zeigt Spalten aller ausgewählten Elemente
# df_data['Standard'] # zeigt Spalte Standard
# Ende Befehl

# Anforderungen Befehl
# Soll die Konzentrationen für ausgewähltes Element von allen Standards in Plot zeigen
# auch für Oxide und weitere Bestandteile (z.B. Carbon Inorga)?
# wenn mehrere Element ausgewählt werden, sollen mehrere Plots erstellt werden
# x-Achse: Standards 
# y-Achse: Elementkonzentration von ausgewähltem Element
# Weiteres: Plots gut anordnen, Achsen beschriften, sinnvolle Werte/Größenordung

# Vorbereitung Befehl
#Test: st.write(zeilen)
#Auswahl = df_data.columns.get_loc('Al') # Spaltennummer von Element Al
#c = df_data.iloc[zeilen, Auswahl] # Zeilen mit Concentration und Spaltennummer des Elements
# Test: st.write(c)
#fig = px.scatter(x=std_names, y=c, log_y=True)
#st.plotly_chart(fig)
# Ende Befehl

#fil2 = df_data['Standard'] == standard
#df_data_std = df_data[fil2]
#st.write(standard + fullEllist)

#furtherinfo = LookUp.loc[[element], ['Further information']]
#st.write(df_data_conc_only[["Standard"] + element + furtherinfo])

#st.write(df_data_conc_only2[["Standard"] + element])

##Drag and drop Menü um Daten hinzuzufügen:
  #st.write('Add your own data:')
  #uploadedfile = st.file_uploader("Choose your file")
  #df2 = pd.read_excel(uploadedfile)

#def SelectData (name):
    #fil  = df_data['Standard'] == name
    #return df_data.loc[fil].T
