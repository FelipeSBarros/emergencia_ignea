// Determinar si el punto de calor está dentro del poligono de Misiones
// fuente: https://github.com/Turfjs/turf/tree/master/packages/turf-boolean-point-in-polygon

var Misiones = turf.polygon([[
     [   -54.60205078125,  -25.587039832050046  ],
     [   -54.66796875,  -25.66628476656516  ],
     [   -54.68994140625,  -25.997549919572098  ],
     [   -54.854736328125,  -26.64254890019605  ],
     [   -55.1513671875,  -26.86328062676624  ],
     [   -55.1239013671875,  -26.961245770526954  ],
     [   -55.2667236328125,  -26.941659545381505  ],
     [   -55.6072998046875,  -27.166695222253104  ],
     [   -55.6072998046875,  -27.313213898568247  ],
     [   -55.7666015625,  -27.444915505146934  ],
     [   -55.865478515625,  -27.347373810080263  ],
     [   -56.03782653808593,  -27.344934165500973  ],
     [   -56.0247802734375,  -27.51314343580719  ],
     [   -55.843505859375,  -27.80020993741824  ],
     [   -55.6182861328125,  -28.2027676859484  ],
     [   -55.2008056640625,  -27.86336037597851  ],
     [   -55.140380859375,  -27.931327412293648  ],
     [   -54.9041748046875,  -27.746746268526383  ],
     [   -54.66796875,  -27.518015241965667  ],
     [   -54.2779541015625,  -27.405909155361034  ],
     [   -53.82751464843749,  -27.13247980102287  ],
     [   -53.6627197265625,  -26.897578097333913  ],
     [   -53.7506103515625,  -26.578702269100557  ],
     [   -53.63525390625,  -26.2145910237943  ],
     [   -53.8330078125,  -25.913585416189797  ],
     [   -53.876953125,  -25.641526373065755  ],
     [   -54.0911865234375,  -25.48295117535531  ],
     [   -54.60205078125,  -25.587039832050046  ]
]]);


  $.get("datos/incendios.csv", function(csvString) {

    var data = Papa.parse(csvString, {header: true, dynamicTyping: true}).data;

    for (var i in data) {
      var row = data[i];

      var punto = turf.point([row.longitude, row.latitude]);
      var enMapa = turf.booleanPointInPolygon(punto, Misiones);

 if (enMapa === true) {

var HoraObservada = row.acq_time;
var HorasAdicionales = 24 - parseInt(row.acq_time/100);

var DiaHoy = new Date(); // .toISOString().slice(9, 2) // AAAA-MM-DD
var DiaHoy = DiaHoy.getDate();
var DiaObservacion = (row.acq_date);
var DiaObservacion = parseInt(DiaObservacion.substr(DiaObservacion.length - 2));
var DiferenciaDias = DiaHoy - DiaObservacion;

var HorasAcumuladas = 0;
if (DiferenciaDias  == 1) {
var HoraObservada = row.acq_time;
var HorasAdicionales = 24 - parseInt(row.acq_time/100);
var HorasAcumuladas = HorasAcumuladas  + HorasAdicionales;
var FechaHoy = new Date();
var HoraActual = FechaHoy.getHours();
var HorasAcumuladas = HorasAcumuladas  + HoraActual;
    };

if (DiferenciaDias  == 0) {
var FechaHoy = new Date();
var HoraActual = FechaHoy.getHours();
var HorasAcumuladas = HorasAcumuladas  + HoraActual;
    };

if (DiferenciaDias <=1 && HorasAcumuladas < 24) {

// Convierte las coordenadas a Sexagesimal

var GradLatitud = Math.abs(row.latitude);
var grados =  parseInt(GradLatitud);
var MinutosReal = (GradLatitud - grados) * 60;
var minutos = parseInt(MinutosReal);
var SegundosReal = (MinutosReal - minutos) * 60;
var segundos = parseInt(SegundosReal);
var latGrados = grados + 'º ' + minutos + '\' ' + segundos + '\"';

var GradLongitud = Math.abs(row.longitude);
var grados =  parseInt(GradLongitud);
var MinutosReal = (GradLongitud - grados) * 60;
var minutos = parseInt(MinutosReal);
var SegundosReal = (MinutosReal - minutos) * 60;
var segundos = parseInt(SegundosReal);
var lonGrados = grados + 'º ' + minutos + '\' ' + segundos + '\"';


      var temperatura = (row.bright_ti4 - 273.15);
             var temp = temperatura.toString();
             var temperatura = temp.substring(0,6);
             var TextoPopup = 'Fuente:<b>' + row.satellite + '</b><br/>'+
                   'Confianza : Alta' + '<br/>' +'Temperatura : ' + temperatura + ' Cº<br/>' +
                   'Coordenadas : ' + latGrados + ' S. ' + lonGrados + ' O.<br/>' +
                   'Coordenadas : ' + row.latitude + ',' + row.longitude + '<br/>' +
                   'Fecha:    ' + row.acq_date + ' hora: ' + row.acq_time + '<br/>' +
                   'Detección: ±' + HorasAcumuladas + ' horas; ' ;

      var marker = L.marker([row.latitude, row.longitude], {
                 icon: IconoIncendio
      }).bindPopup(TextoPopup);

      //marker.addTo(IncendiosVIIRSSNPP);
      marker.addTo(Incendios);

} // (DiferenciaDias<=1 && HorasAcumuladas<19)

    }
}

  });