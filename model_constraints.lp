\ Model HR_Scheduling
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  T_f
Subject To
 one_start_human: start[room_1,human] + start[room_2,human]
   + start[room_3,human] + start[room_4,human] + start[room_5,human]
   + start[room_6,human] = 1
 one_end_human: end[room_1,human] + end[room_2,human] + end[room_3,human]
   + end[room_4,human] + end[room_5,human] + end[room_6,human] = 1
 no_self_loop_room_1_human: x[room_1,room_1,human] = 0
 no_start_room_1_human: start[room_1,human] = 0
 no_end_room_1_human: end[room_1,human] = 0
 start_path_room_1_human: x[room_1,room_1,human] + x[room_2,room_1,human]
   + x[room_3,room_1,human] + x[room_4,room_1,human]
   + x[room_5,room_1,human] + x[room_6,room_1,human] + start[room_1,human]
   = 0
 end_path_room_1_human: x[room_1,room_1,human] + x[room_1,room_2,human]
   + x[room_1,room_3,human] + x[room_1,room_4,human]
   + x[room_1,room_5,human] + x[room_1,room_6,human] + end[room_1,human]
   = 0
 timeline_room_2_room_1_human: - 1e+06 x[room_2,room_1,human] + t_s[room_1]
   - t_s[room_2] >= -999946
 timeline_room_3_room_1_human: - 1e+06 x[room_3,room_1,human] + t_s[room_1]
   - t_s[room_3] >= -999896
 timeline_room_4_room_1_human: - 1e+06 x[room_4,room_1,human] + t_s[room_1]
   - t_s[room_4] >= -999842
 timeline_room_5_room_1_human: - 1e+06 x[room_5,room_1,human] + t_s[room_1]
   - t_s[room_5] >= -999834
 timeline_room_6_room_1_human: - 1e+06 x[room_6,room_1,human] + t_s[room_1]
   - t_s[room_6] >= -999716.4854746513
 timeline_start_room_1_human: - 1e+06 start[room_1,human] + t_s[room_1]
   >= -999852
 makespan_room_1_human: - 1.0001127696767753e+06 end[room_1,human]
   - 73.59347797189639 end[room_2,human] - 54 end[room_3,human]
   - 72.91776189653656 end[room_4,human]
   - 142.1442928857856 end[room_5,human]
   - 113.5957745693034 end[room_6,human] - t_s[room_1] + T_f >= -999995
 no_self_loop_room_2_human: x[room_2,room_2,human] = 0
 no_start_room_2_human: start[room_2,human] = 0
 no_end_room_2_human: end[room_2,human] = 0
 start_path_room_2_human: x[room_1,room_2,human] + x[room_2,room_2,human]
   + x[room_3,room_2,human] + x[room_4,room_2,human]
   + x[room_5,room_2,human] + x[room_6,room_2,human] + start[room_2,human]
   = 0
 end_path_room_2_human: x[room_2,room_1,human] + x[room_2,room_2,human]
   + x[room_2,room_3,human] + x[room_2,room_4,human]
   + x[room_2,room_5,human] + x[room_2,room_6,human] + end[room_2,human]
   = 0
 timeline_room_1_room_2_human: - 1e+06 x[room_1,room_2,human] - t_s[room_1]
   + t_s[room_2] >= -999946
 timeline_room_3_room_2_human: - 1e+06 x[room_3,room_2,human] + t_s[room_2]
   - t_s[room_3] >= -999945
 timeline_room_4_room_2_human: - 1e+06 x[room_4,room_2,human] + t_s[room_2]
   - t_s[room_4] >= -999891
 timeline_room_5_room_2_human: - 1e+06 x[room_5,room_2,human] + t_s[room_2]
   - t_s[room_5] >= -999826.4854746513
 timeline_room_6_room_2_human: - 1e+06 x[room_6,room_2,human] + t_s[room_2]
   - t_s[room_6] >= -999724
 timeline_start_room_2_human: - 1e+06 start[room_2,human] + t_s[room_2]
   >= -999901
 makespan_room_2_human: - 112.769676775275 end[room_1,human]
   - 1.0000735934779719e+06 end[room_2,human] - 54 end[room_3,human]
   - 72.91776189653656 end[room_4,human]
   - 142.1442928857856 end[room_5,human]
   - 113.5957745693034 end[room_6,human] - t_s[room_2] + T_f >= -999995
 no_self_loop_room_3_human: x[room_3,room_3,human] = 0
 start_path_room_3_human: x[room_1,room_3,human] + x[room_2,room_3,human]
   + x[room_4,room_3,human] + x[room_5,room_3,human]
   + x[room_6,room_3,human] + start[room_3,human] = 1
 end_path_room_3_human: x[room_3,room_1,human] + x[room_3,room_2,human]
   + x[room_3,room_4,human] + x[room_3,room_5,human]
   + x[room_3,room_6,human] + end[room_3,human] = 1
 timeline_room_1_room_3_human: - 1e+06 x[room_1,room_3,human] - t_s[room_1]
   + t_s[room_3] >= -999896
 timeline_room_2_room_3_human: - 1e+06 x[room_2,room_3,human] - t_s[room_2]
   + t_s[room_3] >= -999945
 timeline_room_4_room_3_human: - 1e+06 x[room_4,room_3,human] + t_s[room_3]
   - t_s[room_4] >= -999941
 timeline_room_5_room_3_human: - 1e+06 x[room_5,room_3,human] + t_s[room_3]
   - t_s[room_5] >= -999805.2379909181
 timeline_room_6_room_3_human: - 1e+06 x[room_6,room_3,human] + t_s[room_3]
   - t_s[room_6] >= -999716.1830289622
 timeline_start_room_3_human: - 1e+06 start[room_3,human] + t_s[room_3]
   >= -999951
 makespan_room_3_human: - 112.769676775275 end[room_1,human]
   - 73.59347797189639 end[room_2,human] - 1.000054e+06 end[room_3,human]
   - 72.91776189653656 end[room_4,human]
   - 142.1442928857856 end[room_5,human]
   - 113.5957745693034 end[room_6,human] - t_s[room_3] + T_f >= -999995
 no_self_loop_room_4_human: x[room_4,room_4,human] = 0
 start_path_room_4_human: x[room_1,room_4,human] + x[room_2,room_4,human]
   + x[room_3,room_4,human] + x[room_5,room_4,human]
   + x[room_6,room_4,human] + start[room_4,human] = 1
 end_path_room_4_human: x[room_4,room_1,human] + x[room_4,room_2,human]
   + x[room_4,room_3,human] + x[room_4,room_5,human]
   + x[room_4,room_6,human] + end[room_4,human] = 1
 timeline_room_1_room_4_human: - 1e+06 x[room_1,room_4,human] - t_s[room_1]
   + t_s[room_4] >= -999847
 timeline_room_2_room_4_human: - 1e+06 x[room_2,room_4,human] - t_s[room_2]
   + t_s[room_4] >= -999896
 timeline_room_3_room_4_human: - 1e+06 x[room_3,room_4,human] - t_s[room_3]
   + t_s[room_4] >= -999946
 timeline_room_5_room_4_human: - 1e+06 x[room_5,room_4,human] + t_s[room_4]
   - t_s[room_5] >= -999774.9651191086
 timeline_room_6_room_4_human: - 1e+06 x[room_6,room_4,human] + t_s[room_4]
   - t_s[room_6] >= -999695.2379909181
 timeline_start_room_4_human: - 1e+06 start[room_4,human] + t_s[room_4]
   >= -1e+06
 makespan_room_4_human: - 112.769676775275 end[room_1,human]
   - 73.59347797189639 end[room_2,human] - 54 end[room_3,human]
   - 1.0000729177618965e+06 end[room_4,human]
   - 142.1442928857856 end[room_5,human]
   - 113.5957745693034 end[room_6,human] - t_s[room_4] + T_f >= -999990
 no_self_loop_room_5_human: x[room_5,room_5,human] = 0
 no_start_room_5_human: start[room_5,human] = 0
 no_end_room_5_human: end[room_5,human] = 0
 start_path_room_5_human: x[room_1,room_5,human] + x[room_2,room_5,human]
   + x[room_3,room_5,human] + x[room_4,room_5,human]
   + x[room_5,room_5,human] + x[room_6,room_5,human] + start[room_5,human]
   = 0
 end_path_room_5_human: x[room_5,room_1,human] + x[room_5,room_2,human]
   + x[room_5,room_3,human] + x[room_5,room_4,human]
   + x[room_5,room_5,human] + x[room_5,room_6,human] + end[room_5,human]
   = 0
 timeline_room_1_room_5_human: - 1e+06 x[room_1,room_5,human] - t_s[room_1]
   + t_s[room_5] >= -999839
 timeline_room_2_room_5_human: - 1e+06 x[room_2,room_5,human] - t_s[room_2]
   + t_s[room_5] >= -999831.4854746513
 timeline_room_3_room_5_human: - 1e+06 x[room_3,room_5,human] - t_s[room_3]
   + t_s[room_5] >= -999810.2379909181
 timeline_room_4_room_5_human: - 1e+06 x[room_4,room_5,human] - t_s[room_4]
   + t_s[room_5] >= -999774.9651191086
 timeline_room_6_room_5_human: - 1e+06 x[room_6,room_5,human] + t_s[room_5]
   - t_s[room_6] >= -999831
 timeline_start_room_5_human: - 1e+06 start[room_5,human] + t_s[room_5]
   >= -999784.9651191086
 makespan_room_5_human: - 112.769676775275 end[room_1,human]
   - 73.59347797189639 end[room_2,human] - 54 end[room_3,human]
   - 72.91776189653656 end[room_4,human]
   - 1.0001421442928858e+06 end[room_5,human]
   - 113.5957745693034 end[room_6,human] - t_s[room_5] + T_f >= -999990
 no_self_loop_room_6_human: x[room_6,room_6,human] = 0
 no_start_room_6_human: start[room_6,human] = 0
 no_end_room_6_human: end[room_6,human] = 0
 start_path_room_6_human: x[room_1,room_6,human] + x[room_2,room_6,human]
   + x[room_3,room_6,human] + x[room_4,room_6,human]
   + x[room_5,room_6,human] + x[room_6,room_6,human] + start[room_6,human]
   = 0
 end_path_room_6_human: x[room_6,room_1,human] + x[room_6,room_2,human]
   + x[room_6,room_3,human] + x[room_6,room_4,human]
   + x[room_6,room_5,human] + x[room_6,room_6,human] + end[room_6,human]
   = 0
 timeline_room_1_room_6_human: - 1e+06 x[room_1,room_6,human] - t_s[room_1]
   + t_s[room_6] >= -999831.4854746513
 timeline_room_2_room_6_human: - 1e+06 x[room_2,room_6,human] - t_s[room_2]
   + t_s[room_6] >= -999839
 timeline_room_3_room_6_human: - 1e+06 x[room_3,room_6,human] - t_s[room_3]
   + t_s[room_6] >= -999831.1830289622
 timeline_room_4_room_6_human: - 1e+06 x[room_4,room_6,human] - t_s[room_4]
   + t_s[room_6] >= -999805.2379909181
 timeline_room_5_room_6_human: - 1e+06 x[room_5,room_6,human] - t_s[room_5]
   + t_s[room_6] >= -999941
 timeline_start_room_6_human: - 1e+06 start[room_6,human] + t_s[room_6]
   >= -999815.2379909181
 makespan_room_6_human: - 112.769676775275 end[room_1,human]
   - 73.59347797189639 end[room_2,human] - 54 end[room_3,human]
   - 72.91776189653656 end[room_4,human]
   - 142.1442928857856 end[room_5,human]
   - 1.0001135957745693e+06 end[room_6,human] - t_s[room_6] + T_f
   >= -999880
 one_start_robot: start[room_1,robot] + start[room_2,robot]
   + start[room_3,robot] + start[room_4,robot] + start[room_5,robot]
   + start[room_6,robot] = 1
 one_end_robot: end[room_1,robot] + end[room_2,robot] + end[room_3,robot]
   + end[room_4,robot] + end[room_5,robot] + end[room_6,robot] = 1
 no_self_loop_room_1_robot: x[room_1,room_1,robot] = 0
 no_start_room_1_robot: start[room_1,robot] = 0
 no_end_room_1_robot: end[room_1,robot] = 0
 start_path_room_1_robot: x[room_1,room_1,robot] + x[room_2,room_1,robot]
   + x[room_3,room_1,robot] + x[room_4,room_1,robot]
   + x[room_5,room_1,robot] + x[room_6,room_1,robot] + start[room_1,robot]
   = 0
 end_path_room_1_robot: x[room_1,room_1,robot] + x[room_1,room_2,robot]
   + x[room_1,room_3,robot] + x[room_1,room_4,robot]
   + x[room_1,room_5,robot] + x[room_1,room_6,robot] + end[room_1,robot]
   = 0
 timeline_room_2_room_1_robot: - 1e+06 x[room_2,room_1,robot] + t_s[room_1]
   - t_s[room_2] >= -999913.3333333334
 timeline_room_3_room_1_robot: - 1e+06 x[room_3,room_1,robot] + t_s[room_1]
   - t_s[room_3] >= -999830
 timeline_room_4_room_1_robot: - 1e+06 x[room_4,room_1,robot] + t_s[room_1]
   - t_s[room_4] >= -999743.3333333334
 timeline_room_5_room_1_robot: - 1e+06 x[room_5,room_1,robot] + t_s[room_1]
   - t_s[room_5] >= -999730
 timeline_room_6_room_1_robot: - 1e+06 x[room_6,room_1,robot] + t_s[room_1]
   - t_s[room_6] >= -999607.4757910855
 timeline_start_room_1_robot: - 1e+06 start[room_1,robot] + t_s[room_1]
   >= -999727.4757910855
 makespan_room_1_robot: - 1.0002466666666666e+06 end[room_1,robot]
   - 165 end[room_2,robot] - 81.66666666666667 end[room_3,robot]
   - 358.3914681524163 end[room_5,robot]
   - 307.9366818032565 end[room_6,robot] - t_s[room_1] + T_f >= -999995
 no_self_loop_room_2_robot: x[room_2,room_2,robot] = 0
 no_start_room_2_robot: start[room_2,robot] = 0
 no_end_room_2_robot: end[room_2,robot] = 0
 start_path_room_2_robot: x[room_1,room_2,robot] + x[room_2,room_2,robot]
   + x[room_3,room_2,robot] + x[room_4,room_2,robot]
   + x[room_5,room_2,robot] + x[room_6,room_2,robot] + start[room_2,robot]
   = 0
 end_path_room_2_robot: x[room_2,room_1,robot] + x[room_2,room_2,robot]
   + x[room_2,room_3,robot] + x[room_2,room_4,robot]
   + x[room_2,room_5,robot] + x[room_2,room_6,robot] + end[room_2,robot]
   = 0
 timeline_room_1_room_2_robot: - 1e+06 x[room_1,room_2,robot] - t_s[room_1]
   + t_s[room_2] >= -999913.3333333334
 timeline_room_3_room_2_robot: - 1e+06 x[room_3,room_2,robot] + t_s[room_2]
   - t_s[room_3] >= -999911.6666666666
 timeline_room_4_room_2_robot: - 1e+06 x[room_4,room_2,robot] + t_s[room_2]
   - t_s[room_4] >= -999825
 timeline_room_5_room_2_robot: - 1e+06 x[room_5,room_2,robot] + t_s[room_2]
   - t_s[room_5] >= -999717.4757910855
 timeline_room_6_room_2_robot: - 1e+06 x[room_6,room_2,robot] + t_s[room_2]
   - t_s[room_6] >= -999620
 timeline_start_room_2_robot: - 1e+06 start[room_2,robot] + t_s[room_2]
   >= -999740
 makespan_room_2_robot: - 246.6666666666667 end[room_1,robot]
   - 1.000165e+06 end[room_2,robot] - 81.66666666666667 end[room_3,robot]
   - 358.3914681524163 end[room_5,robot]
   - 307.9366818032565 end[room_6,robot] - t_s[room_2] + T_f >= -999995
 no_self_loop_room_3_robot: x[room_3,room_3,robot] = 0
 no_start_room_3_robot: start[room_3,robot] = 0
 no_end_room_3_robot: end[room_3,robot] = 0
 start_path_room_3_robot: x[room_1,room_3,robot] + x[room_2,room_3,robot]
   + x[room_3,room_3,robot] + x[room_4,room_3,robot]
   + x[room_5,room_3,robot] + x[room_6,room_3,robot] + start[room_3,robot]
   = 0
 end_path_room_3_robot: x[room_3,room_1,robot] + x[room_3,room_2,robot]
   + x[room_3,room_3,robot] + x[room_3,room_4,robot]
   + x[room_3,room_5,robot] + x[room_3,room_6,robot] + end[room_3,robot]
   = 0
 timeline_room_1_room_3_robot: - 1e+06 x[room_1,room_3,robot] - t_s[room_1]
   + t_s[room_3] >= -999830
 timeline_room_2_room_3_robot: - 1e+06 x[room_2,room_3,robot] - t_s[room_2]
   + t_s[room_3] >= -999911.6666666666
 timeline_room_4_room_3_robot: - 1e+06 x[room_4,room_3,robot] + t_s[room_3]
   - t_s[room_4] >= -999908.3333333334
 timeline_room_5_room_3_robot: - 1e+06 x[room_5,room_3,robot] + t_s[room_3]
   - t_s[room_5] >= -999682.0633181968
 timeline_room_6_room_3_robot: - 1e+06 x[room_6,room_3,robot] + t_s[room_3]
   - t_s[room_6] >= -999606.971714937
 timeline_start_room_3_robot: - 1e+06 start[room_3,robot] + t_s[room_3]
   >= -999726.971714937
 makespan_room_3_robot: - 246.6666666666667 end[room_1,robot]
   - 165 end[room_2,robot] - 1.0000816666666666e+06 end[room_3,robot]
   - 358.3914681524163 end[room_5,robot]
   - 307.9366818032565 end[room_6,robot] - t_s[room_3] + T_f >= -999995
 no_self_loop_room_4_robot: x[room_4,room_4,robot] = 0
 start_path_room_4_robot: x[room_1,room_4,robot] + x[room_2,room_4,robot]
   + x[room_3,room_4,robot] + x[room_5,room_4,robot]
   + x[room_6,room_4,robot] + start[room_4,robot] = 1
 end_path_room_4_robot: x[room_4,room_1,robot] + x[room_4,room_2,robot]
   + x[room_4,room_3,robot] + x[room_4,room_5,robot]
   + x[room_4,room_6,robot] + end[room_4,robot] = 1
 timeline_room_1_room_4_robot: - 1e+06 x[room_1,room_4,robot] - t_s[room_1]
   + t_s[room_4] >= -999748.3333333334
 timeline_room_2_room_4_robot: - 1e+06 x[room_2,room_4,robot] - t_s[room_2]
   + t_s[room_4] >= -999830
 timeline_room_3_room_4_robot: - 1e+06 x[room_3,room_4,robot] - t_s[room_3]
   + t_s[room_4] >= -999913.3333333334
 timeline_room_5_room_4_robot: - 1e+06 x[room_5,room_4,robot] + t_s[room_4]
   - t_s[room_5] >= -999631.6085318476
 timeline_room_6_room_4_robot: - 1e+06 x[room_6,room_4,robot] + t_s[room_4]
   - t_s[room_6] >= -999572.0633181968
 timeline_start_room_4_robot: - 1e+06 start[room_4,robot] + t_s[room_4]
   >= -999692.0633181968
 makespan_room_4_robot: - 246.6666666666667 end[room_1,robot]
   - 165 end[room_2,robot] - 81.66666666666667 end[room_3,robot]
   - 1e+06 end[room_4,robot] - 358.3914681524163 end[room_5,robot]
   - 307.9366818032565 end[room_6,robot] - t_s[room_4] + T_f >= -999990
 no_self_loop_room_5_robot: x[room_5,room_5,robot] = 0
 no_start_room_5_robot: start[room_5,robot] = 0
 no_end_room_5_robot: end[room_5,robot] = 0
 start_path_room_5_robot: x[room_1,room_5,robot] + x[room_2,room_5,robot]
   + x[room_3,room_5,robot] + x[room_4,room_5,robot]
   + x[room_5,room_5,robot] + x[room_6,room_5,robot] + start[room_5,robot]
   = 0
 end_path_room_5_robot: x[room_5,room_1,robot] + x[room_5,room_2,robot]
   + x[room_5,room_3,robot] + x[room_5,room_4,robot]
   + x[room_5,room_5,robot] + x[room_5,room_6,robot] + end[room_5,robot]
   = 0
 timeline_room_1_room_5_robot: - 1e+06 x[room_1,room_5,robot] - t_s[room_1]
   + t_s[room_5] >= -999735
 timeline_room_2_room_5_robot: - 1e+06 x[room_2,room_5,robot] - t_s[room_2]
   + t_s[room_5] >= -999722.4757910855
 timeline_room_3_room_5_robot: - 1e+06 x[room_3,room_5,robot] - t_s[room_3]
   + t_s[room_5] >= -999687.0633181968
 timeline_room_4_room_5_robot: - 1e+06 x[room_4,room_5,robot] - t_s[room_4]
   + t_s[room_5] >= -999631.6085318476
 timeline_room_6_room_5_robot: - 1e+06 x[room_6,room_5,robot] + t_s[room_5]
   - t_s[room_6] >= -999798.3333333334
 timeline_start_room_5_robot: - 1e+06 start[room_5,robot] + t_s[room_5]
   >= -999918.3333333334
 makespan_room_5_robot: - 246.6666666666667 end[room_1,robot]
   - 165 end[room_2,robot] - 81.66666666666667 end[room_3,robot]
   - 1.0003583914681524e+06 end[room_5,robot]
   - 307.9366818032565 end[room_6,robot] - t_s[room_5] + T_f >= -999990
 no_self_loop_room_6_robot: x[room_6,room_6,robot] = 0
 start_path_room_6_robot: x[room_1,room_6,robot] + x[room_2,room_6,robot]
   + x[room_3,room_6,robot] + x[room_4,room_6,robot]
   + x[room_5,room_6,robot] + start[room_6,robot] = 1
 end_path_room_6_robot: x[room_6,room_1,robot] + x[room_6,room_2,robot]
   + x[room_6,room_3,robot] + x[room_6,room_4,robot]
   + x[room_6,room_5,robot] + end[room_6,robot] = 1
 timeline_room_1_room_6_robot: - 1e+06 x[room_1,room_6,robot] - t_s[room_1]
   + t_s[room_6] >= -999722.4757910855
 timeline_room_2_room_6_robot: - 1e+06 x[room_2,room_6,robot] - t_s[room_2]
   + t_s[room_6] >= -999735
 timeline_room_3_room_6_robot: - 1e+06 x[room_3,room_6,robot] - t_s[room_3]
   + t_s[room_6] >= -999721.971714937
 timeline_room_4_room_6_robot: - 1e+06 x[room_4,room_6,robot] - t_s[room_4]
   + t_s[room_6] >= -999682.0633181968
 timeline_room_5_room_6_robot: - 1e+06 x[room_5,room_6,robot] - t_s[room_5]
   + t_s[room_6] >= -999908.3333333334
 timeline_start_room_6_robot: - 1e+06 start[room_6,robot] + t_s[room_6]
   >= -1e+06
 makespan_room_6_robot: - 246.6666666666667 end[room_1,robot]
   - 165 end[room_2,robot] - 81.66666666666667 end[room_3,robot]
   - 358.3914681524163 end[room_5,robot]
   - 1.0003079366818032e+06 end[room_6,robot] - t_s[room_6] + T_f
   >= -999880
