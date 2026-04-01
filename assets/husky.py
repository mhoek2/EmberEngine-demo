class MyScript:
    value         : float     = export(1.0)
    boost         : float     = export(30.0)
    
    wheel_fl    : PhysicLink = export()
    wheel_fr    : PhysicLink = export()
    wheel_rl    : PhysicLink = export()
    wheel_rr    : PhysicLink = export()
    
    """Default script template"""
    def onStart( self ) -> None:
        #self.camera = self.scene.getCamera()

        pass

    def onEnable( self ):
        pass

    def onDisable( self ):
        pass

              
    def onUpdate(self) -> None:
        from pyrr import Vector3, vector, vector3, matrix44, Matrix44
        
        import numpy as np
        keypress = self.key.get_pressed()
        
        throttle = 0.0
        accel = self.value
        
        if keypress[pygame.K_w]:
            throttle += accel
        elif keypress[pygame.K_s]:
            throttle -= accel
        else:
            throttle *= 0.95  # decay / friction
        
        if keypress[pygame.K_LCTRL] or keypress[pygame.K_RCTRL]:
            throttle *= self.boost
        

        

        steer_left = keypress[pygame.K_d]
        steer_right = keypress[pygame.K_a]
        
        if throttle < 0.05 and (steer_left or steer_right):
            throttle = 0.7

        if steer_left or steer_right:
            throttle *= 2.5
            
        throttle *= 50  # scaling factor
        
        # Apply torque to right wheels
        torque = -throttle if steer_right else throttle
        for wheel in [self.wheel_fr, self.wheel_rr]:
            bodyID = wheel.getBodyId()
            jointD = wheel.getJointId()
            p.setJointMotorControl2(
                bodyUniqueId=bodyID,
                jointIndex=jointD,
                controlMode=p.TORQUE_CONTROL,
                force=torque
            )
        
        # Apply torque to left wheels
        torque = -throttle if steer_left else throttle
        for wheel in [self.wheel_fl, self.wheel_rl]:
            bodyID = wheel.getBodyId()
            jointD = wheel.getJointId()
            p.setJointMotorControl2(
                bodyUniqueId=bodyID,
                jointIndex=jointD,
                controlMode=p.TORQUE_CONTROL,
                force=torque
            )