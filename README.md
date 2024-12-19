# neatcrat

this is a less messy and more readable version of "godcrat", with better plots


工程化idea：

1. 对于每一帧，找到前车
2. 如果前车不存在，输出invalid或者对应的case
3. 如果前车没有变化，输出lead或者对应的case（withlead）
4. 如果前车有变化，输出cross或者对应的case（cutin，cutout）

待提升（priority从高到低，提出时间从早到晚）
1. **左右转crossing更合理的判断：去掉leading消失的情况，去掉“crossing”车辆静止不动的情况，去掉获得leading的情况**
2. **用egoanchor-agent-nextegoanchor角度大小判断是否在ego traj里，而不是用过front and cross dist**
3. **cutin cutout进行时的具体判断标准，当前默认前车变化前后固定几帧为cutin cutout**

1. 考虑周围车辆的自车轨迹预测，可以帮助约后十帧左右的预测
2. 找到前车后用它的轨迹协助预测，思考具体考虑方法
3. 实现中间段的任意车轨迹预测并融合进每一个snapshot（in other words 每一帧, 每一个frame），但是可能会对结果产生不确定的影响
4. 要不要设定leading必须是OBJECT_TYPE_VEHICLE

plot.py介绍：
1. 创建plot：`p = Plot(xmin, xmax, ymin, ymax, size); `（一般设定`p = Plot(-50, 50, -20, 180, 4); `，改动ymax和size最频繁）
2. 输出interactive视频，每一帧都有全部车辆与自车未来20帧的轨迹：`p.draw_scene_with_ego_traj(scene)`，非常适合测试当前基于front的idea的可行性，绿色为已知的未来自车位置和朝向，橙色为轨迹预测得出的未来自车位置和朝向，红色为自车，蓝色为“前方的车”，青绿色为“不是前方的车”（此处“前方的车”是用front_dist > side_dist ^2 算出来的），灰色不是车，可能是自行车或者行人（或者别的？？？），箭头是车辆朝向（yaw），最重要的紫色是根据轨迹判断的前车
> scene可以用`s:Scene = Scene.from_data(Data('0.csv'))`生成，包括每一帧的车辆信息，0.csv换成文件名，不用带目录，数据都放在dataset/data，标签都放在dataset/labels，对应的数据用相同的文件名
3. 输出interactive视频，每一帧只有特定code的车辆：`p.draw_scene_trajectories(s, ['1', '2', '3'])`
> 如果一辆车的id是`scene-000320-1`，那他的code就是`1`，自车的code是`ego`，各个图像上显示的数字就是车辆的code
4. `p.draw_agent(), p.draw_trajectory(), p.draw_scene()`，字面意思，一般作为helper function，如果想用也可以用，但是比较麻烦，这种不输出interactive视频的函数call完了需要用`p.show()`输出
> 这些函数没法在interactive视频上画东西

观察
1. accelerating其实不是前车加速，而是前车比自车快，decelerating同理

## Pseudocode Idea

```python
labels = [INVALID] * N

# INLANE
for frame in frames:
    front = get_front(frame)

    # 前车不存在
    if front does not exist:
        frame.label = 'invalid'
    
    # 前车没有变化
    else if front == previous front:
        if front.velocity is small:
            frame.label = 'stopped'
        else if front.acceleration is negative:
            frame.label = 'decelerating'
        else if front.acceleration is positive:
            frame.label = 'accelerating'
    
    # 前车变化
    else if front != previous front:

        # 需要一种方法来判断是否正在进行cutin cutout
        # 当前naively将前车变化的前后两帧分为cutin cutout
        if previous front is further away from ego:
            frame.previous_3.label = 'cutin'
        else if previous front is nearer to ego:
            frame.next_3.label = 'cutout'

# GOSTRAIGHT & TURNLEFTRIGHT
for frame in frames:
    front = get_front(frame)

    # 前车不存在
    if front does not exist:
        frame.label = 'novehiclesahead'
    # 前车没有变化
    else if front == previous front:
        frame.label = 'leading'
    # 前车变化
    else if front != previous front:
        frame.previous_3_and_next_3.label = 'cuttingahead'
    

# STOP AND WAIT
for frame in frames:
    # 因为自车不动，轨迹预测无效，所以直接用位置关系和朝向判断前车
    front = get_direct_front(frame)

    # 有前车正在等待
    if front is vehicle and faces about the same direction:
        frame.label = 'withleadvehicle'
    # 前方有行人
    else if get_all_agents_in_front(frame) contains pedestrians or bikes:     # a bit difficult
        frame.label = 'pedestrianscrossing'
    # 前方什么也没有
    else:
        frame.label = 'novehiclesahead'
```