Bounds
Binaries
 x[room_1,room_1,human] x[room_1,room_1,robot] x[room_1,room_2,human]
 x[room_1,room_2,robot] x[room_1,room_3,human] x[room_1,room_3,robot]
 x[room_1,room_4,human] x[room_1,room_4,robot] x[room_1,room_5,human]
 x[room_1,room_5,robot] x[room_1,room_6,human] x[room_1,room_6,robot]
 x[room_2,room_1,human] x[room_2,room_1,robot] x[room_2,room_2,human]
 x[room_2,room_2,robot] x[room_2,room_3,human] x[room_2,room_3,robot]
 x[room_2,room_4,human] x[room_2,room_4,robot] x[room_2,room_5,human]
 x[room_2,room_5,robot] x[room_2,room_6,human] x[room_2,room_6,robot]
 x[room_3,room_1,human] x[room_3,room_1,robot] x[room_3,room_2,human]
 x[room_3,room_2,robot] x[room_3,room_3,human] x[room_3,room_3,robot]
 x[room_3,room_4,human] x[room_3,room_4,robot] x[room_3,room_5,human]
 x[room_3,room_5,robot] x[room_3,room_6,human] x[room_3,room_6,robot]
 x[room_4,room_1,human] x[room_4,room_1,robot] x[room_4,room_2,human]
 x[room_4,room_2,robot] x[room_4,room_3,human] x[room_4,room_3,robot]
 x[room_4,room_4,human] x[room_4,room_4,robot] x[room_4,room_5,human]
 x[room_4,room_5,robot] x[room_4,room_6,human] x[room_4,room_6,robot]
 x[room_5,room_1,human] x[room_5,room_1,robot] x[room_5,room_2,human]
 x[room_5,room_2,robot] x[room_5,room_3,human] x[room_5,room_3,robot]
 x[room_5,room_4,human] x[room_5,room_4,robot] x[room_5,room_5,human]
 x[room_5,room_5,robot] x[room_5,room_6,human] x[room_5,room_6,robot]
 x[room_6,room_1,human] x[room_6,room_1,robot] x[room_6,room_2,human]
 x[room_6,room_2,robot] x[room_6,room_3,human] x[room_6,room_3,robot]
 x[room_6,room_4,human] x[room_6,room_4,robot] x[room_6,room_5,human]
 x[room_6,room_5,robot] x[room_6,room_6,human] x[room_6,room_6,robot]
 start[room_1,human] start[room_1,robot] start[room_2,human]
 start[room_2,robot] start[room_3,human] start[room_3,robot]
 start[room_4,human] start[room_4,robot] start[room_5,human]
 start[room_5,robot] start[room_6,human] start[room_6,robot]
 end[room_1,human] end[room_1,robot] end[room_2,human] end[room_2,robot]
 end[room_3,human] end[room_3,robot] end[room_4,human] end[room_4,robot]
 end[room_5,human] end[room_5,robot] end[room_6,human] end[room_6,robot]
End
