set applicationWasNotRunning to application "macSVG" is not running
tell application "macSVG" to activate
if applicationWasNotRunning then tell application "System Events" to tell process "macSVG" to click button "Cancel" of window "Create New MacSVG Document"
tell application "macSVG" to open POSIX path of (system attribute "vector_image_path")
tell application "System Events"
	repeat until not (exists window (system attribute "vector_image_name") of application process "macSVG")
		delay .1
	end repeat
end tell
