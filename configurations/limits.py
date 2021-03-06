from configurations import parameter

DEFAULT_VAL = 100

MODE_CHOICE_LIMITS = {
    "asc_car_d_mu": (0, 15),
    "asc_car_d_sig": (0, 5),
    "asc_car_p_mu": (0, 15),
    "asc_car_p_sig": (0, 5),
    "asc_put_mu": (0, 15),
    "asc_put_sig": (0, 5),
    "asc_ped_mu": (0, 15),
    "asc_ped_sig": (0, 5),
    "asc_bike_mu": (0, 15),
    "asc_bike_sig": (0, 5),
    "asc_cs_sb_mu": (0, 15),
    "asc_cs_sb_sig": (0, 5),
    "asc_cs_ff": (0, 15),
    "asc_taxi": (0, 15),
    "asc_bs": (0, 15),
    "asc_rp": (0, 15),
    "b_tt_car_p_mu": (-2, 0),
    "b_tt_car_p_sig": (0, 1),
    "b_tt_car_d_mu": (-2, 0),
    "b_tt_car_d_sig": (0, 1),
    "b_tt_put_mu": (-2, 0),
    "b_tt_put_sig": (0, 1),
    "b_tt_bike_mu": (-2, 0),
    "b_tt_bike_sig": (0, 1),
    "b_tt_bs": (-2, 0),
    "b_tt_taxi": (-2, 0),
    "b_tt_cs": (-2, 0),
    "b_tt_rp": (-2, 0),
    "b_tt_ped": (-0.8, 0),
    "b_cost": (-1, 0),
    "b_cost_put": (-1, 0),
    "b_inc_high_on_b_cost": (-1, 1),
    "b_inc_high_on_b_cost_put": (-1, 1),
    "b_u_put": (-1, 0),
    "b_zz_rp": (-1, 0),
    "b_wz_rp": (-1, 0),
    "b_logsum_acc_cs": (-1, 0),
    "elasticity_acc_cs": (-1, 0),
    "b_logsum_acc_put": (-5, 0),
    "elasticity_acc_put": (-1, 0),
    "b_park_car_d": (-5, 0),
    "elasticity_parken": (0.001, 1)
}

