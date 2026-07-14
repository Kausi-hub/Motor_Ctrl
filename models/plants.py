# models/plants.py

import math

# BASE PLANT
class BasePlant:
    """
    Abstract base class for all plants.
    """
    def reset(self): pass
    def update(self, control_input, dt): raise NotImplementedError

# IDEAL MOTOR
class IdealMotor(BasePlant):
    """
    Ideal motor model.
    Control input directly affects acceleration.
    acceleration = control_input
    velocity += acceleration * dt
    position += velocity * dt
    """

    def __init__(self):
        self.position = 0.0
        self.velocity = 0.0
    def reset(self):
        self.position = 0.0
        self.velocity = 0.0
    def update(self,control_input,dt):
        acceleration = control_input
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return self.position

# FIRST ORDER PLANT

class FirstOrderPlant(BasePlant):
    """
    First-order system.
    Transfer Function: G(s) = K / (tau*s + 1)
    State equation: dy/dt = (-y + K*u) / tau
    """

    def __init__(self,gain=1.0,tau=1.0):
        self.gain = gain
        self.tau = tau
        self.output = 0.0
    def reset(self): self.output = 0.0
    def update(self,control_input,dt):
        dy = (-self.output + self.gain * control_input) / self.tau
        self.output += dy * dt
        return self.output

# SECOND ORDER PLANT

class SecondOrderPlant(BasePlant):
    """
    Second-order system. Transfer Function:
                    wn²*K
        --------------------------
        s² + 2ζwns + wn²
    Common servo/actuator model.
    """

    def __init__(self,gain=1.0,wn=5.0,zeta=0.7):
        self.gain = gain
        self.wn = wn
        self.zeta = zeta
        self.position = 0.0
        self.velocity = 0.0
    def reset(self):
        self.position = 0.0
        self.velocity = 0.0
    def update(self,control_input,dt):
        acceleration = (self.gain * self.wn**2 * control_input - 2 * self.zeta * self.wn * self.velocity
            - self.wn**2 * self.position
        )
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return self.position

# DC MOTOR

class DCMotor(BasePlant):
    """
    Physics-based DC motor model.
    Electrical: V = L di/dt + Ri + Ke*w
    Mechanical: J dw/dt = Kt*i - B*w
    Position: theta += w*dt
    """

    def __init__(self,R=1.0,L=0.5,Kt=0.05,Ke=0.05,J=0.01,B=0.001):
        self.R = R
        self.L = L
        self.Kt = Kt
        self.Ke = Ke
        self.J = J
        self.B = B
        self.current = 0.0
        self.speed = 0.0
        self.position = 0.0
    def reset(self):
        self.current = 0.0
        self.speed = 0.0
        self.position = 0.0
    def update(self,voltage,dt):
        di = (voltage - self.R * self.current - self.Ke * self.speed) / self.L
        self.current += di * dt
        dw = (self.Kt * self.current - self.B * self.speed) / self.J
        self.speed += dw * dt
        self.position += (self.speed * dt)
        return self.position

# PLANT FACTORY
def create_plant(plant_type):
    """
    Factory function.
    """
    if plant_type == "Ideal Motor": return IdealMotor()
    if plant_type == "First Order": return FirstOrderPlant()
    if plant_type == "Second Order": return SecondOrderPlant()
    if plant_type == "DC Motor": return DCMotor()
    raise ValueError(f"Unknown plant type: {plant_type}")