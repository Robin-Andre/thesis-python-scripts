class Palette:
    def __init__(self):
        self.label_dict = {}
        self.color_dict = {}

    def label_modes(self, s, get_all_and_combined=False):
        if get_all_and_combined:
            return list(self.label_dict.values())
        if s in self.label_dict.keys():
            return self.label_dict[s]
        return "Unknown Label"

    def color_modes(self, s, get_all=False, get_all_and_combined=False):

        if get_all_and_combined:
            return list(self.color_dict.values())
        if get_all:
            return list(self.color_dict.values())[1:]
        if s in self.color_dict.keys():
            return self.color_dict[s]
        return "#000000"


class ModePalette(Palette):
    def __init__(self):
        self.label_dict = {
            -1: "All",
            0: "Bike",
            1: "Car",
            2: "Passenger",
            3: "Pedestrian",
            4: "Pub. Transp."
        }
        self.color_dict = {
            -1: "#888888",
            0: "#2D77BC",
            1: "#BF252C",
            2: "#F89C1C",
            3: "#B3E0F7",
            4: "#70BE43"
        }


# boolean

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_bool, name='True', value='True')

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_bool, name='False', value='False')

# Providers

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_provider, name='KVV.nextbike',
                                value='KVVnextbike')

TypeValue.objects.get_or_create(project=project, color='#2D77BC', data_type=_provider, name='stadtmobil',
                                value='Stadtmobil')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='bikesharing',
                                value='BIKESHARING')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='Bikesharing',
                                value='Bikesharing')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='free-floating carsharing',
                                value='CarsharingFreeFloating')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='station-based carsharing',
                                value='CarsharingStation')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='e-scooter',
                                value='E_SCOOTER')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='no MOIA member',
                                value='Moia_no_member')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='Car2Go', value='Car2Go')

TypeValue.objects.get_or_create(project=project, color='#707070', data_type=_provider, name='Flinkster',
                                value='Flinkster')

# Zone classifications

TypeValue.objects.get_or_create(project=project, color='#00A78E', data_type=_class, name='study area',
                                value='studyArea')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_class, name='extended study area',
                                value='extendedStudyArea')

TypeValue.objects.get_or_create(project=project, color='#B08433', data_type=_class, name='outlying area',
                                value='outlyingArea')

# Gender

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_gender, name='female', value='FEMALE')

TypeValue.objects.get_or_create(project=project, color='#00ADEA', data_type=_gender, name='male', value='MALE')

# Employment

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_employment, name='fulltime',
                                value='FULLTIME')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_employment, name='parttime',
                                value='PARTTIME')

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_employment, name='marginal',
                                value='MARGINAL')

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_employment, name='unemployed',
                                value='UNEMPLOYED')

TypeValue.objects.get_or_create(project=project, color='#DCE3F2', data_type=_employment, name='student',
                                value='STUDENT')

TypeValue.objects.get_or_create(project=project, color='#BCC9E6', data_type=_employment, name='student primary',
                                value='STUDENT_PRIMARY')

TypeValue.objects.get_or_create(project=project, color='#96ADD8', data_type=_employment, name='student secondary',
                                value='STUDENT_SECONDARY')

TypeValue.objects.get_or_create(project=project, color='#7294CC', data_type=_employment, name='student tertiary',
                                value='STUDENT_TERTIARY')

TypeValue.objects.get_or_create(project=project, color='#2D77BC', data_type=_employment, name='education',
                                value='EDUCATION')

TypeValue.objects.get_or_create(project=project, color='#000000', data_type=_employment, name='unkown', value='UNKNOWN')

TypeValue.objects.get_or_create(project=project, color='#000000', data_type=_employment, name='none', value='NONE')

TypeValue.objects.get_or_create(project=project, color='#00A78E', data_type=_employment, name='homekeeper',
                                value='HOMEKEEPER')

TypeValue.objects.get_or_create(project=project, color='#BC1B8D', data_type=_employment, name='retired',
                                value='RETIRED')

TypeValue.objects.get_or_create(project=project, color='#22BBA9', data_type=_employment, name='infant', value='INFANT')

# Car segment

