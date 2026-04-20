import requests

null = None
data = {
    "simulateType": 2,
    "roadNum": 1,
    "dataChannel": "data1754564956860channel1911",
    "commandChannel": "1",
    "evaluateChannel": "1",
    "routingChannel": "1",
    "statusChannel": "1",
    "params": {
        "channel": "data1754564956860channel1911",
        "avNum": 1,
        "simulationNum": 6,
        "pedestrianNum": 0,
        "participantTrajectories": [
            {
                "id": "1",
                "type": "main",
                "model": 1,
                "name": "主车",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20145495795428,31.29131109802531",
                        "longitude": "121.20145495795428",
                        "latitude": "31.29131109802531",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "326.2510560330305"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20131684197933,31.291637346242254",
                        "longitude": "121.20131684197933",
                        "latitude": "31.291637346242254",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "353.7590831920172"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20134716012019,31.291776481167783",
                        "longitude": "121.20134716012019",
                        "latitude": "31.291776481167783",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "5.75265765256032"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20147348570703,31.292109444604097",
                        "longitude": "121.20147348570703",
                        "latitude": "31.292109444604097",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "32.04965451937422"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "10000000",
                "type": "trafficFlowCar",
                "model": 1,
                "name": "交通流1",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20185190102046,31.29267173753533",
                        "longitude": "121.20185190102046",
                        "latitude": "31.29267173753533",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "218.5320704015123"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20138646141386,31.29128614958577",
                        "longitude": "121.20138646141386",
                        "latitude": "31.29128614958577",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "148.10904975049607"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20162114628184,31.291028508583675",
                        "longitude": "121.20162114628184",
                        "latitude": "31.291028508583675",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.7621727852392"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20169806452805,31.290947425887968",
                        "longitude": "121.20169806452805",
                        "latitude": "31.290947425887968",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "141.01131247913975"
                    }
                ],
                "trajectoryType": 0,
                "traffic": {
                    "trafficFlowType": 1,
                    "trafficFlow": [
                        {
                            "flow": "2",
                            "startTime": 0,
                            "endTime": "5",
                            "vehicleTypePercentage": [
                                {
                                    "vehicleType": 1,
                                    "percentage": 100
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "10000001",
                "type": "trafficFlowCar",
                "model": 1,
                "name": "交通流2",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20186425285561,31.292635274955465",
                        "longitude": "121.20186425285561",
                        "latitude": "31.292635274955465",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "218.73241524388038"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20136175774354,31.292062426783822",
                        "longitude": "121.20136175774354",
                        "latitude": "31.292062426783822",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "204.65173529436234"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20137691681398,31.291360994884574",
                        "longitude": "121.20137691681398",
                        "latitude": "31.291360994884574",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "151.70620747376415"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20144148322503,31.29127127647445",
                        "longitude": "121.20144148322503",
                        "latitude": "31.29127127647445",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "144.64023281828636"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 4,
                        "position": "121.20170704768088,31.290986767796376",
                        "longitude": "121.20170704768088",
                        "latitude": "31.290986767796376",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.93614835325243"
                    }
                ],
                "trajectoryType": 0,
                "traffic": {
                    "trafficFlowType": 1,
                    "trafficFlow": [
                        {
                            "flow": "2",
                            "startTime": 0,
                            "endTime": "5",
                            "vehicleTypePercentage": [
                                {
                                    "vehicleType": 1,
                                    "percentage": 100
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "10000002",
                "type": "trafficFlowCar",
                "model": 1,
                "name": "交通流3",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20187604324371,31.29211040415121",
                        "longitude": "121.20187604324371",
                        "latitude": "31.29211040415121",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "319.9874561723631"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.2013718637905,31.29136963087677",
                        "longitude": "121.2013718637905",
                        "latitude": "31.29136963087677",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "151.70620747376415"
                    }
                ],
                "trajectoryType": 0,
                "traffic": {
                    "trafficFlowType": 1,
                    "trafficFlow": [
                        {
                            "flow": "5",
                            "startTime": 0,
                            "endTime": 10,
                            "vehicleTypePercentage": [
                                {
                                    "vehicleType": 1,
                                    "percentage": 100
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "10000003",
                "type": "trafficFlowCar",
                "model": 1,
                "name": "交通流4",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20191590598445,31.29215214444097",
                        "longitude": "121.20191590598445",
                        "latitude": "31.29215214444097",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "320.5851990498477"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20200293027762,31.292732668393846",
                        "longitude": "121.20200293027762",
                        "latitude": "31.292732668393846",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "38.61033025983551"
                    }
                ],
                "trajectoryType": 0,
                "traffic": {
                    "trafficFlowType": 1,
                    "trafficFlow": [
                        {
                            "flow": "5",
                            "startTime": 0,
                            "endTime": 10,
                            "vehicleTypePercentage": [
                                {
                                    "vehicleType": 1,
                                    "percentage": 100
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "102",
                "type": "slave",
                "model": 1,
                "name": "从车1",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.2018749203496,31.29215262421431",
                        "longitude": "121.2018749203496",
                        "latitude": "31.29215262421431",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "320.591765456926"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20196306753685,31.292640552435014",
                        "longitude": "121.20196306753685",
                        "latitude": "31.292640552435014",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "38.50256392212797"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "106",
                "type": "slave",
                "model": 1,
                "name": "从车2",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20137242523757,31.291906979945786",
                        "longitude": "121.20137242523757",
                        "latitude": "31.291906979945786",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "16.588936857484722"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20188558784362,31.292010611199633",
                        "longitude": "121.20188558784362",
                        "latitude": "31.292010611199633",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "138.2193053292545"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "108",
                "type": "slave",
                "model": 1,
                "name": "从车3",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20173736582174,31.291052977312447",
                        "longitude": "121.20173736582174",
                        "latitude": "31.291052977312447",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "321.8265404586892"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20142856994282,31.291411371494533",
                        "longitude": "121.20142856994282",
                        "latitude": "31.291411371494533",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "333.72967446879704"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20152850751816,31.292175653331643",
                        "longitude": "121.20152850751816",
                        "latitude": "31.292175653331643",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "37.95991200251909"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20172725977478,31.29217037582609",
                        "longitude": "121.20172725977478",
                        "latitude": "31.29217037582609",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.2553998085474"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 4,
                        "position": "121.20180080933866,31.2920936120754",
                        "longitude": "121.20180080933866",
                        "latitude": "31.2920936120754",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.64161755754853"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "109",
                "type": "slave",
                "model": 1,
                "name": "从车4",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20181933709141,31.290965657506106",
                        "longitude": "121.20181933709141",
                        "latitude": "31.290965657506106",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "320.79021209682264"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20136119629652,31.291581692214525",
                        "longitude": "121.20136119629652",
                        "latitude": "31.291581692214525",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "350.00402189578216"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20151671713008,31.29216221968054",
                        "longitude": "121.20151671713008",
                        "latitude": "31.29216221968054",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "35.76026569974341"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20174298029225,31.29215406353431",
                        "longitude": "121.20174298029225",
                        "latitude": "31.29215406353431",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.2553998085474"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 4,
                        "position": "121.20179744065636,31.292097450264418",
                        "longitude": "121.20179744065636",
                        "latitude": "31.292097450264418",
                        "lane": "0",
                        "speed": 30.0,
                        "heading": "140.64161755754853"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "110",
                "type": "slave",
                "model": 1,
                "name": "从车5",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20131347329703,31.291664213692158",
                        "longitude": "121.20131347329703",
                        "latitude": "31.291664213692158",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "353.75908319201585"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.2013505288025,31.291808146329064",
                        "longitude": "121.2013505288025",
                        "latitude": "31.291808146329064",
                        "lane": "0",
                        "speed": 15.0,
                        "heading": "5.75265765256032"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.2014347458604,31.292049952664314",
                        "longitude": "121.2014347458604",
                        "latitude": "31.292049952664314",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "27.04977714703106"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20158072209406,31.2922236306414",
                        "longitude": "121.20158072209406",
                        "latitude": "31.2922236306414",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "63.13603209891863"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 4,
                        "position": "121.20175870080972,31.29213775123968",
                        "longitude": "121.20175870080972",
                        "latitude": "31.29213775123968",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "140.2553998085474"
                    }
                ],
                "trajectoryType": 1
            },
            {
                "id": "10000004",
                "type": "trafficFlowCar",
                "model": 1,
                "name": "交通流5",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20167223796362,31.291075047140822",
                        "longitude": "121.20167223796362",
                        "latitude": "31.291075047140822",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "321.2412588853072"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20133817696735,31.291536113460467",
                        "longitude": "121.20133817696735",
                        "latitude": "31.291536113460467",
                        "lane": "0",
                        "speed": 40.0,
                        "heading": "346.94605214919875"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 2,
                        "position": "121.20131066606177,31.291702115974523",
                        "longitude": "121.20131066606177",
                        "latitude": "31.291702115974523",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "357.51504377576356"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 3,
                        "position": "121.20139376022554,31.291966951750098",
                        "longitude": "121.20139376022554",
                        "latitude": "31.291966951750098",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "20.31260727871622"
                    },
                    {
                        "type": "pathway",
                        "time": "0",
                        "frameId": 4,
                        "position": "121.2015127870007,31.292157901720856",
                        "longitude": "121.2015127870007",
                        "latitude": "31.292157901720856",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "35.76026569974341"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 5,
                        "position": "121.20170704768088,31.292191006073434",
                        "longitude": "121.20170704768088",
                        "latitude": "31.292191006073434",
                        "lane": "0",
                        "speed": 25.0,
                        "heading": "139.6025618183742"
                    }
                ],
                "trajectoryType": 0,
                "traffic": {
                    "trafficFlowType": 1,
                    "trafficFlow": [
                        {
                            "flow": "3",
                            "startTime": 0,
                            "endTime": "5",
                            "vehicleTypePercentage": [
                                {
                                    "vehicleType": 1,
                                    "percentage": 100
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "id": "111",
                "type": "slave",
                "model": 1,
                "name": "从车6",
                "trajectory": [
                    {
                        "type": "start",
                        "time": "0",
                        "frameId": 0,
                        "position": "121.20131066606177,31.291744336220468",
                        "longitude": "121.20131066606177",
                        "latitude": "31.291744336220468",
                        "lane": "0",
                        "speed": 0.0,
                        "heading": "1.9058361524354681"
                    },
                    {
                        "type": "end",
                        "time": "0",
                        "frameId": 1,
                        "position": "121.20131347329703,31.29178991487387",
                        "longitude": "121.20131347329703",
                        "latitude": "31.29178991487387",
                        "lane": "0",
                        "speed": 0.05,
                        "heading": "5.730640101387829"
                    }
                ],
                "trajectoryType": 1
            }
        ],
        "frequency": 10
    },
    "mapList": [
        "10"
    ],
    "customizedParams": {
        "sceneType": {
            "type": 0,
            "ttc": 5
        },
        "sceneTrigger": [
            {
                "triggerType": 1,
                "param": [
                    {
                        "type": 1,
                        "value": 5,
                        "describe": "当前场景测试时间5s触发"
                    },
                    {
                        "type": 2,
                        "value": 5,
                        "describe": "主车预计5s后经过冲突点时触发"
                    }
                ]
            }
        ],
        "trafficLight": [],
        "trigger": [
            {
                "lat": 31.29163158893056,
                "lng": 121.2013174034264,
                "vehicles": [
                    103,
                    1000
                ]
            }
        ],
        "obstacles": [
            {
                "id": 1000,
                "type": "broken_car",
                "lat": 31.291803828353146,
                "lng": 121.20131515763819,
                "courseAngle": null,
                "area": null
            }
        ]
    }
}


url = "http://127.0.0.1:7778/jd/startTessng"
requests.post(url, json=data)
