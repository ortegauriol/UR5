// Message definition file for DEcoding Movement Intention project
// Angus McMorland <amcmorl@gmail.com, a.mcmorland@auckland.ac.nz>
// November, 2013

// CHANGELOG
// 2015-09-15 added MT_FT_DATA and MDF_FT_DATA
// 2015-10-05 added RTFT_CONFIG and FT_COMPLETE and TOUCH_DETECT and FT_COMPLETE
// 2015-10-2 added RTFT_extra_settings
// 2015-10-23 changed RTFT_extra_settings to "double"
// 2015-10-29 added MAX_trials, MAX_value and removed RTFT_extra_settings
// 2016-07-26 added MNOME_STATE

/////////////////////////////////////////////////////////////////
// Common definitions
#include "common_defs.h"

#define DF_CONFIG_VERSION               03 // increment this every time you change a definition!!

// message IDs
#define MT_POLARIS_POSITION             5000
#define MT_DAQ_DATA                     5001
#define MT_MARKER_POSITION_COMMONSPACE  5002
#define MT_UR5_MOVEMENT_COMMAND         5003
#define MT_UR5_MOVEMENT_COMPLETE        5004
#define MT_DIO_DATA                     5005
#define MT_UR5_CONNECTED                5006
#define MT_UR5_REQUEST_CONNECTED        5007
#define MT_FT_DATA                      5008
#define MT_RTFT_CONFIG                  5009 
#define MT_FT_COMPLETE                  5010
#define MT_TOUCH_DETECT                 5011
#define MT_MAX_trials                   5012
#define MT_MAX_value                    5013
#define MT_HOTSPOT_POSITION             5014
#define MT_TMS_TRIGGER                  5015
#define MT_PLOT_POSITION                5016
#define MT_MNOME_STATE                  5017
#define MT_TRIGNO_DATA                  5018

// constants
#define DAQ_BUFSIZE            160
#define DIO_BUFSIZE            8

typedef struct {
    int     command_id;
    int     reserved; // for 64-bit alignment
    double  position[6];
    double  max_velocity;
    double  acceleration;
} MDF_UR5_MOVEMENT_COMMAND;

typedef struct {
    int     command_id;
    int     reserved; // for 64-bit alignment
} MDF_UR5_MOVEMENT_COMPLETE;

typedef struct {
    SAMPLE_HEADER sample_header;
    int     tool_id;
    int     missing;
    double  xyz[3];
    double  ori[4];
} MDF_POLARIS_POSITION;

typedef MDF_POLARIS_POSITION MDF_HOTSPOT_POSITION;

typedef MDF_POLARIS_POSITION MDF_PLOT_POSITION;

typedef struct {
    SAMPLE_HEADER sample_header;
    double  buffer[DAQ_BUFSIZE];
} MDF_DAQ_DATA;

typedef struct {
    SAMPLE_HEADER sample_header;
	int     buffer[DIO_BUFSIZE];
} MDF_DIO_DATA;

typedef struct {
    SAMPLE_HEADER sample_header;
    int     tool_id;
    int     missing;
    double  xyz[3];
    double  ori[4];
    int     calib_id;
    int     reserved; // for 64-bit alignment
} MDF_MARKER_POSITION_COMMONSPACE;

typedef struct {
    SAMPLE_HEADER sample_header;
    double F[30];
    double T[30];
} MDF_FT_DATA;

typedef struct {
    SAMPLE_HEADER sample_header;
    int    reserved;
    int    RTFT_display;
    int    shadow_cursor_visible; 
    int    shadow_target_visible;
    int    target_visible;
    int    cursor_visible; // 4 * 4 bytes * 8 bits/byte = 64 aligned
    double target_vector[3]; 
    double max_factor;
} MDF_RTFT_CONFIG;

typedef struct {
    int    ft_complete;
    int    reserved[3];
} MDF_FT_COMPLETE;

typedef struct {
    SAMPLE_HEADER sample_header;
    int     ft_touch_detect;  
    int     reserved; // for 64-bit alignment
    double  touch_threshold;
    double  hold_time;
} MDF_TOUCH_DETECT;

typedef struct {
    SAMPLE_HEADER sample_header; 
    double  target_vector[3];
    double  reserved;
} MDF_MAX_trials;

typedef struct {
    SAMPLE_HEADER sample_header; 
    double  max_factor;
    double  reserved;
} MDF_MAX_value;

typedef struct {
    SAMPLE_HEADER sample_header;
} MDF_TMS_TRIGGER;

typedef struct {
    SAMPLE_HEADER sample_header;
    int  state;
    int  reserved; // for 64-bit alignment
} MDF_MNOME_STATE;

typedef struct {
    SAMPLE_HEADER sample_header;
    double T[432];
} MDF_TRIGNO_DATA;