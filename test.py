from importlib.resources import path
from numpy import sqrt, sin, mgrid
import os
import re

# Enthought imports.
from traits.api import HasTraits, Instance, Button, Str, on_trait_change
from traitsui.api import View, Item, Group
from tvtk.pyface.scene_editor import SceneEditor

from mayavi.core.api import Engine
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


######################################################################
class ActorViewer(HasTraits):
    #Create a mayavi scene with a specified engine
    engine = Instance(Engine, ())
    scene = Instance(MlabSceneModel, ())
    load_next = Button('Load next')
    path = Str
    label = Str

    print("1 "+ str(label))
    # Using 'scene_class=MayaviScene' adds a Mayavi icon to the toolbar,to pop up a dialog editing the pipeline.
    view = View(Item('load_next', label="load"),
                    '_',Group(
                    Item(name='scene',
                    editor=SceneEditor(scene_class=MayaviScene),
                    show_label=False,
                    resizable=True,
                    height=500,
                    width=500),
                    orientation='horizontal', layout='tabbed', springy=True,
                ),
                    title='Multiple scenes',
                    resizable=True
    )

    def __init__(self, path, label, engine=None, **traits):
        self.path = path
        self.label = label
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self, **traits)
        # print("2 "+ str(self.label))
        self.engine.start()
        print("file name ", label)
        if engine is not None:
            self.scene=MlabSceneModel(engine=self.engine)
        else:
            self.scene=MlabSceneModel()
        self.on_trait_change(self.generate_data, 'load_next')
        # self.generate_data()

    @on_trait_change('scene.activated')
    def generate_data(self):
        src=self.scene.mlab.pipeline.open(self.path+self.label)
        self.scene.mlab.view(-40, -50)
        self.scene.mlab.pipeline.outline(src)
        self.scene.mlab.pipeline.iso_surface(src, contours=60, opacity=0.5)
        self.engine.new_scene()

    def load_new_source(self):
        self.scene.add_source

if __name__ == '__main__':
    filelist_sort=[]
    abs_path = "/path/to/a/folder"
    filelist = os.listdir(abs_path)
    for i in filelist:
        if i.endswith(".vtr"):
            filelist_sort.append(i)
    filelist_sort.sort(key=lambda f: int(re.sub('\D', '', f)))
    # print(filelist_sort)
    for i in filelist_sort:
        if ("E1_" in i) or ("E2_" in i):
            print("file name ", i)
            a = ActorViewer(path=abs_path,label=i)
            a.configure_traits()
            # a.edit_traits() #no access to UI, good for image processing