"""
    "b_mode_bef_put": (-5, 5),
    "b_mode_bef_ped": (-5, 5),
    "b_mode_bef_bike": (-5, 5),
    "female_on_asc_ped": (-5, 5),
    "female_on_asc_bike": (-5, 5),
    "female_on_asc_car_p": (-5, 5),
    "female_on_asc_car_d": (-5, 5),
    "female_on_asc_put": (-5, 5),
    "female_on_asc_cs": (-5, 5),
    "female_on_asc_bs": (-5, 5),
    "age_0_17_on_asc_car_p": (-5, 5),
    "age_0_17_on_asc_bike": (-5, 5),
    "age_0_17_on_asc_put": (-5, 5),
    "age_0_17_on_asc_ped": (-5, 5),
    "age_0_17_on_asc_taxi": (-5, 5),
    "age_18_29_on_asc_car_d": (-5, 5),
    "age_18_29_on_asc_car_p": (-5, 5),
    "age_18_29_on_asc_bike": (-5, 5),
    "age_18_29_on_asc_put": (-5, 5),
    "age_18_29_on_asc_ped": (-5, 5),
    "age_18_29_on_asc_cs": (-5, 5),
    "age_18_29_on_asc_bs": (-5, 5),
    "age_18_29_on_asc_rp": (-5, 5),
    "age_50_59_on_asc_car_d": (-5, 5),
    "age_50_59_on_asc_car_p": (-5, 5),
    "age_50_59_on_asc_bike": (-5, 5),
    "age_50_59_on_asc_put": (-5, 5),
    "age_50_59_on_asc_ped": (-5, 5),
    "age_50_59_on_asc_cs": (-5, 5),
    "age_50_59_on_asc_rp": (-5, 5),
    "age_60_69_on_asc_car_d": (-5, 5),
    "age_60_69_on_asc_car_p": (-5, 5),
    "age_60_69_on_asc_bike": (-5, 5),
    "age_60_69_on_asc_put": (-5, 5),
    "age_60_69_on_asc_ped": (-5, 5),
    "age_60_69_on_asc_rp": (-5, 5),
    "age_70_100_on_asc_car_d": (-5, 5),
    "age_70_100_on_asc_car_p": (-5, 5),
    "age_70_100_on_asc_bike": (-5, 5),
    "age_70_100_on_asc_put": (-5, 5),
    "age_70_100_on_asc_ped": (-5, 5),
    "student_on_asc_bike": (-5, 5),
    "student_on_asc_ped": (-5, 5),
    "student_on_asc_car_d": (-5, 5),
    "student_on_asc_car_p": (-5, 5),
    "student_on_asc_put": (-5, 5),
    "student_on_asc_rp": (-5, 5),
    "beruft_on_asc_ped": (-5, 5),
    "beruft_on_asc_bike": (-5, 5),
    "beruft_on_asc_car_p": (-5, 5),
    "beruft_on_asc_car_d": (-5, 5),
    "beruft_on_asc_put": (-5, 5),
    "beruft_on_asc_cs_sb": (-5, 5),
    "beruft_on_asc_rp": (-5, 5),
    "csmit_on_asc_ped": (-5, 5),
    "csmit_on_asc_bike": (-5, 5),
    "csmit_on_asc_car_d": (-5, 5),
    "csmit_on_asc_car_p": (-5, 5),
    "csmit_on_asc_put": (-5, 5),
    "csmit_on_asc_cs": (-5, 5),
    "csmit_on_sig_cs": (-5, 5),
    "pkw_0_on_asc_ped": (-5, 5),
    "pkw_0_on_asc_bike": (-5, 5),
    "pkw_0_on_asc_car_d": (-5, 5),
    "pkw_0_on_asc_car_p": (-5, 5),
    "pkw_0_on_asc_put": (-5, 5),
    "pkw_0_on_asc_cs": (-5, 5),
    "pkw_1_on_asc_ped": (-5, 5),
    "pkw_1_on_asc_bike": (-5, 5),
    "pkw_1_on_asc_car_d": (-5, 5),
    "pkw_1_on_asc_car_p": (-5, 5),
    "pkw_1_on_asc_put": (-5, 5),
    "pkw_1_on_asc_cs": (-5, 5),
    "hhgr_2_on_asc_ped": (-5, 5),
    "hhgr_2_on_asc_bike": (-5, 5),
    "hhgr_2_on_asc_car_d": (-5, 5),
    "hhgr_2_on_asc_car_p": (-5, 5),
    "hhgr_2_on_asc_cs": (-5, 5),
    "hhgr_2_on_asc_bs": (-5, 5),
    "hhgr_34_on_asc_car_d": (-5, 5),
    "hhgr_34_on_asc_car_p": (-5, 5),
    "hhgr_34_on_asc_put": (-5, 5),
    "hhgr_34_on_asc_bs": (-5, 5),
    "inc_low_on_asc_bike": (-5, 5),
    "inc_low_on_asc_put": (-5, 5),
    "inc_high_on_asc_bike": (-5, 5),
    "inc_high_on_asc_put": (-5, 5),
    "inc_low_on_asc_car_d": (-5, 5),
    "inc_high_on_asc_car_d": (-5, 5),
    "ebike_on_asc_bike": (-5, 5),
    "asc_shift_relief_high_ped": (-5, 5),
    "asc_shift_relief_high_bike": (-5, 5),
    "asc_shift_relief_high_car_d": (-5, 5),
    "asc_shift_relief_high_car_p": (-5, 5),
    "asc_shift_relief_high_put": (-5, 5),
    "b_arbeit_car_d": (-5, 5),
    "b_arbeit_car_p": (-5, 5),
    "b_arbeit_put": (-5, 5),
    "b_arbeit_bike": (-5, 5),
    "b_arbeit_ped": (-5, 5),
    "b_arbeit_cs": (-5, 5),
    "b_arbeit_bs": (-5, 5),
    "b_arbeit_rp": (-5, 5),
    "b_dienst_put": (-5, 5),
    "b_dienst_car_d": (-5, 5),
    "b_dienst_car_p": (-5, 5),
    "b_dienst_bike": (-5, 5),
    "b_dienst_ped": (-5, 5),
    "b_ausb_put": (-5, 5),
    "b_ausb_car_d": (-5, 5),
    "b_ausb_car_p": (-5, 5),
    "b_ausb_bike": (-5, 5),
    "b_ausb_ped": (-5, 5),
    "b_ausb_bs": (-5, 5),
    "b_eink_car_d": (-5, 5),
    "b_eink_car_p": (-5, 5),
    "b_eink_put": (-5, 5),
    "b_eink_bike": (-5, 5),
    "b_eink_bs": (-5, 5),
    "b_eink_ped": (-5, 5),
    "b_freiz_car_d": (-5, 5),
    "b_freiz_car_p": (-5, 5),
    "b_freiz_put": (-5, 5),
    "b_freiz_bike": (-5, 5),
    "b_freiz_ped": (-5, 5),
    "b_service_car_d": (-5, 5),
    "b_service_car_p": (-5, 5),
    "b_service_put": (-5, 5),
    "b_service_bike": (-5, 5),
    "b_service_ped": (-5, 5),
    "b_home_car_p": (-5, 5),
    "b_home_put": (-5, 5),
    "b_arbwo_ped": (-5, 5),
    "b_arbwo_bike": (-5, 5),
    "b_arbwo_car_p": (-5, 5),
    "b_arbwo_car_d": (-5, 5),
    "b_arbwo_put": (-5, 5),
    "age_0_17_on_b_tt_car_p": (-5, 5),
    "age_18_29_on_b_tt_car_p": (-5, 5),
    "age_50_59_on_b_tt_car_p": (-5, 5),
    "age_60_69_on_b_tt_car_p": (-5, 5),
    "age_70_100_on_b_tt_car_p": (-5, 5),
    "beruft_on_b_tt_car_p": (-5, 5),
    "age_18_29_on_b_tt_car_d": (-5, 5),
    "age_50_59_on_b_tt_car_d": (-5, 5),
    "age_60_69_on_b_tt_car_d": (-5, 5),
    "age_70_100_on_b_tt_car_d": (-5, 5),
    "beruft_on_b_tt_car_d": (-5, 5),
    "age_0_17_on_b_tt_put": (-5, 5),
    "age_18_29_on_b_tt_put": (-5, 5),
    "age_50_59_on_b_tt_put": (-5, 5),
    "age_60_69_on_b_tt_put": (-5, 5),
    "age_70_100_on_b_tt_put": (-5, 5),
    "beruft_on_b_tt_put": (-5, 5),
    "age_0_17_on_b_tt_bike": (-5, 5),
    "age_18_29_on_b_tt_bike": (-5, 5),
    "age_50_59_on_b_tt_bike": (-5, 5),
    "age_60_69_on_b_tt_bike": (-5, 5),
    "age_70_100_on_b_tt_bike": (-5, 5),
    "beruft_on_b_tt_bike": (-5, 5),
    "age_18_29_on_b_tt_cs": (-5, 5),
    "age_50_59_on_b_tt_cs": (-5, 5),
    "age_60_69_on_b_tt_cs": (-5, 5),
    "age_70_100_on_b_tt_cs": (-5, 5),
    "beruft_on_b_tt_cs": (-5, 5),
    "age_18_29_on_b_tt_rp": (-5, 5),
    "age_50_59_on_b_tt_rp": (-5, 5),
    "age_60_69_on_b_tt_rp": (-5, 5),
    "age_70_100_on_b_tt_rp": (-5, 5),
    "beruft_on_b_tt_rp": (-5, 5),
    "age_0_17_on_b_tt_ped": (-5, 5),
    "age_18_29_on_b_tt_ped": (-5, 5),
    "age_50_59_on_b_tt_ped": (-5, 5),
    "age_60_69_on_b_tt_ped": (-5, 5),
    "age_70_100_on_b_tt_ped": (-5, 5),
    "beruft_on_b_tt_ped": (-5, 5),
    "b_tt_arbeit_put": (-5, 5),
    "b_tt_ausb_put": (-5, 5),
    "b_tt_ausb_ped": (-5, 5),
    "b_tt_freiz_ped": (-5, 5),
    "b_tt_freiz_bike": (-5, 5),
    "b_tt_freiz_car_p": (-5, 5),
    "b_tt_dienst_bike": (-5, 5),
    "b_tt_dienst_ped": (-5, 5),
    "b_tt_service_car_d": (-5, 5),
    "b_tt_service_put": (-5, 5),
} """

