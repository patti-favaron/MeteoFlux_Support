#!/usr/bin/python3

# checkSite.py - Script, performing site-maintenance related checks on data
#                collected using the 'procGen.py' script
#
# Copyright 2023 Patrizia Favaron
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import datetime
import pandas

if __name__ == "__main__":

    # Read command-line parameters
    if len(sys.argv) != 3:
        print("checkSite.py - Maintenance-related data analysis\n")
        print("Usage:\n")
        print("  ./checkSite.py <Processed_File> <Out_Prefix>\n")
        print("Copyright 2024 by Servizi Territorio srl")
        print("                  All rights reserved\n")
        print("Written by: Patrizia Favaron\n")
        sys.exit(1)
    proc_file = sys.argv[1]
    prefix    = sys.argv[2]

    # Convert the loaded data to data frames
    print("Load data")

    zero_time = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    top_time  = datetime.datetime.strptime("9999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    pf = open(proc_file, "r")
    lines = pf.readlines()
    pf.close()
    time_stamp = []
    u_star     = []
    vels       = []
    dirs       = []
    tkes       = []
    phis       = []
    h0s        = []

    max_time = zero_time
    min_time = top_time

    for idx in range(1,len(lines)):

        blocks = lines[idx].split(",")
        time_val = datetime.datetime.strptime(blocks[0], "%Y-%m-%d %H:%M:%S")
        if time_val > zero_time:
            try:
                vel = float(blocks[3])
                if vel < 0.0 or vel > 60.0:
                    vel = None
            except:
                vel = None
            try:
                dir = float(blocks[7])
                if dir < 0.0 or dir > 360.0:
                    dir = None
            except:
                dir = None
            try:
                h0 = float(blocks[24])
            except:
                h0 = None
            try:
                tke = float(blocks[20])
            except:
                tke = None
            try:
                phi = float(blocks[11])
            except:
                phi = None
            try:
                us = float(blocks[21])
                if us <= 0.0:
                    us = None
            except:
                us = None

            if not (vel is None or dir is None or h0 is None or tke is None or phi is None or us is None):
                time_stamp.append(time_val)
                if time_val < min_time:
                    min_time = time_val
                if time_val > max_time:
                    max_time = time_val
                vels.append(vel)
                dirs.append(int(dir))
                tkes.append(tke)
                phis.append(phi)
                h0s.append(h0)
                u_star.append(us)

    print("- Data read: %d processed records found" % (len(time_stamp)))

    print("Check blind spots")
    dir_cnt = [0 for i in range(360)]
    for dir in dirs:
        if dir >= 0 and dir <= 359:
            dir_cnt[dir] += 1
    out_file = prefix + "_BlindSpots.csv"
    f = open(out_file, "w")
    f.write("Dir, Nr\n")
    for i in range(360):
        f.write("%3d, %d\n" % (i, dir_cnt[i]))
    f.close()

    print("Check obstructions nearby")
    friction_index = [0 for i in range(360)]
    num_data = [0 for i in range(360)]
    for i in range(len(dirs)):
        u_star_whg = 100.0 * u_star[i] / vels[i]
        dir_val = dirs[i]
        if dir_val >= 0 and dir_val <= 359 and u_star[i] > 0.0:
            friction_index[dir_val] += u_star[i]
            num_data[dir_val] += 1
    out_file = prefix + "_ObstructionIndex.csv"
    f = open(out_file, "w")
    f.write("Dir, Ustar_over_Vel\n")
    for i in range(360):
        f.write("%3d, %6.2f\n" % (i, 100.0 * friction_index[i] / num_data[i]))
    f.close()

    # Detect missing data and overall availability
    print("Timing and data availability")
    # -1- Detect averaging time, and check monotonicity
    deltas = []
    for i in range(len(time_stamp) - 1):
        deltas.append((time_stamp[i+1] - time_stamp[i]).total_seconds())
    avg_time = 1e6
    is_monotonic = True
    non_positive_runs = 0
    runs_from = []
    runs_to = []
    for i in range(len(deltas) - 1):
        if deltas[i] <= 0:
            is_monotonic = False
            non_positive_runs += 1
            runs_from.append(time_stamp[i])
            runs_to.append(time_stamp[i+1])
        if deltas[i] > 0 and deltas[i] < avg_time:
            avg_time = deltas[i]
    # -1- Is time regular?
    is_regular = True
    non_multiple_times = 0
    strange_times = []
    for i in range(len(deltas) - 1):
        if deltas[i] % avg_time != 0:
            is_regular = False
            non_multiple_times += 1
            strange_times.append(time_stamp[i])
    # -1- Compute time span
    time_span = ((max_time - min_time).total_seconds() + avg_time) / 86400.0
    # -1- Compute the "time defect", that is the number of seconds not
    #     covered by records, or otherwise invalid; then, scale result
    #     as availability fraction
    time_covered = len(time_stamp) * avg_time
    availability = 100.0 * time_covered / (time_span * 86400.0)
    # -1- Write report
    out_file = prefix + "_Availability.txt"
    f = open(out_file, "w")
    f.write("# Basic data timing properties\n\n")
    f.write("Averaging time, as inferred from data: %d seconds\n\n" % avg_time)
    if is_monotonic:
        f.write("Data set is time-monotonic, as expected\n\n")
    else:
        f.write("Data set is not time-monotonic, with %d negative or null runs\n\n" % non_positive_runs)
    if is_regular:
        f.write("Data set is time-regular, as expected\n\n")
    else:
        f.write("Data set is not time-regular, with %d times not exact multiples of averaging time\n\n" % non_multiple_times)
    f.write("# Overall availability\n\n")
    f.write("Data set time span: %6.2f days\n\n" % time_span)
    f.write("- Overall: %s - %s\n\n" % (datetime.datetime.strftime(min_time, "%Y-%m-%d %H:%M:%S"), datetime.datetime.strftime(max_time, "%Y-%m-%d %H:%M:%S")))
    f.write("Data availability: %8.4f percent\n\n" % availability)
    if non_positive_runs > 0:
        f.write("# Date and time glitches\n\n")
        f.write("From, To\n")
        for i in range(len(runs_from)):
            f.write("%s, %s\n" % (datetime.datetime.strftime(runs_from[i], "%Y-%m-%d %H:%M:%S"), datetime.datetime.strftime(runs_to[i], "%Y-%m-%d %H:%M:%S")))
        f.write("\n")
    if non_multiple_times > 0:
        f.write("# Time stamps not multiple of the averaging time\n\n")
        f.write("Time\n")
        for i in range(len(runs_from)):
            f.write("%s\n" % (datetime.datetime.strftime(runs_from[i], "%Y-%m-%d %H:%M:%S")))
        f.write("\n")
    f.close()

    # A bit of physics, for good
    print("H0 statistics")
    # -1- Sensible heat flux simple statistics
    h0_lower_outliers = 0
    h0_upper_outliers = 0
    h0_total_overall  = 0.
    h0_total_censored = 0.
    overall_data      = 0
    censored_data     = 0
    for h0 in h0s:
        if h0 < -200.0:
            h0_lower_outliers += 1
        if h0 > 1600:
            h0_upper_outliers += 1
        h0_total_overall += h0
        overall_data += 1
        if h0 >= -200.0 and h0 <= 1600.0:
            h0_total_censored += h0
            censored_data += 1
    # -1- Daily and monthly averages
    h0_dict = {}
    for i in range(len(time_stamp)):
        current_time = time_stamp[i]
        time_key     = current_time.month
        if h0s[i] >= -200.0 and h0s[i] <= 1600.0:
            try:
                gather = h0_dict[time_key]
            except:
                h0_dict[time_key] = []
            h0_dict[time_key].append(h0s[i])
    h0_monthly_neg = [0 for i in range(12)]
    h0_monthly_pos = [0 for i in range(12)]
    h0_monthly_tot = [0 for i in range(12)]
    h0_num_neg = [0 for i in range(12)]
    h0_num_pos = [0 for i in range(12)]
    for k in sorted(h0_dict.keys()):
        h0_this_month = h0_dict[k]
        month = k - 1
        for h0 in h0_this_month:
            if h0 >= 0.0:
                h0_monthly_pos[month] += h0
                h0_num_pos[month]     += 1
            else:
                h0_monthly_neg[month] += h0
                h0_num_neg[month]     += 1
    for month in range(12):
        if (h0_num_pos[month] + h0_num_neg[month]) > 0:
            h0_monthly_pos[month] /= (h0_num_pos[month] + h0_num_neg[month])
            h0_monthly_neg[month] /= (h0_num_pos[month] + h0_num_neg[month])
            h0_monthly_tot[month] = h0_monthly_pos[month] + h0_monthly_neg[month]
        else:
            h0_monthly_pos[month] = -9999.9
            h0_monthly_neg[month] = -9999.9
            h0_monthly_tot[month] = -9999.9
    # -1- Write report
    out_file = prefix + "_H0.txt"
    f = open(out_file, "w")
    f.write("# H0 energy flow\n\n")
    f.write("- Total balance expressed as mean, outliers included: %8.2f W/m2\n" % (h0_total_overall / overall_data))
    f.write("- Total balance expressed as mean, outliers excluded: %8.2f W/m2\n\n" % (h0_total_censored / censored_data))
    f.write("# Outliers\n\n")
    f.write("- Below -200 W/m2: %d\n" % h0_lower_outliers)
    f.write("- Above 1600 W/m2: %d\n\n" % h0_upper_outliers)
    f.write("# Monthly balances\n\n")
    f.write("Month, Negative_Mean, Positive_Mean, Total_Mean\n")
    for i in range(12):
        f.write("%2d, %9.3f, %9.3f, %9.3f\n" % (i+1, h0_monthly_neg[i], h0_monthly_pos[i], h0_monthly_tot[i]))
    f.write("\n")
    f.close()
