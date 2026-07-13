# models/pid.py

class PIDController:
    """
    Generic PID Controller
    u(t) = Kp * error + Ki * integral(error) + Kd * derivative(error)
    """
    def __init__(self,kp=1.0,ki=0.0,kd=0.0,output_limits=(None, None),integral_limits=(None, None)):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limits = output_limits
        self.integral_limits = integral_limits
        self.reset()

    # RESET
    def reset(self):
        """
        Reset controller state.
        """
        self.prev_error = 0.0
        self.integral = 0.0
        self.last_output = 0.0
        self.last_error = 0.0

    # LIMITER
    @staticmethod
    def clamp(value,lower_limit,upper_limit):

        if (lower_limit is not None and value < lower_limit):
            return lower_limit
        if (upper_limit is not None and value > upper_limit):
            return upper_limit
        return value

    # UPDATE GAINS
    def update_gains(self,kp,ki,kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

    # COMPUTE OUTPUT
    def compute(self,setpoint,measurement,dt):

        if dt <= 0: raise ValueError("dt must be greater than zero")
        error = setpoint - measurement
        # Integral
        self.integral += error * dt
        int_min, int_max = (self.integral_limits)
        self.integral = self.clamp(self.integral,int_min,int_max)
        # Derivative
        derivative = (error - self.prev_error) / dt
        # PID Output
        output = (self.kp * error + self.ki * self.integral + self.kd * derivative)
        out_min, out_max = (self.output_limits)
        output = self.clamp(output,out_min,out_max)
        # Save State
        self.prev_error = error
        self.last_error = error
        self.last_output = output
        return output

    # STATUS
    def get_status(self):
        return {"kp": self.kp, "ki": self.ki, "kd": self.kd, "error": self.last_error, "integral": self.integral, "output": self.last_output}

    # STRING
    def __repr__(self):
        return ("PIDController("f"kp={self.kp}, "f"ki={self.ki}, "f"kd={self.kd})")