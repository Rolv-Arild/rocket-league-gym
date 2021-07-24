import random

from rlgym.utils.common_values import CAR_MAX_SPEED, CAR_MAX_ANG_VEL, BALL_MAX_SPEED, BALL_MAX_ANG_VEL, BALL_RADIUS, \
    CEILING_Z, BACK_WALL_Y, CORNER_CATHETUS_LENGTH, SIDE_WALL_X
from rlgym.utils.state_setters import StateSetter
from rlgym.utils.state_setters import StateWrapper
from rlgym.utils.math import rand_uvec3
import numpy as np
from numpy import random as rand

CAR_MARGIN = 100  # So no matter the rotation car will fit inside field
X_MAX = SIDE_WALL_X - CORNER_CATHETUS_LENGTH / 2 - CAR_MARGIN
Y_MAX = BACK_WALL_Y - CORNER_CATHETUS_LENGTH / 2 - CAR_MARGIN
Z_MAX_BALL = CEILING_Z - BALL_RADIUS
Z_MAX_CAR = CEILING_Z - CAR_MARGIN
PITCH_MAX = np.pi / 2
YAW_MAX = np.pi
ROLL_MAX = np.pi


class RandomState(StateSetter):

    def __init__(self,
                 ball_rand_speed_prob: float = 0.,
                 cars_rand_speed_prob: float = 0.,
                 cars_on_ground_prob: float = 1.
                 ):
        """
        RandomState constructor.

        :param ball_rand_speed_prob: Float indicating probability that ball will have a randomly set velocity.
        :param cars_rand_speed_prob: Float indicating probability that cars will have a randomly set velocity.
        :param cars_on_ground_prob: Float indicating probability that cars should be placed on the ground.
        """
        super().__init__()
        self.ball_rand_speed_prob = ball_rand_speed_prob
        self.cars_rand_speed_prob = cars_rand_speed_prob
        self.cars_on_ground_prob = cars_on_ground_prob

    def reset(self, state_wrapper: StateWrapper):
        """
        Modifies the StateWrapper to contain random values the ball and each car.

        :param state_wrapper: StateWrapper object to be modified with desired state values.
        """
        self._reset_ball_random(state_wrapper, self.cars_rand_speed_prob)
        self._reset_cars_random(state_wrapper, self.cars_on_ground_prob, self.ball_rand_speed_prob)

    def _reset_ball_random(self, state_wrapper: StateWrapper, random_speed_prob: float):
        """
        Function to set the ball to a random position.

        :param state_wrapper: StateWrapper object to be modified.
        :param random_speed_prob: Boolean indicating whether to randomize velocity values.
        """
        state_wrapper.ball.set_pos(rand.uniform(-X_MAX, X_MAX),
                                   rand.uniform(-Y_MAX, Y_MAX),
                                   rand.triangular(BALL_RADIUS, BALL_RADIUS, Z_MAX_BALL))
        if rand.random() < random_speed_prob:
            vel = rand.triangular(0, 0, BALL_MAX_SPEED) * rand_uvec3()
            ang_vel = rand.triangular(0, 0, BALL_MAX_ANG_VEL) * rand_uvec3()
            state_wrapper.ball.set_lin_vel(*vel)
            state_wrapper.ball.set_ang_vel(*ang_vel)

    def _reset_cars_random(self, state_wrapper: StateWrapper, on_ground_prob: float, random_speed_prob: float):
        """
        Function to set all cars to a random position.

        :param state_wrapper: StateWrapper object to be modified.
        :param on_ground_prob: Boolean indicating whether to place cars only on the ground.
        :param random_speed_prob: Boolean indicating whether to randomize velocity values.
        """
        for car in state_wrapper.cars:
            # set random position and rotation for all cars based on pre-determined ranges
            car.set_pos(rand.uniform(-X_MAX, X_MAX),
                        rand.uniform(-Y_MAX, Y_MAX),
                        rand.triangular(CAR_MARGIN, CAR_MARGIN, Z_MAX_BALL))
            car.set_rot(random.uniform(-PITCH_MAX, PITCH_MAX),
                        random.uniform(-YAW_MAX, ROLL_MAX),
                        random.uniform(-ROLL_MAX, ROLL_MAX))

            if rand.random() < random_speed_prob:
                # set random linear and angular velocity based on pre-determined ranges
                vel = rand.triangular(0, 0, CAR_MAX_SPEED) * rand_uvec3()
                ang_vel = rand.triangular(0, 0, CAR_MAX_ANG_VEL) * rand_uvec3()
                car.set_lin_vel(*vel)
                car.set_ang_vel(*ang_vel)

            # 100% of cars will be set on ground if on_ground == True
            # otherwise, 50% of cars will be set on ground
            if rand.random() < on_ground_prob:
                # z position (up/down) is set to ground
                car.set_pos(z=17)
                # z linear velocity (vertical) set to 0
                car.set_lin_vel(z=0)
                # pitch (front of car up/down) set to 0
                # roll (side of car up/down) set to 0
                car.set_rot(pitch=0, roll=0)
                # x angular velocity (affects pitch) set to 0
                # y angular velocity (affects) roll) set to 0
                car.set_ang_vel(x=0, y=0)
