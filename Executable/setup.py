from cx_Freeze import setup, Executable

filesToInclude = ["Intro Splash.png", "Level Select.png", "Levels.png", "You Win.png", "0-small.png", "playerdata.pickle"]
for i in range(8):
	filesToInclude.append(f'{i}.png')

setup(
	name='The Dirty Dozen', 
	version='1.0', 
	description='Happy 31', 
	options= {
	"build_exe": {"include_files": filesToInclude, "excludes": ['numpy']},
	"bdist_msi": {"install_icon": "0-small.png"}
	},
	executables=[Executable("Dirty Dozen.py", icon='0-small.png', shortcut_name='The Dirty Dozen (Shortcut)')]
	)