DESTINATION_CHOICE_LIMITS = {
    "asc_car_d": (0, 100),
    "asc_car_p": (0, 100),
    "asc_put": (0, 100),
    "asc_ped": (0, 100),
    "asc_bike": (0, 100),
    "asc_cs_sb": (0, 100),
    "asc_cs_ff": (0, 100),
    "asc_taxi": (0, 100),
    "asc_bs": (0, 100),
    "asc_rp": (0, 100),
    "b_tt_car_d": (-1, 0),
    "b_tt_car_p": (-1, 0),
    "b_tt_put": (-1, 0),
    "b_tt_ped": (-1, 0),
    "b_tt_bike": (-1, 0),
    "b_tt_cs": (-1, 0),
    "b_tt_taxi": (-1, 0),
    "b_tt_rp": (-1, 0),
    "b_cost": (-1, 0),
    #"b_logsum_acc_put": (-50, 0),  # Disabled Parameter currently not impacting destination choice calculation
    #"elasticity_acc_put": (-1, 0), # Disabled Parameter currently not impacting destination choice calculation
    #"b_logsum_acc_cs": (-50, 50),  # Disabled Parameter currently not impacting destination choice calculation
    "b_tt_acc_put": (-1, 0)
}

DEFAULT_DICT = {
    "b_logsum_pt": (0, 2),
    "b_logsum_drive": (0, 2),
    "b_logsum_pt_fix": (0, 2),
    "b_logsum_drive_fix": (0, 2),
    "b_attr": (0, 2)
}


def generate_mode_choice_parameter_bounds(parameter_name):
    req = parameter.get_all_parameter_limitations(parameter_name)
    if parameter_name.__contains__("elasticity"):
        if parameter_name.__contains__("parken"):
            return 0, 1
        else:
            return -1, 0
    if len(req.keys()) == 1:
        if parameter_name.__contains__("asc_") and not parameter_name.__contains__("sig"):
            return -15, 15
        elif parameter_name.__contains__("asc_") and parameter_name.__contains__("sig"):
            return 0, 5
        elif parameter_name.__contains__("b_tt") and not parameter_name.__contains__("sig"):
            return -2, 0
        elif parameter_name.__contains__("b_tt") and parameter_name.__contains__("sig"):
            return 0, 1
        return -1, 0
    else:
        return -5, 5


def generate_destination_choice_parameter_bounds(parameter_name):
    if parameter_name.__contains__("asc_"):
        return 0, 100
    if parameter_name.__contains__("b_tt"):
        return -1, 0
