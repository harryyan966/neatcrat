from neatcrat import *

data: Data = Data('1007.csv')
scene: Scene = Scene.from_data(data)

# [print(x) for x in scene.snapshots[0]]

true_labels = list(scene.third_class.values())

# print(list(map(lambda x: THIRD_CLASSES[x], true_labels)))

classifier: SceneClassifier = SceneClassifier(scene)
labels = classifier.classify_scene()

# print(list(map(lambda x: THIRD_CLASSES[x], labels)))

print("Press Enter to view true and predicted labels for the next frame...")
for i, (t, l) in enumerate(zip(true_labels, labels)):
    input()
    print(i)
    print(t + '                   ' + l)
