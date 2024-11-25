'''
Constants
'''

SCENE_LENGTH = 40
SECONDS_PER_FRAME = 0.5

OBJECT_TYPES = {
    'AV': 0,
    'Pedestrian': 1,
    'Vehicle' :2,
    'Bicycle' :3,
    'Barrier' :4,
}
OBJECT_TYPE_NAMES = {v:k for k,v in OBJECT_TYPES.items()}

FIRST_CLASSES = {
    '1.GoStraight': 0,
    '2. Crossing': 1,
}
FIRST_CLASSES_NAMES = {v:k for k,v in FIRST_CLASSES.items()}

SECOND_CLASSES = {
    '1.1 InLane': 0,
    '2.1 StopAndWait': 1,
    '2.4 GoStraight': 2,
    '2.5 TurnLeft': 3,
    '2.6 TurnRight': 4,
    '2.7 UTurn': 5,
}
SECOND_CLASSES_NAMES = {v:k for k,v in SECOND_CLASSES.items()}

THIRD_CLASSES = {
    '1.1.1 LeadVehicleConstant': 0,
    '1.1.2 LeadVehicleCutOut': 1,
    '1.1.3 VehicleCutInAhead': 2,
    '1.1.4 LeadVehicleDecelerating': 3,
    '1.1.5 LeadVehicleStppoed': 4,
    '1.1.6 LeadVehicleAccelerating': 5,
    '1.1.7  LeadVehicleWrongDriveway': 6,
    '2.1.4 LeadVehicleStppoed': 7,
    '2.1.5 PedestrianCrossing': 8,
    '2.4.1 NoVehiclesAhead': 9,
    '2.4.2 WithLeadVehicle': 10,
    '2.4.3 VehiclesCrossing': 11,
    '2.5.1 NoVehiclesAhead': 12,
    '2.5.2 WithLeadVehicle': 13,
    '2.5.3 VehiclesCrossing': 14,
    '2.6.1 NoVehiclesAhead': 15,
    '2.6.2 WithLeadVehicle': 16,
    '2.6.3 VehiclesCrossing': 17,
    '2.7.1 NoVehiclesAhead': 18,
}
THIRD_CLASSES_NAMES = {v:k for k,v in THIRD_CLASSES.items()}
THIRD_CLASS_NAMES_INVALID = '9.9.9 Invalid'
