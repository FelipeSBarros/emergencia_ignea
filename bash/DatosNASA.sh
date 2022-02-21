# Requiere  :     
# sudo apt install npm
# sudo npm install -g csv2geojson
 
# Cambia al directorio de datos de la app 
cd /var/www/html/mapas/emergencia/datos/ 
 
 
# Limpia los archivos de trabajo
rm MODIS_C6_1_South_America_24h.csv
rm SUOMI_VIIRS_C2_South_America_24h.csv
rm J1_VIIRS_C2_South_America_24h.csv

rm incendios.csv
echo "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight,satellite" >> incendios.csv

 
# Descarga los archivos de las ultimas 20 horas de la NSA 
# Pagina de referencia: https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt
wget https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_America_24h.csv
wget https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_America_24h.csv
wget https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_America_24h.csv
	
 
#VIIRS 375m / S-NPP
# Limpia el archivo dejando solamente los que tienen confianza alta 
sed -i -e 's/high/alta/g'  SUOMI_VIIRS_C2_South_America_24h.csv
sed -i -e 's/low/baja/g'  SUOMI_VIIRS_C2_South_America_24h.csv
sed -i -e 's/,N/,Noche/g'  SUOMI_VIIRS_C2_South_America_24h.csv
sed -i -e 's/,D/,Día/g'  SUOMI_VIIRS_C2_South_America_24h.csv
while IFS="," read -r c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13
do
    latitud=${c1%.*}
    LatSuperior=$(($latitud+25)) 
    LatInferior=$(($latitud+29)) 
    
    longitud=${c2%.*}  
    LonIzquierda=$(($longitud+53)) 
    LonDerecha=$(($longitud+57))   

    # si el punto está dentro del cuadrante, grabar la linea
    if [ $LatSuperior -lt 0 ];then
    	if [ $LatInferior -gt 0 ];then
    		if [ $LonIzquierda -lt 0 ];then    	
    			if [ $LonDerecha -gt 0 ];then    	    
          			echo "$c1,$c2,$c3,$c4,$c5,$c6,$c7,$c8,$c9,$c10,$c11,$c12,$c13,VIIRS-S-NPP"  >> incendios.csv
			fi
    		fi
	fi
    fi      
done < SUOMI_VIIRS_C2_South_America_24h.csv


#VIIRS 375m / NOAA-20
# Limpia el archivo dejando solamente los que tienen confianza alta 
sed -i -e 's/high/alta/g'  J1_VIIRS_C2_South_America_24h.csv
sed -i -e 's/low/baja/g'  J1_VIIRS_C2_South_America_24h.csv
sed -i -e 's/,N/,Noche/g'  J1_VIIRS_C2_South_America_24h.csv
sed -i -e 's/,D/,Día/g'  J1_VIIRS_C2_South_America_24h.csv
while IFS="," read -r c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13
do
    latitud=${c1%.*}
    LatSuperior=$(($latitud+25)) 

    LatInferior=$(($latitud+29)) 
    
    longitud=${c2%.*}  
    LonIzquierda=$(($longitud+53)) 
    LonDerecha=$(($longitud+57))   
    
    # si el punto está dentro del cuadrante, grabar la linea
    if [ $LatSuperior -lt 0 ];then
    	if [ $LatInferior -gt 0 ];then
    		if [ $LonIzquierda -lt 0 ];then    	
    			if [ $LonDerecha -gt 0 ];then    	    
          			echo "$c1,$c2,$c3,$c4,$c5,$c6,$c7,$c8,$c9,$c10,$c11,$c12,$c13,VIIRS-NOAA-20"  >> incendios.csv
			fi
    		fi
	fi
    fi   
done < J1_VIIRS_C2_South_America_24h.csv


# MODIS
sed -i -e 's/,N/,Noche/g'  MODIS_C6_1_South_America_24h.csv
sed -i -e 's/,D/,Día/g'  MODIS_C6_1_South_America_24h.csv
# Limpia el archivo dejando solamente los que están debajo del paralelo 25   
while IFS="," read -r c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13
do
    latitud=${c1%.*}
    LatSuperior=$(($latitud+25)) 
    LatInferior=$(($latitud+29)) 
    
    longitud=${c2%.*}  
    LonIzquierda=$(($longitud+53)) 
    LonDerecha=$(($longitud+57))   

    # si el punto está dentro del cuadrante, grabar la linea
    if [ $LatSuperior -lt 0 ];then
    	if [ $LatInferior -gt 0 ];then
    		if [ $LonIzquierda -lt 0 ];then    	
    			if [ $LonDerecha -gt 0 ];then    	    
          			echo "$c1,$c2,$c3,$c4,$c5,$c6,$c7,$c8,$c9,$c10,$c11,$c12,$c13,MODIS"  >> incendios.csv
			fi
    		fi
	fi
    fi     
done < MODIS_C6_1_South_America_24h.csv


echo "$(date)"  >  NASA-Ultima-Actualizacion.txt


