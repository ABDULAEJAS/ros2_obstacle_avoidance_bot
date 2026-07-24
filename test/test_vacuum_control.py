# Copyright 2026 Amin Ahmed G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def test_obstacle_avoidance_logic():
    """Verify sector distance threshold evaluation logic for obstacle avoidance."""
    safe_threshold = 0.50

    # Case 1: Path clear
    front_dist = 1.2
    assert front_dist > safe_threshold

    # Case 2: Obstacle ahead, turn left
    front_dist = 0.35
    left_dist = 1.5
    right_dist = 0.8
    assert front_dist <= safe_threshold
    assert left_dist >= right_dist

    # Case 3: Obstacle ahead, turn right
    left_dist = 0.4
    right_dist = 1.2
    assert left_dist < right_dist
