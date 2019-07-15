
def headers(self):
    
        '''
        img_file_name
        img_rank	
        object_id	
        object_link	
        object_lat	
        object_lon	
        object_date	
        object_time	
        object_depth_min	
        object_depth_max	
        object_lat_end	
        object_lon_end	
        object_area	
        object_mean	
        object_stddev	
        object_mode	
        object_min	
        object_max	
        object_x	
        object_y	
        object_xm	
        object_ym	
        object_perim.	
        object_bx	
        object_by	
        object_width	
        object_height	
        object_major	
        object_minor	
        object_angle	
        object_circ.	
        object_feret	
        object_intden	
        object_median	
        object_skew	
        object_kurt	
        object_%area	
        object_xstart	
        object_ystart	
        object_area_exc	
        object_fractal	
        object_skelarea	
        object_tag	
        object_esd	
        object_elongation	
        object_range	
        object_meanpos	
        object_centroids	
        object_cv	
        object_sr	
        object_perimareaexc	
        object_feretareaexc	
        object_perimferet	
        object_perimmajor	
        object_circex	
        object_cdexc	
        process_id	
        process_date	
        process_time	
        process_img_software_version
        process_img_resolution	
        process_img_od_grey	
        process_img_od_std	
        process_img_background_img	
        process_particle_version	
        process_particle_threshold	
        process_particle_pixel_size_mm	
        process_particle_min_size_mm	
        process_particle_max_size_mm	
        process_particle_sep_mask	
        process_particle_bw_ratio
        process_software	
        acq_id	
        acq_min_mesh	
        acq_max_mesh	
        acq_sub_part	
        acq_sub_method	
        acq_hardware	
        acq_software	
        acq_author	
        acq_imgtype	
        acq_scan_date	
        acq_scan_time	
        acq_quality	
        acq_bitpixel	
        acq_greyfrom	
        acq_scan_resolution	
        acq_rotation	
        acq_miror	
        acq_xsize	
        acq_ysize	
        acq_xoffset	
        acq_yoffset	
        acq_lut_color_balance	
        acq_lut_filter	
        acq_lut_min	
        acq_lut_max	
        acq_lut_odrange	
        acq_lut_ratio	
        acq_lut_16b_median	
        acq_instrument	
        sample_id	
        sample_scan_operator	
        sample_ship	
        sample_program	
        sample_stationid	
        sample_bottomdepth	
        sample_ctdrosettefilename	
        sample_other_ref	
        sample_tow_nb	
        sample_tow_type	
        sample_net_type	
        sample_net_mesh	
        sample_net_surf	
        sample_zmax	
        sample_zmin	
        sample_tot_vol	
        sample_comment	
        sample_tot_vol_qc	
        sample_depth_qc	
        sample_sample_qc	
        sample_barcode	
        sample_duration	
        sample_ship_speed	
        sample_cable_length	
        sample_cable_angle	
        sample_cable_speed	
        sample_nb_jar	
        sample_dataportal_descriptor	
        sample_open
        '''

        return ['img_file_name',
        'img_rank'	,
        'object_id'	,
        'object_link',	
        'object_lat',	
        'object_lon',	
        'object_date',	
        'object_time',	
        'object_depth_min',
        'object_depth_max',	
        'object_lat_end'	,
        'object_lon_end'	,
        'object_area'	,
        'object_mean'	,
        'object_stddev'	,
        'object_mode'	,
        'object_min'	,
        'object_max'	,
        'object_x'	,
        'object_y'	,
        'object_xm'	,
        'object_ym'	,
        'object_perim.',	
        'object_bx'	,
        'object_by'	,
        'object_width',	
        'object_height',	
        'object_major'	,
        'object_minor'	,
        'object_angle'	,
        'object_circ.'	,
        'object_feret'	,
        'object_intden'	,
        'object_median'	,
        'object_skew'	,
        'object_kurt'	,
        'object_%area'	,
        'object_xstart'	,
        'object_ystart'	,
        'object_area_exc',	
        'object_fractal',	
        'object_skelarea',	
        'object_tag'	,
        'object_esd'	,
        'object_elongation',	
        'object_range'	,
        'object_meanpos',	
        'object_centroids',	
        'object_cv'	,
        'object_sr'	,
        'object_perimareaexc',	
        'object_feretareaexc',	
        'object_perimferet'	,
        'object_perimmajor'	,
        'object_circex'	,
        'object_cdexc'	,
        'process_id'	,
        'process_date'	,
        'process_time'	,
        'process_img_software_version',
        'process_img_resolution'	,
        'process_img_od_grey'	,
        'process_img_od_std'	,
        'process_img_background_img',	
        'process_particle_version'	,
        'process_particle_threshold',	
        'process_particle_pixel_size_mm',	
        'process_particle_min_size_mm'	,
        'process_particle_max_size_mm'	,
        'process_particle_sep_mask'	,
        'process_particle_bw_ratio',
        'process_software'	,
        'acq_id'	,
        'acq_min_mesh',	
        'acq_max_mesh',	
        'acq_sub_part',	
        'acq_sub_method',	
        'acq_hardware'	,
        'acq_software'	,
        'acq_author'	,
        'acq_imgtype'	,
        'acq_scan_date'	,
        'acq_scan_time'	,
        'acq_quality'	,
        'acq_bitpixel'	,
        'acq_greyfrom'	,
        'acq_scan_resolution',	
        'acq_rotation'	,
        'acq_miror'	,
        'acq_xsize'	,
        'acq_ysize'	,
        'acq_xoffset',	
        'acq_yoffset',	
        'acq_lut_color_balance',	
        'acq_lut_filter'	,
        'acq_lut_min'	,
        'acq_lut_max'	,
        'acq_lut_odrange',	
        'acq_lut_ratio'	,
        'acq_lut_16b_median',	
        'acq_instrument',	
        'sample_id'	,
        'sample_scan_operator',	
        'sample_ship'	,
        'sample_program'	,
        'sample_stationid'	,
        'sample_bottomdepth'	,
        'sample_ctdrosettefilename',	
        'sample_other_ref',	
        'sample_tow_nb'	,
        'sample_tow_type',	
        'sample_net_type',	
        'sample_net_mesh',	
        'sample_net_surf',	
        'sample_zmax'	,
        'sample_zmin'	,
        'sample_tot_vol'	,
        'sample_comment'	,
        'sample_tot_vol_qc'	,
        'sample_depth_qc'	,
        'sample_sample_qc'	,
        'sample_barcode'	,
        'sample_duration'	,
        'sample_ship_speed'	,
        'sample_cable_length',	
        'sample_cable_angle',	
        'sample_cable_speed',	
        'sample_nb_jar',	
        'sample_dataportal_descriptor',	
        'sample_open']

def headers2(self):
        '''
            Second row of headers
        '''
        return [    '[t]',
                    '[f]',	
                    '[t]',
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[t]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[f]',	
                    '[t]',	
                    '[t]']