TypeValue.objects.get_or_create(project=project, color='#DCE3F2', data_type=_segment, name='small', value='SMALL')

TypeValue.objects.get_or_create(project=project, color='#96ADD8', data_type=_segment, name='midsize', value='MIDSIZE')

TypeValue.objects.get_or_create(project=project, color='#2D77BC', data_type=_segment, name='large', value='LARGE')

# Car engine

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_engine, name='Conventional',
                                value='conventional')

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_engine, name='BEV', value='bev')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_engine, name='EREV', value='erev')

# charging

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_charging, name='always', value='ALWAYS')

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_charging, name='low battery',
                                value='ONLY_WHEN_BATTERY_LOW')

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_charging, name='never', value='NEVER')

# graduation

TypeValue.objects.get_or_create(project=project, color='#000000', data_type=_graduation, name='undefined',
                                value='UNDEFINED')

TypeValue.objects.get_or_create(project=project, color='#BC1B8D', data_type=_graduation, name='other', value='OTHER')

TypeValue.objects.get_or_create(project=project, color='#B08433', data_type=_graduation, name='not highschool',
                                value='NOT_HIGHSCHOOL')

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_graduation, name='highschool graduate',
                                value='HIGHSCHOOL_GRADUATE')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_graduation,
                                name='college credet but no degree', value='SOME_COLLEGE_CREDIT_NO_DEGREE')

TypeValue.objects.get_or_create(project=project, color='#00A78E', data_type=_graduation,
                                name='associate technical school degree', value='ASSOCIATE_TECHNICAL_SCHOOL_DEGREE')

TypeValue.objects.get_or_create(project=project, color='#B5D99A', data_type=_graduation, name='bachelor degree',
                                value='BACHELOR_DEGREE')

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_graduation, name='graduate degree',
                                value='GRADUATE_DEGREE')

# cativity type

TypeValue.objects.get_or_create(project=project, color='#CF6953', data_type=_activity, name='undefined',
                                value='UNDEFINED')

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_activity, name='work', value='WORK')

TypeValue.objects.get_or_create(project=project, color='#00A78E', data_type=_activity, name='business',
                                value='BUSINESS')

TypeValue.objects.get_or_create(project=project, color='#22BBA9', data_type=_activity, name='business out',
                                value='BUSINESS_OUT')

TypeValue.objects.get_or_create(project=project, color='#7BCBBF', data_type=_activity, name='business to work',
                                value='BUSINESS_TO_WORK')

TypeValue.objects.get_or_create(project=project, color='#B0DED6', data_type=_activity, name='deliver parcel',
                                value='DELIVER_PARCEL')

TypeValue.objects.get_or_create(project=project, color='#D6EDE9', data_type=_activity, name='business travel',
                                value='BUSINESS_TRAVEL')

TypeValue.objects.get_or_create(project=project, color='#2D77BC', data_type=_activity, name='education',
                                value='EDUCATION')

TypeValue.objects.get_or_create(project=project, color='#7294CC', data_type=_activity, name='education primary',
                                value='EDUCATION_PRIMARY')

TypeValue.objects.get_or_create(project=project, color='#96ADD8', data_type=_activity, name='education secondary',
                                value='EDUCATION_SECONDARY')

TypeValue.objects.get_or_create(project=project, color='#BCC9E6', data_type=_activity, name='education tertiary',
                                value='EDUCATION_TERTIARY')

TypeValue.objects.get_or_create(project=project, color='#DCE3F2', data_type=_activity, name='education occup',
                                value='EDUCATION_OCCUP')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_activity, name='shopping',
                                value='SHOPPING')

TypeValue.objects.get_or_create(project=project, color='#FEEC6A', data_type=_activity, name='shopping daily',
                                value='SHOPPING_DAILY')

TypeValue.objects.get_or_create(project=project, color='#FFF198', data_type=_activity, name='shopping other',
                                value='SHOPPING_OTHER')

TypeValue.objects.get_or_create(project=project, color='#FDF5BF', data_type=_activity, name='private business',
                                value='PRIVATE_BUSINESS')

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_activity, name='leisure', value='LEISURE')

