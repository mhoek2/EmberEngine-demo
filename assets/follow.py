class FollowTarget:
    target    : GameObject = export()
    
    def onStart( self ) -> None:
        self.distance_back = 3.0
        self.height = 0.9
        self.look_ahead = 2.0
        self.smoothness = 0.15
        self._current_pos = None


    def onUpdate( self ) -> None:
        from pyrr import Matrix44, Vector3
        from pyrr import matrix44
        
        car_pos = Vector3(self.target.transform.position)
        car_quat = self.target.transform._local_rotation_quat
        
        rot = Matrix44.from_quaternion(car_quat)

        # direction
        forward = rot * Vector3([1.0, 0.0, 0.0])
        world_up = Vector3([0.0, 1.0, 0.0])

        desired_pos = (
            car_pos
            - forward * self.distance_back
            + world_up * self.height
        )

        # smooth
        if self._current_pos is None:
            self._current_pos = desired_pos

        self._current_pos += (desired_pos - self._current_pos) * self.smoothness
        camera_pos = self._current_pos


        # matrix
        look_target = car_pos + forward * self.look_ahead
        view = matrix44.create_look_at(
            camera_pos,
            look_target,
            world_up
        )

        flip = Matrix44.from_y_rotation(3.14159265)
        model = Matrix44(view).inverse * flip

        self.transform.world_model_matrix = model
        self.transform._update_local_from_world()