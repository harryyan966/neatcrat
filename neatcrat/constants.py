'''
Constants
'''

SCENE_LENGTH = 40
SECONDS_PER_FRAME = 0.5

OT_SELF = 'AV'
OT_PEDESTRIAN = 'Pedestrian'
OT_CAR = 'Vehicle'
OT_BIKE = 'Bicycle'
OT_BARRIER = 'Barrier'

OBJECT_TYPES = {
    OT_SELF: 0,
    OT_PEDESTRIAN: 1,
    OT_CAR :2,
    OT_BIKE :3,
    OT_BARRIER :4,
}
OBJECT_TYPE_NAMES = {v:k for k,v in OBJECT_TYPES.items()}

FIRST_CLASSES = {
    '1.GoStraight': 0,
    '2. Crossing': 1,
}
FIRST_CLASSES_NAMES = {v:k for k,v in FIRST_CLASSES.items()}

INLANE = '1.1 InLane'
WAIT = '2.1 StopAndWait'
STRAIGHT = '2.4 GoStraight'
LEFT = '2.5 TurnLeft'
RIGHT = '2.6 TurnRight'
UTURN = '2.7 UTurn'
INVALID2 = '9.9 Invalid'

SECOND_CLASSES = {
    INLANE: 0,
    WAIT: 1,
    STRAIGHT: 2,
    LEFT: 3,
    RIGHT: 4,
    UTURN: 5,
    INVALID2: -1,
}
SECOND_CLASSES_NAMES = {v:k for k,v in SECOND_CLASSES.items()}

INLANE_LEAD_CONST = '1.1.1 LeadVehicleConstant'
INLANE_CUTOUT = '1.1.2 LeadVehicleCutOut'
INLANE_CUTIN = '1.1.3 VehicleCutInAhead'
INLANE_LEAD_DECELERATE = '1.1.4 LeadVehicleDecelerating'
INLANE_LEAD_STOPPED = '1.1.5 LeadVehicleStppoed'
INLANE_LEAD_ACCELERATE = '1.1.6 LeadVehicleAccelerating'
INLANE_LEAD_WRONGWAY = '1.1.7  LeadVehicleWrongDriveway'

WAIT_HAS_LEAD = '2.1.4 LeadVehicleStppoed'
WAIT_HAS_PEDESTRIANS = '2.1.5 PedestrianCrossing'

STRAIGHT_NOTHING_AHEAD = '2.4.1 NoVehiclesAhead'
STRAIGHT_HAS_LEAD = '2.4.2 WithLeadVehicle'
STRAIGHT_HAS_CROSS = '2.4.3 VehiclesCrossing'

LEFT_NOTHING_AHEAD = '2.5.1 NoVehiclesAhead'
LEFT_HAS_LEAD = '2.5.2 WithLeadVehicle'
LEFT_HAS_CROSS = '2.5.3 VehiclesCrossing'

RIGHT_NOTHING_AHEAD = '2.6.1 NoVehiclesAhead'
RIGHT_HAS_LEAD = '2.6.2 WithLeadVehicle'
RIGHT_HAS_CROSS = '2.6.3 VehiclesCrossing'

UTURN_NOTHING_AHEAD = '2.7.1 NoVehiclesAhead'

INVALID3 = '9.9.9 Invalid'

THIRD_CLASSES = {
    INLANE_LEAD_CONST: 0,
    INLANE_CUTOUT: 1,
    INLANE_CUTIN: 2,
    INLANE_LEAD_DECELERATE: 3,
    INLANE_LEAD_STOPPED: 4,
    INLANE_LEAD_ACCELERATE: 5,
    INLANE_LEAD_WRONGWAY: 6,
    WAIT_HAS_LEAD: 7,
    WAIT_HAS_PEDESTRIANS: 8,
    STRAIGHT_NOTHING_AHEAD: 9,
    STRAIGHT_HAS_LEAD: 10,
    STRAIGHT_HAS_CROSS: 11,
    LEFT_NOTHING_AHEAD: 12,
    LEFT_HAS_LEAD: 13,
    LEFT_HAS_CROSS: 14,
    RIGHT_NOTHING_AHEAD: 15,
    RIGHT_HAS_LEAD: 16,
    RIGHT_HAS_CROSS: 17,
    UTURN_NOTHING_AHEAD: 18,
    INVALID3: -1,
}
THIRD_CLASSES_NAMES = {v:k for k,v in THIRD_CLASSES.items()}