TypeValue.objects.get_or_create(project=project, color='#FBB760', data_type=_activity, name='leisure indoor',
                                value='LEISURE_INDOOR')

TypeValue.objects.get_or_create(project=project, color='#FDCA8A', data_type=_activity, name='leisure outdoor',
                                value='LEISURE_OUTDOOR')

TypeValue.objects.get_or_create(project=project, color='#FEDDB4', data_type=_activity, name='leisure other',
                                value='LEISURE_OTHER')

TypeValue.objects.get_or_create(project=project, color='#FEEED8', data_type=_activity, name='leisure sightseeing',
                                value='LEISURE_SIGHTSEEING')

TypeValue.objects.get_or_create(project=project, color='#B08433', data_type=_activity, name='leisure travel',
                                value='LEISURE_TRAVEL')

TypeValue.objects.get_or_create(project=project, color='#C5A164', data_type=_activity, name='leisure walk',
                                value='LEISURE_WALK')

TypeValue.objects.get_or_create(project=project, color='#D3B88A', data_type=_activity, name='private visit',
                                value='PRIVATE_VISIT')

TypeValue.objects.get_or_create(project=project, color='#E2D0B2', data_type=_activity, name='service', value='SERVICE')

TypeValue.objects.get_or_create(project=project, color='#F0E6D5', data_type=_activity, name='pick up parcel',
                                value='PICK_UP_PARCEL')

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_activity, name='home', value='HOME')

TypeValue.objects.get_or_create(project=project, color='#B5D99A', data_type=_activity, name='other home',
                                value='OTHERHOME')

# mode

TypeValue.objects.get_or_create(project=project, color='#B08433', data_type=_mode, name='undefined', value='UNDEFINED')

TypeValue.objects.get_or_create(project=project, color='#B08433', data_type=_mode, name='unknown', value='UNKNOWN')

TypeValue.objects.get_or_create(project=project, color='#2D77BC', data_type=_mode, name='bike', value='BIKE')

TypeValue.objects.get_or_create(project=project, color='#BF252C', data_type=_mode, name='car', value='CAR')

TypeValue.objects.get_or_create(project=project, color='#F89C1C', data_type=_mode, name='passenger', value='PASSENGER')

TypeValue.objects.get_or_create(project=project, color='#B3E0F7', data_type=_mode, name='pedestrian',
                                value='PEDESTRIAN')

TypeValue.objects.get_or_create(project=project, color='#70BE43', data_type=_mode, name='public transport',
                                value='PUBLICTRANSPORT')

TypeValue.objects.get_or_create(project=project, color='#00A78E', data_type=_mode, name='truck', value='TRUCK')

TypeValue.objects.get_or_create(project=project, color='#CF6953', data_type=_mode, name='park and ride',
                                value='PARK_AND_RIDE')

TypeValue.objects.get_or_create(project=project, color='#FEE500', data_type=_mode, name='taxi', value='TAXI')

TypeValue.objects.get_or_create(project=project, color='#DA8F78', data_type=_mode, name='stationbased carsharing',
                                value='CARSHARING_STATION')

TypeValue.objects.get_or_create(project=project, color='#E8B7A5', data_type=_mode, name='free-floating carsharing',
                                value='CARSHARING_FREE')

TypeValue.objects.get_or_create(project=project, color='#7ECEF3', data_type=_mode, name='e-scooter', value='E_SCOOTER')

TypeValue.objects.get_or_create(project=project, color='#39C0EF', data_type=_mode, name='pedelec', value='PEDELEC')

TypeValue.objects.get_or_create(project=project, color='#00ADEA', data_type=_mode, name='bikesharing',
                                value='BIKESHARING')

TypeValue.objects.get_or_create(project=project, color='#F0DBEA', data_type=_mode, name='ride-pooling',
                                value='RIDE_POOLING')

TypeValue.objects.get_or_create(project=project, color='#D793C0', data_type=_mode, name='ride-hailing',
                                value='RIDE_HAILING')

TypeValue.objects.get_or_create(project=project, color='#BC1B8D', data_type=_mode, name='premium ride-hailing',
                                value='PREMIUM_RIDE_HAILING')
