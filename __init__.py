# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

bl_info = {
    "name" : "test_ui",
    "author" : "cx",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

bpy.types.Object.mychosenObject = bpy.props.StringProperty()

# TEST:操作的对象，如materials,objects
# hello: 操作的具体内容
class TEST_OT_hello(bpy.types.Operator):
    bl_idname = "cx.hello"
    bl_label =  'Hello'
    bl_options = {"REGISTER", "UNDO"}

    mStr : bpy.props.StringProperty(name="mString", default="blender")

    def execute(self, context):
        self.report({"INFO"}, self.mStr)
        return {"FINISHED"}

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


# 操作2：打印选中物体的名称
class TEST_OT_printname(bpy.types.Operator):
    bl_idname = "cx.printname"
    bl_label = "printname"

    def execute(self, context):
        ob = context.object
        self.report({"INFO"}, ob.mychosenObject)
        return {"FINISHED"}



class SpaceAndRegionSetting:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"


# 面板1
class TEST_PT_view3d_1(bpy.types.Panel):
    bl_idname = "TEST_PT_view3d_1"
    bl_label = "view3d test"

    # ui_type: console Timeline等，左上角的下拉选项
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode" # 指定模式
    # 指定分类，如Tool，或者新分类
    bl_category = "TEST"

    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text="header", icon="VIEW_PAN")

    # 面板如何绘制函数
    def draw(self, context):
        # 获取布局
        layout = self.layout
        # icon获取有图标插件，addon界面搜索'icon'
        layout.label(text="panel", icon="BLENDER")
        row = layout.row()

        # 生成按钮
        # row.Operator("cx.hello", text='hello', icon='CUBE').mStr = "hello blender"
        row.operator("cx.hello", text='hello', icon='CUBE')

# 面板2
class TEST_PT_view3d_2(SpaceAndRegionSetting,bpy.types.Panel):
    bl_label = "view3d test 2"
    # 指定分类，如Tool，或者新分类
    bl_category = "TEST"
    
    # 面板2放入面板1下
    bl_parent_id = "TEST_PT_view3d_1"

    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text="header", icon="VIEW_PAN")
        
    # 面板如何绘制函数
    def draw(self, context):
        obj = context.object

        # 获取布局
        layout = self.layout
        # 选择物体，并将选择的物体名返回到Object.mychoseObject
        layout.prop_search(obj, "mychosenObject",  context.scene, "objects")

        # icon获取有图标插件，addon界面搜索'icon'
        layout.label(text="panel", icon="BLENDER")
        row = layout.row()

        # 生成按钮
        # row.Operator("cx.hello", text='hello', icon='CUBE').mStr = "hello blender"
        row.operator("cx.hello", text='hello', icon='CUBE')
        
        # 下拉菜单获取Scene中物体对象
        row = layout.row()
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        # 使用上述方法存在的问题是多个这样的下拉菜单会同时改变，相互之间会受到影响
        # 将选中的物体赋值给ob，
        ob = context.object 
        col = layout.column()
        col.prop(ob,'name',text="Name")
        # 实现操作2，打印物体名称，即UI界面选中的物体，通过context.object在operator可以访问数据
        col.operator("cx.printname", text="print name")


def register():
    bpy.utils.register_class(TEST_OT_hello)
    bpy.utils.register_class(TEST_OT_printname)
    bpy.utils.register_class(TEST_PT_view3d_1)
    bpy.utils.register_class(TEST_PT_view3d_2)
    ...

def unregister():
    bpy.utils.unregister_class(TEST_OT_hello)
    bpy.utils.unregister_class(TEST_OT_printname)
    bpy.utils.unregister_class(TEST_PT_view3d_1)
    bpy.utils.unregister_class(TEST_PT_view3d_2)
    ...
