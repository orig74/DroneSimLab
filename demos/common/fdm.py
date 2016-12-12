# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from cffi import FFI
ffi = FFI()

src="""
enum {
        FG_MAX_ENGINES = 4,
        FG_MAX_WHEELS = 3,
        FG_MAX_TANKS = 4
    };


typedef struct {

    uint32_t version;		// increment when data values change
    uint32_t padding;		// padding

    // Positions
    double longitude;		// geodetic (radians)
    double latitude;		// geodetic (radians)
    double altitude;		// above sea level (meters)
    float agl;			// above ground level (meters)
    float phi;			// roll (radians)
    float theta;		// pitch (radians)
    float psi;			// yaw or true heading (radians)
    float alpha;                // angle of attack (radians)
    float beta;                 // side slip angle (radians)

    // Velocities
    float phidot;		// roll rate (radians/sec)
    float thetadot;		// pitch rate (radians/sec)
    float psidot;		// yaw rate (radians/sec)
    float vcas;             // calibrated airspeed
    float climb_rate;		// feet per second
    float v_north;              // north velocity in local/body frame, fps
    float v_east;               // east velocity in local/body frame, fps
    float v_down;               // down/vertical velocity in local/body frame, fps
    float v_wind_body_north;    // north velocity in local/body frame
                                // relative to local airmass, fps
    float v_wind_body_east;     // east velocity in local/body frame
                                // relative to local airmass, fps
    float v_wind_body_down;     // down/vertical velocity in local/body
                                // frame relative to local airmass, fps

    // Accelerations
    float A_X_pilot;		// X accel in body frame ft/sec^2
    float A_Y_pilot;		// Y accel in body frame ft/sec^2
    float A_Z_pilot;		// Z accel in body frame ft/sec^2

    // Stall
    float stall_warning;        // 0.0 - 1.0 indicating the amount of stall
    float slip_deg;		// slip ball deflection

    // Pressure

    // Engine status
    uint32_t num_engines;        // Number of valid engines
    uint32_t eng_state[FG_MAX_ENGINES];// Engine state (off, cranking, running)
    float rpm[FG_MAX_ENGINES];       // Engine RPM rev/min
    float fuel_flow[FG_MAX_ENGINES]; // Fuel flow gallons/hr
    float fuel_px[FG_MAX_ENGINES];   // Fuel pressure psi
    float egt[FG_MAX_ENGINES];       // Exhuast gas temp deg F
    float cht[FG_MAX_ENGINES];       // Cylinder head temp deg F
    float mp_osi[FG_MAX_ENGINES];    // Manifold pressure
    float tit[FG_MAX_ENGINES];       // Turbine Inlet Temperature
    float oil_temp[FG_MAX_ENGINES];  // Oil temp deg F
    float oil_px[FG_MAX_ENGINES];    // Oil pressure psi

    // Consumables
    uint32_t num_tanks;		// Max number of fuel tanks
    float fuel_quantity[FG_MAX_TANKS];

    // Gear status
    uint32_t num_wheels;
    uint32_t wow[FG_MAX_WHEELS];
    float gear_pos[FG_MAX_WHEELS];
    float gear_steer[FG_MAX_WHEELS];
    float gear_compression[FG_MAX_WHEELS];

    // Environment
    uint32_t cur_time;           // current unix time
                                 // FIXME: make this uint64_t before 2038
    int32_t warp;                // offset in seconds to unix time
    float visibility;            // visibility in meters (for env. effects)

    // Control surface positions (normalized values)
    float elevator;
    float elevator_trim_tab;
    float left_flap;
    float right_flap;
    float left_aileron;
    float right_aileron;
    float rudder;
    float nose_wheel;
    float speedbrake;
    float spoilers;

    //void ByteSwap(void);
} FGNetFDM;
void ByteSwap(FGNetFDM* this);
"""

src2=r"""
/* nasty hack ....
   JSBSim sends in little-endian
 */
void ByteSwap(FGNetFDM* this)
{
    uint32_t *buf = (uint32_t *)this;
    uint32_t i;
    for (i=0; i<(sizeof(*this)/4); i++) {
        buf[i] = ntohl(buf[i]);
    }
    // fixup the 3 doubles
    buf = (uint32_t *)&(this->longitude);
    uint32_t tmp;
    for (i=0; i<3; i++) {
        tmp = buf[0];
        buf[0] = buf[1];
        buf[1] = tmp;
        buf += 2;
    }
}

"""

ffi.cdef(src)
lib=ffi.verify(src+src2)
#ffi.set_source("_fdm",src2,libraries=[])
#ffi.compile()
_fdm_sz=ffi.sizeof("FGNetFDM")

def new_fdm():
    return ffi.new("FGNetFDM[]",1)

def fdm_from_buf(buf):
    fdm=new_fdm()
    nbuf=bytearray(len(buf))
    nbuf[:]=buf
    #print(ffi.list_types())
    #import ipdb;ipdb.set_trace()
    ffi.memmove(fdm,nbuf,_fdm_sz)
    lib.ByteSwap(fdm)
    return fdm

def fdm_to_buf(fdm):
    fdmcopy=new_fdm()
    ffi.memmove(fdmcopy,fdm,_fdm_sz)
    lib.ByteSwap(fdmcopy)
    buf=bytearray(_fdm_sz) 
    ffi.memmove(buf,fdmcopy,_fdm_sz)
    return buf

if __name__=="__main__":
    fdm=new_fdm()
    fdm[0].longitude=8.0
    #lib.ByteSwap(fdm)
    #lib.ByteSwap(fdm)
    newfdm=fdm_from_buf(fdm_to_buf(fdm))
    print(newfdm[0].longitude==fdm[0].longitude)
