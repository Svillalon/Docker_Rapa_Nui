Instrucciones para guardar, limpiar e interpolar sondeos

1. Ejecutar ReadandSaveRapaNui.py para generar los archivos RapaNui_GAW_ozonesondes.csv y RapaNui_CR2_ozonesondes.csv que contienen las bases de datos de sondeos de GAW y CR2 respectivamente.
2. Ejecutar MergeDataBase.py para combinar las bases de datos de GAW y CR2 en el archivo RapaNui_all_ozonesondes.csv. Además, se generará, en caso de no existir, o actualizará el archivo RapaNui_dates_valid.csv, que es donde se indica el estado de validez de cada sondeo.
3. Ejecutar GraphicsandInspectionOzonosondes.py para generar los gráficos de los perfiles de cada sondeo en el archivo RapaNui_all_ozonesondes.csv. Los gráficos se guardan en la carpeta Graphs_Inspection_Valid.
4. Una vez completada y/o actualizada la información de validez de los sondeos en el archivo RapaNui_dates_valid.csv, ejecutar CleaningandSavingRapaNui.py para limpiar e interpolar los sondeos. Se generarán archivos individuales para cada sondeo con las variables interpoladas. Estos archivos individuales se guardan en la carpeta Data_Interpolate. También se generará el archivo RapaNui_all_clear.csv que contiene todos los sondeos interpolados y que será utilizado en la interfaz gráfica.
5. Para contabilizar los sondeos, ejecutar Accounting_Soundings.py, el que entregará 2 archivos: Table_TotalNumSoundings_RapaNui.xlsx, que cuenta todos los sondeos, válidos y no válidos; y Table_ValidNumSoundings_RapaNui.xlsx, que cuenta solo los sondeos validados.


Instrucciones para calcular retrotrayectorias

1. Ejecutar Download_NCEPNCAR_reanalysis.sh para descargar la base de datos NCEP/NCAR requerida para ejecutar hysplit. Es necesario actualizar el periodo de tiempo de datos a descargar.
2. Una vez completada y/o actualizada la información de validez de los sondeos en el archivo RapaNui_dates_valid.csv, ejecutar DateStringforHysplit.py para generar el archivo RapaNui_DatesStr_hysplit.csv que contiene las fechas en formato requerido para ejecutar hysplit.
3. Ejecutar Run_RN_bt.sh para simular las trayectorias de todos los sondeos. Los archivos por trayectoria son guardados en la carpeta Trajec.
4. Ejecutar ReadandSaveTraj.py para juntar y guardar todas las trayectorias en el archivo RapaNui_BackTrajectories.csv.
