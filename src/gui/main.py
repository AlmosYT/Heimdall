import dearpygui.dearpygui as dpg
from os import walk
from src.Logger import Logger
from screeninfo import get_monitors

class GUI():
	def __init__(self,Core=None,debug=False) -> None:
		self.logger = Logger("GUI",DEBUG=debug)
		self.core = Core
		dpg.create_context()
		dpg.create_viewport(title="Heimdall", min_width=1100, min_height=700, width=1100, height=700, decorated=False)
		dpg.setup_dearpygui()
		self.initStyles()
		self.loadTextures()
		self.mainWindow = dpg.add_window(label="Heimdall",on_close=self.closeGUI,horizontal_scrollbar=False,no_title_bar=True,no_scrollbar=True,no_collapse=True,no_close=False,no_resize=True,menubar=False,no_move=True,height=dpg.get_viewport_height(),width=dpg.get_viewport_width())
		dpg.set_primary_window(self.mainWindow,True)
		dpg.set_frame_callback(1,callback=lambda: self.switchState("MAIN"))
		self.centerViewport()
		dpg.show_viewport()
		dpg.start_dearpygui()

	def initStyles(self):  # sourcery skip: extract-duplicate-method
		with dpg.theme() as global_theme:
			with dpg.theme_component(dpg.mvAll):
				dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (13, 17, 23), category=dpg.mvThemeCat_Core)
				dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
			with dpg.theme_component(dpg.mvImageButton):
				dpg.add_theme_color(dpg.mvThemeCol_Button, (0,0,0,0), category=dpg.mvThemeCat_Core)
				dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255,255,255,127), category=dpg.mvThemeCat_Core)
				dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0,0,0,0), category=dpg.mvThemeCat_Core)
		with dpg.theme() as self.exit_button_theme:
			with dpg.theme_component(dpg.mvImageButton):
				dpg.add_theme_color(dpg.mvThemeCol_Button, (0,0,0,0), category=dpg.mvThemeCat_Core)
				dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0,0,0,0), category=dpg.mvThemeCat_Core)
				dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0,0,0,0), category=dpg.mvThemeCat_Core)
		with dpg.theme() as self.search_input_theme:
			with dpg.font_registry():
				self.input_font = dpg.add_font(file="./src/gui/assets/fonts/Roboto-Regular.ttf",size=60)
			with dpg.theme_component(dpg.mvInputText):
				dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0,0,0,0), category=dpg.mvThemeCat_Core)
		dpg.bind_theme(global_theme)

	def loadTextures(self):
		for (_, _, filenames) in walk("./src/gui/assets/main"):
			assets = [filename for filename in filenames if filename.endswith(".png")]
			break
		self.images = {}
		self.textures = {}
		for asset in assets:
			width, height, _, data = dpg.load_image(f"./src/gui/assets/main/{asset}")
			with dpg.texture_registry():
				self.textures[asset.replace(".png","")] = dpg.add_dynamic_texture(width,height,data)
				self.images[asset.replace(".png","")] = [width, height, data]

	def centerViewport(self):
		for monitor in get_monitors():
			if monitor.is_primary:
				monitor_xd = monitor.width
				monitor_yd = monitor.height
		dpg.set_viewport_pos(pos=[(monitor_xd - dpg.get_viewport_width()) / 2,(monitor_yd - dpg.get_viewport_height()) / 2,])

	def switchState(self,GUIState):
		self.resetToDefault()
		match GUIState:
			case "MAIN":
				# Structure
				dpg.add_image(texture_tag=self.textures["bar"],parent=self.mainWindow,pos=[0,0])
				exit_button = dpg.add_image_button(label="button-exit",texture_tag=self.textures["button-exit"],parent=self.mainWindow,pos=[1060,5],callback=self.closeGUI)
				dpg.add_image(texture_tag=self.textures["title"],parent=self.mainWindow,pos=[251,198])
				dpg.add_image_button(label="button-new",texture_tag=self.textures["button-new"],parent=self.mainWindow,pos=[255,342],callback=lambda: self.switchState("SEARCH"))
				dpg.add_image_button(label="button-load",texture_tag=self.textures["button-load"],parent=self.mainWindow,pos=[510,342],callback=lambda: self.switchState("LOAD"))
				dpg.add_image_button(label="button-settings",texture_tag=self.textures["button-settings"],parent=self.mainWindow,pos=[765,342],callback=lambda: self.switchState("SETTINGS"))
				# Style
				dpg.bind_item_theme(exit_button,self.exit_button_theme)
				# Function
				# TODO | Add a drag handler to the "bar" image to drag the window
			case "SEARCH":
				dpg.add_image(texture_tag=self.textures["bar"],parent=self.mainWindow,pos=[0,0])
				dpg.add_image(texture_tag=self.textures["small-title"],parent=self.mainWindow,pos=[468,4])
				exit_button = dpg.add_image_button(label="button-exit",texture_tag=self.textures["button-exit"],parent=self.mainWindow,pos=[1060,5],callback=self.closeGUI)
				dpg.add_image(texture_tag=self.textures["search-background"],parent=self.mainWindow,pos=[0,0])
				search_input = dpg.add_input_text(parent=self.mainWindow,pos=[346,317],width=665,multiline=False,hint="Search")
				dpg.bind_item_font(search_input,self.input_font)
				dpg.bind_item_theme(search_input,self.search_input_theme)
			case "LOADING":
				dpg.add_button(label="loading while searching",parent=self.mainWindow,callback=lambda: self.switchState("MAIN"))
			case "VIEW":
				dpg.add_button(label="view results",parent=self.mainWindow,callback=lambda: self.switchState("MAIN"))
			case "LOAD":
				dpg.add_button(label="load a saved file",parent=self.mainWindow,callback=lambda: self.switchState("MAIN"))
			case "SETTINGS":
				dpg.add_button(label="adjust settings",parent=self.mainWindow,callback=lambda: self.switchState("MAIN"))
			case _:
				dpg.add_button(label="wtf",parent=self.mainWindow,callback=lambda: self.switchState("MAIN"))

	def resetToDefault(self):
		for item in dpg.get_item_children(self.mainWindow)[children_index := 1]:
			dpg.delete_item(item)

	def closeGUI(self):
		dpg.destroy_context()

				# hovered
				# dpg.set_value(item=self.textures[dpg.get_item_label(item)],value=self.images[f"hovered-{dpg.get_item_label(item)}"][image_index := 2])
				# normal
				# dpg.set_value(item=self.textures[dpg.get_item_label(item)],value=self.images[dpg.get_item_label(item)][image_index := 2])
