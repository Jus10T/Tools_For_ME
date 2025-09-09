length_factors = {
    'nanometers': 1e-9,
    'millimeters': 1e-3,
    'centimeters': 1e-2,
    'meters': 1, 
    'kilometers': 1e3,
    'inches': 0.0254,
    'feet': 0.3048,
    'yards': 0.9144,
    'miles': 1609.34,
        }
area_factors = {
    'millimeters²': 1e-6,
    'centimeters²': 1e-4,
    'meters²':1, 
    'kilometers²': 1e6,
    'inches': 0.000645,
    'feet': 0.92903,
    'miles': 2589988,
    'Acres': 4046.856,
        }
mass_factors = {
    'milligrams':1e-3,
    'centigrams': 1e-2, 
    'grams': 1,
    'kilograms': 1e3,
    'metric tonnes': 1e6,
    'newtons': 101.97162129779,
    'kilonewtons':101971.62129779,
    'ounces': 28.34952, 
    'pounds': 453.5924,
    'kip':453592.4,
    'US Tons': 907184.7,   
        }
stress_factors = {
    'atmospheres': 101325, 
    'bars': 1e5, 
    'pascals': 1, 
    'kilopascals': 1e3,
    'megapascals': 1e6,
    'pounds/inches²':6894.757,
    'kip/inches²': 6894757.2932,
    'torr': 133.322368
        }
energy_factors = {
    'joules': 1,
    'kilojoules': 1e3,
    'foot-pound': 1.3558179483,
    'british thermal unit': 1055.0558526,
    'calories': 4186.8,
    'kilowatt-hours': 3600000,
        }
time_factors = {
    'millisecond': 0.01,
    'second': 1, 
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'week': 604800,
        }


unit_types_abrv = {'English':{'Length': {'inches':"in",
                                         'feet':"ft",
                                         'yards':"yd",
                                         'miles':"mi"},

                              'Area': {'inches²':"in²",
                                         'feet²':"ft²",
                                         'miles²':"mi²",
                                         'Acres': "ac"},

                              'Mass / Weight': {'ounces':"oz",
                                                'pounds':"lb",
                                                'kip':"kip",
                                                'US Tons':"ton",
                                                },

                              'Temperature': {'fahrenheit': "°F",
                                              'rankine':"°R"},

                              'Pressure / Stress': {'atmospheres': "atm",
                                                    'pounds/inches²': "psi",
                                                    'kips/inches²': "kips"},

                              'Energy':{"foot-pound": "ft-lb",
                                        'british thermal unit': "Btu",
                                        },

                              'Time': {'seconds': "s",
                                       'minutes': "min",
                                       'hours': "hr",
                                       'days': "day",
                                       'weeks': "wk"},

                              'Moment of Inertia': {'inches⁴': "in⁴",
                                                    'millimeters⁴': "mm⁴"}
                                         },
                         
                'Metric/SI':{'Length': {'nanometers':"nm",
                                'millimeters':"mm",
                                'centimeters':"cm",
                                'meters':"m",
                                'kilometers':"km",
                                    },

                        'Area': {'millimeters²':"mm²",
                                 'centimeters²':"cm²",
                                 'meters²':"m²",
                                 'kilometers²':"km²"},

                        'Mass / Weight': {'milligrams':"mg",
                                          'centigrams':"cg",
                                          'grams':"g",
                                          'kilograms':"kg",
                                          'newtons': "N",
                                          'kilonewtons':"kN"},

                        'Temperature': {'celsius':"°C",
                                        'kelvin':"K"},
                        'Pressure / Stress': {'bars':"bar",
                                              'pascal':"Pa",
                                              'kilopascals':"kPa",
                                              'megapascals':"MPa",
                                              "torr":"Torr"},
                        'Energy':{'joules':"J",
                                  'kilojoules':"kJ",
                                  'calories':"cal",
                                  'kilowatt-hours':"kW-h"},
                        'Time': {'seconds': "s",
                                'minutes': "min",
                                'hour': "hr",
                                'day': "day",
                                'week': "wk"},
                        }}

beam_dropdown_units = {'English': {'Moment of Inertia': {"inches⁴": "in⁴"},
                                    'Elastic Modulus': {'kip/inch²':"ksi"},
                                    'PointLoad':{'pounds':"lb"},
                                    'MomentLoad':{'inch-pounds':"in-lb"},
                                    'distributedLoad':{'pounds/inch':"lb/in"},
                                    'Length':{'inches':"in"}},
                       'Metric / SI': {'Moment of Inertia': {'millimeters⁴':"mm⁴"},
                                        'Elastic Modulus': {'gigapascals':"GPa"},
                                        'PointLoad': {'newton':"N"},
                                        'MomentLoad': {'newton-meters':"N-m"},
                                        'distributedLoad': {'newton/meter':"N/m"},
                                        'Length':{'meters':"m"}}}

